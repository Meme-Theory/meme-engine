# astro MCP — Settings Permissions

## settings.json Additions

Add these to the `permissions.allow` array in `.claude/settings.json`. The astro MCP wraps many external astronomy APIs; these whitelists let Claude Code supplement MCP tool calls with direct `WebFetch` when needed:

```json
"WebFetch(domain:simbad.u-strasbg.fr)",
"WebFetch(domain:vizier.u-strasbg.fr)",
"WebFetch(domain:vizier.cfa.harvard.edu)",
"WebFetch(domain:gea.esac.esa.int)",
"WebFetch(domain:archive.stsci.edu)",
"WebFetch(domain:mast.stsci.edu)",
"WebFetch(domain:irsa.ipac.caltech.edu)",
"WebFetch(domain:ned.ipac.caltech.edu)",
"WebFetch(domain:data.sdss.org)",
"WebFetch(domain:skyserver.sdss.org)",
"WebFetch(domain:astroquery.readthedocs.io)",
"WebFetch(domain:data.desi.lbl.gov)",
"WebFetch(domain:astro-datalab.noirlab.edu)",
"WebFetch(domain:www.gw-openscience.org)",
"WebFetch(domain:gwosc.org)"
```

Add or remove entries depending on which astroquery backends your project actually uses. The MCP itself makes the requests, but `WebFetch` permissions are needed for any supplementary lookups Claude Code does.

## settings.local.json Additions

Add the MCP Python command permission to the personal settings:

```json
"Bash(\"{{PYTHON_CMD}}\":*)"
```

This allows the MCP server process to execute.

## Notes

- `WebFetch(domain:github.com)` and `WebFetch(domain:raw.githubusercontent.com)` are sometimes already present in `settings.json` for the initial clone of `SandyYuan/astro_mcp`. If not, add them for the install step.
- If the project also installs the separate GWOSC MCP (gwosc-mcp), the GW-specific domains above are what it uses; the tool set is distinct from astro-mcp's astroquery services.
