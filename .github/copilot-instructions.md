# Copilot instructions

This repository contains multiple Python packages. Follow the repository's
contribution guidance and the closest applicable package pattern.

## API sources and package patterns

- Verify API definitions against their canonical source and intended revision
  before adding or updating generated packages. Do not base a package on
  unpublished upstream changes without an explicit revision or local
  reference. When another package must use unpublished work, use a Git
  reference to the development branch or fork.
- Before adding a package or changing package metadata, compare it with the
  closest existing packages. Keep differences intentional and minimal; avoid
  introducing one-off conventions that make repository-wide updates harder.
- Keep package descriptions, supported Python versions, operating systems,
  and other support claims consistent with repository conventions, package
  metadata, and actual test coverage. Name supported operating systems
  specifically instead of using broader labels that imply unsupported
  platforms.

## Shared code and change scope

- Before changing shared, duplicated, or vendored code, configuration, or
  documentation, identify its copies and consumers and trace how it is used.
  Keep copies consistent. If a substantial shared fix is needed, update all
  copies together or track it as a separate repository-wide change.
- Keep each change focused. Coordinate broader fixes separately, and ensure a
  tracking issue accurately describes the problem being deferred. Do not use
  an unrelated issue as a placeholder for a different defect.
- Reuse existing test fixtures and helpers, including fixtures for setting up
  mocks. Avoid unnecessary changes to shared code; verify a proposed change is
  needed and that it addresses the actual behavior.

## Documentation and generated files

- Keep package READMEs user-facing and focused on supported behavior. Follow
  the closest package README rather than adding internal implementation or
  contributor workflow details; put generation and contribution instructions
  in the repository's contributor documentation.
- When adapting duplicated documentation configuration, copy the complete
  closest configuration and make only the changes needed. Preserve comments,
  copyright handling, intersphinx references, generated-file directives, and
  other customizations unless there is a specific reason to change them.
- Treat generated files as generated: edit the source and use the documented
  generation workflow. Regenerate generated tables of contents and indexes
  instead of editing them manually.
- Keep documentation dependencies and extensions aligned with their actual
  use. Check other packages before changing a shared convention, and
  coordinate broad dependency cleanup separately.

## Dependencies, tooling, and validation

- Follow repository dependency policies and existing package configuration.
  Avoid redundant dependency declarations and unnecessary version changes;
  understand which metadata is used for package builds versus dependency
  locking. Use optional extras when they match the package's optional
  functionality and existing conventions.
- Keep dependency constraints consistent with repository policy. Update the
  relevant lockfiles with the repository's dependency tooling when manifests
  change, and preserve the package lists and exclusions required by shared
  dependency policies.
- For documentation builds, install only the required dependency groups and
  use the Poetry version supported by the repository's current configuration.
- Document intentional analyzer/test skips with the specific rule and reason.
  Run relevant tests and analyzers after changes, and confirm that CI results
  correspond to the intended commit and change.
