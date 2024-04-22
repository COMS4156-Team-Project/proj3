import pandas as pd


class Dataset(object):
    def __init__(self, path: str):
        self.df = pd.read_csv(path)

    def get_items(self) -> list:
        items  = []
        for col in self.df.columns.values:
            items += list(self.df[col].unique())

        return items

    def get_market_baskets(self) -> list[tuple]:
        return list(self.df.to_records(index=False))

