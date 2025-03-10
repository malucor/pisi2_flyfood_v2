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


instancias = ["att48.tsp", "berlin52.tsp", "eil101.tsp", "pr299.tsp"]


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