# Contributing

Keep diagnostics read-only, add regression tests, update documentation, and cite official sources for security claims. Run:

```bash
python -m compileall -q src tests scripts
python -m unittest discover -s tests -v
```

For advisory changes:

1. Verify the official PHP or vendor notice before adding a CVE or fixed version.
2. Never invent a fixed release or CVSS severity. Use `kind: "mitigation"` when guidance exists but a fixed version is not confirmed.
3. Keep `advisories/` and `src/patchguide/data/advisories/` synchronized.
4. Update the schema and add tests for new behavior.
5. Document whether the record describes a confirmed fix, a mitigation, or a status that remains unknown.

Never submit secrets or private production configuration. PatchGuide must remain read-only during local checks, and docs must describe static inspection limitations honestly.
