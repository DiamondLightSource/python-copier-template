.. _Skeleton:

Working on the Skeleton Repo
============================

The python3-pip-skeleton_ repo has a protected main branch and is restricted to 
rebase PRs only. 
It is also squashed occasionally so some careful procedures are required.

.. _python3-pip-skeleton: https://github.com/DiamondLightSource/python3-pip-skeleton

main
----

This branch is what all adopters of the skeleton project merge from so needs 
to be kept tidy. 
In particular it must not have any #nnn which would refer to the wrong commit 
when merged into other repos (and github will see them and add incorrect 
messages in PRs and Issues). This branch is protected from push and 
restricted so that it can only be updated by a PR with REBASE.

dev-archive
-----------
This branch to tracks all commits, including those that are squashed out of 
main. Force push is disallowed on this branch so that it can be kept as a 
safe record of the history.

Process for making a change
---------------------------
To make changes. First take a new branch off of main, make your changes 
and do a pull request to rebase main on the branch.

- get a branch on main

    - git checkout main
    - git reset --hard origin/main            # because main may have been rebased
    - git checkout -b feature
- Do the changes and test in CI with:

    - git add --all
    - git commit -m'my changes'
    - git push -u origin feature
- When happy with changes use PR to rebase main on feature.
- Next delete feature:

    - git push origin :feature
    - git checkout main
    - git branch -fd feature


Process for squashing main
--------------------------

Once a year or so tidy up the history of main to make new adoptions easy. 
Otherwise multiple changes to the same line in the history may cause multiple 
merge conflicts on that line during re-merge of skeleton into projects
that have already adopted.

Perform these steps

- Get the dev-archive branch to remember your main commits

    - git checkout dev-archive
    - git merge main
- If there are conflicts

    - git checkout --theirs
    - git add --all
    - git commit          # the commit message will be 'merged ...' you can 
      add to it if needed
- Now squash main right back to the original ededf000
    - git checkout main
    - git reset --hard /origin/main
    - git rebase -i ededf000
    - In the rebase edit screen replace all ``pick`` with ``s`` except the first 
      one. save and quit
- Now create a handoff branch
    - git checkout dev-archive
    - git checkout -b handoff/202x-xx-xx
    - git merge main
    - git push -u origin handoff/202x-xx-xx
