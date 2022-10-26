#!/usr/bin/python3

__version__ = "0.0.1"

from ptlibs import ptjsonlib, ptmisclib
import argparse
import sys
import json

from CsvProvider import CsvProvider

class ptwebcategory:
    def __init__(self, args):
        self.ptjsonlib = ptjsonlib.ptjsonlib(args.json)
        self.json_no = self.ptjsonlib.add_json("ptwebcategory")
        self.use_json = args.json
        self.args = args

    def run(self):
        if self.args.file:
            print(self.args.file)
            csv_provider = CsvProvider(self.args.file)
            #...
            csv_provider.extract_forms()
            csv_provider.extract_javascript()
            #csv_provider.extract_css()
            #...
            csv_provider.save_file()
        sys.exit(0)


def get_help():
    return [
        {"description": [
            "Target categorization tool for web application penetration testing"]},
        {"usage": ["ptwebcategory <options>"]},
        {"usage_example": [
            "ptwebcategory -f",
        ]},
        {"options": [
            ["-f", "--file", "<file path>", "Load urls from file"],
            ["-j",  "--json", "",  "Output in JSON format"],
            ["-v",  "--version", "", "Show script version and exit"],
            ["-h", "--help", "", "Show this help message and exit"],
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False, usage=f"{SCRIPTNAME} <options>")
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-v", "--version", action="version",
                        version=f"%(prog)s {__version__}")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)

    args = parser.parse_args()
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptwebcategory"
    args = parse_args()
    script = ptwebcategory(args)
    script.run()


if __name__ == "__main__":
    main()