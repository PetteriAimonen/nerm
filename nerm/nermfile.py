'''Parsing of Nermfile settings file'''

import tomlkit
import os.path

default_settings = {
    'requirement_paths': ['**/*.md'],
    'crossref_paths': ['**/*'],
    'requirement_patterns': [r'^(\[[A-Za-z0-9][^ \]]*\])'],
    'crossref_patterns': [r'(\[[A-Za-z0-9][^ \]]*\]).*'],
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
