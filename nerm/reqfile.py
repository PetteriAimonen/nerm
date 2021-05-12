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
    while node:
        if node.t == 'heading':
            yield (node.sourcepos[0][0], get_text(node))
        node = node.nxt

def iterate_requirements(document, settings):
    '''Iterate requirements from a single document.'''
    patterns = [re.compile(p) for p in settings['requirement_patterns']]
    for lineno, heading in iterate_headings(document):
        for pattern in patterns:
            for match in pattern.finditer(heading):
                yield (lineno, match.group(1))

class Requirement:
    def __init__(self, tag, file, lineno, basedir):
        self.tag = tag
        self.file = file
        self.relpath = os.path.relpath(file, basedir)
        self.lineno = lineno
        self.crossrefs = []

    def __str__(self):
        return 'Requirement(%s, %s)' % (self.tag, self.file)

def find_requirements(settings):
    '''Parses all markdown files found in configured path and
    yields Requirement() objects.
    Implements [FR-Discovery].
    '''
    basedir = settings['basedir']
    parser = commonmark.Parser()
    result = OrderedDict()
    for path in settings['requirement_paths']:
        for file in glob.glob(path, recursive = True):
            document = parser.parse(open(file).read())
            for lineno, tag in iterate_requirements(document, settings):
                result[tag] = Requirement(tag, file, lineno, basedir)
    
    return result

# For manual testing run with `python -m nerm.reqfile`
if __name__ == '__main__':
    from nerm import nermfile
    settings = nermfile.load_settings("Nermfile", False)
    for req in find_requirements(settings).values():
        print('%s: %s' % (req.file, req.tag))
