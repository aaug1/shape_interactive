import pygame
import numpy as np
import math

pygame.init()

# Setup the window
WIDTH, HEIGHT = 500, 500
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Render 3D to 2D Shape")


class Shape():
  def __init__(self, coordinates: dict = {}, faces: list = []):
    self.coordinates = coordinates
    self.id_tracker = len(coordinates)
    self.faces = faces
    self.coordinates_2D = {}
    
    # if len(coordinates) == 0:
    #   self.coordinates_3D = np.empty((0,3), float)
    # else:
    #   self.coordinates_3D = np.array(coordinates)
      
    # Set up 3D to 2D projection matrix
    self.projection_matrix = np.array([[1, 0, 0],
                                [0,1,0],
                                [0,0,0]])
    
  def add_point(self, point):
    point_id = point[0]
    self.coordinates[point_id] = point[1:]
    
    # self.coordinates_3D = np.vstack([self.coordinates_3D, point])
    
  def add_face(self, face_point_ids):
    self.faces.append(face_point_ids)
    
    
  def draw_edges(self):
    for face in self.faces:
      # Convert to 2D
      points_2D = []
      for point in face:
        point_2D = self.convert_to_2D(self.coordinates[point])
        points_2D.append(point_2D)
      point1, point2, point3 = points_2D[0], points_2D[1], points_2D[2]
      # point1, point2, point3 = face[0], face[1], face[2]
      print(f"here {point1}")
      pygame.draw.line(screen, 'black', point1, point2)
      pygame.draw.line(screen, 'black', point1, point3)
      pygame.draw.line(screen, 'black', point2, point3)
    
  def convert_to_2D(self, point, scale = 50):
      # for point_id, point in self.coordinates.items():
      new_point = self.to_pygame_coords_2D(np.dot(self.projection_matrix, point), scale)
        # output.append(new_point)
        # self.coordinates_2D[point_id] = new_point
      return new_point
    
  
  def get_2D_points(self, scale = 50):
    """
    Converts 3D coordinates to 2D coordinates
    """
    output = []
    for point_id, point in self.coordinates.items():
      output.append(self.convert_to_2D(point, scale))
    return output

  def to_pygame_coords_2D(self, coords, scale = 50):
    """
    Convert an object's coords into pygame coordinates 
    (origin at center of pygame coords).
    """
    return ((coords[0] * scale + WIDTH/2), (coords[1] * scale + HEIGHT/2))

    
  def get_points(self):
    return self.coordinates
  
  def rotate_object(self, angle):
    rotation_matrix_x = np.array([[1, 0, 0],
                                  [0, math.cos(angle), -math.sin(angle)],
                                  [0, math.sin(angle), math.cos(angle)]])
    rotation_matrix_y = np.array([[math.cos(angle), 0, math.sin(angle)],
                              [0, 1, 0],
                              [-math.sin(angle), 0, math.cos(angle)]])
    output = []
    for point_id, point in self.coordinates.items():
      rotated_point = np.dot(point, rotation_matrix_x)
      rotated_point = np.dot(rotated_point, rotation_matrix_y)
      point_2D = self.convert_to_2D(rotated_point)
      self.coordinates[point_id] = rotated_point
      output.append(point_2D)
      print(f"point {point_2D}")
    
    return output

############################

## Read in input
with open('object.txt') as f:
  output = []
  for line in f:
    li = line.strip().split(",")
    res = [eval(i) for i in li]
    output.append(res)
  
## Process the input data
shape = Shape()
num_vertices = output[0][0]
num_faces = output[0][1]
hash_points = {}
points = output[1:num_vertices + 1]
for point in points:
  shape.add_point(point) # Add the point  
  
faces = output[1 + num_vertices:]
for face in faces:
  shape.add_face(face) # Add the face


run = True
angle = 0
while run:
  screen.fill('white')
  timer.tick(fps)
  
  # Listen to quit signal
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE):
      run = False
    
  # Draw the shape
  angle = 0.01 % 360
  points = shape.rotate_object(angle)
  #points = shape.get_2D_points(scale = 50)
  for point in points:
    x = point[0]
    y = point[1]
    print((x, y))
    pygame.draw.circle(surface = screen, color = 'red', center = (x, y), radius = 5)
  shape.draw_edges()
  pygame.display.flip()
  
pygame.quit()