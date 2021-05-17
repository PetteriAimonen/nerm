'''Find cross references from git commit history.'''

import re
import os.path
import git
from nerm.crossrefs import Crossref

class Gitref(Crossref):
    def __init__(self, commit, fulltext, relation = 'gitref'):
        self.relation = relation
        self.commit = commit
        self.fullhash = commit.hexsha
        self.shorthash = commit.repo.git.rev_parse(self.fullhash, short = 6)
        self.author = str(commit.author)
        self.summary = commit.summary
        self.message = commit.message
        self.datetime = commit.committed_datetime
        self.date = self.datetime.date()
        self.fulltext = fulltext.strip()

        # For compatibility with Crossref class
        self.file = self.relpath = self.basename = self.relation + '-' + self.shorthash
        self.lineno = ''
    
    def __str__(self):
        return '%s %s' % (self.shorthash, self.fulltext)

def crossref_exists(requirement, commit):
    '''Returns true if a reference to specified commit already exists.'''
    for ref in requirement.crossrefs:
        if isinstance(ref, Gitref) and ref.commit == commit:
            return True
    
    return False

def process_commits(repo, requirements, settings):
    '''Iterate through all commits in current branch and search for tag references.'''
    
    known_tags = set(requirements.keys())
    tag_pattern = re.compile('|'.join(re.escape(tag) for tag in known_tags))
    patterns = [re.compile(p) for p in settings['git']['patterns']]
    
    for commit in repo.iter_commits(reverse = True):
        lines = commit.message.split('\n')
        for line in lines:
            if tag_pattern.search(line):
                for pattern in patterns:
                    match = pattern.search(line)
                    if match:
                        fulltext = match.group(1)

                        for tag in known_tags:
                            if tag in fulltext and not crossref_exists(requirements[tag], commit):
                                requirements[tag].crossrefs.append(Gitref(commit, fulltext))

def process_blame(repo, file, requirements, settings):
    '''Iterate through all commits to a requirement file and note the commit that
    added the requirement.'''

    remaining = set(req.tag for req in requirements.values() if req.file == file)
    
    for commit in repo.iter_commits(paths = file, reverse = True):
        relpath = os.path.relpath(file, repo.working_dir)
        data_at_commit = repo.git.show(commit.hexsha + ':' + relpath)

        for tag in list(remaining):
            if tag in data_at_commit:
                # First appearance of this tag
                remaining.remove(tag)
                requirements[tag].crossrefs.append(Gitref(commit, commit.summary, relation = 'gitadd'))

def find_git_references(requirements, settings):
    '''Automatically detect whether a git repository exists.
    If it does, go through the commits and add cross references to those
    that add new requirements or mention their tag name.
    Implements [FR-Gitreferences].
    '''
    gitpath = os.path.join(settings['basedir'], settings['git']['path'])
    if not os.path.isdir(os.path.join(gitpath, '.git')):
        return
    
    repo = git.Repo(gitpath)

    # Search when each requirement was first added
    files = set(req.file for req in requirements.values())
    for file in files:
        process_blame(repo, file, requirements, settings)
    
    # Search references in commit messages
    process_commits(repo, requirements, settings)

# For manual testing run with `python -m nerm.gitrefs`
if __name__ == '__main__':
    from . import nermfile, reqfile
    settings = nermfile.load_settings("Nermfile.toml", False)
    reqs = reqfile.find_requirements(settings)
    find_git_references(reqs, settings)
    for req in reqs.values():
        print('%s: %s' % (req.tag, [str(c) for c in req.crossrefs]))