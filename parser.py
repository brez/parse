import argparse
import sys
import os.path
import json
from exceptions import UnknownOrAmbiguousPattern
from factories import factory


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Parse your file input into normalized JSON.')
    parser.add_argument(
        '--in', required=True, help='the input file')
    parser.add_argument(
        '--out', default='out.json', help='the output file (default out.json)')
    args = vars(parser.parse_args())

    if(not os.path.isfile(args['in'])):
        sys.exit("The infile you provided is not valid, exiting")

    entries, errors, line_number = ([], [], 0)

    with open(args['in']) as infile:
        for line in infile:
            try:
                entries.append(factory(line).parse())
            except UnknownOrAmbiguousPattern:
                errors.append(line_number)
            line_number += 1

    out = {"entries": entries, "errors": errors}

    with open(args['out'], 'a') as outfile:
        outfile.write(json.dumps(out, sort_keys=True, indent=2))
