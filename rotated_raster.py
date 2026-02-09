import argparse
import importlib
import math
from itertools import product

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def rotate_point(x, y, cx, cy, angle_rad):
    """
    Rotaciona o ponto (x,y) em torno de (cx, cy) pelo angulo INVERSO.
    Isso cria o efeito da imagem girando na direção desejada.
    """
    # 1. Transladar para a origem relativa ao pivô
    tx = x - cx
    ty = y - cy
    
    # 2. Rotação Inversa (-angle)
    # cos(-t) = cos(t)
    # sin(-t) = -sin(t)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    # Fórmula da rotação:
    # x' = x cos(t) - y sin(t)  (mas como é inverso, o sinal do sin muda)
    rx = tx * cos_a + ty * sin_a
    ry = -tx * sin_a + ty * cos_a
    
    # 3. Transladar de volta
    return rx + cx, ry + cy

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution
    
    # Prepara a rotação
    angle_rad = math.radians(args.angle)
    cx, cy = args.center # Centro de rotação

    # Cria imagem preta
    image = np.zeros((height, width, 3))

    # Coordenadas do centro de cada pixel no mundo normal
    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    # Carrega a cena original (sem modificações)
    scene = importlib.import_module(args.scene).Scene()
    
    print(f"Rasterizando cena '{args.scene}' rotacionada em {args.angle}° ao redor de ({cx}, {cy})...")

    # Loop principal
    for j, i in tqdm(product(range(height), range(width)), total=height*width):
        
        # Ponto real do pixel na tela
        px = x_coords[i]
        py = y_coords[j]
        
        # --- A MÁGICA ACONTECE AQUI ---
        # Transformamos a coordenada do pixel para o "Espaço do Objeto"
        # Giramos o ponto ao contrário para ver onde ele cai na cena original estática
        px_rotated, py_rotated = rotate_point(px, py, cx, cy, angle_rad)
        query_point = (px_rotated, py_rotated)

        # Define cor de fundo padrão
        # (Nota: Se a classe Color tiver método as_list, usamos ele, senão array direto)
        bg = scene.background
        if hasattr(bg, 'as_list'):
             image[j, i] = bg.as_list()
        else:
             image[j, i] = [bg.r, bg.g, bg.b]

        # Verifica colisão na cena usando o PONTO ROTACIONADO
        for primitive, color in scene:
            if primitive.in_out(query_point):
                image[j, i] = [color.r, color.g, color.b]
                break # Painter's algorithm simples

    # Salva
    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')
    print(f"Salvo em: {args.output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rasterizador com Rotação de Câmera/Mundo")
    
    # Argumentos Básicos
    parser.add_argument('-s', '--scene', type=str, required=True, default='implicit_scene', help='Nome do arquivo da cena (ex: implicit_scene)')
    parser.add_argument('-w', '--window', type=float, nargs=4, default=[-3, 3, -2, 3], help='Janela: xmin xmax ymin ymax')
    parser.add_argument('-r', '--resolution', type=int, nargs=2, default=[1800, 1200], help='Resolução: width height')
    parser.add_argument('-o', '--output', type=str, default='rotated_output90.png', help='Arquivo de saída')
    
    # Argumentos de Rotação
    parser.add_argument('-a', '--angle', type=float, default=90.0, help='Ângulo de rotação em Graus (anti-horário)')
    parser.add_argument('-c', '--center', type=float, nargs=2, default=[0.0, 0.0], help='Ponto central da rotação (X Y)')

    args = parser.parse_args()
    main(args)