import pandas as pd

class DFPlus(pd.DataFrame):
    @property
    def _constructor(self):
        return DFPlus

    @classmethod
    def from_csv(cls, filepath, **kwargs):
        df = pd.read_csv(filepath, **kwargs)
        return cls(df)

    def print_with_headers(self):
        rows_per_chunk = 10
        total_rows = len(self)

        for start in range(0, total_rows, rows_per_chunk):
            end = min(start + rows_per_chunk, total_rows)
            print("\n=== Rows {} to {} ===".format(start, end - 1))
            print(self.iloc[start:end])


if __name__ == "__main__":
    dfp = DFPlus.from_csv("csv/products.csv")
    dfp.print_with_headers()