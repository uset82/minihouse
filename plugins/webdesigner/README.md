# @local/webdesigner

A configuration-only DeepSeek Harness bundle that bridges the locally installed
[WebDesigner](https://github.com/uset82/webdesigner) engine (Apache-2.0):

- inserts one `@deepseek-ai/dsh-mcp-client` row (`serverName: webdesigner`, stdio)
  pointing at `C:\Users\carlos\.webdesigner\dist\mcp\server.js`, with the server
  cwd pinned to `C:\Users\carlos\PROYECTOS\minihouse\webdesigner`;
- re-enables the Host-plane `skill-filesystem` row (disabled by the web-app
  layer) with two custom roots: the engine's `C:\Users\carlos\.webdesigner\skills`
  catalog and this bundle's `skills/` bridging skill. Host-layer skill providers
  merge into every agent's catalog, so all presets and sessions see them;
  default project/user/bundled roots are preserved.

See `docs/DETAIL.md` for tools, usage, limitations, and troubleshooting. Install
with `plugin_manager` `install_bundle` or **Plugins → Add plugin** pointing at
this directory.