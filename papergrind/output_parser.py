def find_first_tagged_cell(nb, tag):
    """Find the first tagged cell ``tag`` in the notebook.
    Parameters
    ----------
    nb : nbformat.NotebookNode
        The notebook to introspect
    tag : str
        The tag to look for
    Returns
    -------
    nbformat.NotebookNode
        the first nbformat.NotebookNode with tag ``tag``.
    """
    parameters_indices = []
    for cell in nb.cells:
        if tag in cell.metadata.tags:
            return cell
    return None


def find_tagged_cells(nb, tag):
    """Find all the cells with tag ``tag`` in the notebook.
    Parameters
    ----------
    nb : nbformat.NotebookNode
        The notebook to introspect
    tag : str
        The tag to look for
    Returns
    -------
    [nbformat.NotebookNode]
        list of nbformat.NotebookNode with tag ``tag``.
    """
    hits = []
    for cell in nb.cells:
        if tag in cell.metadata.tags:
            hits.append(cell)
    return hits


def find_typed_outputs(nb_cell, output_type, output_filter_fn=None):
    """Find the outputs of specific type.
    The ``output_filter_fn`` is a function that takes in list element from cell.outputs, and
    the index in the located output list, with a signature
    ``lambda: idx: int, cell_output: nbformat.NotebookNode -> bool``

    When ``output_filter_fn`` = None, the ``output_filter_fn`` is equivalent
    to `output_filter_fn = lambda idx, cell_output: True`,
    which accepts any located outputs.
    """
    hits = []
    for _, output in enumerate(nb_cell.outputs):
        if output_type == output.output_type:
            hits.append(output)

    if output_filter_fn is None:
        filtered = hits
    else:
        filtered = []
        for idx, output in enumerate(hits):
            if output_filter_fn(idx, output):
                filtered.append(output)
    return filtered


class CellLocator:
    def locate(self, nb):
        return []


class SingleCellTagLocator(CellLocator):
    def __init__(self, tag):
        self.tag = tag

    def locate(self, nb):
        cell = find_first_tagged_cell(nb, self.tag)
        if cell is not None:
            return [cell]
        return []


class AllCellTagLocator(CellLocator):
    def __init__(self, tag):
        self.tag = tag

    def locate(self, nb):
        return find_tagged_cells(nb, self.tag)


class OutputLocator:
    def locate(self, nb, output_filter_fn=None):
        return []


class TypedOutputLocator(OutputLocator):
    def __init__(self, output_type):
        self.output_type = output_type

    def locate(self, nb, output_filter_fn=None):
        return find_typed_outputs(
            nb, self.output_type, output_filter_fn=output_filter_fn)


class ResultLocator:
    """Locate result outputs from target notebook."""

    def __init__(self, cell_locator, output_locator):
        self.cell_locator = cell_locator
        self.output_locator = output_locator

    def locate(self, nb):
        cells = self.cell_locator.locate(nb)
        outputs = []
        for c in cells:
            outputs += self.output_locator.locate(c)
        return outputs
