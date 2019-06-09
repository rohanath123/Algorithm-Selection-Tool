import pandas as pd 
import numpy as np

class Data:
	def __init__(self, PATH):
		self.main_df = pd.read_csv(PATH)

		self.columns = []
		self.types = []
		self.dtype_dict = {}

		self.set_cols()
		self.set_types()
		self.make_type_dict()

	def set_cols(self):
		self.columns = list(self.main_df.columns)

	def set_types(self):
		self.types = list(self.main_df.dtypes)

	def make_type_dict(self):
		for i in range(len(self.columns)):
			self.dtype_dict[self.columns[i]] = self.types[i]


data = Data("D:/Machine Learning Datasets/game-of-thrones/character-deaths.csv")
