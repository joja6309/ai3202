import  sys, re
from numpy import *
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *

try:
    from IPython import embed
except:
    pass


def joint_tuple(network, var, uppercase = False):
	for node in network.nodes:
		if node.id == 0:
			pollution = node
		if node.id == 1:
			smoker = node
		if node.id == 2:
			cancer = node
		if node.id == 3:
			xray = node
		if node.id == 4:
			dyspnoea = node

	if uppercase:
		if var == 'P':
			input = pollution
		elif var == 'S':
			input = smoker
		elif var == 'C':
			input = cancer
		elif var == 'X':
			input = xray
		elif var == 'D':
			input = dyspnoea
		
			
	else:
		if var == 'p':
			input = (pollution, True)
		elif var == 's':
			input = (smoker, True)
		elif var == 'c':
			input = (cancer, True)
		elif var == 'x':
			input = (xray, True)
		elif var == 'd':
			input = (dyspnoea, True)
		elif var == '~p':
			input = (pollution, False)
		elif var == '~s':
			input = (smoker, False)
		elif var == '~c':
			input = (cancer, False)
		elif var == '~x':
			input = (xray, False)
		elif var == '~d':
			input = (dyspnoea, False)
		
			

	return input
def compute_dis(engine, jointVarArray):
	from itertools import product 
	n = len(jointVarArray)
	newArray = list([jointVarArray]*2**n)
	allorderings = list(product([False, True], repeat = n))
	permutationList = []
	for i in range(len(newArray)):
		temp = []
		for j in range(n):
			temp.append((newArray[i][j], allorderings[i][j]))
		permutationList.append(temp)

	for item in permutationList:
		prob = jointComp(engine, item)
		jointstr = ""
		for twople in item:
			if twople[0].name == 'pollution':
				if twople[1]:
					jointstr += "pollution = low, "
				else:
					jointstr += "pollution = high, "
			else:
				if twople[1]:
					jointstr += twople[0].name + " = true, "
				else:
					jointstr += twople[0].name + " = false, "
		print "Joint probability of " + jointstr + "is " + str(prob)		
def jointComp(engine, item):
	itemCopy = copy.copy(item)
	if len(itemCopy) == 2:
		tupleA, tupleB = itemCopy
		return compute_conditional_probability(engine, tupleB, [tupleA], False) * margins(engine, tupleA[0], False, tupleA[1])

	firstElement = itemCopy.pop(0)
	return compute_conditional_probability(engine, firstElement, itemCopy, False) * jointComp(engine, itemCopy)
def build_network():
	numNodes = 5
	cancer_node = BayesNode(2, 2, name="Cancer")
	xray_node = BayesNode(3, 2, name="X-ray")
	d_node = BayesNode(4, 2, name="Dyspnoea")
	p_node = BayesNode(0, 2, name="Pollution")
	s_node = BayesNode(1, 2, name="Smoker")

	p_node.add_child(cancer_node)
	s_node.add_child(cancer_node)

	cancer_node.add_parent(p_node)
	cancer_node.add_parent(s_node)
	cancer_node.add_child(xray_node)
	cancer_node.add_child(d_node)

	xray_node.add_parent(cancer_node)
	d_node.add_parent(cancer_node)

	nodes = [p_node, s_node, cancer_node, xray_node, d_node]

	pDistribution = DiscreteDistribution(p_node)
	index = pDistribution.generate_index([],[])
	pDistribution[index] = 0.1, 0.9
	p_node.set_dist(pDistribution)

	sDistribution = DiscreteDistribution(s_node)
	index = sDistribution.generate_index([],[])
	sDistribution[index] = 0.7, 0.3
	s_node.set_dist(sDistribution)
	dist = zeros([p_node.size(), s_node.size(), cancer_node.size()], dtype=float32)
	dist[0,0,] = [0.98, 0.02] 
	dist[0,1,] = [0.95, 0.05] 
	dist[1,0,] = [0.999, 0.001] 
	dist[1,1,] = [0.97, 0.03] 
	cDistribution = ConditionalDiscreteDistribution(nodes=[p_node, s_node, cancer_node], table=dist)
	cancer_node.set_dist(cDistribution)
	dist = zeros([cancer_node.size(), xray_node.size()], dtype=float32)
	dist[0,] = [0.8, 0.2] 
	dist[1,] = [0.1, 0.9] 
	xDistribution = ConditionalDiscreteDistribution(nodes=[cancer_node, xray_node], table = dist)
	xray_node.set_dist(xDistribution)
	dist = zeros([cancer_node.size(), d_node.size()], dtype=float32)
	dist[0,] = [0.7, 0.3] 
	dist[1,] = [0.35, 0.65] 
	dDistribution = ConditionalDiscreteDistribution(nodes=[cancer_node, d_node], table = dist)
	d_node.set_dist(dDistribution)
	return BayesNet(nodes)

def Comp_conditional(network, var):
	for node in network.nodes:
		if node.id == 0:
			pollution = node
		if node.id == 1:
			smoker = node
		if node.id == 2:
			cancer = node
		if node.id == 3:
			xray = node
		if node.id == 4:
			dyspnoea = node
	if var == 'p':
		input = (pollution, True)
	elif var == 's':
		input = (smoker, True)
	elif var == 'c':
		input = (cancer, True)
	elif var == 'x':
		input = (xray, True)
	elif var == 'd':
		input = (dyspnoea, True)
	elif var == '~p':
		input = (pollution, False)
	elif var == '~s':
		input = (smoker, False)
	elif var == '~c':
		input = (cancer, False)
	elif var == '~x':
		input = (xray, False)
	elif var == '~d':
		input = (dyspnoea, False)
	
	return input
def margins(engine, input, printable=True, returnable=True):
	Q = engine.marginal(input)[0]

	if input.name == 'pollution':
		tResult = 'low'
		fResult = 'high'
	else:
		tResult = 'true'
		fResult = 'false'

	true = Q.generate_index([True], range(Q.nDims))
	if printable:
		print "Marginal probability of", input.name + " = " + tResult + ":", Q[true]
	false = Q.generate_index([False], range(Q.nDims))
	if printable:
		print "Marginal probability of", input.name + " = " + fResult + ":", Q[false]

	if returnable:
		return Q[true]
	else:
		return Q[false]
def compute_conditional_probability(engine, input, condVarArray, printable=True):
	# Dealing with given conditions
	for var, truefalse in condVarArray:
		engine.evidence[var] = truefalse
		if var.name == 'pollution':
			if truefalse == True:
				condStr = 'pollution = low '
			else:
				condStr = 'pollution = high '
		else:
			if truefalse:
				condStr = var.name + " = true "
			else:
				condStr = var.name + " = false "
	
	# Dealing with unknown variable
	uVar, truefalse = input
	Q = engine.marginal(uVar)[0]
	index = Q.generate_index([truefalse],range(Q.nDims))
	if uVar.name == 'pollution':
		if truefalse:
			desiredResult = 'low'
		else:
			desiredResult = 'high'
	else:
		if truefalse:
			desiredResult = "true"
		else:
			desiredResult = "false"

	if printable:
		print "Probability of", uVar.name + " = " + desiredResult + " |", condStr + "is", Q[index]

	return Q[index]

# This is where the magic happens