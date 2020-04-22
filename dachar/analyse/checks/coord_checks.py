from ._base_check import _BaseCheck


class RankCheck(_BaseCheck):

    characteristics = ['data.coord_names', 'data.shape']

    def run(self, population):
        return 1
