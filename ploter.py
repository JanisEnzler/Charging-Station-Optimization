import matplotlib.pyplot as plt
from MAS.environment.time_converter import convert_time_to_string


def plot_array_as_hist(array, bins, title, xlabel, ylabel):

    formatter = plt.FuncFormatter(convert_time_to_string)

    plt.hist(array, bins=bins)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()

def plot_array(array, title, xlabel, ylabel):
    formatter = plt.FuncFormatter(convert_time_to_string)

    plt.plot(array)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()


def plot_array_as_bar(array, title, xlabel, ylabel):
    formatter = plt.FuncFormatter(convert_time_to_string)

    plt.bar(range(len(array)), array)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()