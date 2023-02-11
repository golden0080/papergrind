class BaseParamSequence(object):
    def param_dict(self):
        all_names = self.names
        for vals in self.values():
            yield dict(zip(all_names, vals))

    def values(self):
        yield from self._seq

    def __iter__(self):
        return iter(self.values())


class LinkedParamSequence(BaseParamSequence):
    def __init__(self, param_names, seq):
        self.names = param_names
        self._seq = seq

    def __len__(self):
        return len(self.names)


class ParamSequence(LinkedParamSequence):
    def __init__(self, param_name, seq):
        super().__init__([param_name], seq)

    def values(self):
        for val in self._seq:
            yield [val]


class CombinationParams(BaseParamSequence):
    def __init__(self, *params):
        self.params = params

    def __len__(self):
        total_len = 0
        for param in self.params:
            total_len += len(param)
        return total_len

    @property
    def names(self):
        all_names = []
        for p in self.params:
            all_names += p.names
        return all_names

    def combo_iter(self, k, cur_values):
        if k >= len(self.params):
            yield cur_values
            return

        cur_iter = iter(self.params[k])
        try:
            while True:
                val = list(next(cur_iter))
                yield from self.combo_iter(k+1, cur_values + val)
        except StopIteration:
            pass

    def values(self):
        yield from self.combo_iter(0, [])
