import os
import json

info = {}
info['student_id'] = os.environ['STUDENT_ID']
assert info['student_id'] != '', "Expected infomation `student_id` not found. Check repository secret"
assert len(info['student_id']) == 9, "Expected infomation `student_id` is not 9 digits. Check repository secret"

info['password'] = os.environ['PASSWORD']
assert info['password'] != '', "Expected infomation `password` not found. Check epository secret"

info['User_Agent'] = os.environ['USER_AGENT']
assert info['User_Agent'] != '', "Expected infomation `User_Agent` not found. Check repository secret"

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
    if info['last_RNA'] == '':
        info['last_RNA'] = 'default'
    if info['last_RNA'] != 'default':
        assert len(info['last_RNA']) == 13, "last_RNA example: 2022-09-01+16"
        assert info['last_RNA'][4] == '-' and info['last_RNA'][7] == '-' and info['last_RNA'][10] == '+', "last_RNA example: 2022-09-01+16"
        assert int(info['last_RNA'][0:4]) >= 2022, "last_RNA example: 2022-09-01+16"
        assert int(info['last_RNA'][5:7]) >= 1 and int(info['last_RNA'][5:7]) <= 12, "last_RNA example: 2022-09-01+16"
        assert int(info['last_RNA'][8:10]) >= 1 and int(info['last_RNA'][8:10]) <= 31, "last_RNA example: 2022-09-01+16"
        assert int(info['last_RNA'][11:13]) >= 0 and int(info['last_RNA'][11:13]) <= 23, "last_RNA example: 2022-09-01+16"
except KeyError:
    info['last_RNA'] = 'default'
except ValueError:
    print("last_RNA example: 2022-09-01+16")
    raise

try:
    info['try_N_times'] = os.environ['TRY_N_TIMES']
    if info['try_N_times'] == '':
        info['try_N_times'] = '3'
    else: assert int(info['try_N_times']) >= 0, "Expected infomation `try_N_times` is a positive integer"
except KeyError:
    info['try_N_times'] = '3'
except ValueError:
    print("Expected infomation `try_N_times` is a positive integer")
    raise

print(json.dumps(info, indent=4, ensure_ascii=False))
with open('config.json', 'w') as f:
    f.write(json.dumps(info, indent=4, ensure_ascii=False))