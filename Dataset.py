import pandas as pd


class Dataset(object):
    def __init__(self, path: str):
        self.df = pd.read_csv(path)
        self._perform_data_quality_checks()

    def _perform_data_quality_checks(self):
        pass

    def get_items(self) -> list:
        pass

    def get_market_baskets(self) -> list[tuple]:
        pass

