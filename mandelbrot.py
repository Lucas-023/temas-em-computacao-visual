from src.base import Shape

class Mandelbrot(Shape):
    def __init__(self, max_iterations=100):
        super().__init__("mandelbrot")
        self.max_iterations = max_iterations
    
    def in_out(self, point):
        """
        Verifica se um ponto (cx, cy) pertence ao conjunto de Mandelbrot.
        O conjunto de Mandelbrot consiste em pontos c para os quais a sequência
        z_{n+1} = z_n^2 + c (começando com z_0 = 0) não diverge.
        """
        cx, cy = point
        zx, zy = 0.0, 0.0
        
        for i in range(self.max_iterations):
            # Calcula z^2 + c
            zx_new = zx * zx - zy * zy + cx
            zy_new = 2.0 * zx * zy + cy
            
            zx, zy = zx_new, zy_new
            
            # Se |z| > 2, o ponto diverge (não está no conjunto)
            if zx * zx + zy * zy > 4.0:
                return False
        
        # Se não divergiu após max_iterations, consideramos que está no conjunto
        return True