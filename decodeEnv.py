import os
import json

info = {}
info['User_Agent'] = os.environ['User_Agent']
info['Cookie'] = os.environ['Cookie']
info['location'] = os.environ['location']
info['body_temp_ok'] = os.environ['body_temp_ok']
info['health_status'] = os.environ['health_status']
info['my_health_code_color'] = os.environ['my_health_code_color']
info['fam_mem_health_code_color'] = os.environ['fam_mem_health_code_color']
info['last_RNA'] = os.environ['last_RNA']
info['try_N_times'] = os.environ['try_N_times']

with open('config.json', 'w') as f:
    f.write(json.dumps(info, indent=4, ensure_ascii=False))