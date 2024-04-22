import pandas as pd


class Dataset(object):
    def __init__(self, path: str):
        self.df = pd.read_csv(path)

    def get_items(self) -> list:
        items = []
        for col in self.df.columns.values:
            extra_items = set()
            if col == 'injured_bucket':
                for injured_val in set(self.df[col].unique()):
                    extra_items |= set(injured_val.split(','))
            else:
                extra_items = self.df[col].unique()

            items += list(extra_items)

        return items

    def get_market_baskets(self) -> list[tuple]:
        def process_record(row):
            updated_row = []
            for val in row:
                if 'injured' in val:
                    updated_row.extend(val.split(','))
                else:
                    updated_row.append(val)
            return tuple(updated_row)

        market_baskets = list(map(process_record, list(self.df.to_records(index=False))))
        return market_baskets

