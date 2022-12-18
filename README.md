# shape_interactive

This repository contains two python files, `shape_wire.py` and `shape_faces.py`, which render 3D objects using the pygame library.

## Setup
To setup, please make sure that you have Python and Pip installed. If not, please refer to the documentation:
* Python Installation: https://www.python.org/downloads/
* Pip Installation: https://pip.pypa.io/en/stable/installation/

Once installed, setup a virtual environment with the following command:

* windows 
  ```
  python -m venv <virtual-env-name>
  pip install -r requirements.txt
  ```
* linux/macosx
  ```
  python3 -m venv <virtual-env-name>
  pip3 install -r requirements.txt
  ```
* For more information, see https://code.visualstudio.com/docs/python/environments

## How to use
To use this file with your own custom shape, move a new text file into the object_files directory. Then, run the following command: ('python3' is 'python' in windows)
```
python3 shape_wire.py
```

The program will ask for 3 input fields:
1. Name of the file
2. RGBA color for points (not displayed if not specified)
3. RGBA color for edges (not displayed if not specified)
  
**Example**:
```
Please type in the name of the file: object.txt
What color do you want the points to be (R, G, B, A)? 0,0,255,255
What color do you want the edges to be (R, G, B, A)? 0,0,255,255
```

Then, the shape will render!

## Description
### Part 1: `shape_wire.py`

Using 2D graphics, this python file  displays a 3D object defined by vertices and triangular faces of the object. The faces of the object are transparent, resulting in a wireframe rendering of the 3D object.

The canvas is set up such that the coordinate frame follows the following convention:
* Positive x: points horizontally to left
* Positive y: points vertically upward
* Positive z: points out of plane toward the observer

To render a 3D object, create a text file with the following format:
* First line: specifies number of vertices and faces in the object--> num_vertices,num_faces
* Second to 1 + num_vertices lines: specifies vertex id, and the x,y,z coordinates --> id,x,y,z
* 2 + num_vertices to end of the file: specifies the 3 point ids that create a triangular face --> point1,point2,point3

This function further supports click-and-drag rotations about the origin, where horizontal and vertical movement of the mouse rotates the 3D object about the vertical Y-axis, horizontal x-axis, respectively. Diagonal movement of the mouse is decomposed into horizontal and vertical movement.



### Part 2 `shape_faces.py`
The same functionality as defined in part 1 is implemented for this second python file. However, running this script will generate the shape with filled-in faces. The color of each face varies (smoothly) between #00005F (when the surface is viewed on edge, i.e. the normal of the surface makes a 90 degree angle to the Z-axis) and #0000FF (when the surface is viewed flat, i.e. orthogonal to the Z-axis) based on the angle with the Z-axis, such that the face is displayed similarly to how a shader would display it. This is equivalent to rgb values of (0,0,95) and (0,0,255), respectively.

## Algorithms

This section specifies the 3D graphics algorithms used in the program

1. **Cross Product**: Calculated using np.cross(A, B). The cross product determines the orthogonal vector  of vectors A and B, which outputs vector $(c_x, c_y, c_z)$ where:
   1. $c_x = a_y b_z - a_z b_y$
   2. $c_y = a_z b_x - a_x b_z$
   3. $c_z = a_x b_y - a_y b_x$

2. **Dot Product**: Calculated using np.dot(A, B). A measure of how closely two vectors align in terms of direction. Equivalent to $a_xb_x + a_yb_y + a_zb_z$. Used here for matrix multiplication (skips transposition step for mxn mxn matrices) and for back-face culling.
3. **Back-face culling**: Used to determine whether the triganle face of the shape was drawn. After determining the normal vector of the triangle face, calulated by choosing any point $v_0$ and using the dot product with the normal vector, N: $(v_0 - P) \cdot N \ge 0$, then cull.
4. **Converting ranges**: The following equation was used to determine the range of colors to map the face to, based on its angle with the z-axis: $$new\_val = \frac{((old\_val - old\_min) * (new\_max - new\_min)}{old\_max - old\_min} + new\_min$$
5. **Projection matrix**: a projection matrix is a square matrix that, when multiplied by vector, will project the points to a subspace. This implementation uses the following projection matrix to map 3D points to 2D: 
   $$
   \begin{pmatrix}
   1 & 0 & 0 \\
   0 & -1 & 0 \\
   0 & 0 & 0 \\
   \end{pmatrix}
   $$
6. **Rotation matrix**: these are square transformation matrices that, when multiplied by a vector, rotates it in euclidean space. For x and y rotations, the following matrices were used:
  $$ R_x = 
  \begin{pmatrix}
  1 & 0 & 0 \\
  0 & cos(\theta) & -sin(\theta) \\
  0 & sin(\theta) & cos(\theta) \\
  \end{pmatrix}
  $$
  $$ R_y = 
  \begin{pmatrix}
  cos(\theta) & 0 & sin(\theta) \\
  0 & 1 & 0 \\
  -sin(\theta) & 0 & cos(\theta) \\
  \end{pmatrix}
  $$