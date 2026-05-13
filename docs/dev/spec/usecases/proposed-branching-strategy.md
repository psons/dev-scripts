# Proposed Branching Strategy

This document outlines a Git branching strategy designed to maintain a detailed history of development activities while producing a clean, squashed history on the release branch.

## 1. Branch Roles

- **`develop` (Detailed Development Branch):** The integration branch for all ongoing work. It contains a highly detailed, granular commit history representing every micro-step, task, and AI interaction executed during development.
- **`release` (Release Branch):** A production-facing branch containing a clean history, where each commit corresponds to a single, complete release package.
- **`feature/*` (Feature Branches):** Short-lived branches created from `develop`. All detailed task work happens here. Once the feature is complete, it is merged back into `develop` (preserving detailed commits), and the feature branch is deleted.

## 2. The Release Workflow

When the team is ready to publish a release:
1. A Git tag is created on the `develop` branch indicating the exact detailed commit that represents the release state (e.g., `v1.2.0-dev`).
2. The detailed commits from `develop` are brought into the `release` branch and **squashed** into a single commit representing the entire release payload.
3. The resulting squashed commit on `release` is tagged as the official release (e.g., `v1.2.0`).

---

## 3. The "History Problem"

**The Issue:** Git determines how to merge branches efficiently by finding their nearest "common ancestor" in the commit graph. If you update the release branch via `git merge --squash develop`, Git stages all the changes but **does not create a merge commit**. It deliberately leaves out the parent lineage linking it to `develop`.

Because the `release` branch doesn't technically record that it incorporated `develop`'s history, the common ancestor between the two branches never moves forward. The *next* time you try to squash-merge `develop` into `release` for a future version, Git will attempt to re-apply every change from the beginning of time (or from the branch point), leading to massive, unresolvable merge conflicts.

## 4. Solutions and Alternatives

To maintain a squashed release branch without crippling the repository's Git history, here are two approaches. Approach A makes the exact requested strategy work flawlessly, while Approach B is a common industry alternative.

### Approach A: The "Ours" Merge Trick (Workaround) (Not chosen alternative)
You can maintain the squashed release branch without breaking Git's history tree by creating a "dummy merge" back to `develop` immediately after a release.

**The Workflow:**
1. **Squash to Release:**
   ```bash
   git checkout release
   git merge --squash develop
   git commit -m "Release v1.2.0"
   git tag v1.2.0
   ```
2. **Tie the History Together:**
   ```bash
   git checkout develop
   # Merge the release branch back using the 'ours' strategy.
   # This tells Git "record the merge to update the common ancestor, 
   # but ignore all file changes from the release branch".
   git merge -s ours release -m "Record release v1.2.0 squash"
   git tag v1.2.0-dev
   ```
**Why this works:** The `merge -s ours` operation creates a parent relationship tying `develop` to the latest commit on `release`. The next time you run `git merge --squash develop` into `release`, Git knows exactly where the last release left off, and the diff will only contain the changes made *since* the last release.

### Approach B: Squash Feature Branches, Tag Releases (Chosen Alternative)
If executing dummy merges introduces too much overhead, consider shifting the squash step earlier in the process.

**The Workflow:**
1. **Detailed Features:** Work on `feature/*` with highly detailed commits (driven by tools like `dtask`).
2. **Squash to Develop:** When a feature is complete, merge it into `develop` using a squash merge. Now `develop` maintains a clean, linear history of *completed features*, rather than individual task iterations.
3. **Fast-Forward Releases:** The `release` branch is updated via simple fast-forward merges or standard merge commits from `develop`. No squashing happens at the release level.
4. **Preserving Detailed History:** If the detailed micro-task history must be kept for auditing or AI-training purposes, you can merge `feature/*` branches into an archival branch (e.g., `archive/detailed-history`) just before squashing them into `develop`, rather than deleting the feature branches completely.