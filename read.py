import pickle
import json
import os

file_des = os.path.join(os.path.dirname(__file__), '8000000_8012661.pkl')  # change the name of the .pkl file
output_des = os.path.join(os.path.dirname(__file__), 'output.json')

read = []

with open(file_des, "rb") as src:
    while 1:
        try:
            read.append(pickle.load(src))
        except EOFError:
            break

with open(output_des, 'w') as o:
    json.dump(read, o)
o.close()
