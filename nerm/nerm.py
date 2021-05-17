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

from .nermfile import load_settings
from .reqfile import find_requirements
from .gitrefs import find_git_references
from .crossrefs import find_cross_references
from .satisfy import check_satisfied
from .update import update_all_crossrefs

parser = argparse.ArgumentParser(description = 'Collect and update requirements')
parser.add_argument('-f', dest = 'nermfile', metavar = 'Nermfile', type=str,
                    help="Nermfile to read settings from")
parser.add_argument('-u', dest = 'update', action = 'store_true',
                    help="Update list of cross-references in requirement documents.")

def main_cli():
    args = parser.parse_args()

    if args.nermfile:
        settings = load_settings(args.nermfile)
    else:
        settings = load_settings("Nermfile.toml", must_exist = False)

    reqs = find_requirements(settings)
    find_git_references(reqs, settings)
    find_cross_references(reqs, settings)
    check_satisfied(reqs, settings)

    for req in reqs.values():
        crossrefs = ', '.join('{c.basename}:{c.lineno}'.format(c = c) for c in req.crossrefs)
        if crossrefs: crossrefs = ' (' + crossrefs + ')'
        satisfied = ''
        if req.satisfied_by: satisfied = ' (satisfied)'
        print('%s: %s%s%s' % (req.relpath, req.tag, crossrefs, satisfied))
    
    if args.update:
        update_all_crossrefs(reqs, settings)

if __name__ == '__main__':
    main_cli()
