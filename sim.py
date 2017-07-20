import random
import math
from Queue import PriorityQueue
# as taxas são sempre calculadas na hora de criação do evento. tem como fazer um array onde é passado um valor a ser calculado?

# procurar como fazer log das informações

# confirmar como são as taxas

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

	def __init__(self, tempoDeChegada, tipo):
		self.tempoDeChegada = tempoDeChegada
		self.tipo = tipo

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
	
	def __init(self):
		self.estado = LIMPO

class Simulacao:

	__init__(self, N, taxaEndogena, taxaExogena, taxaLimpeza):
		self.N = N
		self.taxaEndogena = taxaEndogena
		self.taxaExogena = taxaExogena
		self.taxaLimpeza = taxaLimpeza
		self.filaEventos = PriorityQueue()
		
		for i in range(self.N):
			self.filaEventos.put(Evento(aaa, INFECCAO_EXOGENA))
		


	def criaEvento(tempoAtual, tipo):
		tempo = self.geraTempo(taxas[tipo])

	def geraTempo(taxa):
		u = random.uniform(0, 1)
		tempo = -1*math.log(u)/taxa
		return tempo

	def simulacao:
		N = 8 # número inicial de pessoas na clique
		d = 0 # nenhuma pessoa infectada
		# cria e adiciona NOVA CHEGADA DE PESSOA(S) na lista de eventos
		# cria e adiciona NOVA INFECÇÃO na lista de eventos
		while N < 60:
			if evento.tipo == "chegada":
				N++
				# cria e adiciona NOVA CHEGADA DE PESSOA(S) na lista de eventos
			else if evento.tipo == "infeccao":
				d++
				# cria e adiciona NOVA CURA na lista de eventos
				# cria e adiciona NOVA INFECÇÃO na lista de eventos (será ?)
			else: # evento.tipo == "cura"
				d--
				# cria e adiciona NOVA INFECÇÃO na lista de eventos

	def variasSimulacoes:
		self.simulacao()
		loops = 1
		while(!self.testaConvergencia()	or loops < 100)
			loops++
			self.simulacao()

	def testaConvergencia:
		# a ideia era usar o teste de intervalo de confiança, mas o problema é em que parametro usar o teste
		# usar no numero medio de infectados em N = 60?

		#calculo de intervalo de confia

		# somar vetor de medias de infectados para N = 60 e dividir tudo pelo número de vezes que rodou a simulacao (M)
		mediaAmostral = vetor.sum() / M
		# subtrair a media amostral de cada item do vetor de medias de infectados para N = 60, somar tudo e dividir tudo pelo número de vezes que rodou a simulacao menos 1 (M - 1)
		variancaAmostral = sum(vetor - vetor(mediaAmostral))**2 / (M - 1) 
		#intervalo de confianca
		intervaloDeConfianca = ( 2 * 1.96 * math.sqrt(variancaAmostral) ) / math.sqrt(M)

		if(intervaloDeConfianca < mediaAmostral * 0.1):
			return true
		else:
			return false



























