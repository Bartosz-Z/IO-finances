import argparse


class ArgumentParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('exp_name')
        self._parser.add_argument('json_path')
        self._parser.add_argument('-o', '--out', help='path to where create output directory. Not implemented yet.')
        self._parser.add_argument('-data_path', nargs='?', default=None) # Optional argument
        self._parser.add_argument('-genotype_path', nargs='?', default=None) 

    def parse(self):
        return self._parser.parse_args()
