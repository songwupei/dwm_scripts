#!/bin/python3

import re
from pathlib import Path


def sub_text(filepath):
    with open(filepath) as file:

        text = file.read()
        file.close()
    match_token = re.match(r'\d+年\d+月',filepath.stem)[0]
    print(match_token) 
    new_text = text
    new_text = re.sub(r'2024年(0?[1-9]月|1[0-2]月)',r'\1',new_text)
    new_text = re.sub(r'(0?[1-9]月|1[1-2]月)',r'2024年\1',new_text)
    new_text = re.sub(r'(此外，)本月',match_token,new_text)



    with open(f'2024年{Path(filepath).stem[-10:]}_sub{Path(filepath).suffix}','a+') as file:
        file.write(new_text)    
        file.write('\n')
        file.close()

filepaths = sorted(Path('./').glob('*.txt'),key=lambda x:int(str(x)[5:-15]))
print(filepaths)

for filepath in filepaths:
    sub_text(filepath)
