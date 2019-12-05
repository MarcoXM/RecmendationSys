import math
import pandas as pd

class UserCF(object):
    def __init__(self,data):
        if not data:
            self.data = self._init_user_score()
        else:
            self.data = pd.read_csv(data).to_dict('dict')
        self.user_sim = self.similarity()

    def _init_user_score(self):
        dit = {'A':{'a':3.0,'b':4.0,'c':1.0,'d':2.0,'e':3.0},
                'B':{'a':3.0,'b':4.0,'c':1.0,'d':2.0,'e':3.0},
                'C':{'a':3.0,'b':4.0,'c':1.0,'d':2.0,'e':3.0},
                'D':{'a':3.0,'b':4.0,'c':1.0,'d':2.0,'e':3.0}}
        return dit


    def similarity(self):
        W = dict()
        for u in self.data.keys():
            W.setdefault(u,{})
            for v in self.data.keys():
                if u==v:
                    continue
                u_set = set([key for key in self.data[u].keys() if self.data[u][key]>0])
                v_set = set([key for key in self.data[v].keys() if self.data[v][key]>0])
                W[u][v] = float(len(u_set& v_set))/math.sqrt(len(u_set)+len(v_set)))

        return w
            

    def preUserItemScore(self,usera,item):
        score = 0.

        for user in self.user_sim[usera].keys():
            if user ! usera:
                score += self.user_sim[usera][user] * self.data[user][item]
                
        return score

    def recommend(self,usera):
        user_item_score_dict = {}
        for item in self.data[usera].keys():
            if user.data[usera][item] <= 0:
                user_item_score_dict[item]= self.preUserItemScore(user,item)
        return user_item_score_dict
    

