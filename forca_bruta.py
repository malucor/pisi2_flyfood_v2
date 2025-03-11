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

def calcular_distancia(rota, matriz_distancias):
    custo_total = 0
    for i in range(len(rota) - 1):
        custo_total += matriz_distancias[rota[i]][rota[i + 1]]
    custo_total += matriz_distancias[rota[-1]][rota[0]]
    return custo_total

def gerar_permutacoes(lista):
    if len(lista) == 1:
        return [lista]
    permutacoes = []
    for i, elemento in enumerate(lista):
        restante = lista[:i] + lista[i+1:]
        for p in gerar_permutacoes(restante):
            permutacoes.append([elemento] + p)
    return permutacoes

def forca_bruta_tsp(matriz_distancias):
    num_cidades = len(matriz_distancias)
    menor_custo = float('inf')
    melhor_rota = None

    todas_permutacoes = gerar_permutacoes(list(range(num_cidades)))
    
    for perm in todas_permutacoes:
        custo = calcular_distancia(perm, matriz_distancias)
        if custo < menor_custo:
            menor_custo = custo
            melhor_rota = perm

    return melhor_rota, menor_custo

if __name__ == "__main__":
    cidades, distancias = ler_tsplib("berlin52.tsp")
    melhor_rota, melhor_custo = forca_bruta_tsp(distancias)
    
    print("Melhor rota (Força Bruta):", melhor_rota)
    print("Custo (Força Bruta):", melhor_custo)
