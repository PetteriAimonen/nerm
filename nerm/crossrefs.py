'''Finds cross references to requirement tags.'''

import re
import glob
import os.path

def iterate_crossrefs(file, known_tags, settings):
    '''Yields (lineno, tag, full_text) for
    each known tag found in the file.'''
    patterns = [re.compile(p) for p in settings['crossref_patterns']]
    try:
        lineno = 0
        for line in open(file):
            lineno += 1
            for pattern in patterns:
                match = pattern.search(line)
                if match and match.group(1) in known_tags:
                    yield (lineno, match.group(1), match.group(0))
    except UnicodeDecodeError:
        pass # Binary file

def find_cross_references(requirements, settings):
    '''Search through all files in cross-reference path and
    add found references to the Requirement objects as tuples
    (file, lineno, full_text).
    Implements [FR-Crossreference]
    '''

    known_tags = requirements.keys()

    for path in settings['crossref_paths']:
        for file in glob.glob(path, recursive = True):
            if os.path.isfile(file):
                for lineno, tag, full_text in iterate_crossrefs(file, known_tags, settings):
                    req = requirements[tag]
                    
                    if req.file == file and req.lineno <= lineno <= req.last_lineno:
                        # This is the requirement itself, skip
                        continue
                    else:
                        # Add cross-reference
                        req.crossrefs.append((file, lineno, full_text))

# For manual testing run with `python -m nerm.crossrefs`
if __name__ == '__main__':
    from . import nermfile, reqfile
    settings = nermfile.load_settings("Nermfile", False)
    reqs = reqfile.find_requirements(settings)
    find_cross_references(reqs, settings)
    for req in reqs.values():
        crossrefs = str(["%s:%d" % (os.path.basename(c[0]), c[1]) for c in req.crossrefs])
        print('%s: %s' % (req.tag, crossrefs))