from treelib import Node, Tree
from queue import LifoQueue

class Estado:
  def __init__(self, cidade, pai, nivel):
    self.cidade = cidade
    self.pai = pai
    self.nivel = nivel

class BuscaProfundidadeLimitada:

  def __init__(self):
    self.rotas = {'Porto Alegre': ['Florianópolis','São Paulo'],
                  'Florianópolis': ['Curitiba','Porto Alegre'],
                  'Curitiba': ['Florianópolis','São Paulo','Rio de Janeiro'],
                  'São Paulo':['Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Salvador'],
                  'Rio de Janeiro':['Belo Horizonte','Cuiabá', 'Curitiba'],
                  'Belo Horizonte': ['Brasília','Cuiabá', 'São Paulo','Rio de Janeiro'],
                  'Brasília': ['Belo Horizonte','Fortaleza'],
                  'Salvador': ['Fortaleza','São Paulo'],
                  'Cuiabá': ['Belo Horizonte','Manaus','Rio de Janeiro'],
                  'Fortaleza': ['Manaus','Salvador','Brasília'],
                  'Manaus': ['Cuiabá','Fortaleza']
  }

  def realizaBusca(self, origem, destino, limite):
    fronteira = LifoQueue()
    resultado, qtdVisitados, qtdExpandidos, arvore = self.busca(origem, destino, limite, fronteira)
    self.mostraResultado(resultado, qtdVisitados, qtdExpandidos, arvore)

  def busca(self, origem, destino, limite, fronteira):
    atual = Estado(origem, None, 0)
    fronteira.put(atual)
    visitados = set()
    visitados.add(atual.cidade)
    qtdVisitados = 1
    qtdExpandidos = 0
    ##### As próximas linhas são desnecessárias caso não se deseje ver a árvore no final da execução
    arvore = Tree()
    arvore.create_node(atual.cidade, atual)
    #####
    resultado = None
    # A única diferença entre a busca em profundidade limitada e o controle do nível da árvore por meio da variável n que é um novo critério no while para continuar a busca
    while not fronteira.empty() and resultado == None:
      atual = fronteira.get()
      qtdExpandidos += 1
      resultado, fronteira, visitados, qtdVisitados, arvore = self.geraFilhos(atual, destino, fronteira, visitados, qtdVisitados, arvore, limite)
    return resultado, qtdVisitados, qtdExpandidos, arvore

#Implementação do método geraFilhos. Este método recebe um nodo da árvore como parâmetro e gera os filhos possíveis consultando a lista de adjacências.
#Ele também recebe como parâmetro a cidade de destino para saber se chegou ao resultado ou não e o limite para verificar se atingiu o limite estabelecido.
  def geraFilhos(self, atual,  destino, fronteira, visitados, qtdVisitados, arvore, limite):
    cidades = self.rotas.get(atual.cidade)
    for c in cidades:
      if (c==destino):
        qtdVisitados += 1
        novo = Estado(c, atual, atual.nivel+1)
        visitados.add(c)
        # Esta linha é desnecessária caso não se deseje ver a árvore no final da execução
        arvore.create_node(c, novo, parent=atual)
        return novo, fronteira, visitados, qtdVisitados, arvore
      else:
        # Se os dois ifs abaixo estiverem comentados, a busca vai gerar estados repetidos na árvore, inclusive filhos que serão iguais ao pai de um nó (avô).
        # Se o primeiro if estiver comentado e o segundo if não a busca não vai gerar nenhum estado repetido no árvore
        # Se o segundo if estiver comentando e o primeiro não, a busca vai gerar estados repetidos na árvore, mas não gerará filhos iguais ao avô.

        #if atual.pai == None or c != atual.pai.cidade:
        if c not in visitados:
          qtdVisitados += 1
          visitados.add(c)
          novo = Estado(c, atual, atual.nivel+1)
          # Esta linha é desnecessária caso não se deseje ver a árvore no final da execução
          arvore.create_node(c, novo, parent=atual)
          if atual.nivel + 1 < limite:
            fronteira.put(novo)
    return None, fronteira, visitados, qtdVisitados, arvore


#Implementação do método que apresenta os resultados da busca. O resultado está na ordem inversa pois ele é descoberto retornando do estado final até o estado inicial,
#consultando o atributo pai da classe Estado. Para apresentá-lo na ordem correta, basta inserir os estados em uma lista,
#em vez de mostrá-los diretamente e depois mostrar a lista na ordem inversa.
  def mostraResultado(self, resultado, qtdVisitados, qtdExpandidos, arvore):
    if (resultado==None):
      print('Solução não encontrada.')
    else:
      print('***Rota encontrada***')
      while (resultado != None):
        print(resultado.cidade)
        resultado = resultado.pai
    print('Estados visitados: ',qtdVisitados)
    print('Estados expandidos: ',qtdExpandidos)
    print('****Árvore gerada****')
    arvore.show()

class BuscaAprofundamentoIterativo(BuscaProfundidadeLimitada):

  def __init__(self):
    super().__init__()

  def realizaBusca(self, origem, destino):
    for i in range(1,10):
      fronteira = LifoQueue()
      print("****limite ",i," ***")
      resultado, qtdVisitados, qtdExpandidos, arvore = self.busca(origem, destino, i, fronteira)
      if resultado != None:
        self.mostraResultado(resultado, qtdVisitados, qtdExpandidos, arvore)
        break;

algbusca = BuscaAprofundamentoIterativo()
algbusca.realizaBusca('Porto Alegre','Manaus')