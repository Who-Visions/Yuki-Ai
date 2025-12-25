# Yuki Handoff & Enhancement Protocol

## Current Status

**System Name**: Yuki AI (Snow Fox Spirit)
**Version**: 0.06-local
**Location**: `C:\Yuki_Local`
**State**: Active, but unstructured.

## Structural Audit

The current codebase is a flat directory containing over 200 files.

- **Core**: Mixed between `yuki_local.py` (CLI/Local) and `agent.py` (Server logic).
- **API**: `server.py` and `yuki_api.py`.
- **Tools**: Scattered across `yuki_tools.py`, `tools/`, and root scripts.
- **Modules**: `yuki_memory_system.py`, `yuki_cosplay_platform.py` in root.

## Enhancement Plan (Fleet Standardization)

To align Yuki with the **Who Visions Fleet Standard (VFS)**, we will refactor the codebase into a modular package structure.

### New Structure

* `yuki/` (Top-level Package)
  - `core/` -> Agent logic (`agent.py`, `orchestrator.py`)
  - `api/` -> API Server (`app.py`, `routes.py`)
  - `modules/` -> Feature modules (`memory`, `cosplay`, `anime`)
  - `tools/` -> Tool definitions
- `scripts/` -> Utility scripts (`run_*.py`)
- `tests/` -> Test suite

## Action Items

1. **Refactor**: Move root files into `yuki/` subdirectories.
2. **Standardize**: Rename `server.py` to `app.py` and `yuki_local.py`/`agent.py` to `core/agent.py`.
3. **Config**: Centralize configuration in `yuki/core/config.py`.
4. **Verify**: Ensure all imports resolve correctly.

## Quick Start (Current)

* **Run Server**: `python server.py`
- **Run Local**: `python run_yuki_local.py`

## Next Steps

Trigger the **Yuki Restructuring** workflow to execute this plan.
