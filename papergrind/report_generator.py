import papermill as pm
import nbformat as nbf
from papergrind import notebook_presenter


class ReportNotebookGenerator():

    def __init__(
            self, section_presenter, result_locator_dict,
            report_path=None, result_presenter_dict=None):
        self.output_path = report_path
        self.section_presenter = section_presenter
        self.locator_dict = result_locator_dict
        self.presenter_dict = result_presenter_dict
        if self.presenter_dict is None:
            self.presenter_dict = {}

    def generate_section(self, param_dict, result_nb):
        cells = []
        section_data = self.section_presenter.data(param_dict)
        if section_data is not None:
            cells.append(nbf.v4.new_markdown_cell(**section_data))

        for key, result_locator in self.locator_dict.items():
            result_presenter = self.presenter_dict.get(
                key, notebook_presenter.ResultPresenter(key))

            outputs = result_locator.locate(result_nb)
            present_data = result_presenter.data(outputs)
            if present_data is not None:
                cells.append(nbf.v4.new_code_cell(**present_data))

        return cells

    def generate_report(self, param_nb_pairs):
        report_notebook = nbf.v4.new_notebook()
        for params, result_nb in param_nb_pairs:
            report_notebook.cells += self.generate_section(params, result_nb)

        if self.output_path is not None:
            pm.iorw.write_ipynb(report_notebook, self.output_path)
            print(f"Report generated: '{self.output_path}' ...")
        return report_notebook
