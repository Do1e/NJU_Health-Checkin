import os
import json

info = {}
info['User_Agent'] = os.environ['USER_AGENT']
info['Cookie'] = os.environ['COOKIE']
try:
    info['location'] = os.environ['LOCATION']
    if info['location'] == '':
        info['location'] = 'default'
except KeyError:
    info['location'] = 'default'
try:
    info['body_temp_ok'] = os.environ['BODY_TEMP_OK']
    if info['body_temp_ok'] == '':
        info['body_temp_ok'] = '1'
except KeyError:
    info['body_temp_ok'] = '1'
try:
    info['health_status'] = os.environ['HEALTH_STATUS']
    if info['health_status'] == '':
        info['health_status'] = '1'
except KeyError:
    info['health_status'] = '1'
try:
    info['my_health_code_color'] = os.environ['MY_HEALTH_CODE_COLOR']
    if info['my_health_code_color'] == '':
        info['my_health_code_color'] = '1'
except KeyError:
    info['my_health_code_color'] = '1'
try:
    info['fam_mem_health_code_color'] = os.environ['FAM_MEM_HEALTH_CODE_COLOR']
    if info['fam_mem_health_code_color'] == '':
        info['fam_mem_health_code_color'] = '1'
except KeyError:
    info['fam_mem_health_code_color'] = '1'
try:
    info['last_RNA'] = os.environ['LAST_RNA']
    if info['last_RNA'] == '':
        info['last_RNA'] = 'default'
except KeyError:
    info['last_RNA'] = 'default'
try:
    info['try_N_times'] = os.environ['TRY_N_TIMES']
    if info['try_N_times'] == '':
        info['try_N_times'] = '3'
except KeyError:
    info['try_N_times'] = '3'

print(json.dumps(info, indent=4, ensure_ascii=False))
with open('config.json', 'w') as f:
    f.write(json.dumps(info, indent=4, ensure_ascii=False))