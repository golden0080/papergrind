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

    def run(self, num_workers=1, autosave_every=60):
        results = []
        errs = {}
        outputs = set()
        with multi.Pool(num_workers) as pool:
            futures = []
            for param_dict in self.params.param_dict():
                expected_output = self.get_output_filename(param_dict)
                if expected_output in outputs:
                    print(
                        f"WARN: output overwrite detected on file {expected_output},"
                        " Proceed with cautions...")
                outputs.add(expected_output)
                res_future = pool.apply_async(
                    pm.execute_notebook,
                    args=(
                        self.template_path,
                        expected_output
                    ),
                    kwds={
                        "parameters": param_dict,
                        "autosave_cell_every": autosave_every,
                    }
                )
                futures.append((param_dict, res_future))
            for param_dict, res in futures:
                expected_output = self.get_output_filename(param_dict)
                try:
                    nb_output = res.get()
                    results.append((param_dict, nb_output))
                except e:
                    print(f"Error when running {expected_output}... Recording errors...")
                    errs[expected_output] = e

        return results, errs
