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

# 4. ZOOM PARA DISTÂNCIA DE 0.005 (Limiar de Visibilidade)
    # Alvo no centro da fenda entre as hipotenusas
    # Foco no rosto/olho do leão
    # Foco em uma área densa da juba/corpo dentro da sua janela
    # Foco na borda da forma para o relatório
    target_x, target_y = 0.5, 0.5 
    zoom_range = 0.5 

    # O cálculo agora usa os limites de -2 a 2
    x_start = int((target_x - zoom_range - (-2.0)) * width / (2.0 - (-2.0)))
    x_end   = int((target_x + zoom_range - (-2.0)) * width / (2.0 - (-2.0)))
    y_start = int((target_y - zoom_range - (-2.0)) * height / (2.0 - (-2.0)))
    y_end   = int((target_y + zoom_range - (-2.0)) * height / (2.0 - (-2.0)))
    zoom_img = image[max(0, y_start):min(height, y_end), 
                     max(0, x_start):min(width, x_end)]
    
    # Nome para salvar o experimento de 0.005
    plt.imsave(args.output.replace(".png", "_zoom_limiar.png"), zoom_img, origin='lower')
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scene', type=str, default='lion_scene')
    # Janela conforme sua nova cena
    parser.add_argument('-w', '--window', type=float, nargs=4, default=[0, 238, 2, 379])
    args = parser.parse_args()

    # Resoluções em ordem crescente
    resolutions = [(450, 300),(900, 600)]
    base_name = "lion" # Nome atualizado

    for w, h in resolutions:
        args.resolution = [w, h]
        args.output = f"{base_name}_{w}x{h}.png"
        main(args)