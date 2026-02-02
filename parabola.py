import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def classify(xmin, xmax, ymin, ymax, c):
    y_parabola_esq = (xmin**2) - c
    y_parabola_dir = (xmax**2) - c

    if xmin <= 0 <= xmax:
        y_min_parabola = -c
    else:
        y_min_parabola = min(y_parabola_esq, y_parabola_dir)
    
    y_max_parabola = max(y_parabola_esq, y_parabola_dir)
    
    if ymin > y_max_parabola:
        return 1
    
    # Teste 2: Quadrado totalmente ABAIXO da parábola
    # O ponto mais ALTO do quadrado (ymax) está abaixo do ponto mais BAIXO da parábola
    if ymax < y_min_parabola:
        return -1
    
    # Caso contrário: a parábola atravessa o quadrado
    return 0


def explore(xmin, xmax, ymin, ymax, level, c):
    tipo = classify(xmin, xmax, ymin, ymax, c)
    
    # Critério de parada: 
    # 1. Quadrado resolvido (totalmente acima ou abaixo)
    # 2. Atingiu profundidade máxima
    if tipo != 0 or level == 0:
        return [(xmin, xmax, ymin, ymax, tipo)]
    
    # Divide o quadrado em 4 partes
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    
    resultado = []
    # Subdivide recursivamente (ordem: inferior-esquerda, inferior-direita, superior-esquerda, superior-direita)
    resultado += explore(xmin, xmid, ymin, ymid, level - 1, c)  # inferior-esquerda
    resultado += explore(xmid, xmax, ymin, ymid, level - 1, c)  # inferior-direita
    resultado += explore(xmin, xmid, ymid, ymax, level - 1, c)  # superior-esquerda
    resultado += explore(xmid, xmax, ymid, ymax, level - 1, c)  # superior-direita
    
    return resultado


# === PARÂMETROS ===
constante_c = 0
nivel_recursao = 6

# Explora o domínio [-2, 2] x [-2, 2]
quadrados = explore(-2, 2, -2, 2, nivel_recursao, constante_c)

# === VISUALIZAÇÃO ===
fig, ax = plt.subplots(figsize=(8, 8))

# Desenha cada quadrado com sua cor correspondente
for xmin, xmax, ymin, ymax, tipo in quadrados:
    largura = xmax - xmin
    altura = ymax - ymin
    
    # Define cores
    if tipo == 1:
        cor = '#ccccff'      # Azul claro (acima da parábola)
    elif tipo == -1:
        cor = '#ff9999'      # Vermelho claro (abaixo da parábola)
    else:  # tipo == 0
        cor = '#dddddd'      # Cinza (indeterminado/atravessa)
    
    # Adiciona o retângulo
    rect = patches.Rectangle(
        (xmin, ymin), largura, altura,
        linewidth=0.3,
        edgecolor='black',
        facecolor=cor
    )
    ax.add_patch(rect)

# Plota a parábola y = x² - c
x_parabola = np.linspace(-2, 2, 400)
y_parabola = x_parabola**2 - constante_c
ax.plot(x_parabola, y_parabola, color='blue', linewidth=2.5, label=f'y = x² - {constante_c}')

# Configurações do gráfico
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_title(f'Classificação adaptativa em relação a y = x²)', 
             fontsize=14, fontweight='bold')

# Legenda
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#ccccff', edgecolor='black', label='Acima da parábola'),
    Patch(facecolor='#ff9999', edgecolor='black', label='Abaixo da parábola'),
    Patch(facecolor='#dddddd', edgecolor='black', label='Fronteira (Indeterminado)'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

plt.tight_layout()
plt.show()

# Estatísticas
total = len(quadrados)
acima = sum(1 for q in quadrados if q[4] == 1)
abaixo = sum(1 for q in quadrados if q[4] == -1)
indeterminado = sum(1 for q in quadrados if q[4] == 0)

print(f"\n=== ESTATÍSTICAS ===")
print(f"Total de quadrados: {total}")
print(f"Acima da parábola: {acima} ({100*acima/total:.1f}%)")
print(f"Abaixo da parábola: {abaixo} ({100*abaixo/total:.1f}%)")
print(f"Indeterminados: {indeterminado} ({100*indeterminado/total:.1f}%)")