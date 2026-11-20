# Reference Mode: *In the Praise of The Word* (Qwen3-0.6B)

Use this reference alongside `../SKILL.md` whenever writing or revising a chapter of **"In the Praise of The Word"**, the NCERT-style textbook mapping standard transformer architecture through real traces of **Qwen3-0.6B**.

## Original User Brief

> "create this pdf where you adopt writing style and presentation quirks and 'ahas' from this pdf - https://www.drishtiias.com/images/pdf/social%20science%20demo%20part%201.pdf i loved this book as a kid and want to read everything as a piece from it but do not give it a fake chapter name or something. i need everything standard transformer arch work qwen 0.6B stuff beginning to end fully mapped, it is a textbook so students would need to know everything."

Shaping follow-ups:
- Match the aesthetics of `~/Downloads/Is-4-bit-the-new-lossless-textbook.pdf` (footers: `"Tokenbender"` / `"In the Praise of The Word"`).
- Teach the way you would teach your own kids, with Feynman-level depth and clarity.
- Run the real model and trace it to enrich the PDF; keep it educational material, not a spec sheet; avoid distracting toy/"pocket" machines.
- Title: **In the Praise of The Word**.

## Book Plan

One running request — **`write fibonacci function`** — traced end-to-end through one real machine: **Qwen3-0.6B**.

- **Front matter:** Title page with contents, *"How This Book Was Made"* (method and sources).
- **Chapter 1:** *What Is a Language Model? Why Guess the Next Word?* (the whole story once; exists)
- **Chapter 2:** *From Text to Numbers*
- **Chapter 3:** *Looking Back*
- **Chapter 4:** *One Floor, All the Way Through*
- **Chapter 5:** *From Scores to Text*
- **Chapter 6:** *How the Machine Learns*
- **Chapter 7:** *From Text Predictor to Assistant*
- **Chapter 8:** *Looking Inside*

## Consistent Metaphor Vocabulary (from Chapter 1)

Give the proper technical name once when earned, then use the book's word consistently:

| Book image | Technical concept |
| --- | --- |
| tokens | BPE subword tokens (`·` for space, `↵` for newline) |
| word book | vocabulary & embedding matrix (`embed_tokens`) |
| notebook | residual stream |
| floors | transformer layers (0–27) |
| looking-back room | self-attention (query, key, value, heads, shares/weights, causal mask, quiet corner) |
| clock hands | RoPE (rotary position embeddings) |
| thinking room / experts | MLP / SwiGLU (`gate_proj`, `up_proj`, `down_proj`) |
| scores / chances | logits / softmax probabilities |
| temperature, top-k / top-p | decoding sampling controls |
| shelf | KV cache |
| surprise / loss | negative log-likelihood / cross-entropy loss |

## Real-Trace Workflow for Qwen3-0.6B

Run real Qwen3-0.6B locally when weights are available; if no local model folder is accessible and a browser runtime is available, load public weights directly in the browser:

1. **Fetch weights cleanly:**
   - Open a normal `huggingface.co` page (raw file pages have a CSP that blocks `fetch`).
   - Range-fetch `https://huggingface.co/Qwen/Qwen3-0.6B/resolve/main/model.safetensors`: read 8-byte header length, parse JSON header, then fetch each BF16 tensor; skip `lm_head.weight` (tied to `model.embed_tokens.weight`).
   - Convert `bf16` → `f32` via `u32 = u16 << 16`; keep transformer layers in `f32` (~1.8 GB) and embeddings in `bf16`.
2. **Exact layer math (per layer):**
   - `RMSNorm(eps=1e-6, weight)` → `q/k/v` projections (no bias) → per-head `QK-Norm` → RoPE `rotate_half` (pair `i` with `i+64`, `inv_freq = 1e6^(-2i/128)`) → causal `softmax(qk / sqrt(128))` with GQA (query head `h` uses KV head `h >> 1`) → `o_proj` → residual add
   - `RMSNorm` → `down_proj(silu(gate_proj) * up_proj)` → residual add
   - Final `RMSNorm` → `logits = embedding_rows · vector`.
3. **Instrumentation & hooks:**
   - Capture residual stream snapshots (logit lens), attention probability rows, ablations (skip attention or MLP per layer, RoPE off, position offset), and KV-cached generation with seeded sampling.
   - In browser JS, yield with `MessageChannel` (not `setTimeout`) so background panes are not throttled; run long jobs asynchronously and poll if tool timeouts apply (~45 s).
4. **Sanity validation before writing:**
   - Greedy reply to the chat-templated running request produces a working Python Fibonacci function.
   - `"The capital of France is"` predicts `" Paris"` (~66%).
5. **Tokenization & prompt template:**
   - Tokenize/decode with Qwen tiktoken BPE (`151,643` merges; special tokens `151643–151668`).
   - Non-thinking template:
     `<|im_start|>user\n{msg}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n`
     (`15` tokens for `write fibonacci function`).
6. **Data hygiene & delivery:**
   - Save compact trace summaries to data files; generate all SVGs/charts from those files.
   - Deliver the built PDF in conversation and save to `~/Downloads`, preserving earlier versions.
