# Privacy checks

The package validator checks the publication allowlist and common leak signatures. The privacy checker also reads Git objects and commit/tag metadata, then runs Gitleaks with its built-in secret rules. It never prints matched values.

```sh
brew install gitleaks
python3 scripts/check_privacy.py staged
python3 scripts/check_privacy.py history
```

`staged` inspects the actual index and effective commit identity. It does not confuse an unstaged edit with content that will be committed. `history` inspects all locally reachable commits and annotated tags, including files deleted by later commits. `push` reads Git's pre-push protocol from standard input and checks the refs and new history being sent. A newly created ref receives a complete history check. Missing objects, a missing scanner, and invalid required policy block the operation.

Local hooks must be installed and enabled before Git can block a commit or push. Cloning this repository does not automatically install them. The maintainer also uses a private, external Git policy and personal-repository hooks; private organization names and identifiers are not stored in this public repository.

## Private rules

An external JSON file can add operator-specific patterns:

```json
{
  "deny_patterns": {
    "internal-project": "organization-private-project"
  }
}
```

Set its absolute path with `git config privacy.policyFile <external-policy-path>` and require it with `git config privacy.requirePolicy true`. Keep this file outside the repository. Use generic rule identifiers: findings report rule names but never the matching values. Repository-local Gitleaks exclusions, ignore files, and inline allow comments are not honored by the privacy checker.

Public names, GitHub handles, GitHub noreply addresses, and reserved example email domains are allowed. Other email addresses, personal home paths, private credential filenames, configured organization markers, and detected secrets fail the check. Binary files, oversized files, symlinks, and submodules also fail because this checker cannot establish their publication safety. Review them with suitable tools before designing a narrowly scoped exception; do not silently skip them.

## What is enforced

Local hooks stop ordinary Git commits and pushes before upload. The GitHub workflow repeats package, regression, and full-history checks after upload. A failed workflow does not retract a public push. GitHub's native push protection can block supported credential formats on the server; its account/repository setting must be verified independently.

Hooks can be disabled or bypassed, alternate clients may not execute them, and pattern matching cannot classify every private fact or confidential narrative. Review the proposed diff and metadata before publishing. A failed scan should be fixed and rerun, not bypassed. Existing public history is not erased by these checks.

References: [Git hooks](https://git-scm.com/docs/githooks), [Gitleaks](https://github.com/gitleaks/gitleaks), and [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection).
