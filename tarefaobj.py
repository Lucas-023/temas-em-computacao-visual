import math

def ler_obj(caminho_arquivo):
    vertices = []
    faces = []

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            #separa a linha nos espaços em branco       
            partes = linha.split()
            tipo = partes[0]

            #caso seja vertice
            if tipo == 'v':
                #muda as str para float
                #ignora a primeira parte (o 'v') e pega as coordenadas
                vertice = [float(x) for x in partes[1:4]] 
                vertices.append(vertice)

            #caso seja face
            elif tipo == 'f':
                face = []
                #ignora a primeira parte (o 'f') e pega os índices dos vértices
                for parte in partes[1:]:
                    #conversao para inteiro
                    val_obj = int(parte)
                    #ajuste de indices pois o obj comeca do 1 e python do 0
                    indice = val_obj - 1
                    #guarda o indice na face
                    face.append(indice)
                #guarda a face na lista de faces
                faces.append(face)
    return vertices, faces

    

def atualizar_malha(vertices, faces):
    vertices_novos = [v[:] for v in vertices]  
    faces_novas = []
    cache_ponto_medio = {}
    novo_indice = 0
    def get_ponto_medio(i1, i2):
        #temos que ordenar para que (i,j) seja igual a (j,i)
        chave = tuple(sorted((i1, i2)))
        
        #se a aresta ja foi calcuada, retorna o indice do ponto medio
        if chave in cache_ponto_medio:
            return cache_ponto_medio[chave]
        
        #caso contrario, calcula o ponto medio
        v1 = vertices_novos[i1]
        v2 = vertices[i2]
        
        mid_x = (v1[0] + v2[0]) / 2
        mid_y = (v1[1] + v2[1]) / 2
        mid_z = (v1[2] + v2[2]) / 2
        
        #projeta o vetor na esfera!!! muito importante para aproximar a esfera de fato
        comprimento = math.sqrt(mid_x**2 + mid_y**2 + mid_z**2)


        mid_x /= comprimento
        mid_y /= comprimento
        mid_z /= comprimento
        
        #adiciona o novo vértice na lista
        vertices_novos.append([mid_x, mid_y, mid_z])
        
        #o novo índice é a última posição da lista
        novo_indice = len(vertices_novos) - 1
        
        #guarda no cache para a próxima vez
        cache_ponto_medio[chave] = novo_indice
        
        return novo_indice
        
    for face in faces:
        v1, v2, v3 = face 
        
        #obtém os índices dos pontos médios (novos vértices)
        a = get_ponto_medio(v1, v2)
        b = get_ponto_medio(v2, v3)
        c = get_ponto_medio(v3, v1)
        
        #cria as 4 novas faces(topo, direita, esquerda, centro)
        faces_novas.append([v1, a, c])
        faces_novas.append([v2, b, a])
        faces_novas.append([v3, c, b])
        faces_novas.append([a, b, c])

    return vertices_novos, faces_novas
def salvar_obj(nome_arquivo, vertices, faces):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write("# OBJ gerado automaticamente\n")

        # 1. Escreve os vértices (v x y z)
        for v in vertices:
            arquivo.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # 2. Escreve as faces (f v1 v2 v3)
        for face in faces:
            # Converte cada índice para string somando 1 (Python 0 -> OBJ 1)
            indices_str = [str(i + 1) for i in face]
            
            # Junta os números com espaço: "1 2 3"
            linha_face = " ".join(indices_str)
            
            arquivo.write(f"f {linha_face}\n")
            
    print(f"Arquivo '{nome_arquivo}' salvo com sucesso!")

def normalizar_todos_vertices(vertices):
    """Garante que TODOS os vértices estejam na esfera unitária"""
    for i in range(len(vertices)):
        v = vertices[i]
        comprimento = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        if comprimento > 0:
            vertices[i] = [v[0]/comprimento, v[1]/comprimento, v[2]/comprimento]
    return vertices
def main():
    verts_atuais, faces_atuais = ler_obj("icosaedro.obj")
    
    
    verts_atuais = normalizar_todos_vertices(verts_atuais)
    
    for i in range(1):
        print(f"Refinando nível {i+1}...")
        verts_atuais, faces_atuais = atualizar_malha(verts_atuais, faces_atuais)
        
        verts_atuais = normalizar_todos_vertices(verts_atuais)
    
    salvar_obj("esfera_final.obj", verts_atuais, faces_atuais)


if __name__ == "__main__":
    main()