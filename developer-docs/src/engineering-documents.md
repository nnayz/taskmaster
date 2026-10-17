# Engineering documents

This is the index of canonical engineering documents in the repository. Each
one stays authoritative where it lives; this book links to them rather than
copying their content, and summaries elsewhere must not contradict them.

Status values: **Active** documents define current behavior or process;
**Runbook** documents describe an implemented-but-gated subsystem;
**Historical** documents record finished work and do not create current
requirements; **Gated** documents belong to a feature that is not shipped
until its release gates pass.

## Architecture and transport

| Document | Status | Covers |
|----------|--------|--------|
| [`zeus/REMOTE_PORT.md`](https://github.com/nnayz/zeus/blob/main/zeus/REMOTE_PORT.md) | Active | The remote PTY Holder architecture and maintenance baseline: SSH transport, bootstrap, helper lifecycle, protocol, performance gates, platform matrix. Read before changing remote behavior. |
| [Companion architecture and trust model](companion-architecture.md) | Runbook | The bounded experimental Companion decision, authority/data flow, external v1 contract, pairing and scopes, threat model, and production gates. |
| [`zeus/COMPANION_GATEWAY.md`](https://github.com/nnayz/zeus/blob/main/zeus/COMPANION_GATEWAY.md) | Runbook | Gateway implementation runbook and evidence record (#73). |
| [`zeus/COMPANION_TERMINAL.md`](https://github.com/nnayz/zeus/blob/main/zeus/COMPANION_TERMINAL.md) | Runbook | Command-oriented terminal v1 contract (#75). |
| [`zeus/crates/zeus-companion-api/src/lib.rs`](https://github.com/nnayz/zeus/blob/main/zeus/crates/zeus-companion-api/src/lib.rs) | Active | External v1 DTO authority (`API_MAJOR = 1`). |
| [`zeus/PORT.md`](https://github.com/nnayz/zeus/blob/main/zeus/PORT.md) | Historical | The port of the Engine away from the retired Swift stack, and the rules it followed. |
| [`zeus/PLAN.md`](https://github.com/nnayz/zeus/blob/main/zeus/PLAN.md) | Historical | The GPUI client migration plan. |

## Productivity, status, and catalog

| Document | Status | Covers |
|----------|--------|--------|
| [`zeus/crates/zeus-engine/src/detect/manifest.rs`](https://github.com/nnayz/zeus/blob/main/zeus/crates/zeus-engine/src/detect/manifest.rs) | Active | The manifest schema: states, regions, predicates, capture. The authoritative field list. |
| [`zeus/crates/zeus-engine/manifests/`](https://github.com/nnayz/zeus/tree/main/zeus/crates/zeus-engine/manifests) | Active | The Agent catalog. Never shrink it. |
| [Agent manifests](agent-manifests.md) | Guide | How to read and extend the catalog. |
| [`zeus/NODE.md`](https://github.com/nnayz/zeus/blob/main/zeus/NODE.md) | Pointer | Short pointer for `zeus-node`; the user-facing documentation moved to the User Guide. |

## Performance and power

| Document | Status | Covers |
|----------|--------|--------|
| [`zeus/PERF.md`](https://github.com/nnayz/zeus/blob/main/zeus/PERF.md) | Historical | Dated measurements and the packaged-artifact acceptance gate. Context for a change, not proof it passes. |
| [`zeus/PERF-AUDIT.md`](https://github.com/nnayz/zeus/blob/main/zeus/PERF-AUDIT.md) | Historical | The measurement audit that produced the gates. |
| [`zeus/CLOSED_LID_PLAN.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_PLAN.md), [`CLOSED_LID_DECISIONS.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_DECISIONS.md), [`CLOSED_LID_THREAT_MODEL.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_THREAT_MODEL.md) | Gated | The reviewed plan, decision record, and threat model for the local macOS closed-lid power exception (#70). |
| [`zeus/CLOSED_LID_SPIKE_REPORT.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_SPIKE_REPORT.md), [`CLOSED_LID_EVIDENCE.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_EVIDENCE.md), [`CLOSED_LID_MILESTONE_1.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_MILESTONE_1.md), [`CLOSED_LID_RELEASE_SPIKE.md`](https://github.com/nnayz/zeus/blob/main/zeus/CLOSED_LID_RELEASE_SPIKE.md) | Gated | Completed and blocked evidence for the same feature. Builds must report it unavailable until every recorded gate passes. |

## Packaging and releases

| Document | Status | Covers |
|----------|--------|--------|
| [`zeus/PACKAGING.md`](https://github.com/nnayz/zeus/blob/main/zeus/PACKAGING.md) | Active | Bundle assembly, signing setup, universal targets. |
| [`zeus/UPDATING.md`](https://github.com/nnayz/zeus/blob/main/zeus/UPDATING.md) | Active | The auto-updater implementation and release feed. |
| [`Casks/zeus.rb`](https://github.com/nnayz/zeus/blob/main/Casks/zeus.rb) | Active | The Homebrew cask for the monorepo tap. |

## Policies and process

| Document | Status | Covers |
|----------|--------|--------|
| [`AGENTS.md`](https://github.com/nnayz/zeus/blob/main/AGENTS.md) (`.rules`) | Active | Binding repository instructions: architecture invariants, security rules, build commands, change discipline. |
| [`DESIGN.md`](https://github.com/nnayz/zeus/blob/main/DESIGN.md) | Active | The visual design language for the app and marketing surfaces. |
| [`SECURITY.md`](https://github.com/nnayz/zeus/blob/main/SECURITY.md), [`PRIVACY.md`](https://github.com/nnayz/zeus/blob/main/PRIVACY.md), [`SUPPORT.md`](https://github.com/nnayz/zeus/blob/main/SUPPORT.md) | Active | Reporting, privacy, and support entry points. |
| [`docs/README.md`](https://github.com/nnayz/zeus/blob/main/docs/README.md), [`developer-docs/README.md`](https://github.com/nnayz/zeus/blob/main/developer-docs/README.md) | Active | Documentation sources and local build commands. |

## Client specifications

| Document | Status | Covers |
|----------|--------|--------|
| [`ios/ZeusCompanion/README.md`](https://github.com/nnayz/zeus/blob/main/ios/ZeusCompanion/README.md) | Active | Building and running the native iOS client. |
| [`prototypes/companion-web/README.md`](https://github.com/nnayz/zeus/blob/main/prototypes/companion-web/README.md) | Prototype | The browser prototype, its gateway contract, and bounds. |
| [`prototypes/companion-web/VALIDATION.md`](https://github.com/nnayz/zeus/blob/main/prototypes/companion-web/VALIDATION.md) | Prototype | Measured findings, coverage, and device-validation gaps. |

If you add an engineering document, add it here with its status, and link it
from the relevant book page instead of duplicating its content.
