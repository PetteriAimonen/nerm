Software requirements for nerm
==============================

This document lists the basic requirements for nerm - a simple requirements management tool.

Functional requirements
=======================

[FR-Discovery] Requirements discovery
-------------------------------------
Nerm can be given a list of paths, and it will recursively search for all `*.md` files.
Any heading starting with a tag in brackets `[]` is regarded as a requirement id.

- &#128279; [reqfile.py:69](nerm/reqfile.py#L69): Implements [FR-Discovery].
- &#128279; [test_reqfile.py:6](tests/test_reqfile.py#L6): Tests [FR-Discovery]
- &check; Satisfied by [reqfile.py:69](nerm/reqfile.py#L69) and [test_reqfile.py:6](tests/test_reqfile.py#L6)

[FR-Crossreference] Requirement cross-referencing
-------------------------------------------------
Nerm will search all text files, including source code, for tags in brackets.
If a tag matches an existing requirement tag, a cross-reference to the file is added.

- &#128279; [crossrefs.py:38](nerm/crossrefs.py#L38): Implements [FR-Crossreference]
- &#128279; [test_crossrefs.py:7](tests/test_crossrefs.py#L7): Tests [FR-Crossreference].
- &check; Satisfied by [crossrefs.py:38](nerm/crossrefs.py#L38) and [test_crossrefs.py:7](tests/test_crossrefs.py#L7)

[FR-Gitreferences] Cross-references from git commit messages
------------------------------------------------------------
If a git repository is detected, all commit messages are searched for requirement tags.
A cross-reference is added also from the commit that added the requirement.

[FR-Update] Updating cross-references
-------------------------------------
Nerm can add all discovered cross-references into the markdown file with the requirement.
References are added as relative path links in a list under the heading with the tag.
Any existing links that no longer exist are removed.

- &#128279; [update.py:72](nerm/update.py#L72): Implements [FR-Update].
- &#128279; [test_update.py:9](tests/test_update.py#L9): Tests [FR-Update].
- &check; Satisfied by [update.py:72](nerm/update.py#L72) and [test_update.py:9](tests/test_update.py#L9)

[FR-IncrementalUpdate] Incremental updating of cross-references
---------------------------------------------------------------
Updating the whole cross-reference list easily leads to conflicts between git branches when
line numbers change. Incremental update mode will not change existing lines if only
difference is the numeric values.

[FR-Satisfy] Determine satisfied requirements
---------------------------------------------
Criteria for satisfying a requirement are specified in a Nermfile.
By default there are no rules, i.e. requirements cannot be satisfied.

- &#128279; [satisfy.py:48](nerm/satisfy.py#L48): Implements [FR-Satisfy]
- &#128279; [test_satisfy.py:8](tests/test_satisfy.py#L8): Tests [FR-Satisfy].
- &check; Satisfied by [satisfy.py:48](nerm/satisfy.py#L48) and [test_satisfy.py:8](tests/test_satisfy.py#L8)

[FR-Report] Reporting requirement status
----------------------------------------
Nerm can report discovered requirements and whether they are satisfied.

[FR-Unknown] Reporting unknown cross-references
-----------------------------------------------
Nerm can list tags in brackets which do not correspond to any known requirement.

Documentation requirements
==========================

[DR-Example] A simple example
-----------------------------
A simple example case is needed for getting started with nerm.

[DR-Readme] Basic readme
------------------------
Readme should give installation instructions and simple walk-through with the example.

[DR-Nermfile] Nermfile format
-----------------------------
The format and what can be done within Nermfile should be documented.
