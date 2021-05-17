Software requirements for nerm
==============================

This document lists the basic requirements for nerm - a simple requirements management tool.

Functional requirements
=======================

[FR-Discovery] Requirements discovery
-------------------------------------
Nerm can be given a list of paths, and it will recursively search for all `*.md` files.
Any heading starting with a tag in brackets `[]` is regarded as a requirement id.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09
- &#128462; [reqfile.py:69](nerm/reqfile.py#L69): Implements [FR-Discovery].
- &#128462; [test_reqfile.py:6](tests/test_reqfile.py#L6): Tests [FR-Discovery]
- &check; Satisfied by [reqfile.py:69](nerm/reqfile.py#L69) and [test_reqfile.py:6](tests/test_reqfile.py#L6)

[FR-Crossreference] Requirement cross-referencing
-------------------------------------------------
Nerm will search all text files, including source code, for tags in brackets.
If a tag matches an existing requirement tag, a cross-reference to the file is added.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09
- &#128462; [crossrefs.py:44](nerm/crossrefs.py#L44): Implements [FR-Crossreference]
- &#128462; [test_crossrefs.py:7](tests/test_crossrefs.py#L7): Tests [FR-Crossreference].
- &check; Satisfied by [crossrefs.py:44](nerm/crossrefs.py#L44) and [test_crossrefs.py:7](tests/test_crossrefs.py#L7)

[FR-Gitreferences] Cross-references from git commit messages
------------------------------------------------------------
If a git repository is detected, all commit messages are searched for requirement tags.
A cross-reference is added also from the commit that added the requirement.

- &#9733; Added by Petteri Aimonen in 3c01f9 on 2021-05-12
- &#128462; [gitrefs.py:73](nerm/gitrefs.py#L73): Implements [FR-Gitreferences].

[FR-Update] Updating cross-references
-------------------------------------
Nerm can add all discovered cross-references into the markdown file with the requirement.
References are added as relative path links in a list under the heading with the tag.
Any existing links that no longer exist are removed.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09
- &#9939; 767921: Implement [FR-Update]
- &#128462; [update.py:83](nerm/update.py#L83): Implements [FR-Update].
- &#128462; [test_update.py:9](tests/test_update.py#L9): Tests [FR-Update].
- &check; Satisfied by [update.py:83](nerm/update.py#L83) and [test_update.py:9](tests/test_update.py#L9)

[FR-IncrementalUpdate] Incremental updating of cross-references
---------------------------------------------------------------
Updating the whole cross-reference list easily leads to conflicts between git branches when
line numbers change. Incremental update mode will not change existing lines if only
difference is the numeric values.

- &#9733; Added by Petteri Aimonen in 9a8ac7 on 2021-05-17

[FR-Satisfy] Determine satisfied requirements
---------------------------------------------
Criteria for satisfying a requirement are specified in a Nermfile.
By default there are no rules, i.e. requirements cannot be satisfied.

- &#9733; Added by Petteri Aimonen in f61606 on 2021-05-14
- &#9939; 90f70b: Implement [FR-Satisfy]
- &#128462; [satisfy.py:51](nerm/satisfy.py#L51): Implements [FR-Satisfy]
- &#128462; [test_satisfy.py:8](tests/test_satisfy.py#L8): Tests [FR-Satisfy].
- &check; Satisfied by [satisfy.py:51](nerm/satisfy.py#L51) and [test_satisfy.py:8](tests/test_satisfy.py#L8)

[FR-Report] Reporting requirement status
----------------------------------------
Nerm can report discovered requirements and whether they are satisfied.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09

[FR-Unknown] Reporting unknown cross-references
-----------------------------------------------
Nerm can list tags in brackets which do not correspond to any known requirement.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09

Documentation requirements
==========================

[DR-Example] A simple example
-----------------------------
A simple example case is needed for getting started with nerm.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09

[DR-Readme] Basic readme
------------------------
Readme should give installation instructions and simple walk-through with the example.

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09

[DR-Nermfile] Nermfile format
-----------------------------

- &#9733; Added by Petteri Aimonen in f9bbb1 on 2021-05-09

The format and what can be done within Nermfile should be documented.
