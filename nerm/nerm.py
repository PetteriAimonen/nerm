'''Nerm - No Effort Requirements Management
This file implements the main CLI interface.
'''

import argparse
import os.path
from .nermfile import default_settings, load_settings
from .reqfile import find_requirements

parser = argparse.ArgumentParser(description = 'Collect and update requirements')
parser.add_argument('-f', dest = 'nermfile', metavar = 'Nermfile', type=str,
                    help="Nermfile to read settings from")

def main_cli():
    args = parser.parse_args()

    if args.nermfile:
        settings = load_settings(args.nermfile)
    else:
        settings = load_settings("Nermfile", must_exist = False)

    tags = list(find_requirements(settings)):

    for tag, fpath in find_requirements():
        print('%s: %s' % (fpath, tag))

if __name__ == '__main__':
    main_cli()
