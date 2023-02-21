"""
Integration with papermill to automate result generation

Within Notebooks, run command to install papermill first:
%pip install papermill
"""

import multiprocessing as multi
import papermill as pm


class NotebookRunner():
    def __init__(
            self, params, template_path, output_filename_template_format_str,
    ):
        self.template_path = template_path
        self.output_filename_format_str = output_filename_template_format_str
        self.params = params

    def _validate(self):
        if self.output_filename_format_str is None:
            print("Output filename is empty: No files would be saved.")
            return None
        it = iter(self.params.param_dict())
        param_dict = next(it)
        return self.output_filename_format_str.format(**param_dict)

    def get_output_filename(self, param_dict):
        if self.output_filename_format_str is None:
            return None

        return self.output_filename_format_str.format(**param_dict)

    def run(self, num_workers=1):
        results = []
        with multi.Pool(num_workers) as pool:
            futures = []
            for param_dict in self.params.param_dict():
                res_future = pool.apply_async(
                    pm.execute_notebook,
                    args=(
                        self.template_path,
                        self.get_output_filename(param_dict)
                    ),
                    kwds={
                        "parameters": param_dict,
                    }
                )
                futures.append((param_dict, res_future))
            for param_dict, res in futures:
                nb_output = res.get()
                results.append((param_dict, nb_output))

        return results
