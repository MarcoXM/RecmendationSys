import torch
import torch.nn as nn
import numpy as np 
from sklearn import metrics

class RecSysModel(nn.Module):
    def __init__(self, num_users, num_movies):
        super().__init__()
        self.user_embed = nn.Embedding(num_users, 32)
        self.movie_embed = nn.Embedding(num_movies, 32)
        self.regressor = nn.Linear(64,1)


    def get_metric(self, output, rating ):
        output = output.detach().cpu().numpy()
        rating = rating.detach().cpu().numpy()
        return {
            "rmse" : np.sqrt(metrics.mean_squared_error(rating,output)) ## sklearn , true is the first arguement 
        }



    def forward(self,u , m , r = None):

        x_user = self.user_embed(u)
        x_movie = self.movie_embed(m)
        x = torch.cat([x_user,x_movie],dim = 1)
        output = self.regressor(x)
        loss = None
        metric = None
        if r is not None:
            loss = nn.MSELoss()(output, r.view(-1,1))
            metric = self.get_metric(output, r.view(-1,1))

        return output, loss , metric     



