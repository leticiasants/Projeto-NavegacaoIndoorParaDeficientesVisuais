# imports de bibliotecas necessários para o funcionamento do código
# pip install numpy / pip install rich são as instalações necessárias a serem feitas
import numpy as np
import heapq
import re
import os
from rich import print
import timeit

# Extrai o caracter V/v do nome do vértice de modo a restar apenas o inteiro, para que o inteiro seja usado como indice da matriz
def extraiIndice(s):
    # Verifica se o vértice inserido no terminal é um vértice válido 
    if ((s[0].lower() == 'v') and (2 <= len(s) <= 3) and s[1:].isdigit()):
        # Use uma expressão regular (operações complexas de busca e manipulação de strings) para encontrar o número após o "V"
        match = re.search(r'(?i)V(\d+)', s)
        # Se houver um valor após o V
        if match:
            # Converte o que foi pego a partir da expressão regular em um inteiro
            number = int(match.group(1))
            # Retorna o valor de inteiro
            return number
        # Se não houver um valor após o V
        else:
           return -1
    # Caso o vértice inserido não seja um vértice válido
    else:
        return -1

# Adiciona o V antes do número para que os nomes dos vértices, segundo o mapeamento, sejam printados no terminal
def adicionaV(number):
    # Converte o número em uma string e adiciona o "V" na frente
    result = "V" + str(number)
    return result

def escolhaCaminho(preferencias):
    situacao = 0
    # Enquanto a situação for diferente de 0 ou retornar, dentro do loop, o while roda
    while situacao != "0":
        # Limpar o terminal no sistema UNIX (Linux ou macOS)
        # os.system('clear')
        # Limpar o terminal no Windows
        os.system('cls')
        
        print("[bold]---------------- Menu ------------------[/bold]")
        print("1) Menor caminho\n2) Evitar rampa\n3) Evitar escada\n4) Evitar rampa e escada\n0) Sair")
        situacao = input("Digite o número correspondente à sua escolha: ")   
        
        if situacao == "1":
            return situacao
        elif situacao == "2":
            # Adiciona um valor muito alto a aresta para invalidar o caminho
            preferencias[2][14] = 500
            preferencias[14][2] = 500
            return situacao
        elif situacao == "3":
            # Adiciona um valor muito alto a aresta para invalidar o caminho
            preferencias[25][12] = 500
            preferencias[12][25] = 500
            return situacao
        elif situacao == "4":
            # Adiciona um valor muito alto as arestas para invalidar o caminho
            preferencias[2][14] = 500
            preferencias[14][2] = 500
            preferencias[25][12] = 500
            preferencias[12][25] = 500
            return situacao
        elif situacao != "0":
            print("Entrada incorreta, por favor coloque uma das opções corretas")

# Função para calcular a menor rota 
def dijkstra(matriz, vInicio, vTermino, preferencias):
    # Obtém o número de vértices na matriz
    n = len(matriz)
    
    # Inicializa listas para armazenar custo, rota e informações de visitação
    custo = [float('inf')] * n  # Inicializa todos os custos como infinito
    rota = [-1] * n             # Inicializa todas as rotas como indefinidas
    visitados = [False] * n      # Inicializa todos os vértices como não visitados

    # O custo do vértice de início para ele mesmo é zero
    custo[vInicio] = 0

    # Inicializa a fila de prioridade com o vértice de início e custo zero
    fila_prioridade = [(0, vInicio)]

    # Algoritmo de Dijkstra
    while fila_prioridade:
        # Remove o vértice com menor custo da fila de prioridade
        (atual_custo, u) = heapq.heappop(fila_prioridade)
        
        # Se o vértice já foi visitado, continue para a próxima iteração
        if visitados[u]:
            continue
        
        # Marca o vértice como visitado
        visitados[u] = True

        # Explora todos os vizinhos do vértice atual
        for v in range(n):
            # Verifica se o vértice não foi visitado e há uma aresta entre u e v
            if not visitados[v] and matriz[u][v] != -1:
                # Calcula o custo atualizado considerando preferências
                custo_atualizado = custo[u] + matriz[u][v] + preferencias[u][v]
                
                # Atualiza o custo e a rota se o custo atualizado for menor
                if custo_atualizado < custo[v]:
                    custo[v] = custo_atualizado
                    rota[v] = u
                    # Adiciona o vértice na fila de prioridade
                    heapq.heappush(fila_prioridade, (custo[v], v))

    # Reconstrói o caminho a partir do vértice de término
    caminho = []
    i = vTermino

    while i != vInicio:
        caminho.insert(0, i)
        i = rota[i]

    # Adiciona o vértice de início ao caminho
    caminho.insert(0, vInicio)
    
    # Retorna o caminho e o custo total até o vértice de término
    return caminho, custo[vTermino]

# Função para printar o resultado
def resultado(caminho, custo):
    # Inicialização de variáveis
    path_str = f"[bold]Caminho:[/bold] "
    instructions_str = "\n[bold]Instruções:[/bold]"

    # Loop para criar o print do caminho e das instruções
    for i in range(len(caminho) - 1):
        v1, v2 = caminho[i], caminho[i + 1]
        distance = pathOpen[v1][v2]
        # Adicionando vértice ao caminho
        path_str += f"{adicionaV(v1)} [green]->[/green] "
        # Adicionando instrução
        instructions_str += f"\nSiga de [green]{adicionaV(v1)}[/green] para [green]{adicionaV(v2)}[/green] por {distance} metros."
        

    path_str += adicionaV(caminho[-1])

    # Limpar o terminal no sistema UNIX (Linux ou macOS)
    # os.system('clear')

    # Limpar o terminal no Windows
    os.system('cls')

    # Printagem do caminho, instruções e custo
    print(path_str)
    print(instructions_str)
    print("\n[bold]Metragem total percorrida:[/bold]", custo, "metros")
    

if __name__ == "__main__":
    # Leitura do arquivo de mapeamento
    with open('Código\mapeamento.txt', 'rb') as f:
        pathOpen = np.genfromtxt(f, dtype='int32')

    # Inicialização das preferências
    preferencias = np.zeros_like(pathOpen)

    # Solicitação de preferências ao usuário
    situacao = escolhaCaminho(preferencias)
    
    # Inicialização de variáveis
    origem = -1
    destino = -1

    # Loop para obtenção de origem e destino válidos
    while (origem < 0 or origem > 28) or (destino < 0 or destino > 28) or (origem == destino):
        # Limpar o terminal no sistema UNIX (Linux ou macOS)
        # os.system('clear')

        # Limpar o terminal no Windows
        os.system('cls')
        
        # Solicitação dos vértices de origem e destino
        origem = extraiIndice(input('Qual o seu vértice de origem? '))
        destino = extraiIndice(input('Qual o seu vértice de destino? '))


    # Registra o tempo de início
    start_time = timeit.default_timer()
    
    # Cálculo da rota
    caminho, custo = dijkstra(pathOpen, origem, destino, preferencias)
    
    # Registra o tempo de término
    end_time = timeit.default_timer()

    # Chama a função para printar os resultados
    resultado(caminho, custo)
    
    # Calcula o tempo total de execução
    elapsed_time = (end_time - start_time) * 1000
    
    # Salva os dados em um arquivo txt
    with open("resultado.txt", "a") as arquivo:
        # Escreve o resultado no arquivo
        arquivo.write(f"origem: {origem} - destino: {destino} - preferencia: {situacao} - tempo de execucao: {elapsed_time}\n")
