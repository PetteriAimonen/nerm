'''Parsing of Nermfile settings file'''

import tomlkit
import os.path

default_config = r'''
# Example Nermfile.toml for specifying the settings for nerm requirements management tool.
# The settings shown are the defaults.
# Note: section names and settings are case-sensitive.

# *** Discovery of requirement definitions. ***
[requirements]

# List of files to search for requirement definitions.
# The files are parsed as Markdown files and only tags in headings are taken into account.
# Python glob patterns are supported: *, ? and **
paths = ['**/*.md']

# List of patterns to search for requirement tags.
# This regexp is matched against the heading text, and the first group is used as the tag.
# Default pattern matches tag in form of [TAG] in beginning of line.
patterns = ['(\[[A-Za-z0-9][^ \]]*\])']

# *** Discovery of cross-references in other files. ***
[crossrefs]

# List of files to search for references to requirements
# Files can be any UTF-8 text file type. Binary files are automatically ignored.
paths = ['**/*']

# Patterns to extract the relevant part of a line for cross-reference.
# These attempt to detect common source code comment delimiters.
# They are only applied to lines that contain a known requirement tag pattern.
patterns = [
    '<!---*(.*[^->])-*-->',
    '[#/*]([^#/*].*)',
    '(.*)'
]

# *** Discovery of cross-references in git commit messages ***
[git]

# Path to git repository root, relative to Nermfile.
path = '.'

# Patterns to search for in commit message.
# First group is the descriptive text and second group is the tag name.
patterns = [
    '(.*(\[[A-Za-z0-9][^ \]]*\]).*)'
]

# *** Rules for evaluating the satisfaction of requirements ***
[satisfy]

# Satisfaction is very project-dependent, by default no rules are specified.
# The rules is a list of lists, for example:
#
# rules = [
#    ['TAG-PATTERN', 'CROSSREF-PATTERN'],
#    ['TAG-PATTERN', ['CROSSREF-PATTERN1', 'CROSSREF-PATTERN2', ...]],
#    ...
# ]
#
# Tag pattern is matched against the tag name and the rule is used only for matching tags.
# Crossref patterns are matched against strings generated using template specified below.
# If multiple crossref patterns are given, they all must match for the rule to be satisfied.
#
# For example, this requires a cross-reference that says 'Satisfies' (case-insensitive):
#  ['.*', '(?i)Satisfies']
#
# This requires both a reference saying 'Implement' and another saying 'Test':
#  ['.*', ['(?i)Implement', '(?i)Test']]
#
rules = []

# Ignore specific kinds of cross-references for the purpose of satisfaction analysis.
ignore = ['^gitadd-.*']

# Template used to convert cross references to strings for satisfaction matching.
template = '{c.relpath}:{c.lineno} {c.fulltext}'

# *** Updating of Markdown files ***
[update]

# Location of the cross reference list. Either 'start' or 'end' of section.
location = 'end'

# *** Formatting rules for specific kinds of reference ***
# Existing lines matching one of the formatting prefixes are removed during update.

# References to other text files
[formats.fileref]
prefix = '- &#128462; '
format = '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno}): {c.fulltext}'
    
# References to git commits
[formats.gitref]
prefix = '- &#9939; '
format = '{c.shorthash}: {c.fulltext}'

# Reference to git commit that added the requirement
[formats.gitadd]
prefix = '- &#9733; Added by '
format = '{c.author} in {c.shorthash} on {c.date}'
    
# Reference to set of files that satisfy the requirement
[formats.satisfy]
prefix = '- &check; Satisfied by '
format = '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno})'
delimiter = ' and '

'''

def recursive_update(a, b):
    '''Recursively update a dict with new values.'''
    for k, v in b.items():
        if k in a and hasattr(v, 'items'):
            recursive_update(a[k], v)
        else:
            a[k] = v

def load_settings(filename, must_exist = True):
    '''Load a settings file from given path.'''
    settings = tomlkit.loads(default_config)

    if os.path.exists(filename):
        recursive_update(settings, tomlkit.loads(open(filename).read()))
    elif must_exist:
        raise FileNotFoundError('Not found: ' + filename)

    # Directory paths are relative to Nermfile
    settings['basedir'] = os.path.dirname(os.path.abspath(filename))

    return settings
