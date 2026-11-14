# Exact startup-cost feasibility gate for BITA trait differentiation (2026-11-14)

**Status: analytic extension of Draft PR #361, THEORY ONLY.** This note is restricted to the existing quadratic function-conflict model with a *specified* saturating activation-cost family. It does not establish a biological prevalence, a genetic fixation rate, or the evolutionary origin of a heritable module. It is not part of the active nectar-robbery Letter.

## Previously frozen model

For function weights \(\ w_1,w_2>0\), residual interference \(\lambda\geq0\), function-optimum distance \(d>0\), and separation \(0\leq u\leq1\), let

\[
h=\frac{w_1w_2}{w_1+w_2},\quad
s=\frac{h}{h+\lambda},\quad
G(u)=d^2[2hu-(h+\lambda)u^2].
\]

The *additional assumed* startup cost is \(K(u)=c(1-\exp(-u/\tau))\), with \(c>0,\tau>0\), and relative gain \(\Phi(u)=G(u)-K(u)\). A strict local trap with a globally fitter split phenotype means

\[
\Phi'(0)=2hd^2-c/\tau<0,\qquad
\sup_{0<u\leq1}\Phi(u)>0.
\]

Draft #361 already supplied the **sufficient**, not necessary, interval \(2hd^2\tau<c<shd^2\). This interval can exist only when \(\tau<s/2\). Here we derive the **exact existence gate** for *some* \(c\), without changing the model.

## Proposition 1: an exact existence gate, not a measured biological threshold

For fixed \(d>0,w_1,w_2>0,\lambda\geq0,\tau>0\), there exists at least one \(c>0\) yielding **both** a strict local trap and a positive global differentiation gain **if and only if**

\[
\boxed{\tau<s=\frac{h}{h+\lambda}.}
\]

The exact admissible interval for the cost cap, when nonempty, is

\[
\boxed{
2hd^2\tau<c<C_{\rm crit}(\tau),\qquad
C_{\rm crit}(\tau)=
\sup_{0<u\leq1}
\frac{d^2[2hu-(h+\lambda)u^2]}{1-\exp(-u/\tau)}.
}
\]

The ratio has a finite continuous extension at \(u=0\), equal to \(2hd^2\tau\); this endpoint itself is *not* a positive-gain witness. The upper bound is a numerical one-dimensional maximization problem for fixed parameters, not a new empirical coefficient.

### Proof, impossibility when \(\tau\geq s\)

For all \(x\geq0\), \(1-e^{-x}\geq x-x^2/2\). If the local slope is strictly negative, \(c>2hd^2\tau\). For every \(u>0\),

\[
\begin{aligned}
c(1-e^{-u/\tau})
&>2hd^2\tau(1-e^{-u/\tau})\\
&\geq2hd^2\left(u-\frac{u^2}{2\tau}\right)\\
&\geq2hd^2\left(u-\frac{u^2}{2s}\right)
 =G(u),
\end{aligned}
\]

where the final inequality uses \(\tau\geq s\). Consequently \(\Phi(u)<0\) for all \(u>0\); no globally beneficial split exists.

### Proof, existence when \(\tau<s\)

Write \(Q(u)=G(u)/(1-e^{-u/\tau})\). Its positive-side expansion is

\[
Q(u)=2hd^2\tau+hd^2(1-\tau/s)u+O(u^2).
\]

If \(\tau<s\), its initial linear coefficient is strictly positive. Hence for a sufficiently small positive \(u\), \(Q(u)>2hd^2\tau\). Choosing any \(c\) strictly between these two values makes \(\Phi'(0)<0\) and \(\Phi(u)>0\). This proves the converse.

**Important distinction:** \(\tau<s\) is necessary and sufficient for the *existence of some cost cap* creating the gap; it is not sufficient for a **particular** supplied \(c\). The latter also needs the exact cap interval above. The earlier \(\tau<s/2\) is a conservative sufficient-window condition, not an exact feasibility ceiling.

## Proposition 2: a general curvature exclusion bound

Keep the same concave quadratic \(G(u)\), but allow any twice-continuously-differentiable startup cost \(K(u)\) with \(K(0)=0\). If \(\Phi'(0)<0\) but \(\Phi(u)>0\) for some \(u>0\), the mean-value theorem applied twice implies \(\Phi''(v)>0\) at some \(v\in(0,u)\), so necessarily

\[
\boxed{K''(v)<-2(h+\lambda)d^2\quad\text{for some }v>0.}
\]

In particular, any convex or linear \(K\) makes \(\Phi\) concave and **cannot** produce a locally trapped but globally beneficial split. Mere concavity of \(K\) is not enough; it must locally exceed the negative curvature of the gross gain. This is a *necessary*, not sufficient, curvature test.

For the saturating family, \(K''(u)=-c e^{-u/\tau}/\tau^2\). A necessary (not sufficient) condition becomes \(c/\tau^2>2(h+\lambda)d^2\). These formulas concern the declared trait and score coordinates.

## Concrete synthetic counterexample beyond the old sufficient bound

Hold \(w_1=w_2=1\), \(\lambda=0.5\), \(d=1\), so \(h=s=0.5\). Use \(\tau=0.30\), \(c=0.315\).

- Old sufficient window would require \(\tau<s/2=0.25\) and \(c<shd^2=0.25\); **neither is met**.
- The exact existence gate is open: \(\tau=0.30<s=0.50\).
- The exact initial slope is \(\Phi'(0)=1-0.315/0.30=-0.05\).
- The *explicit witness* at \(u=0.30\) is \(\Phi(0.30)=0.010882023969\ldots>0\). This is sufficient to demonstrate a global gain without relying on an optimizer.
- As a negative control, at \(\tau=s=0.5,c=0.51\), the local slope is negative but **every** split \(u>0\) is globally inferior by Proposition 1.

## Numerical safeguards and reproducibility

The new regression tests use the frozen implementation in \`trait_architecture/evolutionary_accessibility.py\` and test (i) the explicit \(\tau=0.3\) positive-gain witness, (ii) 324 distinct \(\tau\geq s\), negative-initial-gradient configurations, and (iii) 36 additional constructive \(\tau=0.75s<s\) parameter configurations. The \(\tau\geq s\) impossibility itself rests on the inequality proof, not on a finite parameter grid.

Command: \`pytest -q tests/test_evolutionary_accessibility_exact_window.py\`

**Inference ceiling:** This extension corrects the *mathematical sharpness of the feasibility statement within the assumed exponential family*. It does not measure real \(K(u)\), \(\tau\), \(s\), genetic mutational accessibility, organismal fitness, historical origin, or frequency of differentiation in nature. The broad specialization/pleiotropy question predates BITA (Rüffler et al. 2012, PNAS, DOI 10.1073/pnas.1110521109; Guillaume & Otto 2012, Genetics, DOI 10.1534/genetics.112.143214). The ecological Letter and published-data effect tables are untouched.
