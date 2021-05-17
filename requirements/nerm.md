Software requirements for nerm
==============================

This document lists the basic requirements for nerm - a simple requirements management tool.

Functional requirements
=======================

[FR-Discovery] Requirements discovery
-------------------------------------
Nerm can be given a list of paths, and it will recursively search for all `*.md` files.
Any heading starting with a tag in brackets `[]` is regarded as a requirement id.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09
- &#128462; [reqfile.py:69](../nerm/reqfile.py#L69): Implements [FR-Discovery].
- &#128462; [test_reqfile.py:6](../tests/test_reqfile.py#L6): Tests [FR-Discovery]

[FR-Crossreference] Requirement cross-referencing
-------------------------------------------------
Nerm will search all text files, including source code, for tags in brackets.
If a tag matches an existing requirement tag, a cross-reference to the file is added.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09
- &#9939; [a351a5](https://github.com/PetteriAimonen/nerm/commit/a351a5dc8e612f1489c321f2f8e7337905e9fecb): [FR-Crossreference] Basic cross reference discovery implemented
- &#128462; [crossrefs.py:53](../nerm/crossrefs.py#L53): Implements [FR-Crossreference]
- &#128462; [test_crossrefs.py:7](../tests/test_crossrefs.py#L7): Tests [FR-Crossreference].

[FR-Gitreferences] Cross-references from git commit messages
------------------------------------------------------------
If a git repository is detected, all commit messages are searched for requirement tags.
A cross-reference is added also from the commit that added the requirement.

- &#9733; Added by Petteri Aimonen in [3c01f9](https://github.com/PetteriAimonen/nerm/commit/3c01f9039525b4dc1620428b1baf477f21a55bb9) on 2021-05-12
- &#9939; [ace598](https://github.com/PetteriAimonen/nerm/commit/ace598374c975b21746ce8655449700650093cf4): Implement [FR-Gitreferences]
- &#128462; [gitrefs.py:76](../nerm/gitrefs.py#L76): Implements [FR-Gitreferences].

[FR-Update] Updating cross-references
-------------------------------------
Nerm can add all discovered cross-references into the markdown file with the requirement.
References are added as relative path links in a list under the heading with the tag.
Any existing links that no longer exist are removed.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09
- &#9939; [767921](https://github.com/PetteriAimonen/nerm/commit/7679219acb8c8d1804d61db7f6f7b843d5c1932a): Implement [FR-Update]
- &#128462; [update.py:83](../nerm/update.py#L83): Implements [FR-Update].
- &#128462; [test_update.py:9](../tests/test_update.py#L9): Tests [FR-Update].

[FR-IncrementalUpdate] Incremental updating of cross-references
---------------------------------------------------------------
Updating the whole cross-reference list easily leads to conflicts between git branches when
line numbers change. Incremental update mode will not change existing lines if only
difference is the numeric values.

- &#9733; Added by Petteri Aimonen in [9a8ac7](https://github.com/PetteriAimonen/nerm/commit/9a8ac763eba285fc16856f25fab3fea1d2b028ca) on 2021-05-17

[FR-Satisfy] Determine satisfied requirements
---------------------------------------------
Criteria for satisfying a requirement are specified in a Nermfile.
By default there are no rules, i.e. requirements cannot be satisfied.

- &#9733; Added by Petteri Aimonen in [f61606](https://github.com/PetteriAimonen/nerm/commit/f61606d2eabe4bc3a2a30cae4360752212fc697d) on 2021-05-14
- &#9939; [90f70b](https://github.com/PetteriAimonen/nerm/commit/90f70bb71d3123d3b49a23e0ae3a62dab9e39ebe): Implement [FR-Satisfy]
- &#128462; [satisfy.py:51](../nerm/satisfy.py#L51): Implements [FR-Satisfy]
- &#128462; [test_satisfy.py:8](../tests/test_satisfy.py#L8): Tests [FR-Satisfy].

[FR-Report] Reporting requirement status
----------------------------------------
Nerm can report discovered requirements and whether they are satisfied.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09

[FR-Unknown] Reporting unknown cross-references
-----------------------------------------------
Nerm can list tags in brackets which do not correspond to any known requirement.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09

Documentation requirements
==========================

[DR-Example] A simple example
-----------------------------
A simple example case is needed for getting started with nerm.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09
- &#128462; [README.md:34](../README.md#L34): [DR-Readme] and [DR-Example] documented here
- &check; Satisfied by [README.md:34](../README.md#L34)

[DR-Readme] Basic readme
------------------------
Readme should give installation instructions and simple walk-through with the example.

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09
- &#128462; [README.md:34](../README.md#L34): [DR-Readme] and [DR-Example] documented here
- &check; Satisfied by [README.md:34](../README.md#L34)

[DR-Nermfile] Nermfile format
-----------------------------

- &#9733; Added by Petteri Aimonen in [f9bbb1](https://github.com/PetteriAimonen/nerm/commit/f9bbb1b4c583a2d826c12bbaa3b9f85d6985d0d5) on 2021-05-09
- &#128462; [Nermfile.md:3](../docs/Nermfile.md#L3): [DR-Nermfile] documented here
- &check; Satisfied by [Nermfile.md:3](../docs/Nermfile.md#L3)

The format and what can be done within Nermfile should be documented.
