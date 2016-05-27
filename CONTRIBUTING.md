Contributing to Emperor
=======================

[Emperor](http://biocore.github.io/emperor/) is an open source software package, and we welcome community contributions. You can find the source code and test code for Emperor under public revision control in the Emperor git repository on [GitHub](https://github.com/biocore/emperor). We very much welcome contributions.

This document covers what you should do to get started with contributing to Emperor. You should read this whole document before considering submitting code to Emperor. This will save time for both you and the Emperor developers.

Type of Submissions
-------------------

Some of the types of contributions we're interested in are new features (big or small, but for big ones it's generally a good idea to ask us if we're interested in including it before starting development), bug fixes, and documentation updates, additions, and fixes.  When considering submitting a new feature to Emperor, you should begin by posting an issue to the [Emperor issue tracker](https://github.com/biocore/emperor/issues). The information that you include in that post will differ based on the type of contribution. Your contribution will also need to be fully tested (discussed further below).

* For new features, you'll want to describe why the functionality that you are proposing to add is relevant. For it to be relevant, it should be demonstrably useful to Emperor users. This typically means that a new analytic method is implemented (you should describe why it's useful, ideally including a link to a paper that uses this method), or an existing method is enhanced (your implementation matches the performance of the pre-existing method while reducing runtime, memory consumption, etc, or it improves performance over the pre-existing method). We will request benchmark results comparing your method to the pre-existing methods (which would also be required for publication of your method) so pointing to a paper or other document containing benchmark results, or including benchmark results in your issue, will speed up the process.

* For bug fixes, you should provide a detailed description of the bug so other developers can reproduce it. We take bugs in Emperor very seriously. Bugs can be related to errors in code, documentation, or tests. Errors in documentation or tests are usually updated in the next major release of Emperor. Errors in code that could result in incorrect results or inability to access certain functionality may result in a new minor release of Emperor.

 You should include the following information in your bug report:

 1. The exact command or function call that you issue to create the bug.
 2. A link to all necessary input files for reproducing the bug. These files should only be as large as necessary to create the bug. This is *extremely* useful to other developer, and it is likely that if you don't provide this information you'll get a response asking for it. Often this process helps you to better understand the bug as well.
 3. The platform you are using (browser version and operating system).

For documentation additions, you should first post an issue describing what you propose to add, where you'd like to add it in the documentation, and a description of why you think it's an important addition. For documentation improvements and fixes, you should post an issue describing what is currently wrong or missing, and how you propose to address it. For more information about building and contributing to Emperor's documentation, see [this guide](doc/README.md).

When you post your issue, the Emperor developers will respond to let you know if we agree with the addition or change. It's very important that you go through this step to avoid wasting time working on a feature that we are not interested in including in Emperor.


Getting started: "quick fixes"
------------------------------

Some of our issues are labeled as ``quick fix``. Working on [these issues](https://github.com/biocore/Emperor/issues?direction=desc&labels=quick+fix&milestone=&page=1&sort=updated&state=open) is a good way to get started with contributing to Emperor. These are usually small bugs or documentation errors that will only require one or a few lines of code to fix. Getting started by working on one of these issues will allow you to familiarize yourself with our development process before committing to a large amount of work (e.g., adding a new feature to Emperor). If you're interested in working on one of these issues, you should comment on the issue requesting that it be assigned to you.


Code Review
-----------

When you submit code to Emperor, it will be reviewed by one or more Emperor developers. These reviews are intended to confirm a few points:

* Your code is sufficiently well-tested (see Testing Guidelines below).
* Your code adheres to our Coding Guidelines (see Coding Guidelines below).
* Your code is sufficiently well-documented (see Coding Guidelines below).
* Your code provides relevant changes or additions to Emperor (Type of Submissions above).

This process is designed to ensure the quality of Emperor, and can be a very useful experience for new developers.

Particularly for big changes, if you'd like feedback on your code in the form of a code review as you work, you should request help in the issue that you created and one of the Emperor developers will work with you to perform regular code reviews. This can greatly reduce development time (and frustration) so we highly recommend that new developers take advantage of this rather than submitting a pull request with a massive amount of code in one chunk. That can lead to frustration when the developer thinks they are done, but the reviewer requests large amounts of changes, and it is also very hard to review.


Submitting code to Emperor
-----------------------------

Emperor is hosted on [GitHub](http://www.github.com), and we use GitHub's [Pull Request](https://help.github.com/articles/using-pull-requests) mechanism for accepting submissions. You should go through the following steps to submit code to Emperor.

1. Begin by [creating an issue](https://github.com/biocore/Emperor/issues) describing your proposed change. This should include a description of your proposed change (is it a new feature, a bug fix, etc.), and note in the issue description that you want to work on it. Once you hear back from a maintainer that it is OK to make changes (i.e., they dont't have local edits, they agree with the change you'd like to make, and they're comfortable with you editing their code), we will assign the issue to you on GitHub.

2. [Fork](https://help.github.com/articles/fork-a-repo) the Emperor repository on the GitHub website to your GitHub account.

3. Clone your forked repository to the system where you'll be developing with ``git clone``.

4. Ensure that you have the latest version of all files (especially important if you cloned a long time ago, but you'll need to do this before submitting changes regardless). You should do this by adding Emperor as a remote repository and then pulling from that repository. You'll only need to run the ``git remote`` step one time:
```
git checkout master
git remote add upstream https://github.com/biocore/emperor.git
git pull upstream master
```

5. Create a new topic branch that you will make your changes in with ``git checkout -b``:
```
git checkout -b my-topic-branch
```

6. Run ``python tests/all_tests.py --emperor_scripts_dir scripts`` to confirm that the tests pass before you make any changes.

7. Make your changes, add them (with ``git add``), and commit them (with ``git commit``). Don't forget to update associated scripts and tests as necessary. You should make incremental commits, rather than one massive commit at the end. Write descriptive commit messages to accompany each commit.

8. When you think you're ready to submit your code, again ensure that you have the latest version of all files in case some changed while you were working on your edits. You can do this by merging master into your topic branch:
```
git checkout my-topic-branch
git pull upstream master
```

9. Run ``python tests/all_tests.py --emperor_scripts_dir scripts`` to ensure that your changes did not cause anything expected to break.

10. Once the tests pass, you should push your changes to your forked repository on GitHub using:
```
git push origin my-topic-branch
```

11. Issue a [pull request](https://help.github.com/articles/using-pull-requests) on the GitHub website to request that we merge your branch's changes into Emperor's master branch. One of the Emperor developers will review your code at this stage. If we request changes (which is very common), *don't issue a new pull request*. You should make changes on your topic branch, and commit and push them to GitHub. Your pull request will update automatically.

12. Once your pull request is submitted and if there are no merge conflicts, you should see an automatic message posted by [@emperor-helper](https://github.com/emperor-helper). The message will include a link to the built script usage examples (the use-cases that are described at the top of `make_emperor.py --help`). The goal is to provide an easy way for reviewers and developers to verify that the GUI is functional and works as expected **with your new changes**. For more information about @emperor-helper, see this [project](https://github.com/eldeveloper/worker).


Coding Guidelines
-----------------

For **Python** code, we adhere to the [PEP 8](http://www.python.org/dev/peps/pep-0008/) python coding guidelines for code and documentation standards. For **JavaScript** code, we adhere to the [Google closure](https://google.github.io/styleguide/javascriptguide.xml) javascript coding standards, and use [JSDoc](http://usejsdoc.org/) to compile all javascript documentation. When using the closure linter, we allow the `module`, `function`, `constructs`, `alias`, and `default` custom JSDoc tags. For the most up to date version of the allowed JSDoc tags, see the [Travis configuration file](.travis.yml).

Before submitting any code to Emperor, you should read these carefully and apply the guidelines in your code. As part of our automated testing, we make sure that all code passes linter standards and documentation compiles. We use the [gjslint](https://developers.google.com/closure/utilities/) linter to test javascript code with the `--custom_jsdoc_tags module,function,constructs,alias,default` modifier, and the [flake8](https://pypi.python.org/pypi/flake8) linter to test python code.

Testing Guidelines
------------------

All code that is added to Emperor must be unit tested, and the unit test code must be submitted in the same pull request as the library code that you are submitting. We will only merge code that is unit tested and that passes the [continuous integration build](https://github.com/biocore/emperor/blob/master/.travis.yml), this build verifies that the:

- Full test suite executes without errors (including JavaScript and script usage tests).
- All python code in Emperor is PEP8-compliant.
- All javascript code in Emperor is google closure compliant.
- All code is valid in Python 2.7.x.
- The documentation can be built correctly.

Emperor adheres to scikit-bio's coding guidelines see our [expectations for unit tests](http://scikit-bio.org/development/coding_guidelines.html). You should review the unit test section before working on your test code.

If you are adding a new parameter to a command line utility, make sure you add a new usage example to the script and that you add the relevant files to `tests/script_test_data/`.

Tests can be executed using the `all_tests.py` script located inside the tests directory. This script will execute:

- Python unit tests.
- Script usage unit tests.
- JavaScript unit tests (these depend on the [phantom.js](http://phantomjs.org) being installed on your system), but you can also execute them opening `tests/javascript_tests/index.html` in your browser (we recommend Google Chrome).

After this script is executed a summary of the tests that failed will be printed to the screen.

Getting help with git
=====================

If you're new to ``git``, you'll probably find [gitref.org](http://gitref.org/) helpful.
