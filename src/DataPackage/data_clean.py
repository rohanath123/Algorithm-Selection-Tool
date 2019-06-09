import pandas as pd 
import numpy as np

test = [1, 2, ]

class Data:
	def __init__(self, PATH, task):
		self.main_df = pd.read_csv(PATH)

		#self.main_df = df

		self.columns = []
		self.types = []
		self.dtype_dict = {}
		self.idx2col = {}
		self.col2idx = {}
		self.y_labels = []
		self.nan_count = 0
		self.nan_list = []



		self.clean_data()

	
	def clean_data(self):
		self.set_cols()
		self.set_labels()
		self.index()
		self.set_types()
		self.make_type_dict()
		self.count_nan()
		self.remove_nan()

	def set_cols(self):
		self.columns = list(self.main_df.columns)

	def set_labels(self):
		self.y_labels = list(self.main_df[self.columns[0]].tolist())

	def index(self):
		for i in range(len(self.columns)):
			self.idx2col[i] = self.columns[i]
			self.col2idx[self.columns[i]] = i

	def set_types(self):
		self.types = list(self.main_df.dtypes)

	def make_type_dict(self):
		for i in range(len(self.columns)):
			self.dtype_dict[self.columns[i]] = self.types[i]

	def count_nan(self):
		self.nan_count = list(self.main_df.isna().sum())
		self.nan_list = [i for i in range(len(self.nan_count)) if self.nan_count[i] > 0]

	def remove_nan(self):
		#self.determine()
		#print([(self.idx2col[i], self.types[i], self.nan_count[i]) for i in range(len(self.columns))])

		for i in range(len(self.nan_list)):
			if self.dtype_dict[self.idx2col[self.nan_list[i]]] == np.dtype('O'):
				create_none_col()
			else:
				insert_mean()



	



data = Data("D:/Machine Learning Datasets/iris-species/iris_ruined.csv", "classification")
#print(data.main_df.Species.dtype())
#data = Data(x)


