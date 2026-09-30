# Chapter 1 · Pythagorean Identities

[← Contents](README.md)

These three identities are called the **Pythagorean identities**. The name comes from the fact that all three are the Pythagorean theorem $a^2 + b^2 = c^2$ in a different form.

$$
\sin^2\theta + \cos^2\theta = 1
$$

$$
1 + \tan^2\theta = \sec^2\theta
$$

$$
1 + \cot^2\theta = \csc^2\theta
$$

## 1.1 Where they come from

Put the angle $\theta$ on the unit circle. The point on the circle is $(\cos\theta,\ \sin\theta)$. Together with the origin, it makes a right triangle with legs $\cos\theta$ and $\sin\theta$ and a hypotenuse of $1$. The Pythagorean theorem then gives:

$$
\sin^2\theta + \cos^2\theta = 1
$$

The other two follow from this one. You do not need to memorise them separately:

| Divide $\sin^2\theta + \cos^2\theta = 1$ by | Result |
| --- | --- |
| $\cos^2\theta$ | $\tan^2\theta + 1 = \sec^2\theta$ |
| $\sin^2\theta$ | $1 + \cot^2\theta = \csc^2\theta$ |

This uses $\tan\theta = \dfrac{\sin\theta}{\cos\theta}$, $\cot\theta = \dfrac{\cos\theta}{\sin\theta}$, $\sec\theta = \dfrac{1}{\cos\theta}$ and $\csc\theta = \dfrac{1}{\sin\theta}$.

> **Where they hold.** The first identity holds for every $\theta$. The second needs $\cos\theta \neq 0$, and the third needs $\sin\theta \neq 0$, because those are the values you divide by.

## 1.2 The hexagon

The three identities fit on one picture, sometimes called the **trig hexagon** or **magic hexagon**. Put $1$ in the centre and the six functions on the corners:

<p align="center">
  <img src="assets/hexagon.svg" alt="A hexagon with 1 in the centre. Top row: sin, cos. Middle row: tan, 1, cot. Bottom row: sec, csc. Three shaded triangles: sin–cos–1 at the top, tan–1–sec at the lower left, and 1–cot–csc at the lower right." width="340">
</p>

Each function has a fixed place:

- **Left side**: the "co-less" functions, $\sin$, $\tan$, $\sec$.
- **Right side**: their co-functions, $\cos$, $\cot$, $\csc$.
- **Opposite corners** are reciprocals: $\sin \leftrightarrow \csc$, $\cos \leftrightarrow \sec$, $\tan \leftrightarrow \cot$.

### The translation rule

There are three shaded triangles. Each one points down, so it has **two corners on top** and **one corner at the bottom**. Every shaded triangle becomes an equation by the same rule:

$$
(\text{top-left})^2 + (\text{top-right})^2 = (\text{bottom})^2
$$

| Triangle | Top-left | Top-right | Bottom | Equation |
| --- | --- | --- | --- | --- |
| upper | $\sin$ | $\cos$ | $1$ | $\sin^2\theta + \cos^2\theta = 1$ |
| lower left | $\tan$ | $1$ | $\sec$ | $\tan^2\theta + 1 = \sec^2\theta$ |
| lower right | $1$ | $\cot$ | $\csc$ | $1 + \cot^2\theta = \csc^2\theta$ |

(Note that $1^2 = 1$.) So the picture gives you all three Pythagorean identities from one rule.

## 1.3 Using them

The identities are often used rearranged:

$$
\sin^2\theta = 1 - \cos^2\theta \qquad \cos^2\theta = 1 - \sin^2\theta
$$

$$
\tan^2\theta = \sec^2\theta - 1 \qquad \cot^2\theta = \csc^2\theta - 1
$$

**Example.** $\sin\theta = \dfrac{3}{5}$ and $\theta$ is in quadrant II. Find $\cos\theta$ and $\tan\theta$.

$$
\cos^2\theta = 1 - \left(\tfrac{3}{5}\right)^2 = \tfrac{16}{25}
\quad\Rightarrow\quad
\cos\theta = -\tfrac{4}{5}
$$

The sign is negative because cosine is negative in quadrant II. Then:

$$
\tan\theta = \frac{\sin\theta}{\cos\theta} = \frac{3/5}{-4/5} = -\frac{3}{4}
$$

> **Watch the sign.** Taking a square root gives $\pm$. The identity alone cannot choose the sign; the quadrant of $\theta$ chooses it.

## Summary

| Identity | Holds when |
| --- | --- |
| $\sin^2\theta + \cos^2\theta = 1$ | always |
| $1 + \tan^2\theta = \sec^2\theta$ | $\cos\theta \neq 0$ |
| $1 + \cot^2\theta = \csc^2\theta$ | $\sin\theta \neq 0$ |

Hexagon rule: in each shaded triangle, **top² + top² = bottom²**.
