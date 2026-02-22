import argparse
import importlib
from itertools import product
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def main(args):
    xmin, xmax, ymin, ymax = args.window
    width, height = args.resolution

    # 1. Criar matriz para a imagem
    image = np.zeros((height, width, 3))

    x_coords = [xmin + (xmax - xmin) * (i + 0.5) / width for i in range(width)]
    y_coords = [ymin + (ymax - ymin) * (j + 0.5) / height for j in range(height)]

    # Carregar a cena
    scene = importlib.import_module(args.scene).Scene()

    # 2. Rasterização
    for j, i in tqdm(product(range(height), range(width)), total=height*width, desc=f"Render {width}x{height}"):
        point = (x_coords[i], y_coords[j])
        image[j, i] = list(scene.background.as_list())
        
        for primitive, color in scene:
            if primitive.in_out(point):
                image[j, i] = [color.r, color.g, color.b]
                break

    # 3. Salvar Imagem Original
    plt.imsave(args.output, image, vmin=0, vmax=1, origin='lower')
    print(f"Imagem salva: {args.output}")

    if args.zoom:
        zoom_configs = [
            # (centro_x, centro_y, largura_janela, nome)
            (-0.75, 0.1, 0.05, "seahorse_valley"),  
            (-0.5, 0.0, 0.1, "main_body"),           
            (0.285, 0.01, 0.02, "spiral"),           
            (-0.7463, 0.1102, 0.005, "detail"),     
        ]
        
        for target_x, target_y, zoom_range, zoom_name in zoom_configs:
            # Converter coordenadas do mundo para coordenadas da imagem
            x_center = (target_x - xmin) / (xmax - xmin) * width
            y_center = (target_y - ymin) / (ymax - ymin) * height
            
            zoom_width = zoom_range / (xmax - xmin) * width
            zoom_height = zoom_range / (ymax - ymin) * height
            
            x_start = int(x_center - zoom_width / 2)
            x_end = int(x_center + zoom_width / 2)
            y_start = int(y_center - zoom_height / 2)
            y_end = int(y_center + zoom_height / 2)
            
            zoom_img = image[max(0, y_start):min(height, y_end), 
                           max(0, x_start):min(width, x_end)]
            
            zoom_output = args.output.replace(".png", f"_zoom_{zoom_name}.png")
            plt.imsave(zoom_output, zoom_img, origin='lower')
            print(f"Zoom salvo: {zoom_output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renderizador do Fractal de Mandelbrot')
    parser.add_argument('-s', '--scene', type=str, default='mandelbrot_scene',
                       help='Módulo da cena a ser renderizada')
    parser.add_argument('-w', '--window', type=float, nargs=4, default=[-2.5, 1.0, -1.25, 1.25],
                       help='Janela de visualização [xmin, xmax, ymin, ymax]')
    parser.add_argument('--zoom', action='store_true',
                       help='Gerar imagens com zoom em áreas interessantes')
    args = parser.parse_args()

    # Resoluções em ordem crescente
    resolutions = [(150, 100), (450, 300), (900, 600), (1800, 1200)]
    base_name = "mandelbrot"

    for w, h in resolutions:
        args.resolution = [w, h]
        args.output = f"{base_name}_{w}x{h}.png"
        print(f"\n{'='*50}")
        print(f"Renderizando resolução {w}x{h}")
        print(f"{'='*50}")
        main(args)
    
    print(f"\n{'='*50}")
    print("Renderização concluída!")
    print(f"{'='*50}")
