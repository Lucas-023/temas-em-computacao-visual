import math
import numpy as np
from src.base import BaseScene, Color
from src.vector3d import Vector3D
from src.camera import Camera
from src.light import AreaLight
from src.materials import SimpleMaterial
from src.shapes import PlaneUV, ImplicitSurface, ObjectTransform, Cylinder

# --- A CLASSE DO GIRASSOL CONTINUA IGUAL ---
class SunflowerSurface(ImplicitSurface):
    def __init__(self, material):
        bbox_min = Vector3D(-2.5, -0.5, -2.5)
        bbox_max = Vector3D(2.5, 0.5, 2.5)
        super().__init__(material, bbox_min, bbox_max, num_steps=200)

    def function(self, x, y, z):
        r = math.sqrt(x**2 + z**2)
        theta = math.atan2(z, x)
        
        miolo = x**2 + (2.5 * (y - 0.1))**2 + z**2 - 0.9**2
        miolo += 0.04 * math.sin(40 * x) * math.sin(40 * z)
        
        raio_petala = 0.8 + 1.4 * abs(math.cos(7 * theta))
        petalas = r**2 + (12.0 * y)**2 - raio_petala**2
        
        return min(miolo, petalas)

# --- A NOVA CENA DO JARDIM ---
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Jardim de Girassois")
        
        # Céu azul claro
        self.background = Color(0.4, 0.7, 1.0)
        self.ambient_light = Color(0.3, 0.3, 0.3)
        
        # Câmera mais alta e mais afastada para ver todo o jardim
        self.camera = Camera(
            eye=Vector3D(0, 6.0, 18.0),
            look_at=Vector3D(0, 3.0, 0.0),
            up=Vector3D(0, 1, 0),
            fov=45,
            img_width=800, img_height=600 
        )
        
        # Luz do sol mais forte para iluminar uma área maior
        self.lights = [
            AreaLight(Vector3D(10, 15, 10), Vector3D(0, 0, 0), Vector3D(0, 1, 0), 4.0, 4.0, Color(1.0, 0.95, 0.9), 2.0),
            AreaLight(Vector3D(-8, 5, 5), Vector3D(0, 0, 0), Vector3D(0, 1, 0), 2.0, 2.0, Color(0.5, 0.5, 0.6), 0.7)
        ]
        
        # --- MATERIAIS ---
        mat_flor = SimpleMaterial(
            ambient_coefficient=0.2, diffuse_coefficient=0.8, diffuse_color=Color(0.9, 0.7, 0.1), 
            specular_coefficient=0.2, specular_color=Color(1, 1, 1), specular_shininess=16 
        )
        
        mat_caule = SimpleMaterial(
            ambient_coefficient=0.1, diffuse_coefficient=0.7, diffuse_color=Color(0.15, 0.5, 0.15), 
            specular_coefficient=0.1, specular_color=Color(1, 1, 1), specular_shininess=8
        )
        
        # Novo material para o chão: Grama Verde
        mat_grama = SimpleMaterial(
            ambient_coefficient=0.2, diffuse_coefficient=0.8, diffuse_color=Color(0.2, 0.55, 0.2), 
            specular_coefficient=0.05, specular_color=Color(1, 1, 1), specular_shininess=4
        )

        # --- OBJETOS ---
        
        # 1. O CHÃO (Grama)
        self.add(PlaneUV(Vector3D(0, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)), mat_grama)

        # 2. PLANTANDO OS GIRASSÓIS
        # Rotação base para deixar o girassol em pé (calculada uma vez só fora do loop)
        angle_x = math.radians(-90)
        cx, sx = math.cos(angle_x), math.sin(angle_x)
        rot_x = np.array([[1, 0, 0, 0], [0, cx, -sx, 0], [0, sx, cx, 0], [0, 0, 0, 1]])
        
        # Lista de posições (X, Z) no chão onde queremos plantar cada flor
        posicoes_flores = [
            (0.0, 0.0),     # Centro
            (3.5, -2.5),    # Direita e para trás
            (-4.0, -3.0),   # Esquerda e para trás
            (2.5, 3.5),     # Direita e para frente
            (-2.5, 2.0),    # Esquerda e para frente
            (6.5, -1.0),    # Bem à direita
            (-6.0, 0.5)     # Bem à esquerda
        ]
        
        # Loop que cria uma cópia da flor e do caule para cada posição
        for pos_x, pos_z in posicoes_flores:
            
            # --- A Flor ---
            girassol_shape = SunflowerSurface(mat_flor)
            # Translada a flor para a posição X, Z atual, mantendo a altura Y=3.5
            trans_flor = np.array([[1, 0, 0, pos_x], [0, 1, 0, 3.5], [0, 0, 1, pos_z], [0, 0, 0, 1]])
            girassol_transform = trans_flor @ rot_x
            self.add(ObjectTransform(girassol_shape, girassol_transform), mat_flor)
            
            # --- O Caule ---
            # A base do caule acompanha a posição X, Z da flor.
            # O recuo de -0.15 no Z é mantido para ficar atrás do miolo.
            p_base = Vector3D(pos_x, 0.0, pos_z - 0.15)
            direcao = Vector3D(0, 1, 0)
            raio = 0.15
            altura = 4.8  # Usando a altura que você validou!
            
            caule_shape = Cylinder(p_base, direcao, raio, altura)
            self.add(caule_shape, mat_caule)