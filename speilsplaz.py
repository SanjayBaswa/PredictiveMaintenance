import os


pth = 'all_models/S19/20250107145452/'

for i in os.listdir(pth):
    if i.split('.')[-1] == 'h5':
        print(f" model path = {pth}{i}" )
    if i.split('.')[-1] == 'pkl':
        print(f" pkl path = {pth}{i}" )



