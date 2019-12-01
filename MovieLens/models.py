import json
import numpy as np 
import pandas as pd 
import math
import random

class CBrecommand(object):
	def __init__(self,K):
		self.K = K
		self.item_profiles = json.load(open('data/item_profile/json','r'))
		self.user_profiles = json.load(open('data/user_profile.json','r'))

	def get_none_score_item(self,user):
		items = pd.read_csv('data/movies.csv')['MovieID'].values
		data = pd.read_csv('data/ratings.csv')
		have_score_items = data[data['UserID']==user]['MovieID'].values
		none_score_items = set(items)-set(have_score_items)
		return none_score_items

	def cosUI(self,user,item):
		Uia = sum(
			np.array(self.user_profiles[str(user)])
			*
			np.array(self.item_profiles[str(item)])
			)
		Ua = math.sqrt(sum([math.pow(one,2) for one in self.user_profiles[str(user)]]))
		Ia = math.sqrt(sum([math.pow(one,2) for one in self.item_profiles[str(item)]]))
		return Uia/(Ua*Ia)


	def recommand(self,user):
		user_result = {}
		item_list = self.get_none_score_item(user)
		for item in the item_list:
			user_result[item] = self.cosUI(user,item)
		if not self.K:
			result = sorted(user_result.items(),key = lambda k:k[1],reverse = True)

		else:
			result = sorted(user_result.items(),key = lambda k:k[1],reverse = True)[:self.K]

		return result



	def evaluate(self):
		evals = []
		data = pd.read_csv('data/ratings.csv')

		for user in random.sample([one for one in range(6040)],20):
			have_score_items = data[data['UserID'] == user]['MovieID'].values
			items = pd.read_csv('data/movies.csv')['MovieID'].values	
			user_result = {}
			for item in items:
				user_result[item] = self.cosUI(user,item)
			result = sorted(user_result.items(),key = lambda k:k[1],reverse=True)[:len(have_score_items)]

			recItem = []
			for one in result:
				recItem.append(one[0])
			eva = len(set(recItem) & set(have_score_items)) / len(have_score_items)
			evals.append(eva)

		return sum(evals)/len(evals)





if __name__ == "__main__":
	cb = CBrecommand(10)
	print(cb.recommand(12))