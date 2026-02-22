import math
import numpy as np
from src.base import BaseScene, Color
from src.vector3d import Vector3D
from src.camera import Camera
from src.light import AreaLight
from src.shapes import Ball, Cube, Paraboloid, PlaneUV, ObjectTransform, Cylinder, DoubleSidedParaboloid
from src.materials import SimpleMaterial, CheckerboardMaterial

class Scene(BaseScene): 
    def __init__(self):
        super().__init__("Cena Final - Relatorio Transform")
        
        self.background = Color(0.1, 0.1, 0.1)
        self.ambient_light = Color(0.3, 0.3, 0.3)
        
        self.camera = Camera(
            eye=Vector3D(0, 8, 20),
            look_at=Vector3D(0, 1, 0),
            up=Vector3D(0, 1, 0),
            fov=45,
            img_width=800, img_height=800 
        )

        self.lights = [
            AreaLight(Vector3D(0, 15, 0), Vector3D(0, 0, 0), Vector3D(1, 0, 0), 0.5, 0.5, Color(1,1,1), 1.5),
            AreaLight(Vector3D(10, 10, 10), Vector3D(0, 0, 0), Vector3D(0, 1, 0), 0.5, 0.5, Color(0.8, 0.8, 1.0), 0.8)
        ]

        # Materiais
        mat_red    = SimpleMaterial(0.1, 0.8, Color(0.8, 0.1, 0.1), 0.5, Color(1,1,1), 64)
        mat_green  = SimpleMaterial(0.1, 0.8, Color(0.1, 0.8, 0.1), 0.5, Color(1,1,1), 64)
        mat_blue   = SimpleMaterial(0.1, 0.8, Color(0.1, 0.1, 0.8), 0.5, Color(1,1,1), 64)
        mat_white  = SimpleMaterial(0.1, 0.8, Color(0.9, 0.9, 0.9), 0.5, Color(1,1,1), 64) 
        mat_yellow = SimpleMaterial(0.1, 0.8, Color(0.8, 0.8, 0.2), 0.5, Color(1,1,1), 64)
        mat_floor  = CheckerboardMaterial(0.5, 0.6, 2.0, Color(0.8,0.8,0.8), Color(0.2,0.2,0.2))

        sphere_mat = np.diag([1.5, 0.5, 1.0, 1.0]) 
        sphere_mat[0, 3] = -6 
        sphere_mat[1, 3] = 1  
        self.add(ObjectTransform(Ball(Vector3D(0, 0, 0), 1.5), sphere_mat), mat_red)

        base_paraboloid = DoubleSidedParaboloid(y_min=0, y_max=2.0, material=mat_green)
        parab_mat = np.diag([2.0, 1.0, 2.0, 1.0]) 
        parab_mat[0, 3] = 0 
        self.add(ObjectTransform(base_paraboloid, parab_mat), mat_green)

        angle = math.radians(45)
        c, s = math.cos(angle), math.sin(angle)
        cube_mat = np.array([
            [ c, -s,  0,  6.0],
            [ s,  c,  0,  2.0],
            [ 0,  0,  1,  0.0],
            [ 0,  0,  0,  1.0]
        ])
        self.add(ObjectTransform(Cube(Vector3D(0, 0, 0), 1.2), cube_mat), mat_blue)

        angle_cyl = math.radians(30)
        c2, s2 = math.cos(angle_cyl), math.sin(angle_cyl)
        cyl_mat = np.array([
            [1,  0,   0,  -2.0],
            [0, c2, -s2,   1.0],
            [0, s2,  c2,   6.0],
            [0,  0,   0,   1.0]
        ])
        base_cyl = Cylinder(Vector3D(0, 0, 0), Vector3D(0, 1, 0), 0.5, 3.0)
        self.add(ObjectTransform(base_cyl, cyl_mat), mat_yellow)
        self.add(Ball(Vector3D(3, 1.5, 6), 1.5), mat_white)

        self.add(PlaneUV(Vector3D(0, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)), mat_floor)