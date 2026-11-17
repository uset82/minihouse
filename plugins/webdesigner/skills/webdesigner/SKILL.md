---
name: webdesigner
description: Build modern, distinctive UI/UX website apps with the WebDesigner production pipeline. Use whenever the user asks to design or build a website, landing page, web app, dashboard, or frontend interface, or asks to polish or audit an existing UI. Routes the request through the local WebDesigner engine's MCP tools and design skills.
---

# WebDesigner pipeline for DeepSeek Harness

This skill bridges the WebDesigner engine (installed at `C:\Users\carlos\.webdesigner`) to this Harness. The engine's MCP tools are registered under the `webdesigner` server name; its design skills are in the session skill catalog.

## Working directory

The MCP server writes `task_intent.json`, `stack_selection.json`, `artifact_manifest.json`, and every `wd_save_code_file` output relative to its fixed working directory: `C:\Users\carlos\PROYECTOS\minihouse\webdesigner`. One active project lives there at a time — a new `wd_intake_project` overwrites the previous manifest. For a different project folder, run the engine CLI from that folder instead:

```powershell
node C:\Users\carlos\.webdesigner\dist\cli\index.js pipeline "<brief>"
```

## Procedure

1. **Intake first.** Call `mcp__webdesigner__wd_intake_project` with the user's brief (and `title`, `experienceType`, and any `requires*` flags the brief implies). It normalizes intent, selects the stack, and creates the manifest. Read the returned `selection.integrations` — they name the design skills to chain.
2. **Load the design skills.** Load `frontend-design` with the skill tool for aesthetic direction, then the skills named by the selection (for example `webdesigner-design-system`, `shadow-plugin`, `friction-vector`, `gsap-animation`, `animate-ui`, `ui-skills`, `threeui`, `img2threejs`, `toolcraft`). Follow their guidance; where they reference `.antigravity/runtime/schemas/*.json` or other engine-relative files, read them under `C:\Users\carlos\.webdesigner`.
3. **Build.** Generate the site in the engine working directory (or the user's chosen project folder when working through the CLI). Prefer the normal `write`/`edit` tools for files inside the session workspace; use `mcp__webdesigner__wd_save_code_file` for engine-workspace files. Keep every color, margin, and type choice derived from the approved token system.
4. **Record stages.** After each pipeline stage, call `mcp__webdesigner__wd_add_artifact` with the stage, skill, emitted artifacts, and handoff notes. `mcp__webdesigner__wd_get_status` reads current progress. `mcp__webdesigner__wd_get_best_model` reports the engine's routing recommendation only — it does not change this session's model.
5. **Audit and verify.** Run the anti-slop audit (`node C:\Users\carlos\.webdesigner\dist\cli\index.js audit <file>`) and check WCAG AA contrast, 44px touch targets, and keyboard focus. Browser QA needs browser tooling; without it, verify statically and say so.

## Cautions

- The Blender, Remotion, and Stitch skills in the catalog need external MCP servers or tooling that this bundle does not install; do not follow them unless that tooling is present.
- `wd_save_code_file` joins paths without a traversal guard; only pass clean relative paths.
- If the `mcp__webdesigner__*` tools are missing, the engine process failed to start: check that `C:\Users\carlos\.webdesigner\dist\mcp\server.js` and `C:\Program Files\nodejs\node.exe` exist, then reload the WebDesigner bundle in Plugins or restart the Harness.