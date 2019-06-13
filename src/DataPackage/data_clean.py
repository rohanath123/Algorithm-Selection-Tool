import pandas as pd 
import numpy as np

class Data:
	def __init__(self, PATH, task):
		self.ultra_df = pd.read_csv(PATH)
		self.main_df = self.ultra_df.copy()
		self.task = task

		self.y_labels = []
		self.target_var = ""
		self.nan_count = 0
		self.nan_list = []
		self.cat_values_dict_array = []
		self.dep = []
		self.essential_cols = []

		self.df_temp = self.main_df.copy()


		self.clean_data()
	
	def clean_data(self):

		self.set_initial_vars()
		self.convert_cat()
		self.make_dependencies()
		self.sift_essential()
		self.remove_non_essential()

		self.set_initial_vars()
		self.count_nan()
		self.remove_nan()

	def set_initial_vars(self):
		self.dtype_dict = {}
		self.idx2col = {}
		self.col2idx = {}
		self.columns = []
		self.types = []

		self.set_cols()
		self.set_labels()
		self.index()
		self.set_types()
		self.make_type_dict()

	def set_cols(self):
		self.columns = list(self.main_df.columns)
		
	def set_labels(self):
		self.y_labels = self.main_df[self.columns[0]]
		self.target_var = self.columns[0]

	def index(self):
		for i in range(len(self.columns)):
			self.idx2col[i] = self.columns[i]
			self.col2idx[self.columns[i]] = i

	def set_types(self):
		self.types = list(self.main_df.dtypes)
		#print(self.types)

	def make_type_dict(self):
		self.dtype_dict = {self.columns[i]:self.types[i] for i in range(len(self.columns))}
		

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

	def make_dependencies(self):
		self.dep = self.main_df.corr().values.tolist()[0]
		self.dep_total = self.main_df.corr()
		self.dep = self.dep[1:len(self.dep)]

	def sift_essential(self):
		self.essential_cols = [self.idx2col[i+1] for i in range(1, len(self.dep)) if self.dep[i] >= 0.05 or self.dep[i] <= -0.05]
		self.essential_cols[0] = self.columns[0]

	def remove_non_essential(self):
		non_ess = [self.columns[i] for i in range(len(self.columns)) if self.columns[i] not in self.essential_cols]
		for i in range(len(non_ess)):
			self.df_temp = self.df_temp.drop([non_ess[i]], axis = 1)

		self.main_df = self.df_temp.copy()

	def count_nan(self):
		self.nan_count = list(self.main_df.isna().sum())
		self.nan_list = [self.idx2col[i] for i in range(len(self.nan_count)) if self.nan_count[i] > 0]

	def remove_nan(self):
		self.handle_numeric_nans()
		#self.handle_cat_nans()
						
	def handle_numeric_nans(self):
		if self.task == 'classification':
			classes, classwise_mean = self.calculate_classwise_mean()
			classwise_frames = [self.main_df[self.main_df[self.columns[0]] == classes[i]] for i in range(len(classes))]

			for i in range(len(classwise_frames)):
				for col in self.nan_list:
					if self.dtype_dict[col] != np.dtype('O'):
						classwise_frames[i] = classwise_frames[i].fillna({col:classwise_mean[classes[i]][col]})

			df3 = pd.DataFrame([])
			for i in range(len(classwise_frames)):
				df3 = pd.concat([df3, classwise_frames[i]])

			self.main_df = df3.sample(frac = 1).reset_index(drop = True)
			self.set_labels()

		elif self.task == 'regression':
			print("regression")

	def calculate_classwise_mean(self):
		classes = self.y_labels.unique().tolist()
		classwise_mean = {}
		for c in classes:
			temp = self.main_df[self.main_df[self.columns[0]] == c]
			classwise_mean[c] = {self.columns[i]: temp[self.columns[i]].fillna(0).values.mean() for i in range(len(self.columns)) if self.dtype_dict[self.columns[i]] != np.dtype('O')}
		return classes, classwise_mean

		

data = Data("D:/Machine Learning Datasets/titanic/train.csv", "classification")
print(data.main_df)
print(data.y_labels)