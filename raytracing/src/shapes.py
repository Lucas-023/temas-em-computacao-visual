from src.vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon
import math
import numpy as np
class Ball(Shape):
    def __init__(self, center, radius):
        super().__init__("ball")
        self.center = center
        self.radius = radius

    def hit(self, ray):
        # Ray-sphere intersection
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return HitRecord(False, float('inf'), None, None)
        else:
            hit, point, normal = False, None, None
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t > CastEpsilon:
                hit = True
                point = ray.point_at_parameter(t)
                normal = (point - self.center).normalize()
            else:
                t = (-b + discriminant**0.5) / (2.0 * a)
                if t > CastEpsilon:
                    hit = True
                    point = ray.point_at_parameter(t)
                    normal = (point - self.center).normalize()

            return HitRecord(hit, t, point, normal)

class Plane(Shape):
    def __init__(self, point, normal):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                return HitRecord(True, t, point, self.normal)
        return HitRecord(False, float('inf'), None, None)

class PlaneUV(Shape):
    def __init__(self, point, normal, forward_direction):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()
        self.forward_direction = forward_direction.normalize()
        # compute right direction
        self.right_direction = self.normal.cross(self.forward_direction).normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                # Calculate UV coordinates
                vec = point - self.point
                u = vec.dot(self.right_direction)
                v = vec.dot(self.forward_direction)
                uv = Vector3D(u, v, 0)
                return HitRecord(True, t, point, self.normal, uv=uv)
        return HitRecord(False, float('inf'), None, None)

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0
    
class Cube(Shape):
    def __init__(self, center, radius): # radius aqui age como "half_size"
        super().__init__("cube")
        self.center = center
        # Define os cantos min e max
        self.min_bound = center - Vector3D(radius, radius, radius)
        self.max_bound = center + Vector3D(radius, radius, radius)

    def hit(self, ray):
        t_min = 0.0
        t_max = float('inf')

        # Criamos listas auxiliares para poder acessar via índice [i]
        ray_origin = [ray.origin.x, ray.origin.y, ray.origin.z]
        ray_dir = [ray.direction.x, ray.direction.y, ray.direction.z]
        min_b = [self.min_bound.x, self.min_bound.y, self.min_bound.z]
        max_b = [self.max_bound.x, self.max_bound.y, self.max_bound.z]

        for i in range(3): # 0=x, 1=y, 2=z
            origin_i = ray_origin[i]
            direction_i = ray_dir[i]
            min_i = min_b[i]
            max_i = max_b[i]

            if abs(direction_i) < 1e-8:
                # Raio paralelo ao plano da laje
                if origin_i < min_i or origin_i > max_i:
                    return HitRecord(False)
            else:
                t0 = (min_i - origin_i) / direction_i
                t1 = (max_i - origin_i) / direction_i

                if t0 > t1:
                    t0, t1 = t1, t0
                
                t_min = max(t_min, t0)
                t_max = min(t_max, t1)

                if t_max <= t_min:
                    return HitRecord(False)

        # Verifica se o t final é válido
        t = t_min
        if t < CastEpsilon:
            t = t_max
            if t < CastEpsilon:
                return HitRecord(False)
            
        point = ray.point_at_parameter(t)
        normal = self._get_normal(point)
        
        return HitRecord(True, t, point, normal)
    
    def _get_normal(self, point):
        p = point - self.center
        # Recalcula o "radius" baseado nos bounds para garantir consistência
        radius = (self.max_bound.x - self.min_bound.x) / 2.0 
        bias = 1.0001 
        
        if abs(p.x) >= radius / bias:
            return Vector3D(1 if p.x > 0 else -1, 0, 0)
        elif abs(p.y) >= radius / bias:
            return Vector3D(0, 1 if p.y > 0 else -1, 0)
        else:
            return Vector3D(0, 0, 1 if p.z > 0 else -1)

class Cylinder(Shape):
    def __init__(self, center, axis, radius, height):
        super().__init__("cylinder")
        self.center = center
        self.axis = axis.normalize() 
        self.radius = radius
        self.height = height

    def hit(self, ray):
        oc = ray.origin - self.center

        rd_dot_axis = ray.direction.dot(self.axis)
        oc_dot_axis = oc.dot(self.axis)

        # Vetores perpendiculares (projetados no plano ortogonal ao eixo)
        rd_perp = ray.direction - self.axis * rd_dot_axis
        oc_perp = oc - self.axis * oc_dot_axis

        a = rd_perp.dot(rd_perp)
        b = 2.0 * rd_perp.dot(oc_perp)
        c = oc_perp.dot(oc_perp) - self.radius**2

        closest_t = float('inf')
        hit_record = HitRecord(False)
        found_hit = False

        # --- 1. Teste do Corpo (Cilindro Infinito recortado) ---
        if abs(a) > 1e-6:
            discriminant = b*b - 4*a*c
            if discriminant >= 0:
                sqrt_disc = math.sqrt(discriminant)
                t1 = (-b - sqrt_disc) / (2.0 * a)
                t2 = (-b + sqrt_disc) / (2.0 * a)

                for t in [t1, t2]:
                    if t > CastEpsilon and t < closest_t:
                        point = ray.point_at_parameter(t)
                        dist_along_axis = (point - self.center).dot(self.axis)

                        if -self.height/2.0 <= dist_along_axis <= self.height/2.0:
                            closest_t = t
                            axis_point = self.center + self.axis * dist_along_axis
                            normal = (point - axis_point).normalize()
                            hit_record = HitRecord(True, t, point, normal)
                            found_hit = True

        # --- 2. Teste das Tampas (Planos circulares) ---
        for sign in [1.0, -1.0]:
            cap_center = self.center + self.axis * (sign * self.height / 2.0)
            cap_normal = self.axis * sign 

            denom = ray.direction.dot(cap_normal)
            
            # Evita divisão por zero
            if abs(denom) > 1e-6:
                t_cap = (cap_center - ray.origin).dot(cap_normal) / denom
                
                if CastEpsilon < t_cap < closest_t:
                    p_cap = ray.point_at_parameter(t_cap)
                    
                    # Teste: O ponto está dentro do círculo da tampa?
                    v_to_p = p_cap - cap_center
                    if v_to_p.dot(v_to_p) <= self.radius**2:
                        closest_t = t_cap
                        hit_record = HitRecord(True, t_cap, p_cap, cap_normal)
                        found_hit = True

        return hit_record
    


def vec_to_np(v):
    return np.array([v.x, v.y, v.z])

def np_to_vec(n):
    return Vector3D(n[0], n[1], n[2])


class ObjectTransform(Shape):
    def __init__(self, shape, matrix_4x4):
        super().__init__("transformed_object")
        
        self.shape = shape
        if matrix_4x4.shape == (3, 3):
            self.matrix = np.eye(4)
            self.matrix[:3, :3] = matrix_4x4
        else:
            self.matrix = matrix_4x4
            
        self.material = getattr(shape, 'material', None)
        
        try:
            self.inverse = np.linalg.inv(self.matrix)
        except np.linalg.LinAlgError:
            self.inverse = np.eye(4)

        #para as normais, usamos a transposta da inversa (apenas a parte 3x3 superior)
        self.inv_transpose_3x3 = self.inverse[:3, :3].T

    def hit(self, ray):
        orig_4d = np.array([ray.origin.x, ray.origin.y, ray.origin.z, 1.0])
        dir_4d  = np.array([ray.direction.x, ray.direction.y, ray.direction.z, 0.0])

        orig_obj_4d = self.inverse @ orig_4d
        dir_obj_4d  = self.inverse @ dir_4d

        orig_obj = Vector3D(orig_obj_4d[0], orig_obj_4d[1], orig_obj_4d[2])
        dir_obj_raw = Vector3D(dir_obj_4d[0], dir_obj_4d[1], dir_obj_4d[2])
        
        dir_obj_len = dir_obj_raw.length()
        dir_obj = dir_obj_raw / dir_obj_len
        
        ray_obj = ray.__class__(origin=orig_obj, direction=dir_obj)

        rec = self.shape.hit(ray_obj)

        if not rec.hit:
            return rec

        point_obj_4d = np.array([rec.point.x, rec.point.y, rec.point.z, 1.0])
        point_world_4d = self.matrix @ point_obj_4d
        point_world = Vector3D(point_world_4d[0], point_world_4d[1], point_world_4d[2])

        normal_obj_np = np.array([rec.normal.x, rec.normal.y, rec.normal.z])
        normal_world_np = self.inv_transpose_3x3 @ normal_obj_np
        normal_world = Vector3D(normal_world_np[0], normal_world_np[1], normal_world_np[2]).normalize()

        dist_vec = point_world - ray.origin
        t_world = dist_vec.dot(ray.direction)

        final_material = self.material if self.material is not None else rec.material

        return HitRecord(True, t_world, point_world, normal_world, final_material, rec.uv)
class Paraboloid(Shape):
    def __init__(self, y_min, y_max, material):
        super().__init__("paraboloid")
        
        self.y_min = y_min
        self.y_max = y_max
        self.material = material

    def hit(self, ray):
        ox, oy, oz = ray.origin.x, ray.origin.y, ray.origin.z
        dx, dy, dz = ray.direction.x, ray.direction.y, ray.direction.z

        k = 1.0 
        
        a = k*(dx*dx + dz*dz)
        b = k*(2*ox*dx + 2*oz*dz) - dy
        c = k*(ox*ox + oz*oz) - oy

        if abs(a) < 1e-6: return HitRecord(False)

        delta = b*b - 4*a*c
        if delta < 0: return HitRecord(False)

        sqrt_delta = delta**0.5
        t1 = (-b - sqrt_delta) / (2*a)
        t2 = (-b + sqrt_delta) / (2*a)

        best_t = float('inf')
        hit_found = False

        for t in [t1, t2]:
            if t > CastEpsilon and t < best_t:
                p = ray.point_at_parameter(t)
                if self.y_min <= p.y <= self.y_max:
                    best_t = t
                    hit_found = True

        if hit_found:
            p = ray.point_at_parameter(best_t)
            normal = Vector3D(2*p.x, -1, 2*p.z).normalize()
            # Usa self.material
            return HitRecord(True, best_t, p, normal, self.material)
        
        return HitRecord(False)

class DoubleSidedParaboloid(Paraboloid):
    
    def hit(self, ray):
        # 1. Chama o cálculo original
        rec = super().hit(ray)
        
        if rec is not None and rec.normal is not None:
            try:
                if ray.direction.dot(rec.normal) > 0:
                    rec.normal = -rec.normal
            except:
                pass
                
        return rec
    
class NoHit:
    def __init__(self):
        self.hit = False
        self.material = None
        self.uv = (0,0)

class ImplicitSurface(Shape):
    def __init__(self, material, bbox_min, bbox_max, num_steps=100):
        try:
            super().__init__(material)
        except:
            super().__init__()
            
        self.material = material
        self.bbox_min = bbox_min
        self.bbox_max = bbox_max
        self.num_steps = num_steps

    def function(self, x, y, z):
        raise NotImplementedError("Subclasses devem implementar a função implícita")

    def get_normal(self, p):
        # Gradiente por Diferenças Finitas
        eps = 1e-4
        dx = self.function(p.x + eps, p.y, p.z) - self.function(p.x - eps, p.y, p.z)
        dy = self.function(p.x, p.y + eps, p.z) - self.function(p.x, p.y - eps, p.z)
        dz = self.function(p.x, p.y, p.z + eps) - self.function(p.x, p.y, p.z - eps)
        return Vector3D(dx, dy, dz).normalize()

    def intersect_box(self, ray):
        # Algoritmo AABB (Slab method)
        inv_dir_x = 1.0 / ray.direction.x if ray.direction.x != 0 else 1e30
        inv_dir_y = 1.0 / ray.direction.y if ray.direction.y != 0 else 1e30
        inv_dir_z = 1.0 / ray.direction.z if ray.direction.z != 0 else 1e30

        t1 = (self.bbox_min.x - ray.origin.x) * inv_dir_x
        t2 = (self.bbox_max.x - ray.origin.x) * inv_dir_x
        t3 = (self.bbox_min.y - ray.origin.y) * inv_dir_y
        t4 = (self.bbox_max.y - ray.origin.y) * inv_dir_y
        t5 = (self.bbox_min.z - ray.origin.z) * inv_dir_z
        t6 = (self.bbox_max.z - ray.origin.z) * inv_dir_z

        tmin = max(max(min(t1, t2), min(t3, t4)), min(t5, t6))
        tmax = min(min(max(t1, t2), max(t3, t4)), max(t5, t6))

        if tmax < 0 or tmin > tmax:
            return None, None
            
        return tmin, tmax

    def hit(self, ray):
        # 1. Verifica bounding box
        t_start, t_end = self.intersect_box(ray)
        
        # Retorna NoHit se errou a caixa (para compatibilidade com ObjectTransform)
        if t_start is None:
            return NoHit()

        if t_start < 0: t_start = 0

        # 2. Ray Marching
        step_size = (t_end - t_start) / self.num_steps
        
        t_curr = t_start
        
        # --- CORREÇÃO 1: Cálculo manual do ponto (sem usar ray.at) ---
        # p_curr = ray.origin + ray.direction * t_curr
        p_curr = ray.origin + (ray.direction * t_curr)
        # -------------------------------------------------------------
        
        val_curr = self.function(p_curr.x, p_curr.y, p_curr.z)
        
        for i in range(self.num_steps):
            t_next = t_curr + step_size
            if t_next > t_end: break

            # --- CORREÇÃO 2 ---
            p_next = ray.origin + (ray.direction * t_next)
            val_next = self.function(p_next.x, p_next.y, p_next.z)
            
            if val_curr * val_next <= 0:
                # 3. Refinamento (Bissecção)
                t_low, t_high = t_curr, t_next
                
                for _ in range(10):
                    t_mid = (t_low + t_high) * 0.5
                    
                    # --- CORREÇÃO 3 ---
                    p_mid = ray.origin + (ray.direction * t_mid)
                    val_mid = self.function(p_mid.x, p_mid.y, p_mid.z)
                    
                    if val_curr * val_mid <= 0:
                        t_high = t_mid
                    else:
                        t_low = t_mid
                        val_curr = val_mid
                
                t_final = t_low
                # --- CORREÇÃO 4 ---
                p_final = ray.origin + (ray.direction * t_final)
                normal = self.get_normal(p_final)
                
                # Retorna HitRecord válido
                return HitRecord(True, t_final, p_final, normal, self.material, (0,0))
                
            t_curr = t_next
            val_curr = val_next
            
        return NoHit()    
class HeartSurface(ImplicitSurface):
    def __init__(self, material):
        bbox_min = Vector3D(-1.5, -1.5, -1.5)
        bbox_max = Vector3D(1.5, 1.5, 1.5)
        
        super().__init__(material, bbox_min, bbox_max, num_steps=60)

    def function(self, x, y, z):
        base = x**2 + (2.25 * z**2) + y**2 - 1
        return (base**3) - (x**2 * y**3) - (0.1125 * z**2 * y**3)

class MitchelSurface(ImplicitSurface):
    def __init__(self, material):
        # Expandimos a caixa para a esquerda (de -4.5 a -0.5) pois o centro será -2.5
        bbox_min = Vector3D(-4.5, -2.0, -2.0)
        bbox_max = Vector3D(-0.5, 2.0, 2.0)
        super().__init__(material, bbox_min, bbox_max, num_steps=200)

    def function(self, x, y, z):
        # Move a superfície 2.5 unidades para a ESQUERDA
        x = x + 2.5
        r2 = y**2 + z**2
        term1 = 4 * (x**4 + r2**2)
        term2 = 17 * (x**2) * r2
        term3 = -20 * (x**2 + r2)
        return term1 + term2 + term3 + 17