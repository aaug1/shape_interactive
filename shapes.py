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
  def __init__(self, coordinates: dict = {}, edges: list = []):
    self.coordinates = coordinates
    self.id_tracker = len(coordinates)
    
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
    
  
  def get_2D_points(self, scale):
    """
    Converts 3D coordinates to 2D coordinates
    """
    output = []
    for point_id, point in self.coordinates.items():
      new_point = self.to_pygame_coords_2D(np.dot(self.projection_matrix, point), scale)
      output.append(new_point)
    return output

  def to_pygame_coords_2D(self, coords, scale):
    """
    Convert an object's coords into pygame coordinates 
    (origin at center of pygame coords).
    """
    return ((coords[0] * scale + WIDTH/2), (coords[1] * scale + HEIGHT/2))
  
  def connect_points(self, point1, point2):
    pygame.draw.line(screen, 'black', point1, point2)
    
  def get_points(self):
    return self.coordinates

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
for i in range(1, num_vertices + 1):
  # hash_points[output[i][0]] = output[i][1:]
  shape.add_point(output[i]) # Add the point  

run = True
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
  points = shape.get_2D_points(scale = 50)
  for point in points:
    x = point[0]
    y = point[1]
    print((x, y))
    pygame.draw.circle(surface = screen, color = 'red', center = (x, y), radius = 5)
    
  pygame.display.flip()
  
pygame.quit()