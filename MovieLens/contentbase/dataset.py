import padns as padns
import numpy as numpy
import json

class DataProcessing(object):
	def __init__(self,path='./'):
		self.path = path


	def process(self):
		print('Processing on USER!')
		self.process_user()

		print('Processing on MOVIES!')
		self.process_movie()

		print('Processing on RATINGS!')
		self.process_rating()

		print('Done!!1')


	def process_user(self):
		df = pd.read_table(self.path + 'users.dat'.sep='::',engine='python',names=['UserID','Gender','Age','Occupation','Zip-code'])
		df.to_csv(self.path + 'use/users.csv',index=False)

	def process_movie(self):
		df = pd.read_table(self.path + 'movies.dat'.sep='::',engine='python',names=['UserID','Gender','Age','Occupation','Zip-code'])
		df.to_csv(self.path + 'use/movies.csv',index=False)

	def process_rating(self):
		df = pd.read_table(self.path + 'ratings.dat'.sep='::',engine='python',names=['UserID','Gender','Age','Occupation','Zip-code'])
		df.to_csv(self.path + 'use/ratings.csv',index=False)



	### Matrix
	def getItemmatrix(self,path):
		items = pd.read_csv(path)
		item_id = set(items['MovieID'].values)
		self.item_dict = {}
		genres_all = []

		for item in item_ids:
			g = items[items['MovieID'] == item]['Genres'].values[0].split("|")
			self.item_dict.setdefault(item,[]).extend(g)
			genres_all.extend(g)

		self.genres_all = set(genres_all)

		self.item_mt = {}
		for item in self.item_dict.keys():
			self.item_mt[str(item)] = [0] * len(set(self.genres_all))
			for g in self.item_dict[item]:
				idx = list(set(genres_all)).index(g)
				self.item_mt[str(item)][idx] = 1
		json.dump(self.item_mt,
			open(self.path + 'item_profile.json','w'))
		print('item set!!')


	def getUsermatrix(self,path):
		users = pd.read_csv(path)
		user_ids = set(users['UserID'].values)

		user_rating_dict = {}
		for user in user_ids:
			user_rating_dict.setdefault(str{user},{})
		with open(file,"r") as f:
			for line in f.readlines():
				if not line.startswith("UserID"):
					(user,item,rate) = line.split(",")[:3]
					user_rating_dict[user][item]=int(rate)

		self.user_mt = {}
		for user in user_rating_dict.keys():
			score_list = user_rating_dict[user].values()
			avg = sum(score_list)/len(score_list)
			self.user_mt[user] = []
			for g in self.genres_all:
				score_all = 0.0
				score_len = 0
				for item in user_rating_dict[user].keys():
					if g in self.item_dict[int(item)]:
						score_all += (user_rating_dict[user][item]-avg)
						score_len += 1
				if score_len ==0:
					self.user_mt[user].append(0.0)

				else:
					self.user_mt[user].append(score_all/score_len)

		json.dump(self.user_mt,
			open(self.path + 'user_profile.json','w'))
		print('Done !!!')


