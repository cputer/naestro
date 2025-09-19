# Changelog

All notable changes to this project will be documented here. This project adheres to
[Semantic Versioning](https://semver.org).

## [Unreleased]

- Documented: **docs/engineering/determinism.md** detailing the deterministic inference guard for GPU workloads.
- Documented: Runtime toggle `runtime.determinism.guard_enabled` / `NAESTRO_DETERMINISTIC_GUARD` for enabling the guard.
- Documented: Golden and canary evaluation flagging that forces deterministic inference during guard-protected runs.
- Documented: CI hints directing contributors to keep the deterministic guard enabled for local checks.
- Documented: Regression tests that compare logits/hash digests to confirm the guard's determinism guarantees.

- Added: **docs/plugins/deepcode.md** describing the DeepCode plugin lane integration plan.
- Added: README Plugins / Lanes entry linking to the DeepCode lane documentation.
- Documented: DeepCode lane status remains blocked until the adapter is wired to clarify availability expectations.
- Added: AgentScope runtime listing docs + Mermaid diagram.
- Added: Adapter/config stub for AgentScope integrations.
- Updated: **VISION.md** with Engineering Quality, Meta-Cognition, Ecosystem, and Governance sections
- Updated: cross-links in README/ROADMAP; added reference anchors
- Updated: **docs/usecases/agency_automation.md** outlining the Agency Automation flow, rollout plan, and KPIs
- Updated: **ROADMAP.md** “What’s new” section with the REFRAG long-context acceleration lane and Naestro integration notes
- Updated: **REFERENCES.md** to capture the latest REFRAG, SmolHub, and Qwen3-Next citations for roadmap alignment

- Updated: **REFERENCES.md** to include the Ling-flash-2.0 and InfoSeek research citations
- Updated: **ROADMAP.md** with Ling-flash-2.0 milestones and InfoSeek evaluation checkpoints

## [1.4.0] - 2025-09-02

### Added

- Apple OpenELM router (local vLLM) provider and deployment snippet.

### Changed

- Grafana dashboard: `cell_id` template filter for single/multi-desktop.

### Fixed

- Providers schema validation edge cases.
