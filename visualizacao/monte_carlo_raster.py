import argparse
import importlib
import math
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Funcao de amostragem
def generate_sample_offset(distribution='uniform', sigma=0.5):
    if distribution == 'gaussian':
        dx = np.random.normal(0, sigma)
        dy = np.random.normal(0, sigma)
        return dx, dy
    elif distribution == 'hat':
        dx = np.random.triangular(-0.5, 0.0, 0.5)
        dy = np.random.triangular(-0.5, 0.0, 0.5)
        return dx, dy
    else: # uniform
        dx = np.random.uniform(-0.5, 0.5)
        dy = np.random.uniform(-0.5, 0.5)
        return dx, dy

def main(args):
    # 1. Configuração Inicial Geral
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution
    N = args.samples 
    
    print(f"Rasterizando cena '{args.scene}'")
    
    # Carrega a cena
    scene = importlib.import_module(args.scene).Scene()
    
    # Calcula o tamanho físico de cada pixel no mundo
    pixel_w = (xmax - xmin) / width
    pixel_h = (ymax - ymin) / height

    # Pré-calcula coordenadas dos centros dos pixels
    x_centers = np.linspace(xmin + pixel_w/2, xmax - pixel_w/2, width)
    y_centers = np.linspace(ymin + pixel_h/2, ymax - pixel_h/2, height)

    distributions_to_run = ['gaussian'] # Pode adicionar 'uniform' se quiser comparar

    base_filename, ext_filename = os.path.splitext(args.output)

    # === LOOP EXTERNO: Tipos de Distribuição ===
    for dist_name in distributions_to_run:
        print(f"\n--- Iniciando Renderização: {dist_name.upper()} ---")
        
        image = np.zeros((height, width, 3))
        start_time = time.time()

        # 2. Loop Principal (Renderização)
        for j in tqdm(range(height), desc=f"Processando Linhas ({dist_name})"):
            py_center = y_centers[j]
            
            for i in range(width):
                px_center = x_centers[i]
                
                accumulated_color = np.array([0.0, 0.0, 0.0])
                
                # --- MONTE CARLO LOOP ---
                for _ in range(N):
                    dx, dy = generate_sample_offset(dist_name, args.sigma)
                    sample_x = px_center + (dx * pixel_w)
                    sample_y = py_center + (dy * pixel_h)
                    sample_point = (sample_x, sample_y)
                    
                    hit = False
                    
                    # Cor de fundo
                    if hasattr(scene.background, 'as_list'):
                        bg = np.array(scene.background.as_list())
                    else:
                        bg = np.array([scene.background.r, scene.background.g, scene.background.b])

                    for primitive, color_obj in scene:
                        if primitive.in_out(sample_point):
                            accumulated_color += np.array([color_obj.r, color_obj.g, color_obj.b])
                            hit = True
                            break 
                    
                    if not hit:
                        accumulated_color += bg
                # --- FIM DO MONTE CARLO ---
                
                final_color = accumulated_color / N
                image[j, i] = final_color

        elapsed = time.time() - start_time
        print(f"Tempo ({dist_name}): {elapsed:.2f} segundos")

        # Garante intervalo 0-1
        image = np.clip(image, 0, 1)

        # 3. Salva a Imagem Original Completa
        current_output_name = f"{base_filename}_{dist_name}{ext_filename}"
        plt.imsave(current_output_name, image, vmin=0, vmax=1, origin='lower')
        print(f"Imagem completa salva em: {current_output_name}")

        # ========================================================
        # 4. APLICAÇÃO DO ZOOM (RECORTE) IGUAL AO CÓDIGO ENVIADO
        # ========================================================
        if args.crop_enable:
            print(f"   ✂️ Gerando recorte (Zoom) em ({args.crop_center[0]}, {args.crop_center[1]})...")
            
            target_x, target_y = args.crop_center
            zoom_range = args.crop_radius

            # Converte coordenadas do MUNDO para PIXELS
            # A fórmula se adapta automaticamente ao tamanho da janela (xmin, xmax, etc)
            
            # Eixo X
            x_start = int((target_x - zoom_range - xmin) * width / (xmax - xmin))
            x_end   = int((target_x + zoom_range - xmin) * width / (xmax - xmin))
            
            # Eixo Y
            y_start = int((target_y - zoom_range - ymin) / (ymax - ymin) * height)
            y_end   = int((target_y + zoom_range - ymin) / (ymax - ymin) * height)

            # Garante que não saia da imagem (clipping dos índices)
            x_start = max(0, x_start)
            x_end   = min(width, x_end)
            y_start = max(0, y_start)
            y_end   = min(height, y_end)

            # Faz o "Slicing" do array numpy (O Recorte)
            zoom_img = image[y_start:y_end, x_start:x_end]

            # Salva o recorte
            zoom_filename = f"{base_filename}_{dist_name}_ZOOM_CROP{ext_filename}"
            
            # Se a imagem ficou vazia (coordenadas erradas), avisa
            if zoom_img.size == 0:
                print("   ⚠️ AVISO: A área de zoom está fora da janela da imagem! Nada foi salvo.")
            else:
                plt.imsave(zoom_filename, zoom_img, vmin=0, vmax=1, origin='lower')
                print(f"   ✅ Zoom salvo em: {zoom_filename}")
        # ========================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monte Carlo Rasterizer com Zoom de Recorte")
    
    # Argumentos Básicos
    parser.add_argument('-s', '--scene', type=str, required=True, help='Nome do arquivo da cena')
    parser.add_argument('-w', '--window', type=float, nargs=4, default=[0, 238, 2, 379], help='Janela: xmin xmax ymin ymax')
    parser.add_argument('-r', '--resolution', type=int, nargs=2, default=[900, 600], help='Resolução: width height')
    parser.add_argument('-o', '--output', type=str, default='mc_outputlion_900x600.png', help='Nome base do arquivo de saída')
    parser.add_argument('-n', '--samples', type=int, default=25, help='Número de amostras por pixel (N)')
    parser.add_argument('--sigma', type=float, default=0.35, help='Sigma para distribuição gaussiana')

    # === NOVOS ARGUMENTOS PARA O ZOOM (RECORTE) ===
    # Use --crop_enable para ativar
    parser.add_argument('--crop_enable', action='store_true', help='Ativa o salvamento da imagem com zoom (recorte)')
    parser.add_argument('--crop_center', type=float, nargs=2, default=[0.5, 0.5], help='Centro do recorte (x y)')
    parser.add_argument('--crop_radius', type=float, default=0.5, help='Raio da área de recorte (em coordenadas do mundo)')

    args = parser.parse_args()
    main(args)