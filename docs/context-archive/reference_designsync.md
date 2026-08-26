---
name: reference-designsync
description: "DesignSync tool: what it can/can't do, auth blocked in VSCode env (/design-login needs a terminal), and the potential Agourim design-system use"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
---

**What DesignSync IS (verified from schema + probe, 2026-07-05).** A file-sync bridge between local disk and **design-system projects** on claude.ai/design (`type: PROJECT_TYPE_DESIGN_SYSTEM` only). Methods: `list_projects`/`get_project`/`list_files`/`get_file` (read), `create_project`, `finalize_plan` → `write_files`/`delete_files` (plan-gated incremental writes), legacy `register_assets`. Preview cards come from a first-line `<!-- @dsCard group="…" -->` marker in each HTML.

**What it is NOT:** a channel to Claude Design *chat* projects. It cannot send tasks/messages to the "Redesign task card" project and cannot write into regular (non-design-system) projects. Earlier framing of it as "a way to communicate with Claude Design" was wrong.

**Auth status in Yon's VSCode env:** BLOCKED — `list_projects` returns "needs design-system authorization; /design-login requires an interactive terminal". Unlock paths: run `claude` CLI in a plain terminal → `/design-login` → `/design-sync`; or from Claude Design use "Send to Claude Code Web".

**Why it became moot for P3/P4:** the redesign was done locally instead — see [[dc-redesign-p3-p4]].

**Still-interesting future use:** create an "Agourim task-card design system" project from `dc_design_spec.md` (repo root) — one `@dsCard` preview per component — so claude.ai/design sessions can be pointed at the canonical component library for P5–P8 and teacher materials.
