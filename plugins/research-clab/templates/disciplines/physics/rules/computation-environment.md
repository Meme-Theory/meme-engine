# Computation Environment

<!-- DEPLOY: project-root/.claude/rules/computation-environment.md -->
<!-- Path-scoped: loads when working in the computation directory or on Python sources -->
<!-- Source: extracted from Ainulindale Exflation .claude/rules/computation-environment.md -->

---
paths:
  - "{{COMPUTATION_DIR}}/**"
  - "*.py"
---

## Hardware

- **CPU**: `{{CPU}}`
- **RAM**: `{{RAM}}`
- **GPU**: `{{GPU}}`
- **OS**: `{{OS}}`

## Python Environment

**ALWAYS use the GPU-enabled venv for ALL scripts** — do not fall back to the system Python if a GPU-capable venv exists.

- **Python venv**: `{{PYTHON_VENV}}`
- **Torch stack**: `{{TORCH_STACK}}`
- **Invoke**: `"{{PYTHON_VENV}}/Scripts/python.exe" script.py` (Windows) or `"{{PYTHON_VENV}}/bin/python" script.py` (Unix)

### Key Packages

Fill in at pack-install time for the project's specific stack. At minimum, document which of `numpy`, `scipy`, `matplotlib`, `h5py`, `pyfftw`, `numexpr`, `torch` are installed in each environment and which of them have GPU-accelerated backends.

## Running Scripts

- **ALL scripts**: use the venv Python, not the system Python.
- Large-array work (eigenvalue sweeps, Pfaffian computations, spectral-action scans, FFT lattices) benefits from the GPU.

## Heavy Linear Algebra — Prefer GPU (MANDATORY)

Compute-mode agents default to `numpy.linalg` out of training bias. On a GPU-equipped machine that is the wrong default. For matrices ≥ 100×100:

- **Eigvals / SVD / matrix products**: use `torch.linalg.eigvals`, `torch.linalg.svd`, `torch.matmul` on the accelerator backend.
- **FFTs**: use `torch.fft`.
- **Pattern**:
  ```python
  import torch
  t = torch.tensor(M, device='cuda')               # ship to GPU
  evals = torch.linalg.eigvals(t).cpu().numpy()    # compute, bring back
  ```
- **Why**: `numpy.linalg.eigvals` threads across all CPU cores; when two compute-mode agents run in parallel they contend and each takes roughly 2× wall time. A moderately sized eigvals call on GPU runs in tens of milliseconds versus seconds on CPU.
- **Validation**: for first use in a script, cross-check the first few eigenvalues against `numpy.linalg.eigvals` on a small test matrix to catch any numerics surprises.

## CPU Thread Cap When GPU Not Used

If an operation is truly CPU-only (small matrices, iterative solvers without GPU support, legacy scipy paths), cap threads to avoid contention with other concurrent agents:

```python
import os
os.environ.setdefault('OMP_NUM_THREADS', '8')
os.environ.setdefault('MKL_NUM_THREADS', '8')
# … then:
import numpy as np
```

Set **before** `import numpy` — numpy reads these env vars at import time, not at call time.
