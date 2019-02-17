import pickle
from leaper import *

with open('data_2019.pkl', 'r') as f:
    data = pickle.load(f)

print(data)

