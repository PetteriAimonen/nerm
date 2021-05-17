'''Parsing and updating requirement files.'''

import commonmark
import re
import glob
import os.path
from collections import OrderedDict

def get_text(node):
    '''Concatenate the whole text of a node subtree.'''
    return ''.join(item.literal
                   for item, entering
                   in commonmark.node.NodeWalker(node)
                   if item.literal)

def iterate_headings(document):
    '''Iterate through heading texts.
    Yields (lineno, text).'''
    node = document.first_child
    last = node
    while node:
        if node.t == 'heading':
            yield (node.sourcepos[0][0], get_text(node))
        last = node
        node = node.nxt
    
    # Indicate end of document to iterate_requirements()
    yield (last.sourcepos[1][0], '')

class Requirement:
    def __init__(self, tag, file, relpath, lineno, last_lineno):
        self.tag = tag
        self.file = file
        self.relpath = relpath
        self.basename = os.path.basename(file)
        self.lineno = lineno
        self.last_lineno = last_lineno
        self.crossrefs = []
        self.satisfied_by = None

    def __str__(self):
        return 'Requirement(%s, %s)' % (self.tag, self.file)

def iterate_requirements(file, settings):
    '''Iterate requirements from a single document.'''
    parser = commonmark.Parser()
    patterns = [re.compile(p) for p in settings['requirements']['patterns']]
    document = parser.parse(open(file).read())
    relpath = os.path.relpath(file, settings['basedir'])
    prev_line = 0
    prev_tags = []

    for lineno, heading in iterate_headings(document):
        # Emit tags from previous heading, now that we know the end of the section
        for tag in prev_tags:
            yield Requirement(tag, file, relpath, prev_line, lineno - 1)

        prev_line = lineno
        prev_tags.clear()

        # Collect tags from this heading
        for pattern in patterns:
            for match in pattern.finditer(heading):
                prev_tags.append(match.group(1))

def find_requirements(settings):
    '''Parses all markdown files found in configured path and
    yields Requirement() objects.
    Implements [FR-Discovery].
    '''
    basedir = settings['basedir']
    result = OrderedDict()
    for path in settings['requirements']['paths']:
        abspath = os.path.abspath(os.path.join(settings['basedir'], path))
        for file in glob.glob(abspath, recursive = True):
            for req in iterate_requirements(file, settings):
                result[req.tag] = req
    
    return result

# For manual testing run with `python -m nerm.reqfile`
if __name__ == '__main__':
    from nerm import nermfile
    settings = nermfile.load_settings("Nermfile.toml", False)
    for req in find_requirements(settings).values():
        print('%s: %s (lines %d to %d)' % (os.path.relpath(req.file, settings['basedir']),
            req.tag, req.lineno, req.last_lineno))
