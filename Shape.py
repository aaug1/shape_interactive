import pygame
import numpy as np
import math
from typing import Optional, Tuple


class Shape:
    """
    Creates a shape using 3D coordinates to be
    generated on the pygame window
    """

    def __init__(self, points: list, faces: list, screen: pygame.Surface, scale: int):

        self.__coordinates = {}
        for point in points:
            point[3] = -point[3]
            self.add_point(point)

        self.__faces = []
        for face in faces:
            self.add_face(face)

        self.screen = screen
        self.scale = scale

        # Set up 3D to 2D projection matrix, +z to user
        self.__projection_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        self.x_translate = 0
        self.y_translate = 0

    def add_point(self, point: Tuple[int, float, float, float]):
        """Add a point to the shape object"""
        point_id = point[0]
        self.__coordinates[point_id] = point[1:]
        self.__coordinates[point_id][1] = -self.__coordinates[point_id][1]

    def add_face(self, face_point_ids: Tuple[float, float, float]):
        """Add a face to the shape object; corrects winding order to be clockwise"""
        self.__faces.append(face_point_ids)

    def draw_edges(
        self, color: Tuple[float, float, float, Optional[float]] = (0, 0, 0), width=1
    ):
        """Draws the edges (connecting lines btw points) based on input file"""
        for face in self.__faces:
            # Convert points to 2D
            points_2D = []
            for point in face:
                point_2D = self.__convert_to_2D(self.__coordinates[point])
                points_2D.append(point_2D)
            for i in range(3):
                pygame.draw.line(
                    self.screen,
                    color,
                    points_2D[i],
                    points_2D[(i + 1) % 3],
                    width=width,
                )

    def draw_faces(
        self,
        draw_edges: bool = True,
        edges_color: Tuple[float, float, float, Optional[float]] = (0, 0, 0, 255),
    ):
        """Draws the faces based on input file"""
        # Get all of the faces
        for face in self.__faces:
            # Convert to 2D
            points_2D = []
            points_3D = []

            # Get all point coordinates in the face
            for point in face:
                point_2D = self.__convert_to_2D(self.__coordinates[point])
                point_3D = self.__coordinates[point]
                points_2D.append(point_2D)
                points_3D.append(point_3D)
            blue_color = self.__get_color(points_3D)

            # Only display if visible from viewport
            if blue_color >= 95:
                point1, point2, point3 = points_2D[0], points_2D[1], points_2D[2]
                pygame.draw.polygon(
                    self.screen, (0, 0, blue_color, 255), [point1, point2, point3]
                )
                if draw_edges == True:
                    pygame.draw.polygon(
                        self.screen, edges_color, [point1, point2, point3], width=2
                    )

    def draw_points(
        self, color: Tuple[float, float, float, Optional[float]] = (0, 0, 0, 0)
    ):
        """Draws the points based on input file"""
        for point_id, point in self.__coordinates.items():
            x, y = self.__convert_to_2D(point)
            pygame.draw.circle(
                surface=self.screen, color=color, center=(x, y), radius=5
            )

    def rotate_object(self, x_rotate: float, y_rotate: float):
        """Rotates an object about x and y axes"""

        # Rotation matrices, where matrix mult applies specified x or y rotations
        rotation_matrix_x = np.array(
            [
                [1, 0, 0],
                [0, math.cos(x_rotate), -math.sin(x_rotate)],
                [0, math.sin(x_rotate), math.cos(x_rotate)],
            ]
        )
        rotation_matrix_y = np.array(
            [
                [math.cos(y_rotate), 0, math.sin(y_rotate)],
                [0, 1, 0],
                [-math.sin(y_rotate), 0, math.cos(y_rotate)],
            ]
        )

        # Rotate the shape
        for point_id, point in self.__coordinates.items():
            rotated_point = np.dot(point, rotation_matrix_x)
            rotated_point = np.dot(rotated_point, rotation_matrix_y)
            self.__coordinates[point_id] = rotated_point
            
    def translate_object(self, x_translate: float, y_translate: float):
      """Translates an object x and y distances"""
      self.x_translate += x_translate
      self.y_translate += y_translate
      for point_id, point in self.__coordinates.items():
        translated_point = np.add(point, [x_translate, 0, 0])
        translated_point = np.add(translated_point, [0, y_translate, 0])
        self.__coordinates[point_id] = translated_point
        
    def __get_color(self, face: Tuple[float, float, float]):
        """
        Calculates the blue color value in range (0,0,95) to (0,0,255)
        (equivalent to #00005F to #0000FF)
        """
        point1, point2, point3 = face
        print(self.x_translate)
        print(self.__coordinates[1])
        point1 = point1 - [self.x_translate, self.y_translate, 0]
        point2 = point2 - [self.x_translate, self.y_translate, 0]
        point3 = point3 - [self.x_translate, self.y_translate, 0]

        ## Back-culling to remove faces behind other faces
        vec_1 = np.subtract(point2 ,point1)
        vec_2 = np.subtract(point3, point1)
        ortho = np.cross(vec_1[0:2], vec_2[0:2])
        if ortho < 0:  # is CCW, so switch to CW
            point2, point3 = point3, point2

        # Get the (out-facing) normal vector orthogonal to the face
        
        vec_1 = point2 - point1
        vec_2 = point3 - point1
        ortho = np.cross(vec_1, vec_2)
        if (
            np.dot(point1, ortho) >= 0.1
        ):  # face normal and viewing vector are same direction
            return 0

        # Calculates angle between xy-plane and orthogonal vector
        angle = abs(
            math.asin(
                (ortho[2]) / (np.sqrt(ortho[0] ** 2 + ortho[1] ** 2 + ortho[2] ** 2))
            )
        )
        # Range of color specified is rgb 95 to 255. Range of angle is 0 to pi/2
        OldRange = math.pi / 2
        NewRange = 255 - 95
        blue_color = (((angle) * NewRange) / OldRange) + 95
        return blue_color

    def __convert_to_2D(self, point: Tuple[float, float, float]):
        """Convert an object's coords into pygame coordinates
        (origin at center of pygame coords; project to screen space)"""
        WIDTH, HEIGHT = self.screen.get_size()
        coords = np.dot(self.__projection_matrix, point)
        new_point = (
            (coords[0] * self.scale + WIDTH / 2),
            (-coords[1] * self.scale + HEIGHT / 2),
        )
        return new_point
