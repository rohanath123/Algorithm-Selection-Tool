import pandas as pd 
import numpy as np

class Data:
	def __init__(self, PATH, task):
		self.main_df = pd.read_csv(PATH)

		self.columns = []
		self.types = []
		self.dtype_dict = {}
		self.idx2col = {}
		self.col2idx = {}
		self.y_labels = []
		self.target_var = ""
		self.nan_count = 0
		self.nan_list = []
		self.cat_values_dict_array = []
		self.dep = []
		self.essentail_cols = []



		self.clean_data()
	
	def clean_data(self):

		self.set_initial_vars()
		self.convert_cat()
		self.make_dependencies()
		self.sift_essential()
		#self.count_nan()
		#self.remove_nan()

	def set_initial_vars(self):
		self.set_cols()
		self.set_labels()
		self.index()
		self.set_types()
		self.make_type_dict()

	def make_dependencies(self):
		self.dep = self.main_df.corr().values.tolist()[0]
		self.dep = self.dep[1:len(self.dep)]
		print(self.dep)

	def sift_essential(self):
		self.essentail_cols = [self.idx2col[i+1] for i in range(len(self.dep)) if self.dep[i] >= 0.1 or self.dep[i] <= -0.1]
		print(self.essentail_cols)


	def set_cols(self):
		self.columns = list(self.main_df.columns)

	def set_labels(self):
		self.y_labels = list(self.main_df[self.columns[0]].tolist())
		self.target_var = self.columns[0]

	def index(self):
		for i in range(len(self.columns)):
			self.idx2col[i] = self.columns[i]
			self.col2idx[self.columns[i]] = i

	def set_types(self):
		self.types = list(self.main_df.dtypes)

	def make_type_dict(self):
		for i in range(len(self.columns)):
			self.dtype_dict[self.columns[i]] = self.types[i]

	def convert_cat(self):
		for i in range(len(self.dtype_dict)):
			if self.dtype_dict[self.idx2col[i]] == np.dtype('O'):
				self.numeric2cat(i)

	def numeric2cat(self, col_idx):
		unq = list(self.main_df[self.idx2col[col_idx]].unique())
		temp_dict = {unq[i-1]:i for i in range(1, len(unq)+1)}

		self.main_df[self.idx2col[col_idx]] = self.main_df[self.idx2col[col_idx]].replace(temp_dict)
		temp_dict["NAME"] = self.idx2col[col_idx]
		self.cat_values_dict_array.append(temp_dict)

	def count_nan(self):
		self.nan_count = list(self.main_df.isna().sum())
		self.nan_list = [i for i in range(len(self.nan_count)) if self.nan_count[i] > 0]

	def remove_nan(self):
		for n in self.nan_list:
			if self.dtype_dict[self.idx2col[n]] == np.dtype('O'):
				self.create_nan_col(self.idx2col[n])

data = Data("D:/Machine Learning Datasets/iris-species/iris_ruined.csv", "classification")



