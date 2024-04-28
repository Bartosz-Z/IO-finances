import argparse


class ArgumentParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('json_path')

    def parse(self):
        return self._parser.parse_args()
