#!/usr/bin/env python3
# Python 3.6



import random
import math

class GameState():

	def __init__(self, state=[0,0,0,0,0,0,0,0,0], actions = [0,1,2,3,4,5,6,7,8], player = 1):
		self.state = state[:]
		self.actions = actions[:]
		self.player = player

class Tictactoe():
	def __init__(self):
		pass

	def act(self,state,action):
		nextState = GameState(state.state,state.actions,state.player)
		if(state.state[action] == 0):
			nextState.state[action] = state.player
			nextState.player = -1 * state.player
			nextState.actions.remove(action)
			return nextState

	def checkWin(self,state):
		flag = 0
		for i in state.state:
			if(i == 0):
				flag = 1


		if(state.state[0] == state.state[1] and state.state[0] == state.state[2] and state.state[0] != 0):
			#win
			return state.state[0]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[3] == state.state[4] and state.state[3] == state.state[5] and state.state[3] != 0):
			#win
			return state.state[3]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[6] == state.state[7] and state.state[6] == state.state[8] and state.state[6] != 0):
			#win
			return state.state[6]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[0] == state.state[4] and state.state[0] == state.state[8] and state.state[0] != 0):
			#win
			return state.state[0]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[2] == state.state[4] and state.state[2] == state.state[6] and state.state[2] != 0):
			#win
			return state.state[2]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[0] == state.state[3] and state.state[0] == state.state[6] and state.state[0] != 0):
			#win
			return state.state[0]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[1] == state.state[4] and state.state[1] == state.state[7] and state.state[1] != 0):
			#win
			return state.state[1]# retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(state.state[2] == state.state[5] and state.state[2] == state.state[8] and state.state[2] != 0):
			#win
			return state.state[2] # retorna 1 se for o player 1 (computador), -1 se for o player -1 (humano)
		elif(flag == 1):
			#still not finished
			return -2
		else:
			#draw
			return 0


	def randomGameFrom(self,state):
		while(self.checkWin(state) == -2):
			aux = random.choice(state.actions)
			#print(state.actions)
			#print(aux)
			state = self.act(state,aux)
			'''print(state.state[0:3])
			print(state.state[3:6])
			print(state.state[6:10])
			print('\n')'''

		return self.checkWin(state)








class Node():
	def __init__(self,state,parent=None,action=None):
		self.visits = 1
		self.reward = 0.
		self.children = []
		self.state = state
		self.parent = parent
		self.actions_to_be_explored = state.actions
		self.action = action

	def addChild(self,child):
		#child = Node(state,self)
		self.children.append(child)

	def update(self,reward):
		self.reward += reward
		self.visits += 1

	def fullyExpanded(self):
		if(len(self.children) == len(self.state.actions)):
			return True
		else:
			return False

	def removeAction(self,action):
		self.actions_to_be_explored = self.actions_to_be_explored[:]
		self.actions_to_be_explored.remove(action)


def backProp(node,reward):
	while(node!=None):
		node.update(reward)
		node = node.parent

def treePolicy(node):
	'''
	if(not node.fullyExpanded()):
		if(len(node.children) > 0 and random.uniform(0,1) < .5):
			return selectChild(node)
		else:
			return expand(node)
	else:
		return selectChild(node)'''
	while(simulatedGame.checkWin(node.state) == -2): #terminal state
		if len(node.children) == 0:
			return expand(node)
		elif random.uniform(0,1) < .5:
			node = selectChild(node)
		else:
			if(not node.fullyExpanded()):
				return expand(node)
			else:
				node = selectChild(node)
	return node

def expand(node):
	global simulatedGame
	if(len(node.actions_to_be_explored) > 0):
		action = random.choice(node.actions_to_be_explored)
		node.removeAction(action)
		next_state = simulatedGame.act(node.state,action)
		newChild = Node(next_state,parent=node,action=action)
		node.addChild(newChild)
		return newChild






def selectChild(node,C=10):
	# Selecionar pela distribuicao de probabilidade do score
	#scores = []
	#scoret = 0
	#for child in node.children:
	#	score = child.reward/float(child.visits) + C * math.sqrt(2.0*math.log(node.visits)/float(child.visits))
	#	scores.append(score)
	#	scoret += score
	#for i in range(len(scores)):
	#	scores[i] = scores[i] / scoret

	#np.random.choice(np.arange(len(scores)),p=scores)

	# Selecionar o melhor

	bestScore = -100000.0
	bestChildren = []
	for child in node.children:
		score = child.reward/float(child.visits) + C * math.sqrt(2.0*math.log(node.visits)/float(child.visits))
		if(C == 0):
			score = child.reward/float(child.visits)
			print('acao: {} - visitas: {} - reward: {} - score: {}'.format(child.action, child.visits, child.reward, score))
		if(score == bestScore):
			bestChildren.append(child)
		if(score > bestScore):
			bestScore = score
			bestChildren = [child]

	return random.choice(bestChildren)


def MCTS(root):
	for iter in range(10000):
		node=treePolicy(root)
		reward=simulatedGame.randomGameFrom(node.state)
		backProp(node,reward)
	return selectChild(root,C=0)




'''
simulatedGame =  Tictactoe()
initialState = GameState()
rootNode = Node(initialState)
asd = MCTS(rootNode)'''
simulatedGame = Tictactoe()
state = GameState()
rootNode = Node(state)


def main():
	global state
	global simulatedGame
	global rootNode
	while(simulatedGame.checkWin(state) == -2):
		print(state.state[0:3])
		print(state.state[3:6])
		print(state.state[6:10])
		if(state.player == 1):
			asd = MCTS(rootNode)
			print(asd.action)
			state = simulatedGame.act(state,asd.action)
		else:
			print("Digite um local do tabuleiro (jogadas válidas: {}):".format(state.actions))
			asd = int(input(''))
			state = simulatedGame.act(state,asd)
		rootNode = Node(state)
	simulatedGame = Tictactoe()
	state = GameState()
	rootNode = Node(state)


if __name__ == '__main__':
	main()
