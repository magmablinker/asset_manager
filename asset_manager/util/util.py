import matplotlib.pyplot as plt

class Util(object):
    @staticmethod
    def round(value: float) -> float:
        return float("{:.2f}".format(value))

    @staticmethod
    def plot(x_axis: list, y_axis: list, title: str, x_label: str, y_label: str, file_path: str):
        plt.plot(x_axis, y_axis)

        plt.title(title)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        plt.savefig(file_path)
        
        #plt.show()

        plt.clf()