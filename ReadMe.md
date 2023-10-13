antlrCompile.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
~~[wheel (GitLab)](https://gitlab.com/KOLANICH/antlrCompile.py/-/jobs/artifacts/master/raw/dist/antlrCompile-0.CI-py3-none-any.whl?job=build)~~
~~[wheel (GHA via `nightly.link`)](https://nightly.link/UniGrammar-libs/antlrCompile.py/workflows/CI/master/antlrCompile-0.CI-py3-none-any.whl)~~
~~![GitLab Build Status](https://gitlab.com/KOLANICH/antlrCompile.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/UniGrammar/antlrCompile.py/badges/master/coverage.svg)~~
~~[![GitHub Actions](https://github.com/UniGrammar-libs/antlrCompile.py/workflows/CI/badge.svg)](https://github.com/UniGrammar-libs/antlrCompile.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/UniGrammar-libs/antlrCompile.py.svg)](https://libraries.io/github/UniGrammar-libs/antlrCompile.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/UniGrammar/antlrCompile.py, grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

A python wrapper for [ANTLR 4](https://github.com/antlr/antlr4) - a well-known multilanguage LL(*) parser generator. The libs allows you to

* transpile an ANTLR  grammar into the corresponding source code.
* visualize AST resulted from parsing source code with a grammar for debug purposes.

Currently it lacks docs, but be brave to read the source code, it is only a wrapper that is not that big.

Our fork is currently needed
------------------------
You need [our fork of ANTL](https://codeberg.org/UniGrammar/antlr4/tree/tool_refactoring) in order for this to work. We [have tried to upstream our changes](https://github.com/antlr/antlr4/pull/2774), but the project's BDFL is against "big changes". Then I had refactored the changes into several smaller PRs that don't introduce the changes but make it easier for me to introduce them with subclassing. They are still not merged:

* [Refactor `CodeGenerator`: move target initialization code into a separate method](https://github.com/antlr/antlr4/pull/3925)
* [Extracted getting the interp file name into a separate method `Tool::getInterpFileName`](https://github.com/antlr/antlr4/pull/3924)
* [Move a part of `CodeGenerator.write` into a separate reusable method `writeToWriter` to be able to reuse it later](https://github.com/antlr/antlr4/pull/3923)
* [Convert some members of CodeGenerator from private into protected](https://github.com/antlr/antlr4/pull/3922)
