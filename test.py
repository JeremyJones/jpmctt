"""
Test the code for the tech test solution.
"""
import unittest
from models import Instruction, Solution, FIELDS_LIST

class TechTestJerJones(unittest.TestCase):
    def test_Instruction(self):
        """Test the Instruction object, which represents a single Buy or Sell
        instruction from a client.
        """
        i = Instruction()

        assert type(i) == Instruction, "Instruction is an Instruction"

        for mfield in FIELDS_LIST:
            assert bool(type(getattr(i, mfield))) == True, \
                "Instruction has a {} slot".format(mfield)

    def test_Solution(self):
        """Test the top-level Solution object, which holds the data and reports on it.
        """
        s = Solution()

        assert type(s) == Solution, "Solution is a Solution"

        for zmetho in ['add_data','report_amount_settled_every_day',
                     'report_rank_entities']:
            assert getattr(s, zmetho, None) is not None, \
                "Solution has the {} attribute/method".format(zmetho)

        
if __name__ == '__main__':
    unittest.main()
