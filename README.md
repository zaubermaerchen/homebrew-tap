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
```

Alternatively, add the tap first:

```sh
brew tap zaubermaerchen/tap
brew install khsier pipewisp dam outage sluice
```

## Available formulae

| Formula | Description |
| --- | --- |
| [khsier](https://github.com/zaubermaerchen/khsier) | Observe flow and stream boundaries |
| [pipewisp](https://github.com/zaubermaerchen/pipewisp) | React to lifecycle transitions with hooks |
| [dam](https://github.com/zaubermaerchen/dam) | Hold flow until release conditions are satisfied |
| [outage](https://github.com/zaubermaerchen/outage) | Cut flow when a condition is triggered |
| [sluice](https://github.com/zaubermaerchen/sluice) | Switch flow between open and closed states |

## Upgrade

Update Homebrew and upgrade the installed formulae:

```sh
brew update
brew upgrade khsier pipewisp dam outage sluice
```

## Release automation

Published releases can open formula-update PRs through the tap's shared workflow.
See [release automation setup and rollout](docs/release-automation.md) for the
GitHub App's minimum permissions, trusted workflow references and khsier-first rollout.
