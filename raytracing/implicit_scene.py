import math
import numpy as np
from src.base import BaseScene, Color
from src.vector3d import Vector3D
from src.camera import Camera
from src.light import AreaLight
from src.materials import SimpleMaterial, CheckerboardMaterial
from src.shapes import PlaneUV, HeartSurface, MitchelSurface, ObjectTransform

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Cena Funcoes Implicitas - Coracao de Frente")
        
        self.background = Color(0.05, 0.05, 0.08)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        
        self.camera = Camera(
            eye=Vector3D(-0.5, 2.5, 8.0),
            look_at=Vector3D(-0.5, 0.0, 0.0),
            up=Vector3D(0, 1, 0),
            fov=55,
            img_width=600, img_height=600 
        )
        
        self.lights = [
            AreaLight(Vector3D(-5, 5, 3), Vector3D(-2.5, 0, 0), Vector3D(0, 1, 0), 1.0, 1.0, Color(0.7, 0.8, 1.0), 1.2),
            AreaLight(Vector3D(5, 5, 3), Vector3D(1.5, 0, 0), Vector3D(0, 1, 0), 1.0, 1.0, Color(1.0, 0.8, 0.8), 1.0)
        ]
        
        mat_heart = SimpleMaterial(
            ambient_coefficient=0.1, diffuse_coefficient=0.7, diffuse_color=Color(0.8, 0.05, 0.1),
            specular_coefficient=0.8, specular_color=Color(1, 1, 1), specular_shininess=64
        )
        
        mat_mitchel = SimpleMaterial(
            ambient_coefficient=0.1, diffuse_coefficient=0.6, diffuse_color=Color(0.1, 0.5, 0.8),
            specular_coefficient=0.9, specular_color=Color(1, 1, 1), specular_shininess=128
        )
        
        mat_floor = CheckerboardMaterial(
            ambient_coefficient=1.0, diffuse_coefficient=0.5, square_size=1.0, 
            white_color=Color(0.25, 0.25, 0.25), black_color=Color(0.1, 0.1, 0.1)
        )
        
        trans_heart = np.array([
            [1, 0, 0, 1.5],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        heart_transform = trans_heart 
        
        self.add(ObjectTransform(HeartSurface(mat_heart), heart_transform), mat_heart)
        
        angle_mx = math.radians(15)
        cmx, smx = math.cos(angle_mx), math.sin(angle_mx)
        mitchel_transform = np.array([[1, 0, 0, 0], [0, cmx, -smx, 0], [0, smx, cmx, 0], [0, 0, 0, 1]])
        
        self.add(ObjectTransform(MitchelSurface(mat_mitchel), mitchel_transform), mat_mitchel)
        
        self.add(PlaneUV(Vector3D(0, -1.5, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)), mat_floor)