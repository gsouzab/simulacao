# coding: utf-8

import random
import math
from queue import PriorityQueue

'''
Tipos de estados possiveis do Host
- Limpo (suscetivel)
- Infectado
'''
HOST_LIMPO = 1
HOST_INFECTADO = 2

'''
Tipos de eventos possiveis
- Infeccao
- Limpeza
'''
EVENTO_INFECCAO = 1
EVENTO_LIMPEZA = 2

'''
Tipos de vizinhancas
- Clique
- ?
'''
VIZINHANCA_CLIQUE = 1

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
		self.estado = HOST_LIMPO
		self.vizinhos = []

	def calcularVizinhosInfectados(self):
		vizinhosInfectados = 0
		for vizinho in self.vizinhos:
			if vizinho.estado == HOST_INFECTADO:
				vizinhosInfectados += 1

		return vizinhosInfectados

	def ehVizinho(self, host):
		for vizinho in self.vizinhos:
			if vizinho == host:
				return True

		return False

class Simulacao:

	def __init__(self, N, taxaEndogena, taxaExogena, taxaLimpeza, tipoVizinhanca, verbose=False):
		self.N = N
		self.taxaEndogena = taxaEndogena
		self.taxaExogena = taxaExogena
		self.taxaLimpeza = taxaLimpeza
		self.tipoVizinhanca = tipoVizinhanca
		self.tempoSimulacao = 0
		self.filaEventos = PriorityQueue()
		self.listaHosts = []
		self.hostsInfectados = 0
		self.A = 0
		self.infectadosPorIteracao = []
		self.verbose = verbose

		for i in range(self.N):
			novoHost = Host()
			self.listaHosts.append(novoHost)
			self.filaEventos.put(self.criarEvento(EVENTO_INFECCAO, novoHost))


		for i in range(self.N):
			self.gerarVizinhanca(i, tipoVizinhanca)

	def gerarVizinhanca (self, indexHostAtual, tipoVizinhanca):
		if tipoVizinhanca == VIZINHANCA_CLIQUE:
			for i in range(self.N):
				if i != indexHostAtual:
					self.listaHosts[indexHostAtual].vizinhos.append(self.listaHosts[i])

	def reagendarEventosVizinhos(self, host):
			filaEventosTemp = PriorityQueue()

			while not self.filaEventos.empty():
				evento = self.filaEventos.get()
				if evento.tipo == EVENTO_INFECCAO and host.ehVizinho(evento.host):
					evento.tempoDeChegada = self.gerarTempo(evento.tipo, evento.host) + self.tempoSimulacao
				filaEventosTemp.put(evento)

			self.filaEventos = filaEventosTemp

	def tratarEvento(self, evento):
		self.atualizaParametros(evento)
		hostSelecionado = evento.host

		if evento.tipo == EVENTO_INFECCAO:
			hostSelecionado.estado = HOST_INFECTADO
			self.filaEventos.put(self.criarEvento(EVENTO_LIMPEZA, hostSelecionado))

		elif evento.tipo == EVENTO_LIMPEZA:
			hostSelecionado.estado = HOST_LIMPO
			self.filaEventos.put(self.criarEvento(EVENTO_INFECCAO, hostSelecionado))
				
		self.reagendarEventosVizinhos(hostSelecionado)

	def criarEvento(self, tipo, host):
		tempoChegada = self.gerarTempo(tipo, host) + self.tempoSimulacao
		return Evento(tempoChegada, tipo, host)

	def gerarTempo(self, tipo, host=None):
		u = random.uniform(0, 1)

		if tipo == EVENTO_INFECCAO:
			vizinhosInfectados = host.calcularVizinhosInfectados()
			taxa = self.taxaExogena * (self.taxaEndogena**vizinhosInfectados)			
		elif tipo == EVENTO_LIMPEZA:
			taxa = self.taxaLimpeza

		tempo = -1*math.log(u)/taxa
		return tempo

	def atualizaParametros(self, evento):
		if evento.tipo == EVENTO_LIMPEZA:
			self.hostsInfectados -= 1
		else:
			self.hostsInfectados += 1
		
		#self.A += self.hostsInfectados * (evento.tempoDeChegada - self.tempoSimulacao)
		self.tempoSimulacao = evento.tempoDeChegada
		self.infectadosPorIteracao.append(self.hostsInfectados)
		
	def intervaloDeConfianca(self, iteracoes):		
		if iteracoes <= 1:
			return False

		#media = somatorio Xi (n° infectados na iteracao i) / N (iteracoes)
		media = float(sum(self.infectadosPorIteracao)) / iteracoes		
		variancia = sum(map(lambda x: (x - media) ** 2, self.infectadosPorIteracao)) / (iteracoes - 1)
		ic = 2 * 1.96 * math.sqrt(variancia) / math.sqrt(iteracoes)
		return ic < 0.1 * media

	def simular(self, limiteIteracoes):
		i = 0
		
		while i <= limiteIteracoes and not self.intervaloDeConfianca(i):
			evento = self.filaEventos.get()
			self.tratarEvento(evento)
			# print ('[Iteração' , i, '] Tempo de simulação: ', self.tempoSimulacao, 'Infectados: ', simulacao.hostsInfectados)

			i += 1

		# print float(sum(self.infectadosPorIteracao)) / i		
		# return 0
		return float(sum(self.infectadosPorIteracao)) / i

if __name__ == '__main__':

	def intervaloDeConfianca(iteracoes):		
		if iteracoes <= 1:
			return False

		#media = somatorio Xi (n° infectados na iteracao i) / N (iteracoes)
		media = float(sum(mediasDeRodadas)) / iteracoes		
		variancia = sum(map(lambda x: (x - media) ** 2, mediasDeRodadas)) / (iteracoes - 1)
		ic = 2 * 1.96 * math.sqrt(variancia) / math.sqrt(iteracoes)
		return ic < 0.1 * media

	C = 1
	_gama = 0.6
	_mi = 1
	limiteIteracoes = 1000

	while _gama <= 2.6:
		N = 10
		_lambda = float(C) / N
		while N <= 60:
			i = 0
			mediasDeRodadas = []
			while i <= limiteIteracoes and not intervaloDeConfianca(i):
				simulacao = Simulacao(N , _gama, _lambda, _mi, VIZINHANCA_CLIQUE, verbose = True)
				#executar a simulaçao vazias vezes, o slide se refere a multiplas rodadas batch
				# a = simulacao.simular(1000)
				# print(a)
				mediasDeRodadas.append(simulacao.simular(1000))
				i += 1
			print('gama: ', _gama,'; N: ', N,'; Media: ', float(sum(mediasDeRodadas)) / i / N, 'iteracoes: ', i)
			N += 2
		_gama += 0.5
	
