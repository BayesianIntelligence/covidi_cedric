import _env,csv,math
from bni_netica import *

bn_model = 'progression5.trained.dne'

nested_dictionary = { }

def updateBn(param_dict):
    print('Running model with input: {}'.format(param_dict))

    net = Net(bn_model)
    net.retractFindings()
    #pass parameter dictionary to set evidence
    output_test_string = "Values set: "
    for node in net.nodes():
        if node.name() in param_dict:
            try:
                print ('setting evidence for node: ' + node.name() + ' with value: ', param_dict[node.name()])
                if node.name() == 'ci_age_group_bg':
                    print ('    interpolating ci_age_group_bg')
                    #age could be between 0-110
                    #if less than 0 assume 0, if more than 110 assume 110
                    raw_age = int(param_dict[node.name()])
                    young_min = 0
                    young_max = 45
                    young_mid = int((young_max - young_min)/2)
                    adult_min = 46
                    adult_max = 75
                    adult_mid = int(((adult_max - adult_min)/2)+adult_min)
                    senior_min = 76
                    senior_max = 110
                    senior_mid = int(((senior_max - senior_min)/2)+senior_min)
                    if raw_age <= young_max:
                        #age bracket = young
                        if raw_age < young_min: raw_age = young_min
                        if (raw_age <= young_mid):
                            young_result = 1.0
                            adult_result = 0
                            senior_result = 0
                        else:
                            young_fraction = 1/(abs(raw_age - young_mid))
                            adult_fraction = 1/(abs(raw_age - adult_mid))
                            sum_fraction = young_fraction + adult_fraction
                            young_result = young_fraction/sum_fraction
                            adult_result = adult_fraction/sum_fraction
                            senior_result = 0
                    elif raw_age <= adult_max:
                        #age bracket = adult
                        if raw_age == adult_mid:
                            young_result = 0
                            adult_result = 1.0
                            senior_result = 0
                        elif raw_age <  adult_mid:
                            young_fraction = 1/(abs(raw_age - young_mid))
                            adult_fraction = 1/(abs(raw_age - adult_mid))
                            sum_fraction = young_fraction + adult_fraction
                            young_result = young_fraction/sum_fraction
                            adult_result = adult_fraction/sum_fraction
                            senior_result = 0
                        else:
                            adult_fraction = 1/(abs(raw_age - adult_mid))
                            senior_fraction = 1/(abs(raw_age - senior_mid))
                            sum_fraction = adult_fraction + senior_fraction
                            young_result = 0
                            adult_result = adult_fraction/sum_fraction
                            senior_result = senior_fraction/sum_fraction
                    else:
                        #age bracket = senior
                        if raw_age > senior_max: raw_age = senior_max
                        if(raw_age >= senior_mid): node.likelihoods([1.0, 0, 0])
                        else:
                            adult_fraction = 1/(abs(raw_age - adult_mid))
                            senior_fraction = 1/(abs(raw_age - senior_mid))
                            sum_fraction = adult_fraction + senior_fraction
                            young_result = 0
                            adult_result = adult_fraction/sum_fraction
                            senior_result = senior_fraction/sum_fraction
                    node.likelihoods([senior_result, adult_result,young_result])
                    print ('    setting node likelihoods: ', node.likelihoods())
                elif node.type() == Node.CONTINUOUS_TYPE:
                    print ('    Interpolating: ' + node.name() + " with value: ",  param_dict[node.name()])
                    interpolate (node, (param_dict[node.name()]))
                else:
                    print ('    Updating state directly for: ' + node.name() + " to: ",  param_dict[node.name()])
                    enterFinding(node, param_dict[node.name()])
                print ('    Node updated ')
            except Exception as e:
                print ('    exception caught!' , e, file=sys.stderr)
                pass

    #add meta data: the bn name and version, to nested dictionary
    #net.add_net_usr_field('net_version', '1')
    #net.add_net_usr_field('net_name', 'progression model')
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

#TODO I expect this to break if there is only one level
def interpolate(node, value):
    # find out what level the value sits between
    min_marker = -1
    max_marker = 0
    valid_value = False
    levels = []
    for step in node.levels():
        #print (step)
        if min_marker == -1:
            min_marker = step
        else:
            max_marker = step
            levels.append([min_marker,max_marker])
        min_marker = step
    print ('    levels: ', levels)
    valid_value = False
    index = 0
    #determine if levels are ascending or descending
    if levels[0][0] < levels[0][1]:
        level_direction_asc = True
    else:
        level_direction_asc = False
    for level in levels:
        #print ('    checking to see if evidence of: ', value, ' is between level: ', level[0], ':', level[1])
        if level_direction_asc:
            if float(level[0]) <= float(value) <= float(level[1]):
                #TODO - IF NUMBER FALLS BELOW BOTTOM BIN, ASIGN TO BOTTOM BIN and VISA VERSA WITH TOP BIN
                #value falls within this level
                valid_value = True
                value_index = index
        else:
            if float(level[0]) >= float(value) >= float(level[1]):
                #value falls within this level
                valid_value = True
                value_index = index
        index=index+1
    if valid_value:
        print ('    valid value found at level: ', levels[value_index])
        if value_index > 0:
            prev_mid_point = levels[value_index-1][0] + (levels[value_index-1][1]-levels[value_index-1][0])/2
            print ('    prev midpoint = ', prev_mid_point)
        current_mid_point = levels[value_index][0] + (levels[value_index][1]-levels[value_index][0])/2
        print ('    current midpoint = ', current_mid_point)
        if value_index < len(levels)-1:
            next_mid_point = levels[value_index+1][0] + (levels[value_index+1][1]-levels[value_index+1][0])/2
            print ('    next midpoint = ', next_mid_point)
        interpolate_update = [0] * len(levels)
        if float(value) == current_mid_point:
            #instantiate a list
            current_result = 1.0
        elif float(value) < current_mid_point or value_index == len(levels)-1:
            prev_level_fraction = 1/(abs(float(value) - prev_mid_point))
            current_level_fraction = 1/(abs(float(value) - current_mid_point))
            sum_fraction = prev_level_fraction + current_level_fraction
            prev_result = prev_level_fraction/sum_fraction
            current_result = current_level_fraction/sum_fraction
            interpolate_update[value_index-1] = prev_result
            interpolate_update[value_index] = current_result
        elif float(value) > current_mid_point or value_index == 0:
            next_level_fraction = 1/(abs(float(value) - next_mid_point))
            current_level_fraction = 1/(abs(float(value) - current_mid_point))
            sum_fraction = next_level_fraction + current_level_fraction
            next_result = next_level_fraction/sum_fraction
            current_result = current_level_fraction/sum_fraction
            interpolate_update[value_index+1] = next_result
        interpolate_update[value_index] = current_result
        print('    setting likelihoods: ', interpolate_update)
        node.likelihoods(interpolate_update)
    else: print ('    no valid level found for this value')
    #print (node.likelihoods())
    # print (node.levels())
    return 0

if __name__ == '__main__':
    updateBn(param_dict)
