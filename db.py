import sqlite3
from sqlite3 import Error
import json
import sys
import shutil
import os

IMPORT_FOLDER = './data_input/'
EXPORT_FOLDER = './data_output/'
DATABASE_FILE = 'covidi.db'
JSON_FILE = 'test_file.json'

def run_import():
    json_path = IMPORT_FOLDER + JSON_FILE
    db_path = EXPORT_FOLDER + DATABASE_FILE
    
    #check to make sure a json file exists otherwise exit
    if not os.path.exists(json_path):
        print("No JSON file found in the input folder")
        sys.exit(1)
    
    
    create_connection(db_path)
    create_tables(db_path)
    json = import_json(json_path)
    update_tables(db_path, json)
    
    #finally move the import json to export to prevent duplicate entries
    print("Moving the import JSON to: " + EXPORT_FOLDER + JSON_FILE)
    #shutil.move(json_path, EXPORT_FOLDER + JSON_FILE)
    print("IMPORT COMPLETE (SUCESS)")

def create_connection(db_file):
    print("Creating database: " + db_file)
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("SQLITE VERSION: ", sqlite3.version)
    except Error as e:
        print(e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

def create_tables(db_file):
    print("Creating tables")
    conn = None
    try:
        #create an slq_lite db called covid_i
        conn= sqlite3.connect(db_file)
        #create a cursor object to manipulate SQL Commands
        cursor = conn.cursor()
        #create time series table
        print("creating table (if it does not exist): timeseries")
        cursor.execute('''    
        CREATE TABLE IF NOT EXISTS timeSeries (id integer primary key not null,
            Timestamp, usubjid integer, day integer, ci_ho_type, ci_ds_decod, ci_Body_Mass_Index, ci_Body_Mass_Index_u, ci_Diastolic_Blood_Pressure, ci_Diastolic_Blood_Pressure_u, ci_Heart_Rate, ci_Heart_Rate_u, ci_Height, ci_Height_u, ci_Mean_Arterial_Pressure, ci_Mean_Arterial_Pressure_u, ci_Mid_Upper_Arm_Circumference, ci_Mid_Upper_Arm_Circumference_u, ci_Oxygen_Saturation, ci_Oxygen_Saturation_u, ci_Pulse_Rate, ci_Pulse_Rate_u, ci_Respiratory_Rate, ci_Respiratory_Rate_u, ci_Systolic_Blood_Pressure, ci_Systolic_Blood_Pressure_u, ci_Temperature, ci_Temperature_u, ci_Weight, ci_Weight_u, ci_APTTSTND, ci_APTTSTND_u, ci_APTT, ci_APTT_u, ci_ALT, ci_ALT_u, ci_ALB, ci_ALB_u, ci_ALP, ci_ALP_u, ci_AMYLASE, ci_AMYLASE_u, ci_AST, ci_AST_u, ci_BASEEXCS, ci_BASEEXCS_u, ci_BASO, ci_BASO_u, ci_BASOLE, ci_BASOLE_u, ci_BICARB, ci_BICARB_u, ci_BILI, ci_BILI_u, ci_CRP, ci_CRP_u, ci_CA, ci_CA_u, ci_CAION, ci_CAION_u, ci_CAIONPH, ci_CAIONPH_u, ci_CO2, ci_CO2_u, ci_CARBXHGB, ci_CARBXHGB_u, ci_CL, ci_CL_u, ci_CHOL, ci_CHOL_u, ci_CK, ci_CK_u, ci_CREAT, ci_CREAT_u, ci_DDIMER, ci_DDIMER_u, ci_HGBDOXY, ci_HGBDOXY_u, ci_BILDIR, ci_BILDIR_u, ci_EOS, ci_EOS_u, ci_EOSLE, ci_EOSLE_u, ci_MCHC, ci_MCHC_u, ci_MCH, ci_MCH_u, ci_MCV, ci_MCV_u, ci_ESR, ci_ESR_u, ci_RBC, ci_RBC_u, ci_RDW, ci_RDW_u, ci_FERRITIN, ci_FERRITIN_u, ci_FIBRINO, ci_FIBRINO_u, ci_FIBRINOF, ci_FIBRINOF_u, ci_FIO2, ci_FIO2_u, ci_GGT, ci_GGT_u, ci_GLUC, ci_GLUC_u, ci_HCT, ci_HCT_u, ci_HGB, ci_HGB_u, ci_HBA1C, ci_HBA1C_u, ci_INTLK6, ci_INTLK6_u, ci_IRON, ci_IRON_u, ci_LDH, ci_LDH_u, ci_LACTICAC, ci_LACTICAC_u, ci_WBC, ci_WBC_u, ci_LYM, ci_LYM_u, ci_LYMLE, ci_LYMLE_u, ci_MG, ci_MG_u, ci_MPV, ci_MPV_u, ci_HGBMET, ci_HGBMET_u, ci_MONO, ci_MONO_u, ci_MONOLE, ci_MONOLE_u, ci_NEUT, ci_NEUT_u, ci_NEUTLE, ci_NEUTLE_u, ci_OXYSAT, ci_OXYSAT_u, ci_HGBOXY, ci_HGBOXY_u, ci_PO2FIO2, ci_PO2FIO2_u, ci_PCO2, ci_PCO2_u, ci_PO2, ci_PO2_u, ci_PLATHCT, ci_PLATHCT_u, ci_PLAT, ci_PLAT_u, ci_K, ci_K_u, ci_PCT, ci_PCT_u, ci_PROT, ci_PROT_u, ci_INR, ci_INR_u, ci_PT, ci_PT_u, ci_PTAC, ci_PTAC_u, ci_SODIUM, ci_SODIUM_u, ci_TT, ci_TT_u, ci_TROPONIN, ci_TROPONIN_u, ci_TROPONI, ci_TROPONI_u, ci_TROPONT, ci_TROPONT_u, ci_URATE, ci_URATE_u, ci_UREAN, ci_UREAN_u, ci_PH, ci_PH_u, ci_in_trt, ci_in_modify, ci_in_cat, ci_sa_complications, ci_NLR float, ci_MAP float, OxygenTreatment, Status, PulmonaryComplication, CardiacComplication, VascularComplication, AntiCoagulation, AntiInflammatory, AntiViral)
        ''')
        #commit the change to the db
        conn.commit()
        #create subject table
        print("creating table (if it does not exist): subject")
        cursor.execute('''    
        CREATE TABLE IF NOT EXISTS subject (id integer primary key not null,
            USUBJID, STUDYID, DOMAIN, RFSTDTC, DTHFL, AGE, AGETXT, AGEU, SEX, RACE, ETHNIC, ARMCD, ARM, COUNTRY, DMDY, DSDECOD, BaselineStatus, ci_sa_medicalHistory, ci_sa_symptomsOnAdmission, ci_vs_weight, ci_vs_weight_u, ci_vs_height, ci_vs_height_u, ci_vs_bmi, ci_vs_bmi_u, ci_ho_duration, ci_ho_disout, ci_ho_selfcare, HYPERTENSION, CHRONIC_PULMONARY_DISEASE, SMOKING___FORMER, CHRONIC_INFLAMMATORY_DISEASE, OBESITY, OTHER_COMORBIDITIES, CHRONIC_CARDIAC_DISEASE, DIABETES, CHRONIC_NEUROLOGICAL_DISORDER, DEMENTIA, MALNUTRITION, CHRONIC_KIDNEY_DISEASE, SMOKING, DIABETES___TYPE_2, ASTHMA, AIDS_HIV, TUBERCULOSIS, RHEUMATOLOGIC_DISORDER, MALIGNANT_NEOPLASM, HISTORY_OF_PERIPHERAL_OR_CARDI, LIVER_DISEASE, CHRONIC_HEMATOLOGIC_DISEASE, ASPLENIA, DIABETES___TYPE_1, VALVULAR_HEART_DISEASE, SOLID_TUMOR_WITHOUT_METASTASIS, PEPTIC_ULCER_DISEASE_EXCLUDING, CONGESTIVE_HEART_FAILURE, DEPRESSION, STROKE_OR_OTHER_NEUROLOGICAL_D, HEMATOLOGIC_MALIGNANCY, DYSLIPIDEMIA_HYPERLIPIDEMIA, PSYCHOSIS, COVID_19_SYMPTOMS, FATIGUE_MALAISE, SHORTNESS_OF_BREATH, COUGH, MUSCLE_ACHES_JOINT_PAIN, HEADACHE, HISTORY_OF_FEVER, COUGH___WITH_SPUTUM, DIARRHOEA, UPPER_RESPIRATORY_TRACT_SYMPTO, SEIZURES, ABDOMINAL_PAIN, VOMITING_NAUSEA, ALTERED_CONSCIOUSNESS_CONFUSIO, COUGH___NO_SPUTUM, WHEEZING, LYMPHADENOPATHY, SORE_THROAT, LOSS_OF_SMELL, LOSS_OF_TASTE, CHEST_PAIN, RUNNY_NOSE, COUGH_BLOODY_SPUTUM, ANOREXIA, INABILITY_TO_WALK, SKIN_RASH, CONJUNCTIVITIS, CHILLS_RIGORS, MYALGIA_OR_FATIGUE, BACTERIAL_PNEUMONIA, ACUTE_HYPOXIC_RESPIRATORY_FAIL, SEPSIS, SHOCK, SEVERE_DEHYDRATION, OTHER_SIGNS_AND_SYMPTOMS, BLEEDING, SKIN_ULCERS, HEMOGLOBINURIA, LEUKOCYTURIA, PROTEINURIA, HEMATURIA, EAR_PAIN, COUGH_BLOODY_SPUTUM___HAEMOPTY, LETHARGY, REFUSING_TO_EAT_OR_DRINK_HISTO, ci_ICU text, ci_InvVent text)
        ''')
        #commit the change to the db
        conn.commit()
        #close the connectoin
        conn.close()
    except Error as e:
        print(e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

def import_json(json_file):
    print("Importing JSON file: " + json_file)
    try:
        with open(json_file) as json_data:
            d = json.load(json_data)
            #print(d)
            return d
    except FileNotFoundError as e:
        print("ERROR: Cannot find import JSON at file location specified")
        sys.exit(1)
    except Error as e:
        print(e)
        
def update_tables(db_file, json_data):
    print("Loading JSON data into tables")
    conn = None
    try:
        #create an slq_lite db called covid_i
        conn= sqlite3.connect(db_file)
        #create a cursor object to manipulate SQL Commands
        cursor = conn .cursor()
        
        # Output a table schema to stdout if required
        
        #cursor.execute("PRAGMA table_info (timeSeries)")
        #rows = cursor.fetchall()
 
        #for row in rows:
        #    print(row)         
        #conn.commit()
        
        #insert the json into SQL
        for item in json_data:
            sql = "INSERT INTO subject (SEX, AGE, CHRONIC_PULMONARY_DISEASE, COVID_19_SYMPTOMS, ci_ho_disout, ci_ICU, BaselineStatus, ci_ho_duration, ci_InvVent) VALUES (?,?,?,?,?,?,?,?,?)"
            value_gender = str(item.get('Gender'))
            value_age = str(item.get('Age'))
            value_pulmonary = str(item.get('ChronicPulmonaryDisease'))
            value_covid_status = str(item.get('COVIDStatus'))
            value_final_status = str(item.get('FinalStatus'))
            value_icu = str(item.get('AnyICU'))
            value_baseline_status = str(item.get('BaselineStatus'))
            value_stay_duration = item.get('DurationOfStay')
            value_oxygen = str(item.get('OxygenTreatment'))
            
            print(sql, value_gender, value_age, value_pulmonary, value_covid_status, value_final_status, value_icu, value_baseline_status, value_stay_duration, value_oxygen)
            
            cursor.execute(sql, (value_gender, value_age, value_pulmonary, value_covid_status, value_final_status, value_icu, value_baseline_status, value_stay_duration, value_oxygen,))
            conn.commit()
            
            cursor.execute("SELECT last_insert_rowid()")
            last_id = cursor.fetchone()
            print("last_id ", int(last_id[0]))   
            #insert time series int(weight[0])records into SQL
            for inner_item in item.get('TimeSeries'):
                sql = "INSERT INTO timeSeries (usubjid, Timestamp, ci_ho_type, ci_Heart_Rate, ci_Heart_Rate_u, ci_TROPONIN, ci_TROPONIN_u, ci_Diastolic_Blood_Pressure, ci_Diastolic_Blood_Pressure_u, ci_Systolic_Blood_Pressure, ci_Systolic_Blood_Pressure_u, ci_CRP, ci_CRP_u, ci_LDH, ci_LDH_u, ci_LYM, ci_LYM_u, ci_NEUT, ci_NEUT_u, ci_Oxygen_Saturation, ci_Oxygen_Saturation_u, ci_PO2, ci_PO2_u, ci_PCO2, ci_PCO2_u, ci_Respiratory_Rate, ci_Respiratory_Rate_u, ci_APTT, ci_APTT_u, ci_PLAT, ci_PLAT_u, ci_DDIMER, ci_DDIMER_u, ci_CREAT, ci_CREAT_u, ci_LACTICAC, ci_LACTICAC_u, ci_HCT, ci_HCT_u, OxygenTreatment, PulmonaryComplication, CardiacComplication, VascularComplication, AntiCoagulation, AntiInflammatory, AntiViral) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            
                value_usubjid = int(last_id[0])
                value_timestamp = str(inner_item.get('Timestamp'))
                value_status = str(inner_item.get('Status'))
                value_heart_rate = str(inner_item.get('HeartRate'))
                value_heart_rate_u = str(inner_item.get('HeartRateU'))
                value_troponin = str(inner_item.get('Troponin'))
                value_troponin_u = str(inner_item.get('TroponinU'))
                value_diastolic_bp = str(inner_item.get('DiastolicBP'))
                value_diastolic_bp_u = str(inner_item.get('DiastolicBPU'))
                value_systolic_bp = str(inner_item.get('SystolicBP'))
                value_systolic_bp_u = str(inner_item.get('SystolicBPU'))
                value_crp = str(inner_item.get('CRP'))
                value_crp_u = str(inner_item.get('CRPU'))
                value_ldh = str(inner_item.get('LDH'))
                value_ldh_u = str(inner_item.get('LDHU'))
                value_lymphocytes = str(inner_item.get('Lymphocytes'))
                value_lymphocytes_u = str(inner_item.get('LymphocytesU'))
                value_neutrophils = str(inner_item.get('Neutrophils'))
                value_neutrophils_u = str(inner_item.get('NeutrophilsU'))
                value_oxygen_saturation = str(inner_item.get('OxygenSaturation'))
                value_oxygen_saturation_u = str(inner_item.get('OxygenSaturationU'))
                value_po2 = str(inner_item.get('PO2'))
                value_po2_u = str(inner_item.get('PO2U'))
                value_pco2 = str(inner_item.get('PCO2'))
                value_pco2_u = str(inner_item.get('PCO2U'))
                value_respiratory_rate = str(inner_item.get('RespiratoryRate'))
                value_respiratory_rate_u = str(inner_item.get('RespiratoryRateU'))
                value_aptt = str(inner_item.get('aPTT'))
                value_aptt_u = str(inner_item.get('aPTTU'))
                value_platelets = str(inner_item.get('Platelets'))
                value_platelets_u = str(inner_item.get('PlateletsU'))
                value_ddimer = str(inner_item.get('DDimer'))
                value_ddimer_u = str(inner_item.get('DDimerU'))
                value_creatinine = str(inner_item.get('Creatinine'))
                value_creatinine_u = str(inner_item.get('CreatinineU'))
                value_lactate = str(inner_item.get('Lactate'))
                value_lactate_u = str(inner_item.get('LactateU'))
                value_hematocrit = str(inner_item.get('Hematocrit'))
                value_hematocrit_u = str(inner_item.get('HematocritU'))
                value_oxygen_treatment = str(inner_item.get('OxygenTreatment'))
                value_pulmonary_complication = str(inner_item.get('PulmonaryComplication'))
                value_cardiac_complication = str(inner_item.get('CardiacComplication'))
                value_vascular_complication = str(inner_item.get('VascularComplication'))
                value_anticoagulation = str(inner_item.get('AntiCoagulation'))
                value_antiinflammatory = str(inner_item.get('AntiInflammatory'))
                value_antiviral = str(inner_item.get('AntiViral'))
            
                print(sql, value_usubjid, value_timestamp, value_status, value_heart_rate, value_heart_rate_u, value_troponin,value_troponin_u, value_diastolic_bp, value_diastolic_bp_u, value_systolic_bp, value_systolic_bp_u, value_crp, value_crp_u, value_ldh, value_ldh_u, value_lymphocytes, value_lymphocytes_u, value_neutrophils, value_neutrophils_u, value_oxygen_saturation, value_oxygen_saturation_u, value_po2, value_po2_u, value_pco2, value_pco2_u, value_respiratory_rate, value_respiratory_rate_u, value_aptt, value_aptt_u, value_platelets, value_platelets_u, value_ddimer, value_ddimer_u, value_creatinine, value_creatinine_u, value_lactate, value_lactate_u, value_hematocrit, value_hematocrit_u, value_oxygen_treatment, value_pulmonary_complication, value_cardiac_complication, value_vascular_complication, value_anticoagulation, value_antiinflammatory, value_antiviral)
                
                cursor.execute(sql, (value_usubjid, value_timestamp, value_status, value_heart_rate, value_heart_rate_u, value_troponin,value_troponin_u, value_diastolic_bp, value_diastolic_bp_u, value_systolic_bp, value_systolic_bp_u, value_crp, value_crp_u, value_ldh, value_ldh_u, value_lymphocytes, value_lymphocytes_u, value_neutrophils, value_neutrophils_u, value_oxygen_saturation, value_oxygen_saturation_u, value_po2, value_po2_u, value_pco2, value_pco2_u, value_respiratory_rate, value_respiratory_rate_u, value_aptt, value_aptt_u, value_platelets, value_platelets_u, value_ddimer, value_ddimer_u, value_creatinine, value_creatinine_u, value_lactate, value_lactate_u, value_hematocrit, value_hematocrit_u, value_oxygen_treatment, value_pulmonary_complication, value_cardiac_complication, value_vascular_complication, value_anticoagulation, value_antiinflammatory, value_antiviral,))
                conn.commit()
 

        # Output the table if required
        #cursor.execute("SELECT * FROM timeSeries")
        #rows = cursor.fetchall()
 
        #for row in rows:
        #    print(row)         
        #conn.commit()
        
        #close the connection
        conn.close()
    except Error as e:
        print(e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            
if __name__ == '__main__':
    run_import()