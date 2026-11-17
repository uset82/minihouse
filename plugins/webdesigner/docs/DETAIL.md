# WebDesigner

Connects the locally installed [WebDesigner](https://github.com/uset82/webdesigner) production engine (Apache-2.0) to DeepSeek Harness so agents can design and build modern, distinctive UI/UX website apps instead of generic templates.

## What it adds

**MCP tools** (server name `webdesigner`, engine at `C:\Users\carlos\.webdesigner`):

| Tool | Purpose |
| --- | --- |
| `mcp__webdesigner__wd_intake_project` | Normalize a brief into a task intent, select the stack, and create the project manifest |
| `mcp__webdesigner__wd_get_best_model` | Report the engine's model recommendation for a pipeline stage |
| `mcp__webdesigner__wd_add_artifact` | Record a completed stage and its emitted artifacts in the manifest |
| `mcp__webdesigner__wd_get_status` | Read the active project manifest and lifecycle progress |
| `mcp__webdesigner__wd_save_code_file` | Write generated code files inside the engine workspace |

**Skills**: the engine's 30-skill catalog plus a `webdesigner` bridging skill that wires the chat flow to the tools. Load `webdesigner` or `frontend-design` when building a site; the intake result names which design skills to chain (`webdesigner-design-system`, `shadow-plugin`, `friction-vector`, `gsap-animation`, `animate-ui`, `ui-skills`, `threeui`, `img2threejs`, `3d-scroll-website`, `toolcraft`, and more).

## Usage

Ask for a website or app in natural language, for example:

> Design a landing page for MiniHouse with an editorial layout, smooth-shadow elevation, and a scroll-driven hero.

The agent calls `wd_intake_project` first, loads the design skills, builds the site, records each stage with `wd_add_artifact`, and runs the anti-slop audit. You can also run the engine CLI directly from any project folder:

```powershell
node C:\Users\carlos\.webdesigner\dist\cli\index.js pipeline "Industrial audio synthesizer console"
node C:\Users\carlos\.webdesigner\dist\cli\index.js audit path\to\page.html
```

## Limitations

- The MCP server's working directory is pinned to `C:\Users\carlos\PROYECTOS\minihouse\webdesigner`; `wd_*` manifests and `wd_save_code_file` output always land there, in every session. One active project per folder: a new intake overwrites the previous manifest. For another project folder, run the CLI from that folder or edit the `cwd` in this bundle's `cordis.patch.yml` and reinstall.
- The engine must stay installed and built at `C:\Users\carlos\.webdesigner`, and Node.js must exist at the absolute path `C:\Program Files\nodejs\node.exe` (PATH is not used). If either moves, update the patch paths and reinstall.
- `wd_get_best_model` reflects the engine's own routing policy; it does not switch the model of the running Harness session.
- `wd_save_code_file` joins paths without a traversal guard; only pass clean relative paths (upstream engine behavior).
- The Blender, Remotion, and Stitch skills need external MCP servers or tooling this bundle does not install; they dead-end without it.
- Browser QA (stage 6) needs browser tooling; without it the agent verifies statically and says so.

## Troubleshooting

- **`mcp__webdesigner__*` tools missing**: the engine process failed to start. Check that `C:\Users\carlos\.webdesigner\dist\mcp\server.js` and `C:\Program Files\nodejs\node.exe` exist, then reload the WebDesigner bundle in **Plugins** or restart the Harness.
- **Calls fail after working earlier**: the server crashed; the client reconnects automatically (500 ms → 30 s backoff, 10 attempts). After 10 failed attempts the tools are removed until the configuration reloads or the Harness restarts.
- **Skills missing in an old session**: skill-catalog changes reach agents on their next catalog refresh; if a long-running session still lacks them, open a new session.

## Maintenance notes

- The bundle re-enables the Host-plane `skill-filesystem` row with a complete config (the Loader replaces a matched row's whole config). After a DSH upgrade, check the shipped defaults of `@deepseek-ai/dsh-skill-filesystem` and restate any new fields here.
- Custom skill roots rank above user-level skills: a same-named user skill (for example `frontend-design`) is shadowed by the engine's copy. Project skills (`.dsh/skills`, `.agents/skills`) still win.