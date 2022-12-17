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
  def __init__(self, coordinates: list = [], edges: list = []):    
    if len(coordinates) == 0:
      self.coordinates_3D = np.empty((0,3), float)
    else:
      self.coordinates_3D = np.array(coordinates)
      
    # Set up 3D to 2D projection matrix
    self.projection_matrix = np.array([[1, 0, 0],
                                [0,1,0],
                                [0,0,0]])
    
    
  def add_point(self, point):
    self.coordinates_3D = np.vstack([self.coordinates_3D, point])
  
  def get_2D_points(self, scale):
    """
    Converts 3D coordinates to 2D coordinates
    """
    output = []
    for point in self.coordinates_3D:
      new_point = self.to_pygame_coords_2D(np.dot(self.projection_matrix, point), scale)
      output.append(new_point)
    return output

  def to_pygame_coords_2D(self, coords, scale):
    """
    Convert an object's coords into pygame coordinates 
    (origin at center of pygame coords).
    """
    return ((coords[0] * scale + WIDTH/2), (coords[1] * scale + HEIGHT/2))

############################

shape = Shape()
shape.add_point([-1, -1, -1])
shape.add_point([-1, -1, 1])
shape.add_point([-1, 1, -1])
shape.add_point([-1, 1, 1])
shape.add_point([1, -1, -1])
shape.add_point([1, -1, 1])
shape.add_point([1, 1, -1])
shape.add_point([1, 1, 1])

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
  points = shape.get_2D_points(scale = 10)
  for point in points:
    x = point[0]
    y = point[1]
    print((x, y))
    pygame.draw.circle(surface = screen, color = 'red', center = (x, y), radius = 5)
    
  pygame.display.flip()
  
pygame.quit()