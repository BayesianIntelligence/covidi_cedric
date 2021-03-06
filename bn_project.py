import _env,csv,math
from bni_netica import *

bn_models = {"0" :'jump5_start0_period0.trained.dne',\
             "1" :'jump5_start1plus_period0.trained.dne', \
             "2" :'jump5_start0_period1.trained.dne', \
             "3" :'jump5_start1plus_period1.trained.dne', \
             "4" :'jump5_start0_period2.trained.dne', \
             "5" :'jump5_start1plus_period2.trained.dne'}

default_model = "jump5_start0_period2.trained.dne"

nested_dictionary = { }

def updateBn(param_dict):
    print('Running model with input: {}'.format(param_dict))

    #select which BN model to use
    if "time_since_admission" in param_dict and "period" in param_dict:
        if param_dict["time_since_admission"] == "start0" and param_dict["period"] == "period0":
            bn_selection = bn_models["0"]
        elif param_dict["time_since_admission"] == "start1plus" and param_dict["period"] == "period0":
            bn_selection = bn_models["1"]
        elif param_dict["time_since_admission"] == "start0" and param_dict["period"] == "period1":
            bn_selection = bn_models["2"]
        elif param_dict["time_since_admission"] == "start1plus" and param_dict["period"] == "period1":
            bn_selection = bn_models["3"]
        elif param_dict["time_since_admission"] == "start0" and param_dict["period"] == "period2":
            bn_selection = bn_models["4"]
        elif param_dict["time_since_admission"] == "start1plus" and param_dict["period"] == "period2":
            bn_selection = bn_models["5"]
        else:
            print ("Time since admission and/or period not set, Selecting default BN.")
            bn_selection = default_model
    else:
        print ("Time since admission and/or period not set, Selecting default BN.")
        bn_selection = default_model
    print ("Selecting BN: " + bn_selection)
    net = Net(bn_selection)
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
                            #TODO do not need the 1/
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
                #elif node.name() == 'ci_gender_bg':
                #    if 'ci_gender_bg' in param_dict.keys() and param_dict['ci_gender_bg'] == 'other':
                #        print ('    Updating gender to: ',  param_dict[node.name()])
                #        node.likelihoods([1, 1])
                #    elif 'ci_gender_bg' in param_dict.keys():
                #        print ('    Updating gender to: ',  param_dict[node.name()])
                #        enterFinding(node, param_dict[node.name()])
                elif node.type() == Node.CONTINUOUS_TYPE:
                    print ('    Interpolating: ' + node.name() + " with value: ",  param_dict[node.name()])
                    interpolate (node, (param_dict[node.name()]))
                else:
                    print ('    Updating state directly for: ' + node.name() + " to: ",  param_dict[node.name()])
                    enterFinding(node, param_dict[node.name()])
                print ('    Node updated ')
            except Exception as e:
                print ('    1st exception caught!' , e, file=sys.stderr)
                pass
        else:
            try:
                if node.name() == 'ci_status_t0':
                    if 'icu_status' in param_dict.keys() and param_dict['icu_status'] == 'icu':
                        print ("converting icu_status:icu to ci_status_t0:0,0,0,1")
                        node.likelihoods([0, 1, 0, 0])
                    elif 'icu_status' in param_dict.keys() and param_dict['icu_status'] == 'hospital':
                        print ("converting icu_status:icu to ci_status_t0:0,0,1,0")
                        node.likelihoods([0, 0, 1, 0])
                    else:
                        print ("setting ci_status_t0:0,0,1,1")
                        node.likelihoods([0, 1, 1, 0])
            except Exception as e:
                print ('   2nd exception caught!' , e, file=sys.stderr)
                pass
    #add meta data: the bn name and version, to nested dictionary
    #net.add_net_usr_field('net_version', '1')
    #net.add_net_usr_field('net_name', 'progression model')
    print ('API request made for BN name: ' + net.get_net_usr_field('name') + ' with version: ' + net.get_net_usr_field('version'))
    nested_dictionary['model'] = {}
    nested_dictionary['model']['name'] = net.get_net_usr_field('name')
    nested_dictionary['model']['version'] = net.get_net_usr_field('version')
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
            #Add a special condition for other gender
            if node.name() == 'ci_gender_bg':
                nested_dictionary['data'][node.name()]["other"] = 0
            index+=1

    #merge hypoxemia's from 3 states into 2 states
    nested_dictionary['data']['ci_hypoxaemia_t0']['non_severe'] = 1-nested_dictionary['data']['ci_hypoxaemia_t0']['severe']
    del nested_dictionary['data']['ci_hypoxaemia_t0']['normal']
    del nested_dictionary['data']['ci_hypoxaemia_t0']['moderate']
    nested_dictionary['data']['ci_hypoxaemia_t1']['non_severe'] = 1-nested_dictionary['data']['ci_hypoxaemia_t1']['severe']
    del nested_dictionary['data']['ci_hypoxaemia_t1']['normal']
    del nested_dictionary['data']['ci_hypoxaemia_t1']['moderate']
    #create icu_status field
    nested_dictionary['data']['icu_status'] = {}
    nested_dictionary['data']['icu_status']['icu'] = 0
    nested_dictionary['data']['icu_status']['hospital'] = 0

    nested_dictionary['data']['ci_time_since_admission_bg'] = {}
    nested_dictionary['data']['ci_time_since_admission_bg']['start0'] = 0
    nested_dictionary['data']['ci_time_since_admission_bg']['start1plus'] = 0
    nested_dictionary['data']['ci_period_bg'] = {}
    nested_dictionary['data']['ci_period_bg']['period0'] = 0
    nested_dictionary['data']['ci_period_bg']['period1'] = 0
    nested_dictionary['data']['ci_period_bg']['period2'] = 0
    nested_dictionary['data']['ci_vaccine_status_bg'] = {}
    nested_dictionary['data']['ci_vaccine_status_bg']['yes'] = 0
    nested_dictionary['data']['ci_vaccine_status_bg']['no'] = 0
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
    valid_value = False
    index = 0
    level_direction_desc = False
    #determine if levels are ascending or descending
    if levels[0][0] > levels[0][1]:
        level_direction_desc = True
        #reverse levels array
        print ("    reverseing descending array...")
        levels = [i[::-1] for i in levels[::-1]]
        #print (levels)
    print ('    levels: ', levels)
    for level in levels:
        #print ('    checking to see if evidence of: ', value, ' is between level: ', level[0], ':', level[1])
        if float(level[0]) <= float(value) <= float(level[1]):
            #value falls within this level
            valid_value = True
            value_index = index
        elif index==0 and float(value) < float(level[0]):
            #assign value to minimum level
            valid_value = True
            value_index = index
        elif index==len(levels)-1 and float(value) > float(level[1]):
            #assign value to maximum level
            valid_value = True
            value_index = index
        index=index+1
    if valid_value:
        #TODO if we have a scenario where the last 2 levels are [20,20][20,20] eg. the same, I expect a divide by zero error.
        print ('    value assigned to level: ', levels[value_index], 'at index: ', value_index)
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
            current_result = 1.0
            interpolate_update[value_index] = current_result
        elif value_index == 0 and float(value) < current_mid_point:
            current_result = 1.0
            interpolate_update[value_index] = current_result
        elif value_index == len(levels)-1 and float(value) > current_mid_point:
            current_result = 1.0
            interpolate_update[value_index] = current_result
        elif float(value) < current_mid_point:
            distance_to_current_mid_point = abs(float(value)-current_mid_point)
            distance_to_prev_mid_point = abs(float(value)-prev_mid_point)
            total_distance = distance_to_current_mid_point + distance_to_prev_mid_point
            fraction_of_current_level = 1-(distance_to_current_mid_point / total_distance)
            fraction_of_prev_level = 1-(distance_to_prev_mid_point / total_distance)
            interpolate_update[value_index-1] = fraction_of_prev_level
            interpolate_update[value_index] = fraction_of_current_level
        elif float(value) > current_mid_point:
            distance_to_current_mid_point = abs(float(value)-current_mid_point)
            distance_to_next_mid_point = abs(float(value)-next_mid_point)
            total_distance = distance_to_current_mid_point + distance_to_next_mid_point
            fraction_of_current_level = 1-(distance_to_current_mid_point / total_distance)
            fraction_of_next_level = 1-(distance_to_next_mid_point / total_distance)
            print ("ratio of current_level: ", fraction_of_current_level)
            print ("ratio of next_level: ", fraction_of_next_level)
            interpolate_update[value_index+1] = fraction_of_next_level
            interpolate_update[value_index] = fraction_of_current_level
        else: print ('unhandled scenario')
        print('    likelihoods: ', interpolate_update)
        if level_direction_desc:
            print('    reverting descending array...')
            #reverse the interpolation update list for descending levels
            interpolate_update = interpolate_update[::-1]
        node.likelihoods(interpolate_update)
    else: print ('    no valid level found for this value')
    #print (node.likelihoods())
    # print (node.levels())
    return 0

if __name__ == '__main__':
    updateBn(param_dict)
