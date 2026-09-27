<p align="center">
  <img src="assets/banner.gif" alt="60,000 particles orbit a spiral galaxy, condense into the name SkinkEBravia, then detonate in a shockwave" width="100%">
</p>

<h3 align="center">Computer graphics · rendering · real-time VFX</h3>

---

- 👀 I'm interested in **computer graphics**: rendering, simulation and visual effects
- 🌱 Currently learning: CG!
- 💞️ Looking to collaborate on: CG!
- 📫 How to reach me: CG!

<details>
<summary>✨ How the banner is made</summary>

The banner is procedural. [`assets/render_banner.py`](assets/render_banner.py) renders it frame by frame on the CPU with NumPy:

- **60k particles** on differentially rotating orbits in a three-armed log-spiral galaxy, bent by a periodic domain warp so the motion looks like fluid
- **Morph → hold → detonate**: the particles ease into the rasterized name from left to right, shimmer, then get a radial impulse with an expanding shockwave ring
- **Additive splatting** with 4× sub-frame **motion blur**, three-scale Gaussian **bloom**, **chromatic aberration**, vignette and exponential **tone mapping**
- Every orbit completes a whole number of laps, so the 72-frame GIF **loops seamlessly**

```sh
pip install numpy pillow scipy
python assets/render_banner.py
```

</details>
