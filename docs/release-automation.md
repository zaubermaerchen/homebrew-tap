# Release formula updates

The tool's release workflow calls `.github/workflows/update-formula.yml` here after
publishing its assets. Formula update logic lives in this tap. It reads the actual
published release and `SHA256SUMS`, updates only the version and four URL/checksum
pairs, installs/tests the generated formula on Linux and macOS, then opens a PR.
Nothing pushes to `main`; a maintainer reviews and merges the PR. Failed release
validation or Homebrew tests prevent write-token creation and PR mutation.

The supported caller must be `zaubermaerchen/<formula>`. Stable tags are `vX.Y.Z`;
draft/prerelease releases are rejected. Required archives are darwin/linux ×
arm64/amd64. khsier, pipewisp and dam use `<tool>_<tag>_<os>_<arch>.tar.gz`;
outage and sluice use `<tool>-<tag>-<os>-<arch>.tar.gz`. All use `SHA256SUMS`.
Checksums must use the standard `sha256sum` format with one entry per filename;
missing, duplicate or malformed entries fail. The updater does not regenerate
install/test blocks or other metadata. The updater code stays pinned while its
formula template is read from current main. The write job compares that exact base against main again before opening
the PR; if it changed during verification, rerun the workflow so the new formula
is tested rather than overwrite newer metadata. Reruns reuse
`automation/update-<formula>-<tag>`
and the existing open PR. The concurrency group serializes each formula's updates
within its source repository; each supported formula has exactly one caller.

## GitHub App

Create a GitHub App owned by zaubermaerchen with these repository permissions:

- Contents: **Read and write** (read the tap and update the PR branch).
- Pull requests: **Read and write** (create/update the PR).
- Metadata: **Read-only** (GitHub's mandatory default).

No organization permissions, Actions/workflow permission, or webhook subscription
is required. Disable webhooks if unused. Install the App with **Only select
repositories**, selecting **homebrew-tap only**. Generate a private key; keep its
contents out of git, logs, issue comments and documentation. The reusable workflow
requests an installation token for only `homebrew-tap` and the two write
permissions. The token is minted after executable verification and revoked by the
App-token action at job completion. Its write job executes only trusted actions
and copies the generated formula; it does not execute release assets or the updater.

In each authorized tool repository, configure:

- Repository variable `HOMEBREW_TAP_APP_ID`: the App ID.
- Actions secret `HOMEBREW_TAP_APP_PRIVATE_KEY`: the PEM private key.

Restrict who can change those repositories' workflows and access these secrets.
The calling workflow runs only after trusted stable-tag releases or a maintainer's
rerun of a release workflow run that already contains the caller; never expose the key to fork PR jobs or `pull_request_target` jobs.
The caller's `GITHUB_TOKEN` needs only `contents: read`; it is used for release
metadata, not writing to the tap. App-created PRs can trigger this tap's checks.

## Deploy khsier first

1. Publish the reviewed tap commit containing the automation, and record its full
   SHA. GitHub resolves reusable workflows even for skipped jobs, so this commit
   must be available before opening the caller PR. Replace **both** the reusable workflow `uses: ...@main` and
   `automation-ref: main` in the caller with that same full SHA. The initial `main`
   references are owner-controlled bootstrap references; immutable pins are the
   deployment recommendation. Merge the tap automation PR before enabling the
   caller. The pin may reference the reviewed published commit, not necessarily
   the merge commit.
2. Create/install the App and set khsier's variable and secret above.
3. Merge khsier's thin release caller, then publish a stable release. Existing
   release runs created before the caller was installed cannot invoke it through
   a rerun; reruns retain the original workflow definition. Ensure updater and both Homebrew jobs pass, the App
   creates one formula-only PR, and the tap PR checks pass. Review the diff and
   merge it before expecting `brew update` to see the new release.
4. Retry the same tag and confirm no duplicate PR or commit is created. An already
   merged identical update needs no new PR. Older tags fail if newer versions are
   already on main. Existing older
   open PRs can become stale when another release PR merges; maintainers must close
   those PRs rather than merge a downgrade. This workflow never auto-merges.
   For a changed-base failure, rerun all jobs so preparation and both Homebrew
   jobs regenerate and retest the candidate; rerunning only the failed writer
   would reuse the stale base artifact.
5. Only after khsier succeeds, add the same caller job to pipewisp, dam, outage,
   then sluice. Pass the tool's name and published tag, the same App variable/secret,
   and the same trusted tap SHA. Do not copy the updater or add formula-specific
   shell code to tool repositories. Check each project's asset names/checksum
   publication against the contract above before enabling it.

Example job (replace both `main` values with the reviewed tap SHA on deployment):

```yaml
update-homebrew:
  needs: release
  permissions:
    contents: read
  uses: zaubermaerchen/homebrew-tap/.github/workflows/update-formula.yml@main
  with:
    formula: khsier
    tag: ${{ github.event.release.tag_name }}
    automation-ref: main
    app-id: ${{ vars.HOMEBREW_TAP_APP_ID }}
  secrets:
    app-private-key: ${{ secrets.HOMEBREW_TAP_APP_PRIVATE_KEY }}
```

For an existing release workflow that computes its tag in a preparation job, use
that job's output and include both preparation and release jobs in `needs`.
There is no manual-dispatch entry point. Retry only a workflow run that already
contains the caller and references a published stable release tag.

Local updater verification: `python3 -m unittest discover -s tests -v`.
Native Homebrew validation requires the workflow's Linux/macOS runners; local
Python tests alone do not establish that the archives install correctly.
