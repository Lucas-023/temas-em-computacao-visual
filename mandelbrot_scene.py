from src.base import BaseScene, Color
from mandelbrot import Mandelbrot

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mandelbrot Fractal")
        
        # Cor de fundo (preto)
        self.background = Color(0, 0, 0)
        
        # Adicionar o conjunto de Mandelbrot com cor branca
        # Você pode ajustar max_iterations para mais ou menos detalhes
        # Valores maiores = mais precisão, mas renderização mais lenta
        mandelbrot_set = Mandelbrot(max_iterations=100)
        mandelbrot_color = Color(1, 1, 1)  # Branco
        
        self.add(mandelbrot_set, mandelbrot_color)