# Harvesting under a strong Allee effect

<div style="border-left:5px solid #176b87;background:#176b8710;padding:12px"><strong>Read, compute, interpret</strong><br>Five linked work packages study constant catch, proportional effort, collapse boundaries, forward PINNs and inverse inference. All numerical examples are synthetic.</div>

1. WP01 derives scaling, equilibria and stability.
2. WP02 compares explicit harvesting protocols and follows continuous histories with declared restocking.
3. WP03 classifies basins and checks finite extinction by independent quadrature and solvers.
4. WP04 tests forward PINNs against numerical references.
5. WP05 fits identifiable parameter subsets using noisy observations, a classical baseline and held-out windows.

Equations and algorithms precede code; plots are followed by interpretation and limitations. The shared classical APIs use one threshold/branch provider. A small population in B is not finite extinction; A's zero continuation is a declared shutdown policy. Good prediction does not guarantee accurate parameter recovery.

The standalone export includes readable source/config/data/evidence. Restart the kernel and Run All. Recorded final experiments are distinguished from live demonstrations. The two inverse reporting findings from PR #10 remain disclosed in section 5. The Overleaf report, presentation/rehearsal and human approvals are maintained separately.
