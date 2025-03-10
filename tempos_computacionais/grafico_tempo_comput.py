import random
import time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


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
        if linha.startswith("EDGE_WEIGHT_SECTION"):
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

# algoritmo genético

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




# colônia de formigas

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




# buscas tabu

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



def medir_tempo_algoritmo(algoritmo, distancias, *args, **kwargs):
    start_time = time.time()
    algoritmo(distancias, *args, **kwargs)
    return time.time() - start_time


def realizar_experimentos_tempos(instancias):
    tempos = []

    for instancia in instancias:
        cidades, distancias = ler_tsplib(instancia)
        tempo_ag = medir_tempo_algoritmo(algoritmo_genetico, distancias)
        tempo_aco = medir_tempo_algoritmo(colonia_formigas_tsp, distancias)
        tempo_tabu = medir_tempo_algoritmo(busca_tabu_tsp, distancias)
        tempos.append({
            'Instancia': instancia,
            'Algoritmo Genético': tempo_ag,
            'Colônia de Formigas': tempo_aco,
            'Busca Tabu': tempo_tabu
        })
    return pd.DataFrame(tempos)

instancias = ["att48.tsp", "berlin52.tsp", "brazil58.tsp", "eil101.tsp", "pr299.tsp"]

df_tempos = realizar_experimentos_tempos(instancias)

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_tempos, x='Instancia', y='Algoritmo Genético', label='Algoritmo Genético', color='blue', marker='o')
sns.lineplot(data=df_tempos, x='Instancia', y='Colônia de Formigas', label='Colônia de Formigas', color='green', marker='o')
sns.lineplot(data=df_tempos, x='Instancia', y='Busca Tabu', label='Busca Tabu', color='red', marker='o')

plt.title('Tempo de Execução dos Algoritmos para Diferentes Instâncias')
plt.xlabel('Instância do Problema')
plt.ylabel('Tempo de Execução (segundos)')
plt.legend()
plt.show()