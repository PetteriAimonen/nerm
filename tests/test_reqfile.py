import nerm.reqfile
import nerm.nermfile

def test_discovery():
    '''Tests discovery of requirement tags.
    Tests [FR-Discovery]
    '''
    settings = nerm.nermfile.load_settings("tests/data/Nermfile", must_exist = False)
    reqs = list(nerm.reqfile.find_requirements(settings))
    assert reqs[0][0] == '[TEST1]'
    assert reqs[0][1].endswith('tests/data/test.md')
    assert reqs[1][0] == '[TEST2]'
    assert reqs[1][1].endswith('tests/data/test.md')
