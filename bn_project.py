import _env,csv,math
from bni_netica import *

bn_model = 'progression5.trained.dne'

nested_dictionary = { }

def updateBn(param_dict):
    print('Running model with input: {}'.format(param_dict), file=sys.stderr)

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
                    beats = int(param_dict[node.name()])
                    status = ''
                    if beats < 45 or beats > 199:
                        status = 'abnormal'
                        enterFinding(net.node('ci_func_car_t0'), status)
                        print ('    Entering findings for: ci_func_car_t0, with state: ', status)
                elif node.name() == 'ci_oxygen_saturation_t0':
                    print ('    Converting ci_oxygen_saturation_t0 to ci_hypoxaemia_t0')
                    #If SaO2 is between 90-95%, 'ci_hypoxaemia_t0' is 'moderate'. If SaO2 is <=89%, 'ci_hypoxaemia_t0' is 'severe'.
                    sao2 = float(param_dict[node.name()])
                    status = 'normal'
                    if float(sao2) <= 0.89:
                        status = 'verylow'
                        enterFinding(net.node('ci_hypoxaemia_t0'), status)
                        print ('    Entering findings for: ci_hypoxaemia_t0, with state: ', status)
                    elif float(sao2) <= 0.95:
                        status = 'low'
                        enterFinding(net.node('ci_hypoxaemia_t0'), status)
                        print ('    Entering findings for: ci_hypoxaemia_t0, with state: ', status)
                        #DOUBLE CHECK WITH SM - DO we ignore sa02 > 0.95 or do we set it to normal
                elif node.name() == 'ci_creat_t0':
                    print ('    Converting ci_creat_t0 to ci_intravas_volume_t0 OR ci_end_organ_perf_t0')
                    crt = int(param_dict[node.name()])
                    kidney_disease_status = ""
                    if net.node('ci_chronic_kidney_disease_bg').name() in param_dict:
                        kidney_disease_status = param_dict[net.node('ci_chronic_kidney_disease_bg').name()]
                    if crt > 105:
                        enterFinding(net.node('ci_end_organ_perf_t0'), 'low')
                        print ('    Entering findings for: ci_end_organ_perf_t0, with state: low')
                    elif crt > 90 and kidney_disease_status not in ['true', 'True', 'TRUE']:
                        enterFinding(net.node('ci_intravas_volume_t0'), 'low')
                        print ('    Entering findings : ci_intravas_volume_t0, with state: low')
                elif node.name() == 'ci_neut_t0' and 'ci_lym_t0' in param_dict:
                    print ('    combining ci_neut_t0 and ci_lym_t0 to calculate NLR')
                    nlr = float(param_dict[node.name()])/float(param_dict[net.node('ci_lym_t0').name()])
                    if nlr > 5:
                        enterFinding(net.node('ci_sys_immune_resp_t0'), 'abnormal')
                        print ('    Entering findings for: ci_sys_immune_resp_t0, with state: abnormal')
                elif node.name() == 'ci_neut_t0' and 'ci_lym_t0' not in param_dict:
                    print ('    entering finding for neutrophil only')
                    neut = param_dict[node.name()]
                    enterFinding(net.node('ci_neut_t0'), neut)
                    print ('    Entering findings for: ci_neut_t0, with state: ', neut)
                elif node.name() == 'ci_lym_t0'  and 'ci_neut_t0' not in param_dict:
                    print ('    entering finding for lymphocytes only')
                    lym = param_dict[node.name()]
                    enterFinding(net.node('ci_lym_t0'), lym)
                    print ('    Entering findings for: ci_lym_t0, with state: ', lym)
                else:
                    print ('    No translation logic found for ', node.name())
                    enterFinding(node, param_dict[node.name()])
                print ('    Node complete (but not neccessarily updated.) ', file=sys.stderr)
            except Exception as e:
                print ('    exception caught!' , e)
                pass

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
