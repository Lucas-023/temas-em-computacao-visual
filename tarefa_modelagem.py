import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Sua função in_circle (Intacta, apenas ajustei os parametros para passar o centro)
def in_circle(point, circle_center, radius):
    dx = point[0] - circle_center[0]
    dy = point[1] - circle_center[1]
    distance_squared = dx * dx + dy * dy
    
    r2 = radius * radius
    if distance_squared < r2:
        return distance_squared, 'inside'
    elif distance_squared == r2:
        return distance_squared, 'on'
    else:
        return distance_squared, 'outside'

# 2. Sua função classify (Ajustada o ESSENCIAL)
def classify(xmin, xmax, ymin, ymax, circle_center, radius):
    cx, cy = circle_center
    
    # --- 1. Verifica se está TOTALMENTE FORA ---
    # (Mantemos a lógica anterior do ponto mais próximo)
    closest_x = max(xmin, min(cx, xmax))
    closest_y = max(ymin, min(cy, ymax))
    
    dist_min, status_min = in_circle([closest_x, closest_y], circle_center, radius)
    if status_min == 'outside':
        return 1 # Totalmente Fora

    # --- 2. Verifica se está TOTALMENTE DENTRO (Sua Otimização) ---
    # Descobrimos qual X e qual Y estão mais longe do centro
    # Usamos abs() para ver qual distância é maior
    farthest_x = xmin if abs(xmin - cx) > abs(xmax - cx) else xmax
    farthest_y = ymin if abs(ymin - cy) > abs(ymax - cy) else ymax
    
    # Testamos APENAS esse ponto
    _, status_max = in_circle([farthest_x, farthest_y], circle_center, radius)
    
    if status_max == 'inside':
        return -1 # Totalmente Dentro

    # --- 3. Caso Misto ---
    return 0

# 3. Sua função explore (Corrigido o erro de retorno da lista)
def explore(xmin, xmax, ymin, ymax, level, circle_center, radius):
    c = classify(xmin, xmax, ymin, ymax, circle_center, radius)
    
    # Se o quadrado é puro (1 ou -1) OU acabou os niveis
    if c != 0 or level == 0:
        return [(xmin, xmax, ymin, ymax, c)]
        
    else:
        xmid = (xmin + xmax) / 2
        ymid = (ymin + ymax) / 2
        
        # O ERRO ESTAVA AQUI: Você precisa somar as listas retornadas!
        resultado = []
        resultado += explore(xmin, xmid, ymin, ymid, level - 1, circle_center, radius)
        resultado += explore(xmid, xmax, ymin, ymid, level - 1, circle_center, radius)
        resultado += explore(xmin, xmid, ymid, ymax, level - 1, circle_center, radius)
        resultado += explore(xmid, xmax, ymid, ymax, level - 1, circle_center, radius)
        return resultado

# --- 4. Parte da Visualização ---

# Configurações iniciais
centro = [0.3, 0.4]
raio = 0.21
nivel = 6

# Roda o seu código
quadrados = explore(0, 1, 0, 1, nivel, centro, raio)

# Plota o resultado
fig, ax = plt.subplots(figsize=(6, 6))

for xmin, xmax, ymin, ymax, tipo in quadrados:
    largura = xmax - xmin
    altura = ymax - ymin
    
    # Define a cor: Azul (Fora), Vermelho (Dentro), Cinza (Borda)
    cor = 'white'
    if tipo == 1: cor = '#ccccff'   # Azul claro (Fora)
    elif tipo == -1: cor = '#ff9999' # Vermelho (Dentro)
    elif tipo == 0: cor = '#dddddd'  # Cinza (Borda final)

    rect = patches.Rectangle((xmin, ymin), largura, altura, linewidth=0.5, edgecolor='black', facecolor=cor)
    ax.add_patch(rect)

# Desenha o círculo real por cima para conferir
circulo = patches.Circle(centro, raio, fill=False, color='black', linewidth=2)
ax.add_patch(circulo)

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.title(f"Resultado (Nível {nivel})")
plt.show()