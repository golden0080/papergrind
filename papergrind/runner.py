"""
Integration with papermill to automate result generation

Within Notebooks, run command to install papermill first:
%pip install papermill
"""

import papermill as pm


class NotebookRunner():
    def __init__(self, params, template_path, output_filename_template_format_str):
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
        # so far only support single thread
        assert num_workers == 1, "Only Single Worker supported now."

        for param_dict in self.params.param_dict():
            pm.execute_notebook(
                self.template_path,
                self.get_output_filename(param_dict),
                parameters=param_dict
            )
