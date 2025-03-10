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
            dist = (dx ** 2 + dy ** 2) ** 0.5
            distancias[i][j] = dist
            distancias[j][i] = dist
   
    return cidades, distancias




def calcular_custo(rota, matriz):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz[rota[i]][rota[i+1]]        
    custo += matriz[rota[-1]][rota[0]]
    return custo




def gerar_vizinhos(rota):
    vizinhos = []
    for i in range(len(rota)):
        for j in range(i + 1, len(rota)):
            nova_rota = rota[:]
            nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
            vizinhos.append(nova_rota)
    return vizinhos




def busca_tabu_tsp(matriz_distancias, maximo_iteracoes=100, tamanho_tabu=5):
    numero_cidades = len(matriz_distancias)
    solucao_atual = list(range(numero_cidades))
    random.shuffle(solucao_atual)
    melhor_solucao = solucao_atual[:]
    melhor_custo = calcular_custo(melhor_solucao, matriz_distancias)
    lista_tabu = []


    for _ in range(maximo_iteracoes):
        lista_vizinhos = gerar_vizinhos(solucao_atual)
        vizinhos_custos = [(vizinho, calcular_custo(vizinho, matriz_distancias)) for vizinho in lista_vizinhos]
        vizinhos_custos.sort(key=lambda x: x[1])


        movimento_feito = False
        for candidato, custo_candidato in vizinhos_custos:
            if (candidato not in lista_tabu) or (custo_candidato < melhor_custo):
                solucao_atual = candidato
                lista_tabu.append(candidato)
                if len(lista_tabu) > tamanho_tabu:
                    lista_tabu.pop(0)
                if custo_candidato < melhor_custo:
                    melhor_solucao = candidato
                    melhor_custo = custo_candidato
                movimento_feito = True
                break


        if not movimento_feito:
            break


    return melhor_solucao, melhor_custo




if __name__ == "__main__":
    cidades, matriz_distancias = ler_tsplib("berlin52.tsp")
    melhor_rota_tabu, melhor_custo_tabu = busca_tabu_tsp(matriz_distancias)
    print("Melhor rota (Busca Tabu):", melhor_rota_tabu)
    print("Custo (Busca Tabu):", melhor_custo_tabu)