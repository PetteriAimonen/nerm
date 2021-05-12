#!/usr/bin/env python3

'''Nerm - No Effort Requirements Management
This file implements the main CLI interface.
'''

import argparse
import os.path
import sys

# PEP 366 package name setting to allow relative imports in Python 3
# https://stackoverflow.com/questions/2943847/nightmare-with-relative-imports-how-does-pep-366-work
if __name__ == "__main__" and __package__ is None:
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, basedir)
    import nerm
    __package__ = str("nerm")

from .nermfile import default_settings, load_settings
from .reqfile import find_requirements
from .crossrefs import find_cross_references

parser = argparse.ArgumentParser(description = 'Collect and update requirements')
parser.add_argument('-f', dest = 'nermfile', metavar = 'Nermfile', type=str,
                    help="Nermfile to read settings from")

def main_cli():
    args = parser.parse_args()

    if args.nermfile:
        settings = load_settings(args.nermfile)
    else:
        settings = load_settings("Nermfile", must_exist = False)

    reqs = find_requirements(settings)
    find_cross_references(reqs, settings)

    for req in reqs.values():
        crossrefs = ', '.join("%s:%d" % (os.path.basename(c[0]), c[1]) for c in req.crossrefs)
        if crossrefs: crossrefs = ' (' + crossrefs + ')'
        print('%s: %s%s' % (req.relpath, req.tag, crossrefs))

if __name__ == '__main__':
    main_cli()
