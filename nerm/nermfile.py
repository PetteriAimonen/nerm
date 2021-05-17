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
patterns = ['^(\[[A-Za-z0-9][^ \]]*\])']

# *** Discovery of cross-references in other files. ***
[crossrefs]

# List of files to search for references to requirements
# Files can be any UTF-8 text file type. Binary files are automatically ignored.
paths = ['**/*']

# Patterns to search for cross-references.
# The regexp is matched against a single line of file.
# The first group is the description text and second group the tag name.
# Default patterns match a comment text or a whole line.
patterns = [
    '[#/*]\s*([^#/*].*(\[[A-Za-z0-9][^ \]]*\]).*)',
    '([^\s].*(\[[A-Za-z0-9][^ \]]*\]).*)'
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

# Template used to convert cross references to strings for satisfaction matching.
template = '{c.relpath}:{c.lineno} {c.fulltext}'

# *** Updating of Markdown files ***
[update]

# Location of the cross reference list. Either 'start' or 'end' of section.
location = 'end'

# Prefix to use in new cross references added to list.
# Any lines starting with this prefix will be removed during update.
crossref_prefix = '- &#128279; '

# Format for cross references, by default a link with #L123 anchor to jump to line.
crossref_format = '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno}): {c.fulltext}'

# Prefix to use in lines indicating requirement satisfaction.
# Any lines starting with this prefix will be removed during update.
satisfy_prefix = '- &check; Satisfied by '

# Format for terms in requirement satisfaction line
satisfy_term_format = '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno})'

# Delimiter between multiple terms
satisfy_term_delimiter = ' and '

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
