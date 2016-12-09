import sys
import csv
import matplotlib.pyplot as plt

from os import listdir, makedirs
from os.path import isfile, isdir, join, exists, dirname, split


def check_output(output_path):
    dir_path = dirname(output_path)
    if not exists(dir_path):
        makedirs(dir_path)
    elif not isdir(dir_path):
        raise Exception("The given output %s was not a directory" % dir_path)


def get_files(input_path):
    files = []
    if isfile(input):
        files = [input]
    elif isdir(input):
        for f in listdir(input):
            path = join(input, f)
            if isfile(path) and path.endswith('.csv'):
                files.append(path)
    else:
        raise Exception("Could not locate input: %s" % input)

    return files


def csv_reader(paths):
    offsets = []
    times = []
    for f in paths:
        with open(f) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                offsets.append(row[2])
                times.append(row[0])

    return (offsets, times)


def plot_offset_time(offsets, times, output):
    plt.plot(offsets, times)
    plt.xlabel('Offset (Bytes)')
    plt.ylabel('Time (Miliseconds)')
    plt.title('The Time it Takes to Read a GeoTiff at a\nGiven Byte Offset'
              'in Miliseconds')
    (dir_path, file_name) = split(output)
    plt.savefig(join(dir_path, file_name))


if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]

    check_output(output)
    files = get_files(input)
    (offsets, times) = csv_reader(files)
    plot_offset_time(offsets, times, output)
