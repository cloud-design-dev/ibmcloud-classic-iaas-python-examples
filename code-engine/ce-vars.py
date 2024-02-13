import os
import json
from datetime import datetime

def pullallCeServicesVars():
    ceVars = os.environ.get('CE_SERVICES', "[]") 
    if not ceVars.strip():
        print("CE_SERVICES is not set or is empty")
    try:
        ceVarsToJson = json.loads(ceVars)
        if isinstance(ceVarsToJson, dict):
            allCeVars  = list(ceVarsToJson.values())
        else:
            allCeVars = ceVarsToJson
    except Exception as e:
        print("CE_SERVICES does not contain valid JSON. Error: " + str(e))
    return allCeVars
def pullAllVars():
    allVars = {}
    for name, value in os.environ.items():
        allVars[name] = value
    return allVars


try:
    currentTime = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    print("Reporting Code Engine Service Binding Env Vars: " + currentTime)
    ceServicesVars = pullallCeServicesVars()
    print("Reporting All exported Env Vars: " + currentTime)
    allVars = pullAllVars()
    print(allVars)
except Exception as e:
    print("Python Virtualenv test failed. Error: " + str(e))