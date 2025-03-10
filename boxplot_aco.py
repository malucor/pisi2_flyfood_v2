import random
import seaborn as sns
import matplotlib.pyplot as plt


melhor_solucao_conhecida = 7542


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




def realizar_experimentos_aco(matriz_distancias, numero_experimentos=100, numero_formigas=10, alfa=1.0, beta=2.0, evaporacao=0.2, numero_iteracoes=100):
    resultados = []
    for _ in range(numero_experimentos):
        _, custo = colonia_formigas_tsp(matriz_distancias, numero_formigas, alfa, beta, evaporacao, numero_iteracoes)
        resultados.append(custo)
    return resultados




def colonia_formigas_tsp(
    matriz_distancias, numero_formigas=10, alfa=1.0, beta=2.0,
    evaporacao=0.2, numero_iteracoes=100
):
    numero_cidades = len(matriz_distancias)


    def visibilidade(cidade_atual, proxima_cidade):
        dist = matriz_distancias[cidade_atual][proxima_cidade]
        return 1.0 / dist if dist != 0 else 1e10


    feromonio = [[1.0 for _ in range(numero_cidades)] for _ in range(numero_cidades)]
    melhor_rota = None
    melhor_custo = float("inf")


    for _ in range(numero_iteracoes):
        todas_rotas = []


        for _ in range(numero_formigas):
            cidade_inicial = random.randint(0, numero_cidades - 1)
            rota = [cidade_inicial]
            nao_visitadas = set(range(numero_cidades)) - {cidade_inicial}


            while nao_visitadas:
                cidade_atual = rota[-1]
                probabilidades = []
                soma_probabilidades = 0.0


                for proxima_cidade in nao_visitadas:
                    tau = feromonio[cidade_atual][proxima_cidade] ** alfa
                    eta = visibilidade(cidade_atual, proxima_cidade) ** beta
                    prob = tau * eta
                    probabilidades.append((proxima_cidade, prob))
                    soma_probabilidades += prob


                valor_aleatorio = random.random() * soma_probabilidades
                acumulado = 0.0
                for cidade, p in probabilidades:
                    acumulado += p
                    if acumulado >= valor_aleatorio:
                        rota.append(cidade)
                        nao_visitadas.remove(cidade)
                        break


            custo_rota = sum(
                matriz_distancias[rota[i]][rota[i + 1]] for i in range(len(rota) - 1)
            )
            custo_rota += matriz_distancias[rota[-1]][rota[0]]
            todas_rotas.append((rota, custo_rota))


            if custo_rota < melhor_custo:
                melhor_rota, melhor_custo = rota, custo_rota


        for i in range(numero_cidades):
            for j in range(numero_cidades):
                feromonio[i][j] *= (1 - evaporacao)


        for rota, custo_rota in todas_rotas:
            deposito = 1.0 / custo_rota
            for i in range(len(rota) - 1):
                c1, c2 = rota[i], rota[i + 1]
                feromonio[c1][c2] += deposito
                feromonio[c2][c1] += deposito
            feromonio[rota[-1]][rota[0]] += deposito
            feromonio[rota[0]][rota[-1]] += deposito


    return melhor_rota, melhor_custo




if __name__ == "__main__":
    cidades, distancias = ler_tsplib("berlin52.tsp")
    melhor_rota_aco, melhor_custo_aco = colonia_formigas_tsp(
        distancias, numero_formigas=10, alfa=1, beta=2, evaporacao=0.2, numero_iteracoes=100
    )


    resultados_aco = realizar_experimentos_aco(distancias)


    sns.boxplot(data=resultados_aco)
    plt.axhline(melhor_solucao_conhecida, color='red', linestyle='--', label=f'Melhor Solução Conhecida ({melhor_solucao_conhecida})')
    plt.title('Distribuição dos Custos das Soluções Geradas pela Colônia de Formigas (ACO)')
    plt.ylabel('Custo da Rota')
    plt.legend()
    plt.show()