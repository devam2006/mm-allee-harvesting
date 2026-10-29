# WP01 slide contribution and speaker script (0-5 min)

Speaker: WP01 owner. Three slides for WP02 to merge into the shared deck. All figures are in
`artifacts/figures/` (PNG for slides, EPS/PDF for the report). Synthetic/analytical results only.

## Slide 1: Problem, model and assumptions (about 1.5 min)

**Title:** Harvesting a population with a minimum viable size

- Some harvested stocks collapse and do not recover when fishing is reduced (Hutchings and Reynolds 2004).
- Strong Allee effect: below a threshold A, the population shrinks on its own (mate finding, group defence).
- Model A (fixed quota): dN/dt = rN(1 - N/K)(N/A - 1) - H
- Model B (fixed effort): dN/dt = rN(1 - N/K)(N/A - 1) - hN
- Assumptions: one closed, well-mixed population; deterministic; constant r, K, A; quota stops once N = 0.

**Script:** "We study a population that has a minimum viable size. Below a threshold A, too few
individuals means growth is negative, so the stock shrinks even with no fishing. We add harvesting
in two ways: a fixed quota H every year, which is Model A, and a fixed fraction hN, which is Model B.
The model is deterministic, unstructured and closed, with constant parameters. One modelling choice
matters: you cannot catch fish that do not exist, so once N hits zero we stop and call it extinct."

## Slide 2: Scaling and the logistic baseline (about 1.5 min)

**Title:** Two numbers control the dynamics

- x = N/K, tau = rt, a = A/K, q = H/(rK): dx/dtau = G(x) - q with G(x) = x(1 - x)(x/a - 1)
- Chain rule: dN/dt = rK dx/dtau, so four parameters become two (a, q).
- Logistic recap: x(1-x) = q gives x = (1 +/- sqrt(1 - 4q))/2; upper stable, lower unstable;
  they merge at q = 1/4, so H_c = rK/4.
- Figure: left half of `wp01_logistic_vs_allee.png` (production hill, harvest lines, phase lines).

**Script:** "Dividing by K and measuring time in units of 1/r leaves just two numbers: a, the threshold
as a fraction of capacity, and q, the quota as a fraction of rK. Equilibria are where the production
curve meets the harvest line. For plain logistic growth the hill and the line cross twice: the upper
point is stable, the lower one unstable. At q equal to one quarter they touch, which is the classical
maximum sustainable yield rK over 4, and above that every population crashes."

## Slide 3: Model A equilibria and the fold (about 2 min)

**Title:** A fixed quota creates a cliff

- Figure: `wp01_model_a_branches.png` (or right half of `wp01_logistic_vs_allee.png`).
- q = 0: equilibria 0 (stable), a (unstable threshold), 1 (stable). Extinction is now stable.
- 0 < q < q_c: unstable x_- in (a, x*), stable x_+ in (x*, 1); the negative cubic root is not a population.
- q = q_c: double root at x* = (1 + a + sqrt(1 - a + a^2))/3, semistable (f' = 0, so check signs).
- q > q_c: no equilibrium. For q > 0, x = 0 is not an equilibrium: the stock hits zero in finite time.
- a = 0.2: x* = 0.706, q_c = 0.525. At q = 0.5 the safety margin x_+ - x_- is only 0.149.

**Script:** "With the Allee factor the hill dips below zero between 0 and a, so even without harvest
there is a threshold. As the quota rises, the stable state x-plus and the threshold x-minus move towards
each other and meet at the fold, at x star and q_c, which come from setting G prime to zero. At the fold
the derivative is zero, so linearisation tells us nothing; looking at signs, the flow is downward on
both sides, so it attracts from above and repels below: semistable. Past q_c nothing survives. Near q_c
the safety margin shrinks like the square root of q_c minus q, so a small shock tips the stock over.
We found the roots with Brent's method on brackets from this calculus and checked every stability label
by simulating small perturbations. Devam will now quantify when collapse happens and how long it takes."

## Likely questions (backup)

- Why is x = 0 not an equilibrium of Model A when H > 0? f(0) = -q < 0, so the field still points down at zero.
- Why can't you use f'(x) at the fold? It is zero there; the linear term vanishes, so the sign of f on each side decides.
- Where does x* come from? G'(x) = 0 is 3x^2 - 2(1 + a)x + a = 0; G'(a) > 0 and G'(1) < 0 put exactly one root in (a, 1).
- Why is H_c bigger than the logistic rK/4? r plays a different role once the (x/a - 1) factor multiplies it; comparing needs a calibration (WP02).
- What does the negative root mean? Nothing physical; it is a root of the cubic that lies outside the population domain.
- How did you check the numerics? Independent bounded maximisation for q_c, companion-matrix roots, residuals below 1e-12, finite-difference derivatives and perturbed RK45 trajectories; deliberate bugs each fail a test.
