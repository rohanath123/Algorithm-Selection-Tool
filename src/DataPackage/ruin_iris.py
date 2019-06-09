import pandas as pd 
import numpy as np 
import random
import csv

df = pd.read_csv("D:/Machine Learning Datasets/iris-species/Iris.csv")
rands = [random.randint(0, len(df) - 1) for i in range(45)]
df = df.values.tolist()

for r in rands:
	df[r][2] = None 

def write_to_excel(data, mode):
    with open("D:/Machine Learning Datasets/iris-species/iris_ruined.csv", mode, newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    f.close()

for i in range(len(df)):
	print(i)
	write_to_excel(df[i], 'a')

