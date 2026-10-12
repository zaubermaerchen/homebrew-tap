# Homebrew Tap

Homebrew formulae for command-line tools by [zaubermaerchen](https://github.com/zaubermaerchen).

## Install

Install any formula directly from this tap:

```sh
brew install zaubermaerchen/tap/khsier
brew install zaubermaerchen/tap/pipewisp
brew install zaubermaerchen/tap/dam
brew install zaubermaerchen/tap/outage
brew install zaubermaerchen/tap/sluice
brew install zaubermaerchen/tap/trysudo
```

Alternatively, add the tap first:

```sh
brew tap zaubermaerchen/tap
brew install khsier pipewisp dam outage sluice trysudo
```

## Available formulae

| Formula | Description |
| --- | --- |
| [khsier](https://github.com/zaubermaerchen/khsier) | Observe flow and stream boundaries |
| [pipewisp](https://github.com/zaubermaerchen/pipewisp) | React to lifecycle transitions with hooks |
| [dam](https://github.com/zaubermaerchen/dam) | Hold flow until release conditions are satisfied |
| [outage](https://github.com/zaubermaerchen/outage) | Cut flow when a condition is triggered |
| [sluice](https://github.com/zaubermaerchen/sluice) | Switch flow between open and closed states |
| [trysudo](https://github.com/zaubermaerchen/trysudo) | Run with sudo when allowed, otherwise directly |

## Upgrade

Update Homebrew and upgrade the installed formulae:

```sh
brew update
brew upgrade khsier pipewisp dam outage sluice trysudo
```

## Formula checks

Pull requests install and test only added or changed `Formula/*.rb` files on
Linux and macOS. Deleted formulae are excluded; documentation-only or
deletion-only changes skip Brew checks. Changes outside `Formula/*.rb`,
`README.md`, `LICENSE`, and `docs/` check all formulae, including shared
workflows, scripts, and tests. If PR diff detection fails, all formulae are checked.

Pushes to `main` check all formulae. In Actions, run **Formula checks** manually
with an existing formula name (for example, `trysudo`) in the `formula` input;
leave it empty to check all formulae. Invalid names fail before installation.
The formula list is generated from `Formula/*.rb`. Python tests and
`git diff --check` run even when Brew checks are skipped.

## Release automation

Published releases can open formula-update PRs through the tap's shared workflow.
See [release automation setup and rollout](docs/release-automation.md) for the
GitHub App's minimum permissions, trusted workflow references and khsier-first rollout.
