import random
import math
from Queue import PriorityQueue

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

	def __init__(self, tempoDeChegada, tipo, host):
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
		
		for i in range(self.N):
			self.listaHosts.append(Host())
			self.filaEventos.put(self.criarEvento(INFECCAO_EXOGENA, self.listaHosts[i]))

	def tratarEvento(self, evento):
		return 0
		#if evento.tipo == INFECCAO_EXOGENA:

	def criarEvento(self, tipo, host):
		tempoChegada = self.gerarTempo(tipo)
		return Evento(tempoChegada, tipo, host)

	def gerarTempo(self, tipo):
		u = random.uniform(0, 1)

		if tipo == INFECCAO_ENDOGENA:
			tempo = -1*math.log(u)/self.taxaEndogena
		elif tipo == INFECCAO_EXOGENA: 
			tempo = -1*math.log(u)/self.taxaExogena
		elif tipo == LIMPEZA: 
			tempo = -1*math.log(u)/self.taxaLimpeza

		return tempo

	def simular(self, limiteIteracoes):
		return 0

if __name__ == '__main__':
	N = 10
	C = 1
	_lambda = float(C)/ float(N)
	_gama = 0.1
	_mi = 1

	simulacao = Simulacao(N , _gama, _lambda, _mi)

	''' 
	for i in range(N):
		evento = simulacao.filaEventos.get() 
		print evento.tempoDeChegada, evento.tipo
	'''






















