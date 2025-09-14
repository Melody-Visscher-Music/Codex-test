# Agents

## Roles

- **Bootstrapper**: set up repository structures and maintain zero placeholders.
- **Planner**: extend export, optimize and animation planners.
- **Adapter**: integrate with real or simulated Blender environments.
- **QA**: run format, lint, typecheck and tests via scripts before committing.
- **Docs**: keep README and this file synchronized with code.

## Operating Rules

- No placeholders or incomplete sections.
- Scripts in `scripts/` are idempotent and deterministic.
- Use Conventional Commits.
- Always execute `./scripts/format.sh`, `./scripts/lint.sh`, `./scripts/typecheck.sh` and `./scripts/test.sh` before pushing.

## Change Protocol

1. Create a feature branch.
2. Implement changes with tests.
3. Run the QA scripts above.
4. Commit using Conventional Commits.
5. Open a pull request; semantic-release manages versions.

## Extending Planners

To add a new exporter or optimizer:

1. Create a planner function in the relevant module.
2. Add command-line options in `cli.py`.
3. Implement unit tests.
4. Update documentation with examples.

