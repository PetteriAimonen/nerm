'''Parsing of Nermfile settings file'''

import tomlkit
import os.path

default_settings = {
    'requirement_paths': ['**/*.md'],
    'crossref_paths': ['**/*'],
    'requirement_patterns': [r'^(\[[A-Za-z0-9][^ \]]*\])'],
    'crossref_patterns': [r'(?:[^\s][^#/*]*)?(\[[A-Za-z0-9][^ \]]*\]).*'],
    'crossref_prefix': '- &#128279; ',
    'crossref_format': '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno}): {c.fulltext}',
    'crossref_location': 'end',
    'satisfy_rules': [],
    'satisfy_template': '{c.relpath}:{c.lineno} {c.fulltext}',
    'satisfy_prefix': '- &check; Satisfied by ',
    'satisfy_term_delimiter': ' and ',
    'satisfy_term_format': '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno})',
}

def load_settings(filename, must_exist = True):
    '''Load a settings file from given path.'''
    settings = dict(default_settings)

    if os.path.exists(filename):
        settings.update(tomlkit.loads(open(filename).read()))
    elif must_exist:
        raise FileNotFoundError('Not found: ' + filename)

    # Make directory paths relative to Nermfile
    basedir = os.path.dirname(os.path.abspath(filename))
    settings_with_path = ['requirement_paths', 'crossref_paths']
    for sname in settings_with_path:
        settings[sname] = [os.path.join(basedir, path) for path in settings[sname]]

    settings['basedir'] = basedir

    return settings
