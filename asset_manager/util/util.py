class Util(object):
    @staticmethod
    def round(value: float) -> float:
        return float("{:.2f}".format(value))