import pprint


class MarkdownPresenter(object):
    def data(self, input_data):
        """
        return {
            "source": "",
        }
        """
        return None


class ResultPresenter(object):
    def data(self, result_outputs):
        """
        return {
            "source": "",
            "outputs": [],
        }
        """
        return None


class ParameterPresenter(MarkdownPresenter):
    def source(self, param_dict):
        return "# Results generated using the following overrides\n\n```\n{param_dict}\n```".format(
            param_dict=pprint.pformat(param_dict)
        )

    def data(self, param_dict):
        return {
            "source": self.source(param_dict),
        }


class ResultPresenter(ResultPresenter):
    def __init__(self, result_title):
        self.result_title = result_title

    def source(self):
        return f"# {self.result_title}"

    def data(self, results):
        return {
            "source": self.source(),
            "outputs": results,
        }
