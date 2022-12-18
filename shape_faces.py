import pygame
from InputHandler import InputHandler
from PygameEngine import PygameEngine


# Setup the window
if __name__ == "__main__":
    WIDTH, HEIGHT = 500, 500
    fps = 60
    shape_scale = 50
    caption = "Render 3D to 2D Shape"
    file_repo = "./object_files/"
    input_handler = InputHandler()

    # Read in file
    filename = input("Please type in the name of the file: ")
    shape_points, shape_faces = input_handler.read_file(file_repo, filename)

    # Check to ensure color is of correct form
    colors = []
    colors.append(input("What color do you want the points to be (R, G, B, A)? "))
    colors.append(input("What color do you want the edges to be (R, G, B, A)? "))

    for i, rgba in enumerate(colors):
        colors[i] = input_handler.check_color(rgba)

    game = PygameEngine(
        WIDTH, HEIGHT, fps, caption, shape_points, shape_faces, shape_scale, colors, False
    )
    game.play_animation()
    pygame.quit()
