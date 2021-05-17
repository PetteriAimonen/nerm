'''Update markdown files to list cross-references.'''

import re
import os
import os.path
from tempfile import NamedTemporaryFile

def is_generated_line(line, settings):
    '''Checks if the line starts with one of the prefixes for generated lines.'''
    for k, v in settings['formats'].items():
        if line.startswith(v['prefix']):
            return True
    
    return False

def write_crossrefs(dstfile, requirement, settings):
    '''Write list of cross-references to output file.'''
    for crossref in requirement.crossrefs:
        fmt = settings['formats'].get(crossref.relation)

        if fmt and fmt.get('prefix'):
            dstfile.write(fmt['prefix']
                          + fmt['format'].format(c = crossref, r = requirement)
                          + '\n')

def write_satisfy(dstfile, requirement, settings):
    '''Write a line indicating the requirement is satisfied.'''
    if requirement.satisfied_by:
        fmt = settings['formats']['satisfy']
        terms = [fmt['format'].format(c = crossref, r = requirement)
                 for crossref in requirement.satisfied_by]
        terms = fmt['delimiter'].join(terms)
        dstfile.write(fmt['prefix'] + terms + '\n')

def update_document(file, dstfile, requirements, settings):
    '''Update all cross references in given file.
    Removes any existing lines that start with crossref_prefix.
    Adds new lines according to crossrefs in Requirement objects.
    '''
    srcfile = open(file)
    
    if isinstance(dstfile, str):
        dstfile = open(dstfile, 'w')
    
    # Collect positions of document where we need to insert crossrefs
    insertion_points = set()
    for req in requirements.values():
        if settings['update']['location'] == 'start':
            req.crossref_pos = req.lineno
        else:
            req.crossref_pos = req.last_lineno
        
        insertion_points.add(req.crossref_pos)

    prev_line_removed = False
    srclineno = 0
    for line in srcfile:
        srclineno += 1
        
        # Remove any old cross-references, keep other lines
        if is_generated_line(line, settings):
            line = ''
            prev_line_removed = True
        elif prev_line_removed and not line.strip():
            # Empty line after a removed line
            pass
        else:
            dstfile.write(line)
            prev_line_removed = False
        
        if srclineno in insertion_points:
            for req in requirements.values():
                if srclineno == req.crossref_pos and req.crossrefs:
                    if line.strip():
                        dstfile.write('\n') # Empty line before list

                    write_crossrefs(dstfile, req, settings)
                    write_satisfy(dstfile, req, settings)
                    dstfile.write('\n') # Empty line at end

def update_all_crossrefs(requirements, settings):
    '''Go through all requirement documents and update the cross reference lists in-place.
    Implements [FR-Update].
    '''
    files = set(req.file for req in requirements.values())
    for file in files:
        # Update in-place with a temporary file
        dstfile = NamedTemporaryFile(mode = "w", dir = os.path.dirname(file),
                                     prefix = os.path.basename(file) + "~",
                                     suffix = '.tmp',
                                     delete = False)
        dstname = dstfile.name

        try:
            update_document(file, dstfile, requirements, settings)
            dstfile.close()
            os.rename(dstname, file)
        finally:
            if os.path.exists(dstname):
                os.remove(dstname)

# For manual testing run with `python -m nerm.update`
# Results are written under /tmp
if __name__ == '__main__':
    from . import nermfile, reqfile, crossrefs
    settings = nermfile.load_settings("Nermfile.toml", False)
    reqs = reqfile.find_requirements(settings)
    crossrefs.find_cross_references(reqs, settings)

    files = set(req.file for req in reqs.values())
    for file in files:
        dst_path = '/tmp/' + os.path.basename(file)
        update_document(file, dst_path, reqs, settings)
        print(os.path.relpath(file, settings['basedir']) + " -> " + dst_path)
