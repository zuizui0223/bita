from __future__ import annotations

from typing import Callable, Iterable, Sequence


def componentwise_leq(a: Sequence[float], b: Sequence[float], *, tol: float = 1e-12) -> bool:
    if len(a) != len(b) or not a:
        raise ValueError("points must have the same nonzero dimension")
    return all(x <= y + tol for x, y in zip(a, b))


def monotone_path_audit(
    points: Iterable[Sequence[float]],
    margins: Iterable[float],
    *,
    tol: float = 1e-12,
) -> bool:
    xs = tuple(tuple(float(v) for v in p) for p in points)
    ms = tuple(float(v) for v in margins)
    if not xs or len(xs) != len(ms):
        raise ValueError("points and margins must have the same nonzero length")
    dim = len(xs[0])
    if dim == 0 or any(len(p) != dim for p in xs):
        raise ValueError("all points must have the same nonzero dimension")

    for i in range(1, len(xs)):
        if not componentwise_leq(xs[i - 1], xs[i], tol=tol):
            raise ValueError("path is not coordinatewise nondecreasing")
        if ms[i] + tol < ms[i - 1]:
            return False
    return True


def has_positive_to_negative_reentry(margins: Iterable[float], *, tol: float = 1e-12) -> bool:
    seen_positive = False
    for value in margins:
        margin = float(value)
        if margin > tol:
            seen_positive = True
        elif seen_positive and margin < -tol:
            return True
    return False


def minimal_positive_indices(
    points: Iterable[Sequence[float]],
    margins: Iterable[float],
    *,
    tol: float = 1e-12,
) -> tuple[int, ...]:
    xs = tuple(tuple(float(v) for v in p) for p in points)
    ms = tuple(float(v) for v in margins)
    if not xs or len(xs) != len(ms):
        raise ValueError("points and margins must have the same nonzero length")
    dim = len(xs[0])
    if dim == 0 or any(len(p) != dim for p in xs):
        raise ValueError("all points must have the same nonzero dimension")

    positive = [i for i, margin in enumerate(ms) if margin > tol]
    minimal: list[int] = []
    for i in positive:
        dominated_by_positive = False
        for j in positive:
            if i == j:
                continue
            if componentwise_leq(xs[j], xs[i], tol=tol) and any(
                a < b - tol for a, b in zip(xs[j], xs[i])
            ):
                dominated_by_positive = True
                break
        if not dominated_by_positive:
            minimal.append(i)
    return tuple(minimal)
