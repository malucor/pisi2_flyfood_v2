import random
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


melhor_solucao_conhecida = 7542


if __name__ == "__main__":
    cidades, distancias = ler_tsplib("berlin52.tsp")


    resultados_ag = realizar_experimentos_ag(distancias)
    resultados_aco = realizar_experimentos_aco(distancias)
    resultados_tabu = realizar_experimentos_tabu(distancias)


    df = pd.DataFrame({
        'Custo': resultados_ag + resultados_aco + resultados_tabu,
        'Algoritmo': ['Algoritmo Genético'] * len(resultados_ag) +
                     ['Colônia de Formigas'] * len(resultados_aco) +
                     ['Busca Tabu'] * len(resultados_tabu)
    })


    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Algoritmo', y='Custo', data=df)
    plt.axhline(melhor_solucao_conhecida, color='red', linestyle='--', label=f'Melhor Solução Conhecida ({melhor_solucao_conhecida})')
    plt.title('Distribuição dos Custos das Soluções para os Algoritmos')
    plt.xlabel('Algoritmo')
    plt.ylabel('Custo da Rota')
    plt.legend()
    plt.show()