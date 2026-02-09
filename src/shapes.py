from .base import Shape
import math
class Circle(Shape):
    def __init__(self, center, radius):
        super().__init__("circle")
        self.center = center
        self.radius = radius

    def in_out(self, point):
        dx = point[0] - self.center[0]
        dy = point[1] - self.center[1]
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

class Triangle(Shape):
    def __init__(self, vertex1, vertex2, vertex3):
        super().__init__("triangle")
        self.v1 = vertex1
        self.v2 = vertex2
        self.v3 = vertex3

    def in_out(self, point):
        def dist(p1, p2):
            return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        #calcula a área usando a fórmula de Heron
        def heron_area(a, b, c):
            s = (a + b + c) / 2.0
            
            return math.sqrt(max(0, s * (s - a) * (s - b) * (s - c)))

        #lados do triângulo principal
        side_ab = dist(self.v1, self.v2)
        side_bc = dist(self.v2, self.v3)
        side_ca = dist(self.v3, self.v1)

        #distâncias do ponto P aos vértices
        dist_pa = dist(point, self.v1)
        dist_pb = dist(point, self.v2)
        dist_pc = dist(point, self.v3)

        area_total = heron_area(side_ab, side_bc, side_ca)
        
        area_pab = heron_area(side_ab, dist_pa, dist_pb)
        area_pbc = heron_area(side_bc, dist_pb, dist_pc)
        area_pca = heron_area(side_ca, dist_pc, dist_pa)

        #verificando se a soma das áreas dos triângulos formados pelo ponto e os lados do triângulo é igual à área do triângulo original
        epsilon = 1e-5 
        return abs(area_total - (area_pab + area_pbc + area_pca)) < epsilon

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0