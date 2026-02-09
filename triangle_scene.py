from src.base import BaseScene, Color
from src.shapes import Triangle

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Triangle Scene")
        self.background = Color(1, 1, 1)

        # Distância: 0.01
                                # Distância: 0.1
                ## Distância: 0.005 (Meio termo entre o micro e o visível)  
        self.add(Triangle((-0.6, -0.5), (0.0, -0.5), (-0.2, 0.5)), Color(1.0, 0.0, 0.0)) 
        self.add(Triangle((0.005, -0.5), (-0.195, 0.5), (0.605, 0.7)), Color(0.0, 0.0, 1.0))