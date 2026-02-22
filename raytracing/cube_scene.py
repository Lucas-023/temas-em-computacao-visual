import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV, Cube, Cylinder 
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterial, TranslucidMaterial, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Geometric Scene")

        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 10 
        
        self.camera = Camera(
            eye=Vector3D(1, 0, 0.4) * 12.0,
            look_at=Vector3D(0, 0, 1.0),
            up=Vector3D(0, 0, 1),
            fov=35,
            img_width=800,
            img_height=500
        )

        self.lights = [
            AreaLight(
                position=Vector3D(5, 5, 10),
                look_at=Vector3D(0, 0, 0),
                up=Vector3D(0, 0, 1),
                width=4,
                height=4,
                color=Color(1, 1, 1),
                intensity=1.8
            )
        ]

        red_material = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0.5, 0, 0),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        self.add(
            Ball(center=Vector3D(0, -1.5, 1.2), radius=1.0), 
            red_material
        )

        cube_material = SimpleMaterial(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.8, 0.6, 0.2), 
            specular_coefficient=0.3,
            specular_color=Color(1, 1, 1),
            specular_shininess=16
        )
        
        self.add(
            Cube(center=Vector3D(0, 2.0, 0.9), radius=0.9),
            cube_material
        )

        cylinder_material = SimpleMaterial(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.6,
            diffuse_color=Color(0.1, 0.6, 0.2), # Verde
            specular_coefficient=0.4,
            specular_color=Color(1, 1, 1),
            specular_shininess=64
        )

        axis_vector = Vector3D(-1, 0, 1).normalize()
        
        self.add(
            Cylinder(
                center=Vector3D(-3, 0, 2), 
                axis=axis_vector,
                radius=0.6,
                height=4.0
            ),
            cylinder_material
        )
        gray_material = CheckerboardMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0), 
                normal=Vector3D(0, 0, 1), 
                forward_direction=Vector3D(1, 0, 0)
            ), 
            gray_material
        )