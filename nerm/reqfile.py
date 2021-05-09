'''Parsing and updating requirement files.'''

import marko
from . import nermfile
import re
import glob

heading_types = (marko.block.Heading, marko.block.SetextHeading)

def iterate_headings(document):
    '''Iterate through heading texts'''
    for item in document.children:
        if isinstance(item, heading_types):
            if item.children and isinstance(item.children[0].children, str):
                yield item.children[0].children

def iterate_requirements(document, settings = nermfile.default_settings):
    '''Iterate requirements from a single document.'''
    pattern = re.compile(settings['requirement_pattern'])
    for heading in iterate_headings(document):
        for match in pattern.findall(heading):
            yield match

def find_requirements(settings = nermfile.default_settings):
    '''Parses all markdown files found in configured path and iterates
    requirement tags as tuples ('tag', 'file.md').
    Implements [FR-Discovery].
    '''
    markdown = marko.Markdown()
    for path in settings['requirement_paths']:
        for fpath in glob.glob(path, recursive = True):
            document = markdown.parse(open(fpath).read())
            for tag in iterate_requirements(document, settings):
                yield (tag, fpath)

# For manual testing
if __name__ == '__main__':
    for tag, fpath in find_requirements():
        print('%s: %s' % (fpath, tag))
