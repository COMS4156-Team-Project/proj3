import sys
from Apriori import Apriori


def get_cmdline_args():
    if len(sys.argv) != 4:
        sys.exit("REQUIRED FORMAT: python main.py [integrated dataset file path] [Minimum support] [Minimum confidence]")

    filename, min_supp, min_conf = sys.argv[1:]
    min_supp = float(min_supp)
    min_conf = float(min_conf)
    return filename, min_supp, min_conf


if __name__ == '__main__':
    filename, min_supp, min_conf = get_cmdline_args()
    apriori_algo = Apriori(filename, min_supp, min_conf, test=True)
    apriori_algo.execute()

