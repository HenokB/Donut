
<p align="center">
 
![Untitled video - Made with Clipchamp (1)](https://github.com/HenokB/Donut/assets/46082799/5b622aff-7f4b-4fb4-80de-35dff7d3d1e7)

 <h2 align="center">3D Donut Renderer</h2>
 <p>A simple, interactive ASCII art of a spinning 3D donut in the terminal, implemented in Python. </p>

</p>

</p>
  <p align="center">
    <a href="https://github.com/HenokB/Donut/graphs/contributors">
      <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/HenokB/Donut" />
    </a>
    <a href="https://github.com/HenokB/Donut/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/HenokB/Donut?color=0088ff" />
    </a>
    <a href="https://github.com/HenokB/Donut/pulls">
      <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/HenokB/Donut?color=0088ff" />
    </a>
    <br />
    <br />
  </p>


## Prerequisites

- Python 3
- NumPy
- Keyboard

## Installation

Install the dependencies using pip:

```bash
pip install numpy keyboard
```

## Usage
Run the script via the terminal:


```bash
python colored_donut.py
```

## Controls
- Zoom In: Up Arrow
- Zoom Out: Down Arrow

## Logic Behind the Rotation

The spinning 3D donut animation involves fascinating mathematical logic, applying rotations in 3D space, and translating it into a 2D terminal view using ASCII characters.

### Defining the Rotation

In 3D graphics, rotating a point \((x, y, z)\) around any axis involves trigonometric transformations. The code primarily applies rotations around the X and Z axes, denoted as "A" and "B" respectively in the code. The transformation in 3D coordinates post-rotation by angles A (around X-axis) and B (around Z-axis) can be represented using rotation matrices:

\[ R_x(A) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos A & -\sin A \\ 0 & \sin A & \cos A \end{bmatrix} \]
\[ R_z(B) = \begin{bmatrix} \cos B & -\sin B & 0 \\ \sin B & \cos B & 0 \\ 0 & 0 & 1 \end{bmatrix} \]

In the code, these rotations are not applied simultaneously, but successively, resulting in the derivation:

```python
x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T
y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T
z = ((K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T
```
Here, np.outer() calculates the outer product of two arrays, effectively computing the results for all points simultaneously, enhancing computational efficiency.

Rendering Perspective
To visualize the 3D model in a 2D terminal, a perspective projection step is implemented in the code, translating 3D points to 2D. The computation involves K1, K2, ooz (one over z for depth perception), and other variables. The consistent recalculations of sine and cosine values, as angles A and B change, provide the animated rotational effect, crafting a mesmerizing visualization of a 3D donut rotating in the 2D terminal space.

## Troubleshooting
Ensure Python and pip are correctly installed and in your PATH.
Adjust time.sleep() delay in the script if the animation speed is not suitable.

## Acknowledgements
Inspired by the iconic "donut.c" code by [Andy Sloane](https://www.a1k0n.net/).

Contributions are welcome! <3

Made with :heart: and Python.

