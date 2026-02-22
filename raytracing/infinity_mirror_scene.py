from src.base import BaseScene, Color
from src.vector3d import Vector3D
from src.camera import Camera
from src.light import AreaLight
from src.shapes import PlaneUV, Ball
from src.materials import SimpleMaterial, CheckerboardMaterial, MirrorMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Cena - Corredor Infinito Desbloqueado")

        self.max_depth = 15

        self.background = Color(0.02, 0.02, 0.02)
        self.ambient_light = Color(0.1, 0.1, 0.1)

        self.camera = Camera(
            eye=Vector3D(2.5, 2.5, 2),       
            look_at=Vector3D(-0.5, 1.0, -10),   
            up=Vector3D(0, 1, 0),
            fov=60,
            img_width=400, img_height=300
        )

        self.lights = [
            AreaLight(Vector3D(0, 10, 0), Vector3D(0, 0, 0), Vector3D(1, 0, 0), 2.0, 2.0, Color(1, 1, 1), 2.0),
        ]

        mat_mirror = MirrorMaterial(reflection_coefficient=1.0)
        mat_floor = CheckerboardMaterial(0.2, 0.5, 2.0, Color(0.9, 0.9, 0.9), Color(0.1, 0.1, 0.1))
        mat_red_shiny = SimpleMaterial(0.1, 0.8, Color(0.9, 0.1, 0.1), 0.7, Color(1, 1, 1), 64)

        mirror_front = PlaneUV(Vector3D(0, 0, -10), Vector3D(0, 0, 1), Vector3D(0, 1, 0))
        self.add(mirror_front, mat_mirror)

        mirror_back = PlaneUV(Vector3D(0, 0, 10), Vector3D(0, 0, -1), Vector3D(0, 1, 0))
        self.add(mirror_back, mat_mirror)

        floor = PlaneUV(Vector3D(0, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1))
        self.add(floor, mat_floor)

        ball = Ball(Vector3D(-1.0, 1.5, -4), 1.5)
        self.add(ball, mat_red_shiny)