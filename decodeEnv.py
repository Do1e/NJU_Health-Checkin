import os
import json

info = {}
info['USER_AGENT'] = os.environ['USER_AGENT']
info['COOKIE'] = os.environ['COOKIE']
info['LOCATION'] = os.environ['LOCATION']
info['BODY_TEMP_OK'] = os.environ['BODY_TEMP_OK']
info['HEALTH_STATUS'] = os.environ['HEALTH_STATUS']
info['MY_HEALTH_CODE_COLOR'] = os.environ['MY_HEALTH_CODE_COLOR']
info['FAM_MEM_HEALTH_CODE_COLOR'] = os.environ['FAM_MEM_HEALTH_CODE_COLOR']
info['LAST_RNA'] = os.environ['LAST_RNA']
info['TRY_N_TIMES'] = os.environ['TRY_N_TIMES']

with open('config.json', 'w') as f:
    f.write(json.dumps(info, indent=4, ensure_ascii=False))