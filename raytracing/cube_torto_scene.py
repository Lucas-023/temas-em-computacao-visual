import numpy as np
from src.base import BaseScene, Color
from src.vector3d import Vector3D
from src.camera import Camera
from src.light import AreaLight
from src.shapes import Cube, ObjectTransform, PlaneUV
from src.materials import SimpleMaterial, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Cena - Cubo Voador e Torto")

        self.background = Color(0.1, 0.1, 0.15)
        self.ambient_light = Color(0.2, 0.2, 0.2)

        self.camera = Camera(
            eye=Vector3D(0, 1.5, 8),
            look_at=Vector3D(0, 3, 0),
            up=Vector3D(0, 1, 0),
            fov=60,
            img_width=400, img_height=300
        )

        self.lights = [
            AreaLight(Vector3D(5, 8, 5), Vector3D(0, 3, 0), Vector3D(1, 0, 0), 2.0, 2.0, Color(1.0, 0.9, 0.8), 2.0),
            AreaLight(Vector3D(-2, -2, 4), Vector3D(0, 3, 0), Vector3D(0, 1, 0), 1.0, 1.0, Color(0.4, 0.4, 0.6), 1.0)
        ]

        
        mat_cube = SimpleMaterial(0.1, 0.8, Color(0.2, 0.4, 0.8), 0.5, Color(1, 1, 1), 64)
        
        mat_floor = CheckerboardMaterial(0.2, 0.8, 2.0, Color(0.5, 0.5, 0.5), Color(0.3, 0.3, 0.3))

        base_cube = Cube(Vector3D(0, 0, 0), 1.0)
        angle_x = np.radians(-30) 
        c_x, s_x = np.cos(angle_x), np.sin(angle_x)
        rot_x_matrix = np.array([
            [1, 0,    0,   0],
            [0, c_x, -s_x, 0],
            [0, s_x,  c_x, 0],
            [0, 0,    0,   1]
        ])

        angle_y = np.radians(45)
        c_y, s_y = np.cos(angle_y), np.sin(angle_y)
        rot_y_matrix = np.array([
            [ c_y, 0, s_y, 0],
            [ 0,   1, 0,   0],
            [-s_y, 0, c_y, 0],
            [ 0,   0, 0,   1]
        ])

        translation_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 3],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        final_matrix = translation_matrix @ rot_y_matrix @ rot_x_matrix

        self.add(ObjectTransform(base_cube, final_matrix), mat_cube)
        
        floor = PlaneUV(Vector3D(0, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1))
        self.add(floor, mat_floor)