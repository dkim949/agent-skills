# PyTorch diagnosis

Use these checks to build ranked, testable hypotheses within `diagnosing-bugs`. Record the installed PyTorch version, backend (CPU/CUDA/MPS), precision, relevant shapes, and the exact failing step. Use documentation matching that version before changing APIs. A suspected anti-pattern is not proof of cause.

## Locate the failure

- NaN/inf: check input, target, output, loss, and gradient finiteness to find the first invalid value. Inspect mathematical domains, loss/target compatibility, reduction denominators, learning rate, and precision. Use anomaly detection for a bounded reproduction when appropriate; it adds overhead.
- Gradients or plateau: verify the intended parameters receive finite gradients and optimizer updates. Check zeroing and accumulation boundaries, detached tensors, frozen parameters, optimizer membership, scheduler order, target scaling, and train/eval mode. Compare a tiny fixed batch or known baseline before attributing a plateau to architecture.
- Device/dtype errors: inspect parameters, buffers, inputs, targets, masks, and newly created tensors at the failing operation. Match the operation's required dtype and device; avoid indiscriminate casts that change target or mask semantics.
- Padding: verify that attention, pooling, and loss exclude padding as required. If missingness defines validity, construct the validity mask before replacing missing values; verify mask polarity and broadcasting at every consumer.

## Memory

- Separate live tensor allocations from allocator reservations and other processes. On CUDA, compare allocated/reserved and peak counters; use a bounded memory snapshot if needed. PyTorch snapshots may miss memory allocated outside its allocator.
- Check retained graphs in accumulated losses, outputs, callbacks, or caches. For scalar logging use `.item()` when appropriate; detach stored diagnostic tensors. A CPU copy alone does not necessarily sever autograd history.
- Validate batch size, sequence length, optimizer state, gradient accumulation, and validation autograd settings. `model.eval()` changes layer behavior; it does not disable gradient recording. Use `no_grad` or inference mode where their semantics fit.
- `empty_cache()` releases unused cached CUDA blocks; it does not free live tensors or increase memory available to PyTorch. Consider it only for an identified allocator/fragmentation need, not as mandatory cleanup after validation.

## Throughput

Measure data wait, host/device transfer, and compute separately before tuning. Benchmark `num_workers`, pinning, and persistent workers with the actual workload and host memory budget; zero workers can be correct. More workers or pinned memory are not universally faster. Persistent workers retain worker processes between epochs when workers are enabled.

For mixed precision, inspect backend/dtype support and numerical behavior. With GradScaler, unscale gradients before clipping or inspecting their true magnitude, after accumulation is complete. Gradient clipping, AMP, and clamping a logarithm input are conditional interventions, not universal fixes; preserve the intended mathematics and compare correctness and convergence.

## Official references

Checked during consolidation on 2026-10-27; use the installed version at diagnosis time:

- [DataLoader](https://docs.pytorch.org/docs/stable/data.html): workers, pinning, persistence and resource tradeoffs.
- [Autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html): evaluation mode and gradient modes.
- [AMP examples](https://docs.pytorch.org/docs/stable/notes/amp_examples.html): scaling, accumulation, and gradient clipping.
- [CUDA memory management](https://docs.pytorch.org/docs/stable/notes/cuda.html#memory-management): allocated vs reserved memory and cache behavior.
- [CUDA memory snapshots](https://docs.pytorch.org/docs/stable/torch_cuda_memory): capture scope and limitations.
- [PyTorch FAQ](https://docs.pytorch.org/docs/stable/notes/faq.html): retained history and out-of-memory diagnosis.

The former `pytorch-debug/learnings.md` contained no recorded feedback at migration; no diagnostic learnings were omitted.
