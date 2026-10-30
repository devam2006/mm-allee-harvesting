# WP02 speaking contribution — target 5 minutes

Editable slides: `wp02/wp02_slides.pptx`; PDF companion: `wp02/wp02_slides.pdf`.
The PDF is a raster companion; editable charts, table and text are in the PPTX.
These are three WP02 slides, not the complete five-person presentation.
Speaker: @AshChan07. Slide notes retain sources, numerical settings and caveats.

## Slide 1 — Model B (target 1:30)

“A fixed catch keeps taking the same amount as the population falls. Here catch
is h times population, so it falls with the population. That does not remove the
Allee threshold. A steady population replaces exactly what is caught. Factoring
the equation gives zero and a quadratic for the positive steady populations.
The lower positive root divides the starting populations that decline from those
that survive. The higher root attracts nearby populations. When the two roots meet,
the field is negative on both sides: attraction only from above. Zero is always
stable because its derivative is -1-e.”

Point to both branches and the zero branch. Know x_minus/plus and ec from the report;
do not spend the full allocation reading their algebra.

## Slide 2 — fair comparisons (target 1:30)

“H and h have different units. We compare equal initial catch, or equal fractions
of each policy's threshold. Those are different experiments. With initial biomass
900 tonnes, matching initial catch gives both A and B 131.28 tonnes/year. Matching
half of each threshold instead gives B 180 tonnes/year. The table shows the latter.
The logistic baseline at the first protocol's catch collapses because 131.28 exceeds
its 125-tonne/year maximum. That does not make Allee growth universally safer:
equal r and K have not matched the production curves.”

Describe the units and 60-year horizon. The examples are synthetic.

## Slide 3 — history and recovery (target 2:00)

“We raise harvesting to 1.3 times critical, hold it there, and then reduce it to
zero. The population is carried through every step; there is no restart on the
way down. At both tested dwell times the population collapses. Model A reaches
zero and we explicitly shut down harvest. Model B approaches zero without an
exact finite extinction event. Even after harvesting stops, a population below
the Allee threshold keeps declining. A separate run adds 0.6K above that threshold,
and recovery follows. This is a recovery barrier with explicit restocking, not a
closed spontaneous hysteresis loop. Devam will now quantify the collapse boundaries
and extinction times.”

The slide shows dwell=1; the report figure includes both dwell=1 and dwell=3.
Population below the numerical absolute tolerance has no claimed relative precision.
Codex assisted drafting, computation and tests; humans must verify and explain them.

## Group assembly and rehearsal handoff

Keep the existing five-speaker order in `outline.md` (25 minutes plus 5 Q&A).
WP01's contribution is available as text; WP03–WP05 completed slide contributions
are absent from this checkout. Import reviewed contributions in the existing order,
standardise x/tau/a/q/e and legends, retain synthetic-data and AI disclosures,
then export the final editable group deck and PDF. Do not fill gaps with expected PINN results.

| Speaker | Target | Observed rehearsal | Status |
|---|---|---|---|
| Raghav / WP01 | 5:00 | not recorded | contribution text available |
| AshChan07 / WP02 | 5:00 | not recorded | three slides and script prepared |
| Devam / WP03 | 5:00 | not recorded | final contribution needed |
| Prem / WP04 | 5:00 | not recorded | final contribution needed |
| Rohan / WP05 | 5:00 | not recorded | final contribution needed |
| Q&A | 5:00 | not recorded | all five |

Understanding check, not an approval gate: why does setting h=0 fail to revive a
population below A? Human understanding/rehearsal has not been assessed by the agent.
