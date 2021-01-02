# Advanced Setup (optional)

_This document applies to the newer project features implemented by [PR #185](https://github.com/codeforpdx/dwellinglybackend/pull/185) as part of the push to enforce uniform code standards for the Dwellingly backend.
Any additional setup instructions referenced here are completely optional, but are worth the extra step if you feel comfortable doing so._

## Table of Contents

- [Introduction](#Introduction)
  - [This sounds painful, is it even worth it?](#This-sounds-painful-is-it-even-worth-it)
- [Flake8](#Flake8)
  - [Flake8 on Command Line](#Flake8-Command-Line-Usage)
  - [Flake8 in your Editor](#Use-Flake8-in-Your-Editor)
- [Black](#Black)
  - [Black on Command Line](#Black-Command-Line-Usage)
  - [Black in your Editor](#Use-Black-in-Your-Editor)
- [Git Blame](#Git-Blame)

## Introduction

We recently introduced strict linting and formatting requirements for all code being added to the Dwellingly backend repo. This is accomplished through a combination of:

- [Flake8](https://github.com/PyCQA/flake8) (supplemented by [Flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)) for linting
- [Black](https://github.com/psf/black) for formatting Python files, and
- [Pre-commit](https://pre-commit.com/) to run these checks as well as some whitespace checks on every `git commit`.

As the name suggests, Pre-commit will do the following _before_ your commit is processed:

- Check for the required newline at the end of every file (will auto-fix)
- Check for trailing whitespace on all lines of every file (will auto-fix)
- Check Python files for compliance with Black formatting (will auto-fix if possible)
- Check Python files for [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance via Flake8 and Flake8-bugbear (will **not** auto-fix)

If any of these checks don't pass, your commit will be aborted &mdash; _even if your files were auto-fixed by the pre-commit hook_.

Occasionally, Black will not be able to auto-format some of your code during the pre-commit hook (e.g., if you have a really long string or comment).  In that case, you will need to make that fix manually.  All Flake8 errors will need to be resolved manually as well.

Once all changes have been made (by you or by automation), you must `git add` and `git commit` again. If everything was properly resolved, your commit will be successful.

### This sounds painful, is it even worth it?

Yes, absolutely.

The pre-commit hook (and the backup pre-commit hook in our CI) will ensure that no matter which contributor wrote the code, all Python in the repo will be formatted the same way. Some advantages include:

- Faster review:
  - All the code will look similar, with no personal quirks or strange styling hold-overs from other languages. This makes it faster to read, comprehend and give feedback on newly added code.
  - Git diffs will be smaller and clearer because Black tends to make the code more vertical. Vertical code means there won't be a gigantically long diff when, e.g., one item in a list gets changed.
- Faster time to merge:
  - Gone are the days of being asked to add a newline or remove an import before your PRs can be merged. The pre-commit takes care of this for you before the reviewer ever sees your code.
- Closer to production ready:
  - Extraneous code, such as unused imports or unused variables, will always trigger a Flake8 error and cannot be committed. Cleaner code now means less work in the future when we switch from development to production.

It is also important to recognize that you don't have to go blindly into your commit, hoping to pass the tests. Pre-commit is the enforcer, but the real power behind linters and formatters comes through using them as you write your code, not only at the end.

The following sections contain instructions on using Flake8 and Black on the command line as well and links on how to set these up for automatic use with a variety of IDEs and code editors. [Git Blame](https://git-scm.com/docs/git-blame#Documentation/git-blame.txt) is also mentioned, as it is a useful tool when working on teams and requires some special set-up since we migrated to Black late in the project.

---

## Flake8

Flake8 lints your Python files, letting you know if you have any problems with your code or if your code does not meet PEP8 standards.  If it detects problems with your code, you will have to fix them yourself.  You can lint your code periodically from the command line, or set up your editor to do it for you by following the instructions below.

### Flake8 Command Line Usage

Run the following command from the `dwellinglybackend` directory to lint all Python files in the repo:

```console
pipenv run flake8
```

You can also narrow the scope of your linting by passing in the path for the directory or file you want to lint:

```console
pipenv run flake8 {path_to_dir_or_file}
```

If you need more advanced options, check out the [Flake8 documentation](https://flake8.pycqa.org/en/latest/user/invocation.html).

### Use Flake8 in Your Editor

For even more instantaneous linting, you can also set up Flake8 with most IDEs and code editors.

Every editor is configured differently, so if your editor of choice isn't listed, a quick Google search may be needed. Please add documentation links to this list if you successfully integrate Flake8 with an editor not listed here!

- VS Code:
  - Add the settings from [settings.json.example](./settings.json.example) to your `settings.json` file; or
  - Follow the [official documentation](https://code.visualstudio.com/docs/python/linting)
- PyCharm:
  - Follow the instructions in this [Real Python article](https://code.visualstudio.com/docs/python/linting) (under the section _Using Plugins and External Tools in PyCharm_)
- Atom:
  - Go to Settings -> Install, search for the `linter-flake8` package, then click Install
- Vim:
  - Follow the instructions in [this gist](https://gist.github.com/za/983db825aee2dc352d5341da357cbfb4)


## _Black_

Black is a code formatter that formats Python files according to very opinionated PEP8-compliant styling rules. When Black is run, it will check your file(s) and if it decides changes are needed, it will re-format your code to the best of its abilities.  This will never change the substance of your code, only the styling. Occasionally, Black will not be able to auto-format part of your code (such as extra long strings or comments) and you will need to make those changes manually.

### _Black_ Command Line Usage

Run the following command from the `dwellinglybackend` directory to format all Python files in the repo using Black:

```console
pipenv run black .
```

To format only a specific file or directory, you simply specify the path, as you would with Flake8:

```console
pipenv run black {source_file_or_directory}
```

For advanced command line options, see the [Black documentation](https://black.readthedocs.io/en/stable/installation_and_usage.html#usage).

### Use _Black_ in Your Editor

One of the best features of code formatters is that you can set them up to _format on save_ with your editor. Once set up, every time you save your file, Black will auto-format the code you wrote. This is a no-brainer way to fix your code before commit time.

- Most Editors:
  - The Black documentation has a fairly extensive section on [editor integration](https://black.readthedocs.io/en/stable/editor_integration.html). Follow those instructions, and if your editor is not listed, consider opening up an issue on their [GitHub page](https://github.com/psf/black).

## Git Blame

Git blame is a built-in feature of Git that allows you to see the most recent commit and author that changed any given line of code in a file. Git blame can be incredibly useful on team projects because if you find a bug or don't understand a certain section of the code, you can reach out to the original author or read the commit messages where the code was added.

### Cleansing the Git Blame

One unfortunate side effect of migrating to Black code style late in a project's lifecycle is that the initial re-formatting of the files will pollute the git blame.  Essentially, most lines of most files will blame the author of the commit that did the re-formatting rather than the last person who _really_ changed the code.

If you want to use Git Blame for this project, you should tell Git to ignore the re-formatting commit by running the following command from inside the `dwellinglybackend` directory:

```console
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

After this command is run, lines modified by backend PR #185 will be blamed on the previous revision that modified those lines.

### Git Blame Command Line Usage

To use Git blame on the command line, it's as simple as running this command:

```console
git blame {path_to_file}
```

You will see the blame annotations in your terminal and you can navigate through them using the up and down arrows.  To exit the blame, press `q`.  If you are familiar with using the `git log` command, this will be familiar to you.

For advanced command line options, see the [git documentation](https://git-scm.com/docs/git-blame#Documentation/git-blame.txt).

### Git Blame in Your Editor

Where Git blame really shines is in the interactive extensions for various code editors &mdash; VS Code in particular.  These extensions have awesome features that range from color-coded revisions to in-line annotations and GitHub integration. Below are examples for some editors we use.

Every editor has different extensions, so if your editor of choice isn't listed, a quick Google search may be needed. Please add documentation links to this list if you find an awesome Git blame extension for an editor not listed here!

- VS Code:
  - [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) - the gold standard of Git blame extensions.
- PyCharm:
  - PyCharm's built-in [VCS Annotations](https://www.jetbrains.com/help/pycharm/investigate-changes.html#annotate)
- Atom:
  - [Atom-inline-blame](https://github.com/gregorym/atom-inline-blame) and/or
  - the [git-blame](https://github.com/alexcorre/git-blame/tree/v1.8.0) package
- Vim:
  - [Fugitive.vim](https://github.com/tpope/vim-fugitive) and/or
  - [Git-blame.vim](https://github.com/zivyangll/git-blame.vim)
