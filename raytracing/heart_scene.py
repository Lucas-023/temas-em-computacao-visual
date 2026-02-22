import math
import numpy as np
from src.base import BaseScene, Color
from src.materials import SimpleMaterial
from src.vector3d import Vector3D
from src.camera import Camera
from src.light import PointLight
from src.shapes import ImplicitSurface, ObjectTransform, HeartSurface

def Scene():
    scene = BaseScene("Contorno de Coracao com Matrizes")
    
    NUM_HEARTS = 50 
    SPREAD_SCALE = 0.25 
    SMALL_HEART_SCALE = 0.4 
    
    scene.background_color = Color(0.1, 0.1, 0.15) 
    scene.ambient_light = Color(0.3, 0.3, 0.3)
    scene.lights = [] 

    scene.camera = Camera(
        eye=Vector3D(0, 1.0, 12), 
        look_at=Vector3D(0, 1.0, 0),
        up=Vector3D(0, 1, 0),
        fov=45,
        img_width=200,
        img_height=200 
    )

    scene.lights.append(PointLight(Vector3D(5, 5, 10), Color(0.9, 0.9, 0.9))) 
    scene.lights.append(PointLight(Vector3D(-5, -2, 10), Color(0.3, 0.2, 0.2))) 

    red_mat = SimpleMaterial(0.1, 0.8, Color(0.9, 0.05, 0.05), 0.7, Color(1, 0.8, 0.8))

    print(f"A desenhar o contorno com {NUM_HEARTS} corações vermelhos via ObjectTransform...")

    pure_heart = HeartSurface(red_mat)

    for i in range(NUM_HEARTS):
        t = (i / NUM_HEARTS) * 2 * math.pi
        
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        
        final_x = x * SPREAD_SCALE
        final_y = (y * SPREAD_SCALE) + 1.0 
        final_z = 0.0

        s = SMALL_HEART_SCALE
        transform_matrix = np.array([
            [s,   0.0, 0.0, final_x],
            [0.0, s,   0.0, final_y],
            [0.0, 0.0, s,   final_z],
            [0.0, 0.0, 0.0, 1.0    ]
        ])

        transformed_heart = ObjectTransform(pure_heart, transform_matrix)
        
        scene.add(transformed_heart, red_mat)

    print("Contorno montado! A iniciar renderização...")
    return scene