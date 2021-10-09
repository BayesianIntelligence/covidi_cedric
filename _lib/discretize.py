import math, glob, os
from bni_netica import *


setLicense('+Site/MonashU/120,310-6-AS/47037')


for fn in ['busPatronage.dne']:#,'DARTPatronage.dne','OtherPatronage.dne','School BusPatronage.dne','SmartbusPatronage.dne','TelebusPatronage.dne','University feedersPatronage.dne']:

	net = Net('data/'+fn)#TramPatronage.dne')

	for node in net.nodes():
		states = node.stateNames()
		if states[0].split('_')[0] == 's1':
			name = node.name()
			title = node.title()
			parents = node.parents()
			children = node.children()
			levels = []
			levels.append(states[0].split('_')[1])
			for state in states:
				levels.append(state.split('_')[2])
			levels = [0 if ele=='below' else net.INFINITY if ele=='up' else round(float(ele), 2 - int(math.floor(math.log10(abs(float(ele))))) - 1) for ele in levels]
			
			node.removeChildren(children)
			node.remove()
			
			new = net.addNode(name, levels)
			new.title(title)
			new.addParents(parents)
			new.addChildren(children)
			
	net.write('bns/'+fn)


