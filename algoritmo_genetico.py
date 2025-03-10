import random




def ler_tsplib(arquivo):
    with open(arquivo, "r") as f:
        linhas = f.readlines()


    cidades = []
    lendo_coordenadas = False


    for linha in linhas:
        linha = linha.strip()


        if linha.startswith("NODE_COORD_SECTION"):
            lendo_coordenadas = True
            continue


        if linha.startswith("EOF"):
            break


        if lendo_coordenadas:
            partes = linha.split()
            if len(partes) >= 3:
                x, y = float(partes[1]), float(partes[2])
                cidades.append((x, y))


    num_cidades = len(cidades)
    distancias = [[0] * num_cidades for _ in range(num_cidades)]


    for i in range(num_cidades):
        for j in range(i + 1, num_cidades):
            dx = cidades[i][0] - cidades[j][0]
            dy = cidades[i][1] - cidades[j][1]
            dist = (dx**2 + dy**2) ** 0.5
            distancias[i][j] = dist
            distancias[j][i] = dist


    return cidades, distancias




def calcular_custo_rota(rota, matriz_distancias):
    custo_total = sum(
        matriz_distancias[rota[i]][rota[i + 1]] for i in range(len(rota) - 1)
    )
    custo_total += matriz_distancias[rota[-1]][rota[0]]
    return custo_total




def criar_rota_aleatoria(numero_cidades):
    rota = list(range(numero_cidades))
    random.shuffle(rota)
    return rota




def populacao_inicial(tamanho_populacao, numero_cidades):
    return [criar_rota_aleatoria(numero_cidades) for _ in range(tamanho_populacao)]




def crossover(pai1, pai2):
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))


    filho = [None] * tamanho
    filho[inicio : fim + 1] = pai1[inicio : fim + 1]


    posicoes_para_preencher = [i for i in range(tamanho) if filho[i] is None]
    valores_para_preencher = [cidade for cidade in pai2 if cidade not in filho]


    for i, posicao in enumerate(posicoes_para_preencher):
        filho[posicao] = valores_para_preencher[i]


    return filho




def mutacao(rota, taxa_mutacao=0.01):
    for i in range(len(rota)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(rota) - 1)
            rota[i], rota[j] = rota[j], rota[i]




def algoritmo_genetico(matriz_distancias, tamanho_populacao=20, numero_geracoes=200, taxa_mutacao=0.02):
    numero_cidades = len(matriz_distancias)
    populacao = populacao_inicial(tamanho_populacao, numero_cidades)


    melhor_rota = None
    melhor_custo = float("inf")


    for _ in range(numero_geracoes):
        populacao.sort(key=lambda r: calcular_custo_rota(r, matriz_distancias))


        custo_melhor_atual = calcular_custo_rota(populacao[0], matriz_distancias)
        if custo_melhor_atual < melhor_custo:
            melhor_rota = populacao[0]
            melhor_custo = custo_melhor_atual


        tamanho_elite = tamanho_populacao // 2
        nova_populacao = populacao[:tamanho_elite]


        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.sample(populacao[:tamanho_elite], 2)
            filho = crossover(pai1, pai2)
            mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)


        populacao = nova_populacao


    return melhor_rota, melhor_custo




if __name__ == "__main__":
    cidades, distancias = ler_tsplib("berlin52.tsp")
    melhor_rota_ag, melhor_custo_ag = algoritmo_genetico(distancias)


    print("Melhor rota (Algoritmo Genético):", melhor_rota_ag)
    print("Custo (Algoritmo Genético):", melhor_custo_ag)