# coding: utf-8

import random
import math
from Queue import PriorityQueue

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
		self.tempoSimulacao = evento.tempoDeChegada
		hostSelecionado = evento.host

		if evento.tipo == EVENTO_INFECCAO:
			hostSelecionado.estado = HOST_INFECTADO
			self.hostsInfectados += 1
			self.filaEventos.put(self.criarEvento(EVENTO_LIMPEZA, hostSelecionado))

		elif evento.tipo == EVENTO_LIMPEZA:
			hostSelecionado.estado = HOST_LIMPO
			self.hostsInfectados -= 1
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

	def simular(self, limiteIteracoes):
		i = 0
		while i < limiteIteracoes:
			print '[Iteração' , i, '] Tempo de simulação: ', self.tempoSimulacao, 'Infectados: ', simulacao.hostsInfectados
			evento = self.filaEventos.get()
			self.tratarEvento(evento)
			i += 1
		return 0

if __name__ == '__main__':
	
	N = 50
	C = 1
	_lambda = float(C)/ float(N)
	_gama = 1.1
	_mi = 1

	simulacao = Simulacao(N , _gama, _lambda, _mi, VIZINHANCA_CLIQUE, verbose = True)
	simulacao.simular(1000)
