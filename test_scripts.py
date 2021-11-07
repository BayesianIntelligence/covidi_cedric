import requests
import json

def runTests(test_dict):
    response = requests.post("http://localhost:5000/getall", json = test_dict)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    try:
        test_dict = {'ci_pulse_rate_t0': '44'}
        assertion_expectation = "ci_func_car_t0->Abnormal should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_func_car_t0"]["abnormal"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_func_car_t0"]["abnormal"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_pulse_rate_t0': '45'}
        assertion_expectation = "ci_func_car_t0->Abnormal should not be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_func_car_t0"]["abnormal"] != 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_func_car_t0"]["abnormal"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_pulse_rate_t0': '199'}
        assertion_expectation = "ci_func_car_t0->Abnormal should not be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_func_car_t0"]["abnormal"] != 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_func_car_t0"]["abnormal"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_pulse_rate_t0': '200'}
        assertion_expectation = "ci_func_car_t0->Abnormal should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_func_car_t0"]["abnormal"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_func_car_t0"]["abnormal"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_oxygen_saturation_t0': '0.89'}
        assertion_expectation = "ci_hypoxaemia_t0->verylow should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_hypoxaemia_t0"]["verylow"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_hypoxaemia_t0"]["verylow"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_oxygen_saturation_t0': '0.95'}
        assertion_expectation = "ci_hypoxaemia_t0->low should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_hypoxaemia_t0"]["low"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_hypoxaemia_t0"]["low"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_oxygen_saturation_t0': '0.99'}
        assertion_expectation_1 = "ci_hypoxaemia_t0->verylow should not be 1.0"
        assertion_expectation_2 = "ci_hypoxaemia_t0->low should not be 1.0"
        print ("Running test with: ", test_dict)
        print ("Expectation 1: ", assertion_expectation_1)
        print ("Expectation 2: ", assertion_expectation_2)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_hypoxaemia_t0"]["verylow"] != 1.0, "ASSERTION ERROR: " + assertion_expectation_1 + " but is " + str(testResponse["data"]["ci_hypoxaemia_t0"]["verylow"])
        assert testResponse["data"]["ci_hypoxaemia_t0"]["low"] != 1.0, "ASSERTION ERROR: " + assertion_expectation_2 + " but is " + str(testResponse["data"]["ci_hypoxaemia_t0"]["low"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_creat_t0': '106'}
        assertion_expectation = "ci_end_organ_perf_t0->low should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_end_organ_perf_t0"]["low"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_end_organ_perf_t0"]["low"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_creat_t0': '99'}
        assertion_expectation = "ci_intravas_volume_t0->low should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_intravas_volume_t0"]["low"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_intravas_volume_t0"]["low"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_creat_t0': '99', 'ci_chronic_kidney_disease_bg' : 'true'}
        assertion_expectation = "ci_intravas_volume_t0->low should not be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_intravas_volume_t0"]["low"] != 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_intravas_volume_t0"]["low"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_neut_t0': '10', 'ci_lym_t0' : '2'}
        assertion_expectation = "ci_sys_immune_resp_t0->abnormal should not be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_sys_immune_resp_t0"]["abnormal"] != 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_sys_immune_resp_t0"]["abnormal"])
    except AssertionError as ae:
        print (ae)

    try:
        test_dict = {'ci_neut_t0': '10', 'ci_lym_t0' : '1.5'}
        assertion_expectation = "ci_sys_immune_resp_t0->abnormal should be 1.0"
        print ("Running test with: ", test_dict, " expecting: ", assertion_expectation)
        testResponse = runTests(test_dict)
        assert testResponse["data"]["ci_sys_immune_resp_t0"]["abnormal"] == 1.0, "ASSERTION ERROR: " + assertion_expectation + " but is " + str(testResponse["data"]["ci_sys_immune_resp_t0"]["abnormal"])
    except AssertionError as ae:
        print (ae)

        #for key, value in testResponse["data"]["ci_func_car_t0"].items():
        #    print(key, ":", value)

#param_dict = {'ci_creat_t0': '91', 'ci_chronic_kidney_disease_bg': 'false', 'ci_neut_t0': '23'}
