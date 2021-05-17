import nerm.reqfile
import nerm.nermfile

def test_discovery():
    '''Tests discovery of requirement tags.
    Tests [FR-Discovery]
    '''
    settings = nerm.nermfile.load_settings("tests/data/Nermfile.toml")
    reqs = nerm.reqfile.find_requirements(settings)
    result = [(req.tag, req.relpath, req.lineno)
              for req in reqs.values()]
    assert result == [('[TEST1]', 'test.md', 4),
                      ('[TEST2]', 'test.md', 8)]
    