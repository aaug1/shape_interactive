# shape_interactive

This repository contains two python files, `shapes_wire.py` and `shapes_faces.py`, which render 3D objects using the pygame library. 

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


## Part 1: `shapes_wire.py`

### How to use
To use this file with your own custom shape, move a new text file into the object_files directory.

### Description
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



## Part 2
