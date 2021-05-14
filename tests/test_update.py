import nerm.reqfile
import nerm.nermfile
import nerm.crossrefs
import nerm.update
import tempfile

def test_update():
    '''Test the writing of cross-reference list to Markdown file.
    Tests [FR-Update].
    '''
    settings = nerm.nermfile.load_settings("tests/data/Nermfile", must_exist = False)
    reqs = nerm.reqfile.find_requirements(settings)
    nerm.crossrefs.find_cross_references(reqs, settings)

    dst = tempfile.NamedTemporaryFile('w+')
    nerm.update.update_document('tests/data/test.md', dst, reqs, settings)

    dst.seek(0)
    lines = dst.readlines()

    lines_with_refs = [line for line in lines if line.startswith(settings['crossref_prefix'])]
    
    assert 'otherdoc.md' in lines_with_refs[0]
    assert 'test.md' in lines_with_refs[1]