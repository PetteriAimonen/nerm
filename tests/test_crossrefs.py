import nerm.reqfile
import nerm.nermfile
import nerm.crossrefs

def test_crossrefs():
    '''Test the matching of cross-references to requirement tags.
    Tests [FR-Crossreference].
    '''
    settings = nerm.nermfile.load_settings("tests/data/Nermfile.toml")
    reqs = nerm.reqfile.find_requirements(settings)
    nerm.crossrefs.find_cross_references(reqs, settings)
    result = [(req.tag, [cref.lineno for cref in req.crossrefs])
              for req in reqs.values()]
    assert result == [('[TEST1]', [1]),
                      ('[TEST2]', [6])]
