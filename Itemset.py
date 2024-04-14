from typing import Union
from typing_extensions import Self


class Itemset(object):
    items_dict = {}
    items_list = []

    def __init__(self, itemset: Union[list, tuple] = [], mask = None):
        if mask is not None:
            self.mask = mask
        else:
            self.mask = 0
            for item in itemset:
                assert(item in self.__class__.items_dict)
                self.mask ^= (1 << self.__class__.items_dict[item])

        self.items_list = self.get_items_list()
        self.mask_str = self.get_mask_str()

    @staticmethod
    def set_items(updated_items: Union[list, tuple]):
        Itemset.items_dict.clear()
        Itemset.items_list = updated_items
        for ind, item in enumerate(updated_items):
            Itemset.items_dict[item] = ind

    def get_highest_item_index(self):
        return self.mask.bit_length() - 1

    def is_subset_of(self, other: Self):
        if isinstance(other, Itemset):
            return (self.mask | other.mask) == other.mask
        else:
            raise ValueError("Must be an instance of Itemset class")

    def get_mask_str(self) -> str:
        mask_str = ""
        for i in range(len(Itemset.items_dict)):
            if (1 << i) & self.mask:
                mask_str += "1"
            else:
                mask_str += "0"

        return mask_str

    def get_items_list(self) -> tuple:
        self.items_list = []
        for i in range(len(Itemset.items_list)):
            if (1 << i) & self.mask:
                self.items_list.append(Itemset.items_list[i])

        return tuple(self.items_list)

    def __xor__(self, other):
        if isinstance(other, Itemset):
            return Itemset(mask = self.mask ^ other.mask)
        else:
            raise ValueError("Must be an instance of Itemset class")

    def __and__(self, other):
        if isinstance(other, Itemset):
            return Itemset(mask = self.mask & other.mask)
        else:
            raise ValueError("Must be an instance of Itemset class")

    def __or__(self, other):
        if isinstance(other, Itemset):
            return Itemset(mask = self.mask | other.mask)
        else:
            raise ValueError("Must be an instance of Itemset class")

    def __eq__(self, other):
        if isinstance(other, Itemset):
            return self.mask == other.mask
        else:
            raise ValueError("Must be an instance of Itemset class")

    def __str__(self):
        return str(self.items_list)

    def __repr__(self):
        return f"<Itemset Obj: {self.mask_str}>"

    def __hash__(self):
        return self.mask
