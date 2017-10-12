"""
models.py -- class definitions for use in the tech test

Models for working with Buy/Sell instructions.

Contents: 

  Instruction - Object to represent a single buy/sell instruction from a client.
  Solution - Object to create a list of instructions from data and report on them.
"""

# fields contained within the data
FIELDS_LIST = ['Entity','Buy/Sell','AgreedFx','Currency','InstructionDate',
               'SettlementDate','Units','Price per unit']

# this is for parsing incoming dates and formatting output
DATE_FORMAT = '%d %b %Y' 

# default list of valid settlement weekdays, with exceptions. (python weekday(), not isoweekday())
WORKING_DAYS = {'_default': [0,1,2,3,4], 'AED': [6,0,1,2,3], 'SAR': [6,0,1,2,3]}

# we need datetime to parse date strings and timedelta for SettlementDate updates
from datetime import datetime, timedelta

# helpers to cast incoming text values to other types
STR_TO_FLOAT = lambda _: float(_)
STR_TO_INT = lambda _: int(_)
STR_TO_DATE = lambda _: datetime.strptime(_, DATE_FORMAT).date()

# list of those fields which need their values to be cast, and how to do it
TYPE_CONVERSIONS = {'AgreedFx': STR_TO_FLOAT, 'Price per unit': STR_TO_FLOAT,
                    'InstructionDate': STR_TO_DATE, 'SettlementDate': STR_TO_DATE,
                    'Units': STR_TO_INT}


# the field & record separators to expect in the data
FIELD_SEP = "\t"
RECORD_SEP = "\n"


class Instruction:
    """An Instruction represents a buy/sell instruction.
    """
    def __init__(self):
        """Create a new Instruction. Set placeholder attributes for the fields in FIELDS_LIST."""
        for field in FIELDS_LIST:
            setattr(self, field, None)

    def finalise(self):
        """Correct the SettlementDate if necessary and calculate USD Amount.
        """
        self._correctSettlementDate()
        self._addUSD()
            
    def _correctSettlementDate(self):
        try:
            working_days = WORKING_DAYS[self.Currency]
        except KeyError:
            working_days = WORKING_DAYS['_default']

        if len(working_days): # ensure we have at least one
            while self.SettlementDate.weekday() not in working_days:
                self.SettlementDate = self.SettlementDate + timedelta(days=1)

    def _addUSD(self):
        setattr(self, 'USD Amount',
                float('{usd:.02f}'.format(usd=getattr(self, 'Price per unit') *
                                          self.Units * self.AgreedFx)))

class Solution:
    """Primary class to process the data and present the results."""

    def __init__(self):
        """Create a Solution object with an empty 'instructions' list."""
        self.instructions = []

    def add_data(self, fh):
        """Iterate over the supplied filehandle for tab-separated data and append it to
        the internal list.

        fh should be an iterable with an optional header line.
        """
        for line in fh:
            if line.startswith(FIELD_SEP.join(FIELDS_LIST[:2])):
                continue # skip header lines
            
            instruction = Instruction()
                
            thisrow = [x.lstrip().rstrip() for x in line.split(FIELD_SEP)]
            for i in range(len(FIELDS_LIST)):
                key, val = FIELDS_LIST[i], thisrow[i]
                
                try:
                    val = TYPE_CONVERSIONS[key](val)
                except KeyError:
                    pass
                        
                setattr(instruction, key, val)

            instruction.finalise() # adjust settlement date & add usd amount
            self.instructions.append(instruction)

        self._summarise_data() # sort the data so we're ready to report on it

    def _summarise_data(self):
        """Go through the current list of instructions and set internal
        lists of totals by settlement date and by entity, for use in
        reporting.
        """

        # sort the instructions into (temporary) dicts with totals per date/entity
        self._by_date = {}
        self._by_entity = {"incoming": {},
                           "outgoing": {}}
        
        for instr in self.instructions:
            sdate = instr.SettlementDate
            buy_or_sell = getattr(instr, 'Buy/Sell')
            amount = getattr(instr, 'USD Amount')
            inout = 'outgoing' if buy_or_sell == 'B' else 'incoming'

            if sdate not in self._by_date:
                self._by_date[sdate] = {'incoming': 0.0,
                                        'outgoing': 0.0}
            
            self._by_date[sdate][inout] += amount
            try:
                self._by_entity[inout][instr.Entity] += amount
            except KeyError:
                self._by_entity[inout][instr.Entity] = amount

                
        # use those new dicts to create summary lists
        self._by_date_list = []
        for date in sorted(self._by_date.keys()):
            self._by_date_list.append([date,
                                        self._by_date[date]['incoming'],
                                        self._by_date[date]['outgoing']])

        for inout in ['incoming','outgoing']:
            setattr(self, '_by_entity_{}_list'.format(inout), [])
            
            for entity in sorted(self._by_entity[inout].keys(),
                                 key=lambda _: self._by_entity[inout][_],
                                 reverse=True):

                getattr(self, '_by_entity_{}_list'.format(inout)).\
                    append([entity, self._by_entity[inout][entity]])

                
        # delete those temporary dicts
        self._by_date = None
        self._by_entity = None


    def report_amount_settled_every_day(self):
        """Return a plain-text report on the amounts incoming & outgoing every
        day in the data.
        """
        str_format = FIELD_SEP.join(['{date:13s}','{incoming:>17s}','{outgoing:>17s}'])

        return "{headers}{sep}{data}".\
            format(headers="AMOUNTS SETTLED EVERY DAY{s}{s}".format(s=RECORD_SEP) +\
                   str_format.format(date='DATE',
                                     incoming='INCOMING (USD)',
                                     outgoing='OUTGOING (USD)'),
                   sep=RECORD_SEP,
                   data=RECORD_SEP.join([str_format.\
                                         format(date=_[0].strftime(DATE_FORMAT),
                                                incoming='{a:.02f}'.format(a=_[1]),
                                                outgoing='{a:.02f}'.format(a=_[2]))
                                         for _ in self._by_date_list]))

    
    def report_rank_entities(self, incoming_or_outgoing='incoming'):
        """Return a plain-text report on entities in the data, ranked by
        'outgoing' or 'incoming'.
        """
        return self._report_by_entity(incoming_or_outgoing)

    
    def _report_by_entity(self, in_or_out):
        str_format = FIELD_SEP.join(['{rank:>10s}','{entity:16s}','{amount:>16s}'])

        return "{title}{s}{headerline}{s}{data}".\
            format(title=("RANKING OF ENTITIES BASED ON {io} AMOUNT{se}".\
                          format(se=RECORD_SEP, io=in_or_out.upper())),
                   s=RECORD_SEP,
                   headerline=str_format.format(rank="Rank", entity="Entity", amount="USD"),
                   data=RECORD_SEP.join([str_format.\
                                         format(rank=str(x+1),
                                                entity=getattr(self,
                                                               '_by_entity_{}_list'.\
                                                               format(in_or_out))[x][0],
                                                amount='{a:.02f}'.\
                                                format(a=getattr(self,
                                                                 '_by_entity_{}_list'.\
                                                                 format(in_or_out))[x][1]))
                                         for x in range(len(getattr(self,'_by_entity_{}_list'.\
                                                                    format(in_or_out))))]))
