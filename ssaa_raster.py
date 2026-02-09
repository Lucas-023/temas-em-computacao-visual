import argparse
import importlib
import math
from itertools import product

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# --- FUNÇÃO AUXILIAR: Gera os offsets e pesos para o Anti-Aliasing ---
def get_samples(n_samples, filter_type):
    """
    Gera uma lista de offsets (dx, dy) relativos ao centro do pixel e seus pesos.
    """
    samples = []
    
    # Define o tamanho da grade (grid_size x grid_size)
    grid_size = int(math.sqrt(n_samples))
    if grid_size * grid_size != n_samples:
        print(f"Aviso: {n_samples} amostras não formam um quadrado perfeito. Usando grid {grid_size}x{grid_size}.")
    
    step = 1.0 / grid_size
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Posição relativa dentro do pixel (0.0 a 1.0)
            ry = (i + 0.5) * step
            rx = (j + 0.5) * step
            
            # Offset relativo ao centro (-0.5 a +0.5)
            dx = rx - 0.5
            dy = ry - 0.5
            
            # Cálculo do peso baseado no filtro
            dist = math.sqrt(dx*dx + dy*dy)
            weight = 1.0

            if filter_type == 'box':
                weight = 1.0
            elif filter_type == 'hat':
                weight = max(0.0, 1.0 - (dist * 2.0))
            elif filter_type == 'gaussian':
                sigma = 0.35
                weight = math.exp(-(dist*dist) / (2 * sigma * sigma))

            samples.append((dx, dy, weight))
            
    return samples

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution

    # Tamanho do pixel no mundo (necessário para calcular a posição das sub-amostras)
    pixel_w = (xmax - xmin) / width
    pixel_h = (ymax - ymin) / height

    # Pre-calcula os offsets de amostragem
    sample_offsets = get_samples(args.samples, args.filter)

    # create tensor for image: RGB
    image = np.zeros((height, width, 3))

    # Find coordinates for center of each pixel
    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    # load scene from file args.scene
    # Recarrega o módulo para garantir limpeza entre interações do loop de resolução
    scene_module = importlib.import_module(args.scene)
    importlib.reload(scene_module)
    scene = scene_module.Scene()

    print(f"Renderizando {width}x{height} | Samples: {args.samples} | Filtro: {args.filter}")

    # for each pixel...
    for j, i in tqdm(product(range(height), range(width)), total=height*width):
        
        # Centro do pixel atual
        cx, cy = x_coords[i], y_coords[j]
        
        # Acumuladores para a cor média
        final_color = np.zeros(3)
        total_weight = 0.0

        # --- LOOP DE ANTI-ALIASING (SSAA) ---
        for dx, dy, w in sample_offsets:
            # Calcula a posição exata da sub-amostra no mundo
            sx = cx + dx * pixel_w
            sy = cy + dy * pixel_h
            point = (sx, sy)

            # Inicia com a cor do fundo para esta amostra
            sample_color = np.array(list(scene.background.as_list()))[:3]

            # Verifica colisão com primitivas
            for primitive, color in scene:
                if primitive.in_out(point):
                    # Se bateu, usa a cor do primitivo
                    sample_color = np.array([color.r, color.g, color.b])
                    break  # Painter's algo simples (para no primeiro hit)
            
            # Acumula cor ponderada
            final_color += sample_color * w
            total_weight += w
        
        # Normaliza e atribui ao pixel
        if total_weight > 0:
            image[j, i] = final_color / total_weight

    # save image as png using matplotlib
    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Raster module main function")
    parser.add_argument('-s', '--scene', type=str, help='Scene name', default='implicit_scene')
    parser.add_argument('-w', '--window', type=float, nargs=4, help='Window: xmin xmax ymin ymax', default=[-3, 3, -2, 3])
    
    # Argumentos originais de resolução e output (serão sobrescritos pelo loop, mas mantidos aqui por padrão)
    parser.add_argument('-r', '--resolution', type=int, nargs=2, help='Resolution: width height', default=[3840, 2160])
    parser.add_argument('-o', '--output', type=str, help='Output file name', default='output.png')

    # --- NOVOS ARGUMENTOS PARA O EXERCÍCIO ---
    parser.add_argument('-n', '--samples', type=int, default=9, help='Numero total de amostras (1, 4, 9, 16...)')
    parser.add_argument('-f', '--filter', type=str, choices=['box', 'hat', 'gaussian'], default='gaussian', help='Tipo de filtro AA')

    args = parser.parse_args()

    # --- LÓGICA DE MÚLTIPLAS RESOLUÇÕES (Solicitada) ---
    
    # Lista de resoluções padrão (Largura, Altura)
    resolutions = [
        (600, 400),
        (1200, 800),
    ]

    # Salva o nome base
    base_name = "ssaa_gaussian_implicit"

    # Loop para gerar as imagens nas resoluções pedidas
    for w, h in resolutions:
        # 1. Atualiza a resolução
        args.resolution = [w, h]
        
        # 2. Atualiza o nome do arquivo de saída
        # Ex: area_lion_600x400.png
        args.output = f"{base_name}_{w}x{h}.png"
        
        # 3. Chama a função principal com a lógica SSAA
        main(args)
        
    print("Todas as resoluções foram geradas com sucesso.")