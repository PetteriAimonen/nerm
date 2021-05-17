Nerm - No Effort Requirements Management
========================================

Nerm is a tool that automatically updates Markdown-formatted text files to track
project requirements. For each requirement, nerm will list any files and git commits
that mention it. User can specify rules for satisfying requirements, such as
each requirement must have an implementation and a test, and nerm will check that.

Check out the [example requirements document](requirements/nerm.md).

Core principles
---------------

1. Requirement management tool should reduce effort, not add it.
   Nerm does not require boilerplate or complex formatting for the input files.

2. Information in one place: Instead of separate reports, the cross-references
   are added directly in the requirements document.


Installation
------------

Easiest way to install nerm is using Python package manager `pip`:

    pip install nerm

If `pip` on your system is Python 2.x, use `pip3` instead.

Once installed, you can test it works by running `nerm --help`.

Getting started
---------------
<!--- [DR-Readme] and [DR-Example] documented here --->

Create your requirements document as a Markdown formatted file.
For each requirement, add a heading that starts with a requirement tag in format `[TAG]`:

    [ExampleReq] Example requirement
    --------------------------------
    This is my example requirement.

When you add code or other files related to the requirement, use the tag in e.g. comments:

    myfunction() {
        // This function implements [ExampleReq]
    }

Now when you run `nerm -u`, the requirement document will get updated with a list of cross-references for each discovered tag.

To customize the functionality, you can create a `Nermfile.toml`.
See [full documentation](docs/Nermfile.md) for the available options.

Also check out [the requirements document](requirements/nerm.md) and [Nermfile](Nermfile.toml) of this project itself.