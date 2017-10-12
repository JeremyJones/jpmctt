"""main.py -- tech test by Jeremy Jones

Given text data representing the instructions sent by various clients
to execute in the international market, create a report that shows:

- Amount in USD settled incoming every day
- Amount in USD settled outgoing every day
- Ranking of entities based on incoming and outgoing amount

Usage: python main.py < data.tsv
"""

from sys import stdin
from models import Solution

def main():
    """Process the data provided on standard input and print reports of
    the results to standard output.
    """

    sol = Solution()
    sol.add_data(stdin)

    print("=========================================================")
    print(sol.report_amount_settled_every_day())
    print("=========================================================")
    print(sol.report_rank_entities('incoming'))
    print("=========================================================")
    print(sol.report_rank_entities('outgoing'))

    
if __name__ == '__main__':
    main()
