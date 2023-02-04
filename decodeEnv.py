import os
import re
import json

info = {}
info['student_id'] = os.environ['STUDENT_ID']
assert info['student_id'] != '', "Expected infomation `student_id` not found. Check repository secret"
assert len(info['student_id']) == 9 or len(info['student_id']) == 10 or len(info['student_id']) == 12, "Expected infomation `student_id` is not 9, 10 or 12 digits. Check repository secret"

info['password'] = os.environ['PASSWORD']
assert info['password'] != '', "Expected infomation `password` not found. Check epository secret"
try:
    info['User_Agent'] = os.environ['USER_AGENT']
    if info['User_Agent'] == '':
        info['User_Agent'] = 'Mozilla/5.0 (Linux; Android 12; M2007J1SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15'
except KeyError:
    info['User_Agent'] = 'Mozilla/5.0 (Linux; Android 12; M2007J1SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15'

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
    else: assert info['body_temp_ok'] in ['0', '1'], "Expected infomation `body_temp_ok` is 0 or 1"
except KeyError:
    info['body_temp_ok'] = '1'

try:
    info['health_status'] = os.environ['HEALTH_STATUS']
    if info['health_status'] == '':
        info['health_status'] = '1'
    else: assert info['health_status'] in ['0', '1'], "Expected infomation `health_status` is 0 or 1"
except KeyError:
    info['health_status'] = '1'

try:
    info['my_health_code_color'] = os.environ['MY_HEALTH_CODE_COLOR']
    if info['my_health_code_color'] == '':
        info['my_health_code_color'] = '1'
    else: assert info['my_health_code_color'] in ['0', '1', '2'], "Expected infomation `my_health_code_color` is 0, 1 or 2"
except KeyError:
    info['my_health_code_color'] = '1'

try:
    info['fam_mem_health_code_color'] = os.environ['FAM_MEM_HEALTH_CODE_COLOR']
    if info['fam_mem_health_code_color'] == '':
        info['fam_mem_health_code_color'] = '1'
    else: assert info['fam_mem_health_code_color'] in ['0', '1', '2'], "Expected infomation `fam_mem_health_code_color` is 0, 1 or 2"
except KeyError:
    info['fam_mem_health_code_color'] = '1'

try:
    info['last_RNA'] = os.environ['LAST_RNA']
    if info['last_RNA'] == '' or info['last_RNA'] == 'default':
        info['last_RNA'] = 'default24'
    else:
        res = re.match(r'\d{4}-\d{2}-\d{2}\+\d{2}$', info['last_RNA'])
        if not res:
            res = re.match(r'\d+$', info['last_RNA'])
            if not res:
                raise ValueError("Expected infomation `last_RNA` is not in correct format. last_RNA example: 2022-09-01+16 or 24")
            else:
                info['last_RNA'] = 'default' + info['last_RNA']
except KeyError:
    info['last_RNA'] = 'default24'

try:
    info['try_N_times'] = os.environ['TRY_N_TIMES']
    if info['try_N_times'] == '':
        info['try_N_times'] = '0'
    else: assert int(info['try_N_times']) >= 0, "Expected infomation `try_N_times` is a positive integer"
except KeyError:
    info['try_N_times'] = '0'
except ValueError:
    print("Expected infomation `try_N_times` is a positive integer")
    raise

try:
    info['leave_NJ'] = os.environ['LEAVE_NJ']
    if info['leave_NJ'] == '':
        info['leave_NJ'] = 'default'
    else: assert info['leave_NJ'] in ['default', '0', '1'], "Expected infomation `leave_NJ` is default, 0 or 1"
except KeyError:
    info['leave_NJ'] = 'default'

try:
    info['infection_status'] = os.environ['INFECTION_STATUS']
    if info['infection_status'] == '':
        info['infection_status'] = '2'
    else: assert info['infection_status'] in ['1', '2', '3'], "Expected infomation `infection_status` is 1, 2 or 3"
except KeyError:
    info['infection_status'] = '2'

print(json.dumps(info, indent=4, ensure_ascii=False))
with open('config.json', 'w') as f:
    f.write(json.dumps(info, indent=4, ensure_ascii=False))
