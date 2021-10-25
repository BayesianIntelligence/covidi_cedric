import _env,csv,math 
from bni_netica import *

bn_model = 'progression5.trained.dne'

nested_dictionary = { }

def updateBn(param_dict):
	print('Running model with output: {}'.format(param_dict), file=sys.stderr)
	
	net = Net(bn_model)
	net.retractFindings()
	#pass parameter dictionary to set evidence
	output_test_string = "Values set: "
	for node in net.nodes():
		if node.name() in param_dict:
			try:
				print ('setting evidence for node: ' + node.name() + ' with value: ', param_dict[node.name()], file=sys.stderr)
				enterFinding(node, param_dict[node.name()])
				print ('output: ', node.beliefs(), file=sys.stderr)
			except:
				print ('    exception caught!', file=sys.stderr)
				pass
			for state in node.states():
				print ('    state name: ' + state.name(), file=sys.stderr)
			
	#update output dictionary
				
	for node in net.nodes():
		nested_dictionary[node.name()] = {}
		index = 0
		for state in node.states():
			nested_dictionary[node.name()][state.name()] = node.beliefs()[index]
			index+=1
				
	return nested_dictionary
	
	
def enterFinding(node, value):
    if node.type() == Node.DISCRETE_TYPE: node.finding(state=value)
    if node.type() == Node.CONTINUOUS_TYPE: node.finding(value=value)

if __name__ == '__main__':
    updateBn(param_dict)