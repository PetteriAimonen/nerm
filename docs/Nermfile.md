Nermfile settings reference
===========================
<!--- [DR-Nermfile] documented here --->

The functionality of nerm can be customized by creating a file called `Nermfile.toml`
in the project root folder (the folder where you run `nerm`).
A simple template is shown below:

    # Example config file
    [requirements]
    paths = ['requirements/**/*.md']

    [crossrefs]
    paths = ['**/*.c', '**/*.h', '**/*.md']

The default settings can be viewed in source code [nerm/nermfile.py](../nerm/nermfile.py).
Below they are explained section by section.

Requirements section
--------------------
Requirements section configures how requirement definitions and tags are discovered.

    [requirements]
    paths = ['**/*.md']
    patterns = ['^(\[[A-Za-z0-9][^ \]]*\])']

The `paths` key configures the list of files to search for requirement definitions.
Currently only Markdown-formatted files are supported.
Python glob patterns (`?`, `*` and `**`) can be used in the paths to match single character, any characters or any hierarchy of directories, respectively.

The `patterns` key has list of regular expression patterns that are searched for in the Markdown headings to detect the tag names. The default pattern matches tags separated by brackets `[]`.

Crossrefs section
-----------------
Crossrefs section configures how other files are searched for references to requirements.

    [crossrefs]
    paths = ['**/*']
    patterns = [
        '<!---*\s*(.*(\[[A-Za-z0-9][^ \]]*\]).*[^->])-*-->',
        '[#/*]\s*([^#/*].*(\[[A-Za-z0-9][^ \]]*\]).*)',
        '(.*(\[[A-Za-z0-9][^ \]]*\]).*)'
    ]

The `paths` key configures files that are scanned for tag references.
Note that the whole file is read, which can become slow for large projects.
This may be optimized in future, but for now it is recommended to exclude e.g. 3rd party libraries that are known to have no requirement references.

The `patterns` key configures patterns that are matched against each line in files.
The patterns are matched in order, and search ends on first match.
The default patterns attempt to first match a comment text, and then the whole line.
The first group in a pattern is the descriptive text for reference.

Git section
-----------
Git section configures optional integration with git version management.

    [git]
    path = '.'
    patterns = ['(.*(\[[A-Za-z0-9][^ \]]*\]).*)']

The `path` key configures path to the git repository root, relative to `Nermfile.toml` location.

The `patterns` key configures regexp pattern that is matched against each line in a commit message. It works the same way as `crossrefs.patterns`.

Satisfy section
---------------
Satisfy section configures rules that are used to evaluate whether a requirement has been met.
The default rules are empty, because this is very project-dependent configuration.

    [satisfy]
    rules = []
    ignore = ['^gitadd-.*']
    template = '{c.relpath}:{c.lineno} {c.fulltext}'

The `rules` key is a list of lists.
Each entry has the form `['TAG-PATTERN', 'CROSSREF-PATTERN']`.
The tag pattern selects which requirements the rule applies to.
The crossref pattern can also be a list of patterns, all of which must be matched.
For example this rule applies to any tag, and requires a cross reference that says "Satisfies" (case-insensitive): `['.*', '(?i)Satisfies']`.

The `ignore` key is a list of patterns, to ignore specific kinds of cross-references.
By default the automatically added references to the commit that adds the requirement are ignored for satisfy rules.

The `template` key specifies what fields of the reference are included in the text that is matched against the patterns. See the section *Format string keys* for list of available fields.

Update section
--------------
Update section configures how requirements files are modified when `-u` switch is specified.

    [update]
    location = 'end'

The `location` key can be set to `start` or `end` to list the cross references at either start or end of the document section.

Formats section
---------------
For each kind of cross reference there is a format specification section.
Currently the reference types are `fileref`, `gitref`, `gitadd` and `satisfy`.

    [formats.fileref]
    prefix = '- &#128462; '
    format = '[{c.basename}:{c.lineno}]({c.relpath}#L{c.lineno}): {c.fulltext}'

The `prefix` key specifies a string that is added to the beginning of the generated line.
This is also used to identify the generated lines the next time the tool is run, so it should
have a format that is not used in manually written text.
The default formats use unicode characters for the purpose.
If you want to change the prefix, it is suggested to first run `nerm -c` to remove any lines with old prefix, edit the `Nermfile` and then run `nerm -u` to add the new lines.

The `format` key configures the text generated for the reference.
It is a Python [str.format()](https://docs.python.org/3/library/stdtypes.html#str.format) specifier. The available keys are listed below in section *Format string keys*.

Format string keys
------------------
The conversion from internal object representation to text strings is controlled by format strings. The fields are surrounded by curly braces `{}`, such as `{c.basename}`. There are two available objects: `c` cross-reference object, and `r` requirement object.

The `c` object has following properties:
* `relation`: Type of reference, one of `fileref`, `gitref` and `gitadd`.
* `file`: Full path to file that has the reference.
* `relpath`: Relative path from the requirements document to the file with cross reference.
* `basename`: Filename, without path.
* `lineno`: Line number of the file that mentions the tag.
* `fulltext`: Full text on the line matched by the cross reference pattern.

For the `git` references, extra fields of `c` are available:
* `fullhash`: The full hash of the commit.
* `shorthash`: Shortened 6+ character hash of the commit.
* `author`: Name of the author of the commit.
* `summary`: First line of the commit message.
* `message`: Full text of the commit message.
* `datetime`: Date and time of the commit.
* `date`: Date only of the commit.

The `r` object has following properties:
* `tag`: The tag name of the requirement.
* `file`: Full path to the file that defines the requirement.
* `relpath`: Relative path from project root to the requirements document.
* `basename`: Filename of requirements document, without path.
* `lineno`: First line number of the requirement section.
* `last_lineno`: Last line number of the requirement section.
