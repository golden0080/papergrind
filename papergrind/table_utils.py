import pandas as pd

def export_to_csv(df, file_csv):
    df.to_csv(file_csv, index=False)


def read_from_csv(file_csv):
    df = pd.read_csv(file_csv)


class TableResultCollector():

    def __init__(self, params, path_format_str):
        self.params = params
        self.path_format_str = path_format_str

    def get_file_path(self, param_dict):
        return self.path_format_str.format(**param_dict)

    def collect_data(self, filter_fn=None, apply_fn=None):
        """Collect data from output table data files.
        `filter_fn` is of signature: lambda param_dict: bool, return True for all data file that want to collect.
        """
        if filter_fn is None:
            filter_fn = lambda _: True

        all_df = []
        for param_dict in self.params.param_dict():
            if not filter_fn(param_dict):
                continue
            df = read_from_csv(self.get_file_path(param_dict))
            all_df.append(df)

        output = pd.concat(all_df, ignore_index=True, axis=0)
        if apply_fn is not None:
            output = output.apply(apply_fn, axis=1, result_type="expand")
        return output
