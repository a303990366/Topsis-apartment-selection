import pandas as pd
import numpy as np
#----591---
import re
from turn_item_to_score import alter_house_type,alter_rent_type,alter_role_type

class TOPSIS:
    def __init__(self,data,weight,criteria):
        self.ori_data = data
        self.weight = weight
        self.criteria_stand = criteria
        self.base_val = []
        self.V_positive = []
        self.V_negative = []
    def vector_normalization(self,x):
        '''Function of normalization'''
        return (np.square(x).sum())**0.5
    def create_base_val(self):
        for col in self.df.columns:
            val = self.vector_normalization(self.df[col].to_list())
            self.base_val.append(val)
    def get_prefer(self):
        self.V_positive = self.normalize_weight_matrix.max().to_list()
        self.V_negative = self.normalize_weight_matrix.min().to_list()
        print(self.V_positive,self.V_negative)

        for standard_index in range(len(self.criteria_stand)):
            if self.criteria_stand[standard_index] == -1: 
                self.V_positive[standard_index],self.V_negative[standard_index] = self.V_negative[standard_index],self.V_positive[standard_index]
    def get_ideal_solution(self):
        positive_ideal_solution = ((((self.normalize_weight_matrix - self.V_positive)**2).sum(axis=1))**0.5).round(4)
        negative_ideal_solution = ((((self.normalize_weight_matrix - self.V_negative)**2).sum(axis=1))**0.5).round(4)
        self.normalize_weight_matrix['positive_ideal_solution'] = positive_ideal_solution
        self.normalize_weight_matrix['negative_ideal_solution'] = negative_ideal_solution
    def main(self):
        #self.df = self.ori_data.set_index('attribute')#set attribute column as index
        self.df =self.ori_data
        self.create_base_val()
        self.normalize_matrix = (self.df/self.base_val).round(4)    
        self.normalize_weight_matrix = (self.normalize_matrix* self.weight).round(4) #normalize
        self.get_prefer()
        self.get_ideal_solution()
        self.normalize_weight_matrix['diff_ideal_solution'] = self.normalize_weight_matrix['positive_ideal_solution'] + \
                                                    self.normalize_weight_matrix['negative_ideal_solution']
        self.normalize_weight_matrix['performance_score'] = self.normalize_weight_matrix['negative_ideal_solution'] / self.normalize_weight_matrix['diff_ideal_solution']
        self.rank_solution = self.normalize_weight_matrix['performance_score'].rank(ascending=False).to_frame()
        self.rank_solution.columns = ['Rank']
        self.ori_data['rank'] = self.rank_solution

def run_topsis_and_get_result(path,weight):
    #'final_591data.csv'
    data = pd.read_csv(path)
    #preprocessing data
    data['price'] = data['price'].apply(lambda x : float(x.replace(',','')))
    data['rent type'] = data['rent type'].apply(lambda x: alter_rent_type(x))
    data['area'] = data['area'].apply(lambda x: float(x.replace('坪','')))
    data['building type'] = data['building type'].apply(lambda x: alter_house_type(x))
    data['role'] = data['role'].apply(lambda x: alter_role_type(x))
    data['reach ratio'] = data['favorite num']/data['browse num']
    data['reach ratio'] = data['reach ratio'].fillna(0)
    #real input frame
    input_frame = data[["price",'rent type','traffic','life','education','area','building type','equiment','role','reach ratio']]
    #set criteria direction: 1 means the column's value should be higher
    criteria = [1 for i in range(len(input_frame.columns))]
    criteria[0] = -1 #price
    #run topsis
    test=TOPSIS(input_frame,weight=weight,
      criteria = criteria)
    test.main()
    final_info = pd.merge(data,test.ori_data,how = 'outer')
    return final_info


##if __name__ =="__main__":
##    info = run_topsis_and_get_result()
