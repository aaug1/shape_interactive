import pygame
import numpy as np
import math
from typing import Optional, Tuple 
import re

class Shape():
  """
  Creates a shape using 3D coordinates to be
  generated on the pygame window
  """
  def __init__(self, points: list, faces:list, screen: pygame.Surface, scale:int, colors:list=(0,0,0,1)):
    
    self._coordinates = {} # "_" in python is protected
    self._faces = []
    for point in points:
      self.add_point(point) # Add the point  
    for face in faces:
      self.add_face(face) # Add the face
      
    self.screen = screen
    self.scale = scale
    self.colors = colors

    
    # Set up 3D to 2D projection matrix, +z to user
    self._projection_matrix = np.array([[1, 0, 0],
                                      [0,-1,0],
                                      [0,0,0]])
    
  def add_point(self, point: Tuple[int, float, float, float]):
    """Add a point to the shape object"""
    point_id = point[0]
    self._coordinates[point_id] = point[1:]
    
  def add_face(self, face_point_ids: Tuple[float, float, float]):
    """Add a face to the shape object"""
    self._faces.append(face_point_ids)
    
  def draw_edges(self, color: Tuple[float, float, float, Optional[float]] = (0,0,0)):
    """Draws the edges (connecting lines btw points) based on input file"""
    for face in self._faces:      
      # Convert points to 2D
      points_2D = []
      for point in face:
        point_2D = self.convert_to_2D(self._coordinates[point])
        points_2D.append(point_2D)
      point1, point2, point3 = points_2D[0], points_2D[1], points_2D[2]
      
      # Draw the edges
      pygame.draw.line(self.screen, self.colors['edge'], point1, point2)
      pygame.draw.line(self.screen, self.colors['edge'], point1, point3)
      pygame.draw.line(self.screen, self.colors['edge'], point2, point3)
      
  def draw_faces(self):
    """Draws the faces based on input file"""
    # Get all of the faces
    faces = []
    for face in self._faces:
      # Convert to 2D
      points_2D = []
      points_3D = []
      for point in face:
        point_2D = self.convert_to_2D(self._coordinates[point])
        point_3D = self._coordinates[point]
        points_2D.append(point_2D)
        points_3D.append(point_3D)
      blue_color = self.get_color(points_3D) # Calculate color of face
      points_2D.append(blue_color)
      faces.append(points_2D)
      
    faces.sort(key = lambda x:x[3]) # Order rendering based on RGB blue value
    
    # Render all polygon faces
    for points_2D in faces:
      blue_color = points_2D[3]
      point1, point2, point3 = points_2D[0], points_2D[1], points_2D[2]
      pygame.draw.polygon(self.screen, (0, 0, blue_color, 255), [point1, point2, point3], 0)
    
  def get_color(self, face: Tuple[float, float, float]):
    """
    Calculates the blue color value in range (0,0,95) to (0,0,255)
    (equivalent to #00005F to #0000FF)
    """
    point1, point2, point3 = face
    
    # Get the vector orthogonal to the face
    vec_1 = point2 - point1
    vec_2 = point3 - point2
    ortho = np.cross(vec_1, vec_2)
    
    # Calculates angle between xy-plane and orthogonal vector
    angle = abs(math.asin((ortho[2])/(np.sqrt(ortho[0]**2+ortho[1]**2+ortho[2]**2))))
    
    # Range of color specified is rgb 95 to 255. Range of angle is -pi/2 to pi/2
    OldRange = (math.pi/2)  
    NewRange = (255 - 95)
    blue_color = (((angle) * NewRange) / OldRange) + 95
    return blue_color
    
    
    
  def convert_to_2D(self, point: Tuple[float, float, float]):
    """Convert an object's coords into pygame coordinates 
    (origin at center of pygame coords)"""
    coords = np.dot(self._projection_matrix, point)
    new_point = ((coords[0] * self.scale + WIDTH/2), (coords[1] * self.scale + HEIGHT/2))
    return new_point
    
  
  def get_2D_points(self):
    """Returns list of 2D points, based on added 3D points"""
    output = []
    for point_id, point in self._coordinates.items():
      output.append(self.convert_to_2D(point))
    return output
  
  def draw_points(self):
    for point_id, point in self._coordinates.items():
      x, y = self.convert_to_2D(point)
      pygame.draw.circle(surface = self.screen, color = self.colors['point'], center = (x, y), radius = 5)
    

  def rotate_object(self, x_rotate: float, y_rotate: float):
    # Rotation matrices, where matrix mult applies specified x or y rotations
    rotation_matrix_x = np.array([[1, 0, 0],
                                  [0, math.cos(x_rotate), -math.sin(x_rotate)],
                                  [0, math.sin(x_rotate), math.cos(x_rotate)]])
    rotation_matrix_y = np.array([[math.cos(y_rotate), 0, math.sin(y_rotate)],
                              [0, 1, 0],
                              [-math.sin(y_rotate), 0, math.cos(y_rotate)]])
    
    # Rotate the shape
    for point_id, point in self._coordinates.items():
      rotated_point = np.dot(point, rotation_matrix_x)
      rotated_point = np.dot(rotated_point, rotation_matrix_y)
      self._coordinates[point_id] = rotated_point
      
  def translate_object(self, x_translate: float, y_translate: float):
    for point_id, point in self._coordinates.items():
      print(point)
      translated_point = np.add(point, [x_translate, 0, 0])
      translated_point = np.add(translated_point, [0, y_translate, 0])
      self._coordinates[point_id] = translated_point
      


class Pygame_Window():
  def __init__(self, WIDTH: int, HEIGHT: int, fps: int, caption: str, points: list, faces:list, shape_scale: float, colors: list):
    pygame.init()
    pygame.display.set_caption(caption)
    self.fps = fps
    self.timer = pygame.time.Clock()
    self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
    self.points = points
    self.faces = faces
    self.shape_scale = shape_scale
    self.shape = Shape(points, faces, self.screen, shape_scale, colors)
    self.colors = colors
    
  def play_animation(self):
    run = True
    mouse_press = False
    while run:
      self.screen.fill('white')
      self.timer.tick(self.fps)
      
      # Listen to quit signal
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE):
          run = False
          
        x_translate, y_translate = 0, 0
        speed = 0.5
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT:
              x_translate = -1 * speed
          if event.key == pygame.K_RIGHT:
              x_translate = 1 * speed
          if event.key == pygame.K_UP:
              y_translate = -1 * speed
          if event.key == pygame.K_DOWN:
              y_translate = 1 * speed
              
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
          self.shape = Shape(self.points, self.faces, self.screen, self.shape_scale, self.colors)
          
      # Recognize user mouse interaction
      x_rotate, y_rotate = 0, 0
      if pygame.mouse.get_pressed()[0] == True:
        if mouse_press == False:
          pygame.mouse.get_rel() # starts the shift from cur location
          mouse_press = True
        y_rotate, x_rotate = pygame.mouse.get_rel()
        x_rotate = (x_rotate) / WIDTH * 2
        y_rotate = (y_rotate) / HEIGHT * 2
      else:
        mouse_press = False
      

      # Render the shape
      self.shape.translate_object(x_translate, y_translate)
      self.shape.rotate_object(x_rotate, y_rotate)
      self.shape.draw_points()
      self.shape.draw_faces()
      self.shape.draw_edges()
      pygame.display.flip()

class InputHandler:  
  
  def check_color(self, rgba: str):
    # Check to ensure color is of correct form
    regex = r"(\d+),\s*(\d+),\s*(\d+),\s*(((\d*)?\.\d*)|1|0)"
    keys = ['r', 'g', 'b', 'a']
    if not rgba: # No input specified. Default to black
      return (0,0,0,1)
    
    x = re.search(regex, rgba)

    if not x:
      raise Exception(f"Please format input as '(r,g,b,a) without negative values'")
    else:
      x = list(x.groups())

    for i in range(3):
      try:
        x[i] = int(x[i])
      except ValueError:
        raise Exception(f"{x[i]} could not be converted to an integer for {keys[i]} channel")

      if x[i] > 255 or x[i] < 0:
        raise Exception(f"{x[i]} is not in a valid range for {keys[i]} channel")
    try:
      x[3] = float(x[3])
    except ValueError:
      raise Exception(f"{x[3]} could not be converted to an integer for {keys[3]} channel")
    
    return x[0:4]
  
  def read_file(self, file_repo: str, filename: str):
    try:
      with open(file_repo + filename) as f:
        output = []
        for line in f:
          li = line.strip().split(",")
          res = [eval(i) for i in li]
          output.append(res)
      num_vertices = output[0][0]
      shape_points = output[1:num_vertices + 1]
      shape_faces = output[1 + num_vertices:]
      return shape_points, shape_faces
    except FileNotFoundError:
      raise Exception(f"File does not exist. Please make sure it is in object_files directory")      
    except IndexError:
      raise Exception(f"Input file is formatted incorrectly")    

# Setup the window
WIDTH, HEIGHT = 500, 500
fps = 60
shape_scale = 50
caption = "Render 3D to 2D Shape"
file_repo = './object_files/'
input_handler = InputHandler()

# Read in file
filename = input('Please type in the name of the file: ')
shape_points, shape_faces = input_handler.read_file(file_repo, filename)

# Check to ensure color is of correct form
colors = {}
colors['point'] = input('What color do you want the points to be (R, G, B, A)? ')
colors['edge'] = input('What color do you want the edges to be (R, G, B, A)? ')

for color_id, rgba in colors.items():
  colors[color_id] = input_handler.check_color(rgba)

game = Pygame_Window(WIDTH, HEIGHT, fps, caption, 
                     shape_points, shape_faces, shape_scale, colors)
game.play_animation()
pygame.quit()