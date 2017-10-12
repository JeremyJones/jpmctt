# JPMCTT by Jeremy Jones

## Description

JJ technical coding task, October 2017.

## Synopsis

    $ python main.py < sample-data.tsv

## Requirements Summary

> Given text data representing the instructions sent by various clients
> to execute in the international market, create a report that shows:
> 
> - Amount in USD settled incoming every day
> - Amount in USD settled outgoing every day
> - Ranking of entities based on incoming and outgoing amount

## Assumptions

In addition to the task details (as provided in the email) the
following assumptions have also been made:

* Python 3
* Data will contain a field delimiter (default tab), so that each record can be split()
* Consistent list of field names as defined in the sample data
* Consistent data types, format, and trust of incoming data
* The field names & other configuration information (e.g. workdays etc), for this version,
  do not need to be independently updateable e.g. via a config file or db option

## Output

To run the solution, send the data to main.py on standard input and
view the results on standard output, e.g.:

    $ cat sample-data.tsv | python main.py
    =========================================================
    AMOUNTS SETTLED EVERY DAY
    
    DATE         	   INCOMING (USD)	   OUTGOING (USD)
    04 Jan 2016  	             0.00	         30075.00
    07 Jan 2016  	         44698.50	             0.00
    =========================================================
    RANKING OF ENTITIES BASED ON INCOMING AMOUNT
    
          Rank	Entity          	             USD
             1	bar             	        44698.50
    =========================================================
    RANKING OF ENTITIES BASED ON OUTGOING AMOUNT
    
          Rank	Entity          	             USD
             1	foo             	        30075.00

    $

Depending on the amount of data it may be convenient to pipe the
output into `more` or `less` or into a file for further review.

## Notes

The format specifier .02f is used for rounding.

## Navigating the Repository

This repository contains:

* README.md - this file
* main.py - **primary wrapper** which adds the data from stdin and
  outputs the results to stdout.
* models.py - class definitions and configuration data.
* sample-data-longer.tsv - longer version of the sample data.
* sample-data.tsv - sample data as provided.
* test.py - unittest script

## Issues

* Reliance on hard-coded field names + globals, particularly for
  settlement date adjustments and USD calculation.
* The object code has a mixture of getattr/setattr style, and normal
  dot attribute style.
* The test coverage is not comprehensive.

## More Information

Running `pydoc` on main.py, models.py or test.py will display
additional information.

On main.py:

    $ pydoc ./main.py
    
    Help on module main:
    
    NAME
        main - main.py -- tech test by Jeremy Jones
    
    DESCRIPTION
        Given text data representing the instructions sent by various clients
        to execute in the international market, create a report that shows:
        
        - Amount in USD settled incoming every day
        - Amount in USD settled outgoing every day
        - Ranking of entities based on incoming and outgoing amount
        
        Usage: python main.py < data.tsv
    
    FUNCTIONS
        main()
            Process the data provided on standard input and print reports of
            the results to standard output.
    
    DATA
        stdin = <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>
    
    FILE
        main.py
    
    (END)

On models.py:

    $ pydoc ./models.py
    
    Help on module models:
    
    NAME
        models - models.py -- class definitions tech test
    
    DESCRIPTION
        Models for working with Buy/Sell instructions 
        
        Contents: 
        
          Instruction - Object to represent a single buy/sell instruction from a client.
          Solution - Object to create a list of instructions from data and report on them.
    
    CLASSES
        builtins.object
            Instruction
            Solution
        
        class Instruction(builtins.object)
         |  An Instruction represents a buy/sell instruction.
         |  
         |  Methods defined here:
         |  
         |  __init__(self)
         |      Create a new Instruction. Set placeholder attributes for the fields in FIELDS_LIST.
         |  
         |  finalise(self)
         |      Correct the SettlementDate if necessary and calculate USD Amount.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
        
        class Solution(builtins.object)
         |  Primary class to process the data and present the results.
         |  
         |  Methods defined here:
         |  
         |  __init__(self)
         |      Create a Solution object with an empty 'instructions' list.
         |  
         |  add_data(self, fh)
         |      Iterate over the supplied filehandle for tab-separated data and append it to
         |      the internal list.
         |      
         |      fh should be an iterable with an optional header line.
         |  
         |  report_amount_settled_every_day(self)
         |      Return a plain-text report on the amounts incoming & outgoing every
         |      day in the data.
         |  
         |  report_rank_entities(self, incoming_or_outgoing='incoming')
         |      Return a plain-text report on entities in the data, ranked by
         |      'outgoing' or 'incoming'.
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
    
    FUNCTIONS
        STR_TO_DATE lambda _
        
        STR_TO_FLOAT lambda _
            # helpers to cast incoming text values to other types
        
        STR_TO_INT lambda _
    
    DATA
        DATE_FORMAT = '%d %b %Y'
        FIELDS_LIST = ['Entity', 'Buy/Sell', 'AgreedFx', 'Currency', 'Instruct...
        FIELD_SEP = '\t'
        RECORD_SEP = '\n'
        TYPE_CONVERSIONS = {'AgreedFx': <function <lambda>>, 'InstructionDate'...
        WORKING_DAYS = {'AED': [6, 0, 1, 2, 3], 'SAR': [6, 0, 1, 2, 3], '_defa...
    
    FILE
        models.py
    
    (END)
    
For more contact:

* https://www.linkedin.com/in/jerjones/
* https://stackoverflow.com/users/5324657/jeremy-jones
