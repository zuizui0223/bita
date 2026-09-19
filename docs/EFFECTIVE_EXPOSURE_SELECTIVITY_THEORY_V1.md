# Effective-exposure selectivity theory v1

## Purpose

Provide a compact mechanistic spine for the refocused BITA macro-ecology paper without restoring the old claim that one observed trait interaction identifies one ecological mechanism.

The theory asks a narrower biological question:

> When can one flower-associated defence/access axis reduce antagonist use before it imposes a comparable cost on legitimate pollination?

## 1. Effective exposure

Let:

- \(x \ge 0\): expressed intensity of a focal defence/access trait;
- \(q_H \ge 0\): antagonist effective-domain coefficient;
- \(q_P \ge 0\): pollinator effective-domain coefficient.

The coefficients \(q_j\) summarize the fraction of trait intensity that is actually experienced by each consumer channel.

They can incorporate:

```text
susceptibility
access geometry
attack route
time overlap
cumulative exposure
functional mode
response stage
```

Define effective exposure:

\[
z_H = q_H x,
\qquad
z_P = q_P x.
\]

This is not a claim that all biological mechanisms are literally multiplicative. It is the minimal scalar representation needed to derive threshold predictions.

## 2. Response thresholds

Let:

- \(\tau_H\): effective exposure required to suppress the antagonist channel;
- \(\tau_P\): effective exposure at which pollinator interference begins.

The corresponding trait-intensity thresholds are:

\[
x_H^* = \frac{\tau_H}{q_H},
\qquad
x_P^* = \frac{\tau_P}{q_P},
\]

when \(q_H,q_P>0\).

A selective window exists when:

\[
\boxed{x_H^* < x_P^*}
\]

or equivalently

\[
\boxed{
\frac{\tau_H}{q_H}
<
\frac{\tau_P}{q_P}
}
\]

and realised expression falls inside:

\[
\boxed{
x_H^* < x < x_P^*
}
\]

so that antagonist use is suppressed before pollinator interference is triggered.

## 3. Biological interpretations

### Separated effective domains

If the antagonist is more exposed/susceptible than the pollinator,

\[
q_H \gg q_P,
\]

then \(x_H^*\) falls relative to \(x_P^*\), widening the selective window.

This can arise from:

- different body size or access geometry;
- different attack routes;
- different temporal windows;
- different biochemical susceptibility;
- different visitor functional modes.

Prediction:

> separated systems should more often show antagonist suppression with a pollinator-compatible state.

### Overlapped effective domains

If both channels experience similar exposure,

\[
q_H \approx q_P,
\]

then selectivity depends mainly on the difference between \(\tau_H\) and \(\tau_P\).

If thresholds are similar, the window is narrow or absent.

Prediction:

> strongly overlapping systems should more often show mutualist interference once the defence is strong enough to suppress antagonists.

### Bypass or tolerance

If the antagonist bypasses the defended surface/route or is effectively insensitive,

\[
q_H \to 0,
\]

then

\[
x_H^* \to \infty.
\]

Prediction:

> the apparent defence can be conspicuous yet fail to reduce the focal antagonist channel.

### Transitional states

Holding \(q_H,q_P,\tau_H,\tau_P\) fixed while increasing \(x\) gives:

```text
x < x_H*:
    defence ineffective

x_H* < x < x_P*:
    guarded/selective window

x > x_P*:
    antagonist suppressed + pollinator interference
```

Prediction:

> increasing dose, cumulative exposure, or response-stage exposure can move one system from null/guarded to interfering without changing its defence category.

## 4. Route switching under access barriers

The threshold model describes whether a focal access route is usable, but antagonists may switch routes rather than disappear.

Let \(L\) denote legitimate access and \(B\) a bypass route.

When the legitimate route is increasingly constrained,

\[
A_L(x) \downarrow,
\]

an exploiter can maintain reward access if a bypass route exists:

\[
A_B > 0.
\]

Prediction:

> stronger geometric mismatch should shift cheating from use of the legitimate opening toward bypass/robbing.

This is the community-scale prediction tested with the Sakhalkar network.

## 5. Mapping to the empirical layers

### Matched-D corpus

Tests the cross-system state prediction:

```text
SEPARATED  -> selective / pollinator-compatible state
OVERLAPPED -> interference more plausible
BYPASS     -> focal antagonist-reduction failure
```

Current strict direct subset is too small to estimate a general coefficient.

### D-side conditionality

Tests the within-system threshold prediction:

```text
increase x / exposure / effective susceptibility
-> cross x_H*
-> enter selective window
-> cross x_P*
-> pollinator interference
```

### Sakhalkar community network

Tests the route-switch prediction:

```text
increasing flower tube length / access constraint
-> cheating shifts from thieving through the opening
   toward robbing/bypass
```

Observed BITA reanalysis:

\[
\rho = 0.346786,\qquad p_{\mathrm{perm}}=0.0086,
\]

for tube length versus species-level robbing–thieving balance.

## 6. Relation to legacy BITA

This theory preserves the useful biological content of the earlier mechanism-first BITA:

- selectivity windows;
- dose/exposure switching;
- consumer-specific response;
- spatial/temporal/access separation;
- bypass boundaries.

It does **not** replace the identification result:

```text
observed A x D interaction != unique ecological mechanism
```

That result remains a claim boundary.

The macro paper uses the threshold theory prospectively to organize biological predictions, while the identification framework controls how strongly any one empirical pattern is interpreted.

## 7. Falsifiers

The effective-domain theory would be weakened by repeated systems in which:

1. independently coded `SEPARATED` domains produce strong direction-supported pollinator impairment at effective antagonist-reducing D;
2. independently coded `OVERLAPPED` domains repeatedly preserve pollination despite comparable exposure and no tolerance difference;
3. `BYPASS_TOLERANCE` systems show strong focal antagonist suppression through the supposedly bypassed route;
4. increasing exposure repeatedly moves systems opposite to the threshold ordering;
5. community-scale access constraint reduces bypass/robbing while increasing use of the legitimate exploitation route.

These are more informative than simply adding supportive case studies.

## 8. Current inference ceiling

The theory is a mechanistic scaffold with qualitative and ordinal predictions.

Current evidence supports recurrence of the predicted states across several implementations, but does not yet identify universal numerical values for:

\[
q_H,\ q_P,\ \tau_H,\ \tau_P.
\]

Nor does the current strict matched-D subset permit a formal comparison showing that domain relation outperforms broad defence modality.

The empirical contribution is therefore:

> recurrent cross-scale predictions from one effective-exposure mechanism, plus a quantitative community-scale route-switch test.
