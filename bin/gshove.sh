#!/bin/bash

# gshove.sh: A Git helper script to move uncommitted changes to a new branch and push it.
# The purpose is to reduce the risk that you might lose un-pushed work if your workstation 
# breaks or gets lost.

# If the START_BRANCH has uncommitted work, this script leaves git in a state where 
# you can't checkout the new branch without committing or stashing the changes first.

# To clean up the branch on the remote, 
#    git push origin --delete <branch_name>

# To clean up the local branch,
#    git branch -D <branch_name>
# (Use -D instead of -d if you want to force-delete it without checking if it was merged).

set -e

if [ -z "$1" ]; then
    echo "Error: Please provide a commit message."
    echo "Usage: gshove \"your commit message\""
    exit 1
fi

COMMIT_MSG="$1"
START_BRANCH=$(git branch --show-current)

if [ -z "$START_BRANCH" ]; then
    echo "Error: You are not currently on a branch (Detached HEAD)."
    exit 1
fi

NEW_BRANCH="shove-${START_BRANCH}"

if ! git check-ref-format --branch "$NEW_BRANCH" &>/dev/null; then
    echo "Error: Derived name '$NEW_BRANCH' is not a valid Git branch name."
    exit 1
fi

if git rev-parse --verify "$NEW_BRANCH" &>/dev/null || git rev-parse --verify "origin/$NEW_BRANCH" &>/dev/null; then
    echo "Error: Target branch '$NEW_BRANCH' already exists."
    exit 1
fi

# If no changes exist, just create and push an empty branch
if [ -z "$(git status --porcelain)" ]; then
    echo "No uncommitted changes found. Creating empty branch '$NEW_BRANCH'..."
    git checkout -b "$NEW_BRANCH"
    git push -u origin "$NEW_BRANCH"
    git checkout "$START_BRANCH"
    echo "Done! Back on '$START_BRANCH'."
    exit 0
fi

echo "Moving uncommitted work to '$NEW_BRANCH'..."

# 1. Stash everything, keeping track of what was staged vs unstaged
git stash push --include-untracked -m "gshove_temporary_holder"

# 2. Create the new branch from the clean starting point
git checkout -b "$NEW_BRANCH"

# 3. USE APPLY INSTEAD OF POP (This leaves the stash safely in the stash list)
git stash apply --index

# 4. Commit and push the new branch
git add .
git commit -m "$COMMIT_MSG"
git push -u origin "$NEW_BRANCH"
echo "Successfully pushed '$NEW_BRANCH' to remote."

# 5. Switch back to the original branch
echo "Restoring uncommitted changes back to '$START_BRANCH'..."
git checkout "$START_BRANCH"

# 6. POP THE STASH HERE (This perfectly restores unstaged/staged/untracked states)
# We use || true in case of rare index locking issues, so the stash isn't lost
git stash pop --index

echo "Done! You are back on '$START_BRANCH' with your working tree perfectly restored."