from AssociationRule import AssociationRule
from Dataset import Dataset
from Itemset import Itemset
from typing import Dict
from utils import get_subsets


class Apriori(object):
    '''
        Class for defining the Apriori Algorithm
    '''
    def __init__(self, dataset_path: str = None, min_supp: float = 0.1, min_conf: float = 0.9, test: bool = False):
        self.min_supp = min_supp
        self.min_conf = min_conf

        if test: # Only for testing purposes
            self.items = ['pen', 'ink', 'diary', 'soap']
            self.market_baskets = [
                ('pen', 'ink', 'diary', 'soap'),
                ('pen', 'ink', 'diary'),
                ('pen', 'diary'),
                ('pen', 'ink', 'soap')
            ]
        else:
            assert(dataset_path is not None)
            dataset = Dataset(dataset_path)
            self.items = dataset.get_items()
            self.market_baskets = dataset.get_market_baskets()

        Itemset.set_items(self.items)
        self.market_basket_itemsets = []
        for basket in self.market_baskets:
            self.market_basket_itemsets.append(Itemset(basket))

    def need_to_prune(self, freqset: Itemset, prev_freqsets: set[Itemset]) -> bool:
        '''
        Checks if we need to prune the itemset
        '''
        mask = freqset.mask
        prev_freqsets = set(prev_freqsets)
        for i in range(len(freqset.items_list)):
            if (1 << i) & mask:
                temp_mask = mask ^ (1 << i)
                temp_itemset = Itemset(mask=temp_mask)
                if temp_itemset not in prev_freqsets:
                    return True
        return False

    def filter_by_support(self, cand_itemsets: set[Itemset]) -> tuple[set[Itemset], Dict[Itemset, float]]:
        '''
        Filters itemsets with provided minsupp value.
        '''
        filtered_itemsets = set()
        itemset_support_dict = dict()
        for itemset in cand_itemsets:
            count = 0
            for basket in self.market_basket_itemsets:
                if itemset.is_subset_of(basket):
                    count += 1

            if count / len(self.market_basket_itemsets) >= self.min_supp:
                filtered_itemsets.add(itemset)
                itemset_support_dict[itemset] = count / len(self.market_basket_itemsets)

        return filtered_itemsets, itemset_support_dict

    def apriori_gen(self, large_itemsets: set[Itemset]) -> set[Itemset]:
        # Base case: To get size 1 itemsets
        if len(large_itemsets) == 0:
            return set(Itemset([item]) for item in self.items)

        itemset_grps: Dict[Itemset: list[Itemset]] = {}
        cand_itemsets: set[Itemset] = set()
        for itemset in large_itemsets:
            kth_idx = itemset.get_highest_item_index()
            kth_idx_item = Itemset(mask=(1<<kth_idx))
            itemset_without_kth_idx = itemset ^ kth_idx_item
            if itemset_without_kth_idx not in itemset_grps:
                itemset_grps[itemset_without_kth_idx] = []
            itemset_grps[itemset_without_kth_idx].append(kth_idx_item)

        for itemset_without_kth_idx, kth_idx_item_list in itemset_grps.items():
            kth_idx_item_list.sort(key=lambda item: item.mask)
            for i in range(len(kth_idx_item_list)):
                for j in range(i+1, len(kth_idx_item_list)):
                    cand_itemset = (itemset_without_kth_idx ^ kth_idx_item_list[i] ^ kth_idx_item_list[j])
                    if not self.need_to_prune(cand_itemset, large_itemsets):
                        cand_itemsets.add(cand_itemset)

        return  cand_itemsets

    def get_all_itemsets_with_min_support(self) -> Dict[Itemset, float]:
        itemset_support_dict = {}
        prev_itemsets = set()

        while True:
            cand_itemsets = self.apriori_gen(prev_itemsets)
            filtered_itemsets, filtered_itemset_support_dict = self.filter_by_support(cand_itemsets)
            itemset_support_dict.update(filtered_itemset_support_dict)
            if len(filtered_itemsets) == 0:
                break
            prev_itemsets = filtered_itemsets

        return itemset_support_dict

    def filter_by_confidence(self, itemset_supp_dict: Dict[Itemset, float]) -> set[AssociationRule]:
        association_rules = set()
        for itemset, supp in itemset_supp_dict.items():
            for submask in get_subsets(itemset.mask):
                lhs = Itemset(mask=submask)
                rhs = lhs ^ itemset
                conf = supp / itemset_supp_dict[lhs]
                if conf >= self.min_conf:
                    association_rules.add(AssociationRule(lhs, rhs, supp, conf))

        return association_rules

    def print_association_rules(self, association_rules: set[AssociationRule]):
        print(f"==High-confidence association rules (min_conf={round(self.min_conf * 100, 2)}%)")
        for rule in sorted(list(association_rules), key=lambda x: x.conf, reverse=True):
            print(rule)

    def print_frequent_itemsets(self, min_supp_itemset_dict: Dict[Itemset, float]):
        print(f"==Frequent itemsets (min_sup={round(self.min_supp * 100, 2)}%)")
        min_supp_itemset_tuples = list(min_supp_itemset_dict.items())
        for itemset, supp in sorted(min_supp_itemset_tuples, key=lambda x: x[1], reverse=True):
            print(f"{str(itemset)}, {round(supp * 100, 2)}%")


    def filter_spurious_association_rules(self, association_rules: set[AssociationRule]):
        filtered_rules = set()
        for rule in association_rules:
            lhs_injured = False
            lhs_killed = False
            rhs_injured = False
            rhs_killed = False
            if True in [('injured' in item) for item in rule.lhs.items_list]:
                lhs_injured = True
            if True in [('killed' in item) for item in rule.lhs.items_list]:
                lhs_killed = True
            if True in [('injured' in item) for item in rule.rhs.items_list]:
                rhs_injured = True
            if True in [('killed' in item) for item in rule.rhs.items_list]:
                rhs_killed = True

            if (lhs_killed or lhs_injured) and (rhs_killed or rhs_injured):
                continue

            filtered_rules.add(rule)

        return filtered_rules

    def execute(self):
        min_supp_itemset_dict = self.get_all_itemsets_with_min_support()
        association_rules = self.filter_by_confidence(min_supp_itemset_dict)
        self.print_frequent_itemsets(min_supp_itemset_dict)
        self.print_association_rules(self.filter_spurious_association_rules((association_rules)))

