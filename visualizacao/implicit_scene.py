from src.shapes import ImplicitFunction
from src.base import BaseScene, Color

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Implicit Function Scene")
        self.background = Color(1, 1, 1)

        # Definindo os termos da função implícita
        def implicit_func(point):
            x, y = point
            
            term0 = 0.004
            term1 = 0.110 * x
            term2 = -0.177 * y            
            term3 = -0.174 * (x ** 2)
            term4 = 0.224 * x * y
            term5 = -0.303 * (y ** 2)            
            term6 = -0.168 * (x ** 3)
            term7 = 0.327 * (x ** 2) * y
            term8 = -0.087 * x * (y ** 2)
            term9 = -0.013 * (y ** 3)
            term10 = 0.235 * (x ** 4)
            term11 = -0.667 * (x ** 3) * y
            term12 = 0.745 * (x ** 2) * (y ** 2)
            term13 = -0.029 * x * (y ** 3)
            term14 = 0.072 * (y ** 4)
            
            return (term0 + term1 + term2 + term3 + term4 + term5 + 
                    term6 + term7 + term8 + term9 + term10 + term11 + 
                    term12 + term13 + term14)

        self.add(ImplicitFunction(implicit_func), Color(0.2, 0.6, 0.9))  # Light blue
