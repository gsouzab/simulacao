# coding: utf-8

import random
import math
from queue import PriorityQueue

# Sugestões:
# Fazer a simulação a partir de uma lista de adjacencias. Com isso podemos simular vários grafos e não só a clique
# Considerar apenas INFECCOES, sem diferenca de exogena e endogena

'''
Tipos estados possiveis
Limpo (e por consquencia suscetivel)
Infectado
''' 
LIMPO = 1
INFECTADO = 2

'''
Tipos de eventos possiveis
Infeccao exogena
Infeccao endogena
Limpeza
''' 
INFECCAO_EXOGENA = 1
INFECCAO_ENDOGENA = 2
LIMPEZA = 3

class Evento:

	def __init__(self, tempoDeChegada, tipo, host=None):
		self.tempoDeChegada = tempoDeChegada
		self.tipo = tipo
		self.host = host

	def __gt__(self, other):
		return self.tempoDeChegada > other.tempoDeChegada

	def __ge__(self, other):
		return self.tempoDeChegada >= other.tempoDeChegada

	def __lt__(self, other):
		return self.tempoDeChegada < other.tempoDeChegada

	def __le__(self, other):
		return self.tempoDeChegada <= other.tempoDeChegada

	def __eq__(self, other):
		return self.tempoDeChegada == other.tempoDeChegada

	def __ne__(self, other):
		return self.tempoDeChegada != other.tempoDeChegada

class Host:
	
	def __init__(self):
		self.estado = LIMPO

class Simulacao:

	def __init__(self, N, taxaEndogena, taxaExogena, taxaLimpeza):
		self.N = N
		self.taxaEndogena = taxaEndogena
		self.taxaExogena = taxaExogena
		self.taxaLimpeza = taxaLimpeza
		self.tempoSimulacao = 0
		self.filaEventos = PriorityQueue()
		self.listaHosts = []
		self.d = 0
		self.mediaInfectados = 0
		self.A = 0
		self.listaMediaDeInfectados = []
		
		self.filaEventos.put(self.criarEvento(INFECCAO_EXOGENA))

		'''
		Gera N tempos possíveis infecções exógenas
		Escolhe o menor tempo dentre as gerados
		Cria um evento com o tempo escolhido
		'''
		temposDeEvento = []
		for i in range(self.N):
			self.listaHosts.append(Host())
			temposDeEvento.append(self.gerarTempo(INFECCAO_EXOGENA))
		self.filaEventos.put(Evento(min(temposDeEvento), INFECCAO_EXOGENA))
		
		# for i in range(self.N):
		# 	self.listaHosts.append(Host())
		# 	self.filaEventos.put(self.criarEvento(INFECCAO_EXOGENA, self.listaHosts[i]))

	def tratarEvento(self, evento):
		if evento.tipo == INFECCAO_EXOGENA or evento.tipo == INFECCAO_ENDOGENA:
			# Sorteia host das adjacencias e se estiver vulnerável:
			hostSelecionado = random.choice(self.listaHosts)
			if hostSelecionado.estado == LIMPO:
				# Infecta
				hostSelecionado.estado = INFECTADO
				# Atualiza parametros e metricas da simulação
				self.atualizaParametros()
				# Agenda infecção endogena+exogena ou cura (o que vier primeiro)
				tempoCura = self.gerarTempo(LIMPEZA)
				tempoInfeccao = self.gerarTempo(INFECCAO_ENDOGENA)
				if tempoCura < tempoInfeccao:
					self.filaEventos.put(self.criarEvento(LIMPEZA, hostSelecionado))
				else:
					self.filaEventos.put(self.criarEvento(INFECCAO_ENDOGENA, hostSelecionado))
			else:
				# no caso do host já estar infectado, só gera uma nova infecção
				self.filaEventos.put(self.criarEvento(INFECCAO_ENDOGENA))
		else: 
			#evento.tipo == LIMPEZA
			# Cura host especificado no evento
			evento.host.estado = LIMPO
			# Atualiza parametros e metricas da simulação
			self.atualizaParametros()
			# Agenda próxima infecção endógena+exogena
			self.filaEventos.put(self.criarEvento(INFECCAO_EXOGENA))

	def criarEvento(self, tipo, host=None):
		tempoChegada = self.gerarTempo(tipo) + self.tempoSimulacao
		return Evento(tempoChegada, tipo, host)

	def gerarTempo(self, tipo):
		u = random.uniform(0, 1)

		'''
		if tipo == INFECCAO_ENDOGENA:
			tempo = -1*math.log(u)/self.taxaEndogena
		'''
		if tipo == INFECCAO_EXOGENA or tipo == INFECCAO_ENDOGENA: 
			taxa = self.taxaExogena * (self.taxaEndogena**self.d)
			tempo = -1*math.log(u)/taxa
		elif tipo == LIMPEZA: 
			tempo = -1*math.log(u)/self.taxaLimpeza

		return tempo

	def atualizaParametros(evento):
		self.A += self.d*(evento.tempoDeChegada - tempoSimulacao)
		self.tempoSimulacao = evento.tempoDeChegada
		self.mediasDeInfectados.put(float(self.A) / self.tempoSimulacao)
		if evento.tipo == LIMPEZA:
			self.d -= 1
		else:
			self.d += 1

	def intervaloDeConfianca(iteracoes):
		media = sum(self.mediasDeInfectados) / iteracoes
		variancia = (map(lambda x: x - media, lista))**2 / (iteracoes - 1)
		ic = 2 * 1.96 * math.sqrt(variancia) / math.sqrt(iteracoes)
		if ic < 0.1 * media:
			return true
		else:
			return false

	def simular(self, limiteIteracoes):
		i = 1
		while i <= limiteIteracoes and !self.intervaloDeConfianca(i) :
			print('[Iteração' , i, '] Tempo de simulação: ', self.tempoSimulacao, 'Infectados: ', self.d)
			evento = self.filaEventos.get()
			self.tratarEvento(evento)
			i += 1 
		return sum(self.mediasDeInfectados) / i-1

def intervaloDeConfianca(iteracoes):
		media = sum(mediasDeRodadas) / iteracoes
		variancia = (map(lambda x: x - media, mediasDeRodadas))**2 / (iteracoes - 1)
		ic = 2 * 1.96 * math.sqrt(variancia) / math.sqrt(iteracoes)
		if ic < 0.1 * media:
			return true
		else:
			return false

if __name__ == '__main__':
	N = 20
	C = 1
	_lambda = float(C) / float(N)
	_gama = 0.9
	_mi = 1
	mediasDeRodadas = []

	simulacao = Simulacao(N , _gama, _lambda, _mi)

	i = 1
	while i <= 100 and !intervaloDeConfianca(i):
		mediasDeRodadas.put(simulacao.simular(1000))
		i += 1

	''' 
	for i in range(N):
		evento = simulacao.filaEventos.get() 
		print evento.tempoDeChegada, evento.tipo
	'''






















