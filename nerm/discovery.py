'''Discovery of requirements from Markdown files.'''

import marko

heading_types = (marko.block.Heading, marko.block.SetextHeading)

def list_requirements(document):
    '''List requirements from a single document.'''
    for item in document.children:
        if isinstance(item, marko.block.

def find_requirements(paths):
    '''Parses all markdown files given as argument, and returns a list of
    requirement tags as strings. Implements FR-Discovery.'''
