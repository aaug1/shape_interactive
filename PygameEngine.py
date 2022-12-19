import pygame
from Shape import Shape
import math


class PygameEngine:
    def __init__(
        self,
        WIDTH: int,
        HEIGHT: int,
        fps: int,
        caption: str,
        points: list,
        faces: list,
        shape_scale: float,
        colors: list,
        is_wireframe: bool
    ):
        pygame.init()
        pygame.display.set_caption(caption)
        self.fps = fps
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.width = WIDTH
        self.height = HEIGHT
        self.points = points
        self.faces = faces
        self.shape_scale = shape_scale
        self.shape = Shape(points, faces, self.screen, shape_scale)
        self.colors = colors
        self.is_wireframe = is_wireframe

    def play_animation(self):
        run = True
        mouse_press = False
        while run:
            self.screen.fill("white")
            self.timer.tick(self.fps)

            # Listen to quit signal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and (
                    event.key == pygame.K_q or event.key == pygame.K_ESCAPE
                ):
                    run = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.shape = Shape(
                        self.points, self.faces, self.screen, self.shape_scale
                    )
                x_translate, y_translate = 0,0
                speed = 0.5
                if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_LEFT:
                      x_translate = -1 * speed
                  if event.key == pygame.K_RIGHT:
                      x_translate = 1 * speed
                  if event.key == pygame.K_UP:
                      y_translate = 1 * speed
                  if event.key == pygame.K_DOWN:
                      y_translate = -1 * speed

            # Recognize user mouse interaction for rotation
            x_rotate, y_rotate = 0, 0
            if pygame.mouse.get_pressed()[0] == True:
                if mouse_press == False:
                    pygame.mouse.get_rel()  # starts the shift from cur location
                    mouse_press = True
                y_rotate, x_rotate = pygame.mouse.get_rel()
                x_rotate = (x_rotate) / self.width * 2
                y_rotate = (y_rotate) / self.height * 2
            else:
                mouse_press = False

            # Render the shape
            self.shape.translate_object(x_translate, y_translate)
            self.shape.rotate_object(x_rotate, y_rotate)
            
            if len(self.colors) > 0 and self.colors[0]:
                self.shape.draw_points(self.colors[0])      

            if self.is_wireframe == True:
              if len(self.colors) > 1 and self.colors[1]:
                self.shape.draw_edges(self.colors[1])
              else:
                self.shape.draw_edges()
            else:
              if len(self.colors) > 1 and self.colors[1]:
                  self.shape.draw_faces(edges_color=self.colors[1])
              else:
                  self.shape.draw_faces(draw_edges=False)
            pygame.display.flip()
