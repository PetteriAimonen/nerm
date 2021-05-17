import nerm.reqfile
import nerm.nermfile
import nerm.crossrefs
import nerm.satisfy

def test_satisfy():
    '''Test applying satisfaction rules.
    Tests [FR-Satisfy].
    '''
    settings = nerm.nermfile.load_settings("tests/data/Nermfile.toml")
    reqs = nerm.reqfile.find_requirements(settings)
    nerm.crossrefs.find_cross_references(reqs, settings)
    nerm.satisfy.check_satisfied(reqs, settings)

    assert reqs['[TEST1]'].satisfied_by
    assert reqs['[TEST2]'].satisfied_by is None
