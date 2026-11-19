---
name: molab-gpu
description: Run experiments and transfer files through Molab's remote notebook connection. Use for requested Molab GPU work, file transfers, connection setup, or session recovery.
---

# Molab GPU

Operate the user's intended live Molab notebook from your own shell using the official `marimo pair` CLI. Code executes in the remote notebook kernel. This skill works on a Mac or in a cloud agent with outbound access; local files and credentials are not shared between agents automatically.

## Connect

Use the target notebook's **Config → Connect your agent → Prompt** to obtain its server URL and authentication instructions. The public notebook page URL is not the execution server URL. Attach the GPU through Molab's compute menu if needed. Reuse an explicitly supplied connection; do not switch to another notebook after a connection error.

The examples use the tested CLI version 0.25.2. Use an available `uvx` (or equivalent project-local marimo installation). Set `MOLAB_URL` to the supplied server URL. Keep tokens in private files and pass `--token-file PATH` to every list/execute call when required; never embed credentials in this skill, shared code, or reports.

```bash
uvx marimo==0.25.2 pair notebook list --url "$MOLAB_URL"
```

Choose the returned `session_id` for the intended notebook and set `MOLAB_SESSION`. If several candidate sessions are ambiguous, clarify the target. After a restart, refresh the server URL and session ID. For CLI or API differences, inspect `pair --help` or the module's help rather than guessing.

## Execute and verify

```bash
uvx marimo==0.25.2 pair execute --url "$MOLAB_URL" --session "$MOLAB_SESSION" --code-file /absolute/path/to/experiment.py
```

This sends that local file's Python source only. Supporting files, imports, packages, and paths must exist remotely. `marimo edit NOTEBOOK_URL` downloads a notebook for local execution; it does not connect to Molab's GPU.

Before GPU work, verify `torch.cuda.is_available()`, report the actual device and VRAM, and run a small CUDA calculation with a known expected result. Inspect the response's `success`, `stdout`, and `stderr`: a zero CLI exit code alone is insufficient. Return measured results and usable artifacts. Distinguish execution checks from performance benchmarks.

Scratchpad execution is temporary. For durable work, use `marimo._code_mode` inside `pair execute`: `async with cm.get_context() as ctx`, then `ctx.create_cell(code)` or `ctx.edit_cell(id, code)` and `ctx.run_cell(id)`. Inspect cell status and errors afterwards; queued execution is not completion. Coordinate one writer per notebook.

After a timeout or disconnect, inspect remote status and saved outputs before rerunning a potentially active job. Save long-run checkpoints to verified persistent storage. Sessions are finite; do not add keepalives or assume arbitrary runtime files survive a restart.

## Files in both directions

For small files, transfer bytes through `pair execute`. Upload: base64-encode locally, supply Python through `--code-file -` on stdin, and decode/write at the intended remote path. Download: read remote bytes in bounded chunks, print base64 in JSON, and capture/decode directly to a local file. Start with 4 KiB download chunks; increase only if responses remain complete. Keep payloads out of the model's context. Verify byte counts and SHA-256 at both ends; preserve existing destination files unless replacement is authorized.

For large datasets or weights, transfer directly between Molab and the user's chosen storage or model/dataset host, using its supported client and existing access. Do not make private data public to obtain a download URL. A Grok cloud file is not automatically a Mac file.

CLI-written runtime files are not automatically persistent. Use supported file-browser uploads, persistent caching, or external storage as appropriate; see the [storage policy](https://marimo.io/blog/seamless-storage-in-molab).

Reference only when needed: [official pairing guide](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/) and [Molab compute/storage documentation](https://docs.marimo.io/guides/molab/).
