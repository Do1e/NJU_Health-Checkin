import os
import json

info = {}
info['User_Agent'] = os.environ['USER_AGENT']
info['Cookie'] = os.environ['COOKIE']
try:
    info['location'] = os.environ['LOCATION']
except KeyError:
    info['location'] = 'default'
try:
    info['body_temp_ok'] = os.environ['BODY_TEMP_OK']
except KeyError:
    info['body_temp_ok'] = '1'
try:
    info['health_status'] = os.environ['HEALTH_STATUS']
except KeyError:
    info['health_status'] = '1'
try:
    info['my_health_code_color'] = os.environ['MY_HEALTH_CODE_COLOR']
except KeyError:
    info['my_health_code_color'] = '1'
try:
    info['fam_mem_health_code_color'] = os.environ['FAM_MEM_HEALTH_CODE_COLOR']
except KeyError:
    info['fam_mem_health_code_color'] = '1'
try:
    info['last_RNA'] = os.environ['LAST_RNA']
except KeyError:
    info['last_RNA'] = 'default'
try:
    info['try_N_times'] = os.environ['TRY_N_TIMES']
except KeyError:
    info['try_N_times'] = '3'

print(json.dumps(info, indent=4, ensure_ascii=False))
with open('config.json', 'w') as f:
    f.write(json.dumps(info, indent=4, ensure_ascii=False))