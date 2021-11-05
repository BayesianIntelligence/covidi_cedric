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

                if node.name() == 'ci_pulse_rate_t0':
                    print ('    Converting ci_pulse_rate_t0 to ci_func_car_t0')
                    beats = param_dict[node.name()]
                    status = ''
                    if beats < 45 and beats > 199:
                        status = 'abnormal'
                    else:
                        status = 'normal'
                    #TODO Check with Yue, assume greater than 95 is low
                    enterFinding(net.node('ci_func_car_t0'), status)
                if node.name() == 'ci_oxygen_saturation_t0':
                    print ('    Converting ci_oxygen_saturation_t0 to ci_hypoxaemia_t0')
                    #If SaO2 is between 90-95%, 'ci_hypoxaemia_t0' is 'moderate'. If SaO2 is <=89%, 'ci_hypoxaemia_t0' is 'severe'.
                    sao2 = param_dict[node.name()]
                    status = ''
                    if sao2 <= 0.89:
                        status = 'severe'
                    else:
                        status = 'moderate'
                        #TODO Check with Yue, assume greater than 95 is low
                    enterFinding(net.node('ci_hypoxaemia_t0'), status)
                if node.name() == 'CREATININE':
                    print ('    CONVERT CRT INTEGER TO DISCRETISATION')
                if node.name() == 'NEUTRO' and 'LYMPH':
                    print ('    CALC to NLR and CONVERT NLR int to DISCRETISATION')
                if node.name() == 'NEUTRO' and 'LYMPH':
                    print ('    CALC to NLR and CONVERT NLR int to DISCRETISATION')
                if node.name() == 'NEUTRO' and not 'LYMPH':
                    print ('    CONVERT NEUTRO int to DISCRETISATION')
                if node.name() == 'LYMPH' and not 'NEUTRO':
                    print ('    CONVERT LYMPH int to DISCRETISATION')
                else:
                    enterFinding(node, param_dict[node.name()])
                print ('output: ', node.beliefs(), file=sys.stderr)
            except:
                print ('    exception caught!', file=sys.stderr)
                pass
            for state in node.states():
                print ('    state name: ' + state.name(), file=sys.stderr)

    #add meta data: the bn name and version, to nested dictionary
    #TODO remove this line and replace with user defined variable in the netica BN net_version
    net.add_net_usr_field('net_version', '1')
    #TODO remove this line and replace with user defined variable in the netica BN net_name
    net.add_net_usr_field('net_name', 'progression model')
    print ('API request made for BN name: ' + net.get_net_usr_field('net_name') + ' with version: ' + net.get_net_usr_field('net_version'))
    nested_dictionary['model'] = {}
    nested_dictionary['model']['name'] = net.get_net_usr_field('net_name')
    nested_dictionary['model']['version'] = net.get_net_usr_field('net_version')
    nested_dictionary['data'] = {}

    #update output dictionary
    for node in net.nodes():
        nested_dictionary['data'][node.name()] = {}
        index = 0
        for state in node.states():
            if state.name() == '':
                nested_dictionary['data'][node.name()]['s'+str(index)] = node.beliefs()[index]
            else:
                nested_dictionary['data'][node.name()][state.name()] = node.beliefs()[index]
            index+=1
    return nested_dictionary

def enterFinding(node, value):
    if node.type() == Node.DISCRETE_TYPE: node.finding(state=value)
    if node.type() == Node.CONTINUOUS_TYPE: node.finding(value=value)

if __name__ == '__main__':
    updateBn(param_dict)
