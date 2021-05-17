'''Finds cross references to requirement tags from text files.'''

import re
import glob
import os.path
from .update import is_generated_line

class Crossref:
    def __init__(self, file, relpath, lineno, fulltext, relation = 'fileref'):
        self.relation = relation
        self.file = file
        self.relpath = relpath
        self.basename = os.path.basename(file)
        self.lineno = lineno
        self.fulltext = fulltext.strip()

    def __str__(self):
        return '%s:%d %s' % (self.basename, self.lineno, self.fulltext)

def iterate_crossrefs(file, known_tags, settings):
    '''Yields (lineno, tag, full_text) for
    each known tag found in the file.'''
    tag_pattern = re.compile('|'.join(re.escape(tag) for tag in known_tags))
    patterns = [re.compile(p) for p in settings['crossrefs']['patterns']]
    try:
        lineno = 0
        for line in open(file):
            lineno += 1

            if is_generated_line(line, settings):
                continue

            if tag_pattern.search(line):
                # Contains at least one tag, find the comment format.

                for pattern in patterns:
                    match = pattern.search(line)
                    if match:
                        fulltext = match.group(1)
                        for tag in known_tags:
                            if tag in fulltext:
                                yield (lineno, tag, fulltext)
                        break


    except UnicodeDecodeError:
        pass # Binary file

def find_cross_references(requirements, settings):
    '''Search through all files in cross-reference path and
    add found references to the Requirement objects as tuples
    (file, lineno, full_text).
    Implements [FR-Crossreference]
    '''

    known_tags = set(requirements.keys())

    for path in settings['crossrefs']['paths']:
        abspath = os.path.abspath(os.path.join(settings['basedir'], path))
        for file in glob.glob(abspath, recursive = True):
            if os.path.isfile(file):
                for lineno, tag, fulltext in iterate_crossrefs(file, known_tags, settings):
                    req = requirements[tag]
                    
                    if req.file == file and req.lineno <= lineno <= req.last_lineno:
                        # This is the requirement itself, skip
                        continue
                    else:
                        # Add cross-reference
                        relpath = os.path.relpath(file, os.path.dirname(req.file))
                        req.crossrefs.append(Crossref(file, relpath, lineno, fulltext))

# For manual testing run with `python -m nerm.crossrefs`
if __name__ == '__main__':
    from . import nermfile, reqfile
    settings = nermfile.load_settings("Nermfile.toml", False)
    reqs = reqfile.find_requirements(settings)
    find_cross_references(reqs, settings)
    for req in reqs.values():
        print('%s: %s' % (req.tag, [str(c) for c in req.crossrefs]))