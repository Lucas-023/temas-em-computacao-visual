import math
import random
from src.base import BaseScene, Color
from src.shapes import Ball
from src.materials import SimpleMaterial
from src.vector3d import Vector3D
from src.ray import Ray
from src.light import PointLight 

class CameraDoF:
    def __init__(self, eye, look_at, up, fov, img_width, img_height, lens_radius, focal_distance):
        self.eye = eye
        self.img_width = img_width
        self.img_height = img_height
        self.lens_radius = lens_radius
        self.focal_distance = focal_distance

        aspect_ratio = img_height / img_width
        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.w = (eye - look_at).normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    def _random_in_unit_disk(self):
        while True:
            p = Vector3D(random.uniform(-1, 1), random.uniform(-1, 1), 0)
            if p.dot(p) < 1.0:
                return p

    def ray(self, x, y):
        x_ndc = self.su * (x / self.img_width - 0.5)
        y_ndc = self.sv * (y / self.img_height - 0.5)
        
        pixel_dir = (self.u * x_ndc + self.v * y_ndc - self.w).normalize()
        focal_point = self.eye + (pixel_dir * self.focal_distance)

        sample = self._random_in_unit_disk() * self.lens_radius
        offset = self.u * sample.x + self.v * sample.y
        new_origin = self.eye + offset

        return Ray(new_origin, (focal_point - new_origin).normalize(), depth=0)

def Scene():
    LENS_RADIUS = 0.8     
    FOCAL_DISTANCE = 5.0  

    scene = BaseScene("Depth of Field Activity")
    
    scene.lights = [] 
    scene.ambient_light = Color(0.1, 0.1, 0.1)
    scene.background_color = Color(0.05, 0.05, 0.05) 

    scene.lights.append(PointLight(Vector3D(5, 5, 10), Color(1, 1, 1)))

    scene.camera = CameraDoF(
        eye=Vector3D(0, 0, 10),
        look_at=Vector3D(0, 0, 0),
        up=Vector3D(0, 1, 0),
        fov=40,
        img_width=800,
        img_height=600,
        lens_radius=LENS_RADIUS,
        focal_distance=FOCAL_DISTANCE
    )

    red = SimpleMaterial(0.2, 0.8, Color(1, 0, 0), 0.5, Color(1, 1, 1))
    green = SimpleMaterial(0.2, 0.8, Color(0, 1, 0), 0.5, Color(1, 1, 1))
    blue = SimpleMaterial(0.2, 0.8, Color(0, 0, 1), 0.5, Color(1, 1, 1))

    scene.add(Ball(Vector3D(-2.5, 0, 5), 1), red)    
    scene.add(Ball(Vector3D(0, 0, 0), 1), green)     
    scene.add(Ball(Vector3D(2.5, 0, -5), 1), blue)   

    return scene