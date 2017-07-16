# General

1. prerequisite for this package is "Package Control" sublime plugin


# Manual installation

1. copy the whole directory ShowPr to ~/.config/sublime-text-3/Packages/
2. make .zip of the directory and change name to ShowPr.sublime-package
3. copy ShowPr.sublimePackage to ~/.config/sublime-text-3/Installed Packages/
4. dependencies should be installed automatically
5. restart sublime


# Configuration

1. Type CTRL+SHIFT+P in sublime
2. go to "list packages"
3. go to ShowPr
4. edit ShowPr.sublime-settings file and set:
- user
- password
- organization
- repos (not necessary)


# Usage

1. press CTRL+. or CTRL+SHIFT+P and search for "Bitbucket: Show PR"
2. type repo you want to scan, for example:

- common_utils

or a organization followed by repo name, for example:
- my_org:common_utils

4. list of PR's should show up if data is valid
5. choose a PR it will open your default browser on the PR
