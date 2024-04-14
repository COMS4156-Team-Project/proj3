from Itemset import Itemset


class AssociationRule(object):
    def __init__(self, lhs: Itemset, rhs: Itemset, supp: float, conf: float):
        self.lhs = lhs
        self.rhs = rhs
        self.supp = supp
        self.conf = conf

    def __repr__(self):
        return f"{str(self.lhs)} => {str(self.rhs)} (Conf: {round(self.conf * 100, 2)}%, Supp: {round(self.supp * 100, 2)}%)"

    def __hash__(self):
        return hash(f"{str(self.lhs)} => {str(self.rhs)}")