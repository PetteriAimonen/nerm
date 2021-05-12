Software requirements for nerm
==============================

This document lists the basic requirements for nerm - a simple requirements management tool.

Functional requirements
=======================

[FR-Discovery] Requirements discovery
-------------------------------------
Nerm can be given a list of paths, and it will recursively search for all `*.md` files.
Any heading starting with a tag in brackets `[]` is regarded as a requirement id.

[FR-Crossreference] Requirement cross-referencing
-------------------------------------------------
Nerm will search all text files, including source code, for tags in brackets.
If a tag matches an existing requirement tag, a cross-reference to the file is added.

[FR-Gitreferences] Cross-references from git commit messages
------------------------------------------------------------
If a git repository is detected, all commit messages are searched for requirement tags.
A cross-reference is added also from the commit that added the requirement.

[FR-Update] Updating cross-references
-------------------------------------
Nerm can add all discovered cross-references into the markdown file with the requirement.
References are added as relative path links in a list under the heading with the tag.
Any existing links that no longer exist are removed.

[FR-Report] Reporting requirement status
----------------------------------------
Nerm can report discovered requirements and whether they are satisfied.
Criteria for satisfying a requirement are specified in a Nermfile.
By default a requirement is satisfied if it is referenced at least once.

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
