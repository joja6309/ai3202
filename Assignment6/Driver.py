import getopt, sys, re
from numpy import *
from pbnt.Graph import *
from NetworkOperations import*
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *


try:
    from IPython import embed
except:
    pass

def main():
	arg_array,whatsLeft = getopt.getopt(sys.argv[1:], 'm:g:j:')
	Bayes_Network = build_network()
	for condition in Bayes_Network.nodes:

		if condition.id == 4:
			D_ys = condition
		elif condition.id == 3:
			X_ray = condition
		elif condition.id == 2:
			C_ncer = condition
		elif condition.id == 1:
			S_mk = condition
		elif condition.id == 0:
			P_lution = condition
	Generator = JunctionTreeEngine(Bayes_Network)
	for prob_flag, arguments in arg_array:
		if prob_flag == "-m":	#Marginal Probability 
			if arguments == 'P':
				input = P_lution
			elif arguments == 'X':
				input = X_ray
			elif arguments == 'D':
				input = D_ys
			elif arguments == 'S':
				input = S_mk
			elif arguments == 'C':
				input = C_ncer
			margins(Generator,input)
		
		elif prob_flag == "-g": #Conditional Probability
			split = arg_array.split('|')
			result, whatsLeft = split
			input = Comp_conditional(Bayes_Network, result)
			firstArray = []
			secondArray = re.findall('~?[a-z]', whatsLeft)
			for var in secondArray:
				firstArray.append(Comp_conditional(Bayes_Network, var))
			conditional_compute(Generator, input, firstArray)
		elif prob_flag == "-j": #Joint Probability 
			# separate out capitol letters first
			split = re.findall('[A-Z]', arguments)
			jointVarArray = []
			if len(split) > 0:
				if len(re.findall('~?[a-z]', arguments)) > 0:
					usage()
				for var in split:
					jointVarArray.append(joint_tuple(Bayes_Network, var, True))
				compute_dis(Generator, jointVarArray)
			else: # implies that only lower case letters were used as args.	
				split = re.findall('~?[a-z]', arguments)
				for var in split:
					jointVarArray.append(joint_tuple(Bayes_Network, var))
					out_p = ""
				for item in jointVarArray:
					if item[0].name == 'P_lution':
						if item[1]:
							out_p += "P_lution = low, "
						else:
							out_p += "P_lution = high, "
					else:
						if item[1]:
							out_p += item[0].name + " = true, "
						else:
							out_p += item[0].name + " = false, "
				print "Joint Probability of  " + out_p + "is", jointComp(Generator, jointVarArray)
		


if __name__ == "__main__":
    main()