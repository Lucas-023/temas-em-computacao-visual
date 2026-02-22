from PIL import Image
import os

def criar_gif_pil_direto(lista_arquivos, nome_saida, ms_por_frame=5000):
    """
    Cria GIF usando APENAS a biblioteca PIL (Pillow).
    ms_por_frame: Tempo em milissegundos. 5000 = 5 segundos.
    """
    if not lista_arquivos:
        print(f"Lista vazia: {nome_saida}")
        return

    print(f"--- Processando: {nome_saida} ---")

    # 1. Carregar e Redimensionar as imagens
    imagens_processadas = []
    
    # Primeiro, descobre o tamanho máximo
    max_w, max_h = 0, 0
    imagens_cruas = []

    for arquivo in lista_arquivos:
        if os.path.exists(arquivo):
            try:
                img = Image.open(arquivo)
                imagens_cruas.append(img)
                if img.width > max_w: max_w = img.width
                if img.height > max_h: max_h = img.height
            except:
                pass
        else:
            print(f"  Arquivo não achado: {arquivo}")

    if not imagens_cruas:
        return

    # Redimensiona tudo para o tamanho máximo (mantendo o pixelado)
    for img in imagens_cruas:
        if img.size != (max_w, max_h):
            # O segredo do pixel art: NEAREST
            img = img.resize((max_w, max_h), resample=Image.Resampling.NEAREST)
        imagens_processadas.append(img)

    # 2. SALVAR USANDO PIL DIRETO (AQUI É A MUDANÇA)
    # A primeira imagem comanda, as outras são anexadas.
    if imagens_processadas:
        primeira = imagens_processadas[0]
        outras = imagens_processadas[1:]

        try:
            primeira.save(
                nome_saida,
                save_all=True,          # Diz que é uma animação
                append_images=outras,   # Adiciona o resto
                duration=ms_por_frame,  # DURAÇÃO EM MILISSEGUNDOS (INT)
                loop=0                  # 0 = Loop infinito
            )
            print(f"✅ GIF CRIADO: {nome_saida}")
            print(f"   Tempo configurado: {ms_por_frame} ms ({ms_por_frame/1000} segundos)\n")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")

# ==========================================
# LISTAS DE ARQUIVOS
# ==========================================

imgs_triangulo = [
    'triangulos/area_triangle_300x200_zoom.png',
    'triangulos/area_triangle_600x400_zoom.png',
    'triangulos/area_triangle_900x600_zoom.png',
    'triangulos/area_triangle_1200x800_zoom.png',
    'triangulos/area_triangle_1800x1200_zoom.png'
]

imgs_juntos = [
    'triangulos/raster_triangles_juntos_300x200_zoom.png',
    'triangulos/raster_triangles_juntos_600x400_zoom.png',
    'triangulos/raster_triangles_juntos_900x600_zoom.png',
    'triangulos/raster_triangles_juntos_1200x800_zoom.png',
    'triangulos/raster_triangles_juntos_1800x1200_zoom.png'
]

imgs_gaussian = [
    'mc_output_150x100_gaussian.png',
    'mc_output_450x300_gaussian.png',
    'mc_output_900x600_gaussian.png',
    'mc_output_1350x900_gaussian.png'
]

imgs_lion = [
    'lion_150x100_zoom_limiar.png',
    'lion_300x200_zoom_limiar.png',
    'lion_450x300_zoom_limiar.png',
    'lion_900x600_zoom_limiar.png'
]

# ==========================================
# EXECUÇÃO (NOMES NOVOS)
# ==========================================

# 5000 ms = 5 Segundos
# Se quiser 10 segundos, coloque 10000

#criar_gif_pil_direto(imgs_triangulo, 'PIL_triangulo_resolucao.gif', ms_por_frame=1000)
#criar_gif_pil_direto(imgs_juntos, 'PIL_triangulo_juntos.gif', ms_por_frame=1000)

# Rotação um pouco mais rápida (1 segundo)
#criar_gif_pil_direto(imgs_gaussian, 'PIL_gaussian.gif', ms_por_frame=1000)

criar_gif_pil_direto(imgs_lion, 'PIL_lion.gif', ms_por_frame=1000)