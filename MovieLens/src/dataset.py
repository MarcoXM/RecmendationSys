import torch 



class MovieDataset:
    def __init__(self, users, movies , ratings):
        self.users  = users
        self.movies = movies 
        self.ratings = ratings

    def __len__(self):
        return len(self.users)


    def __getitem__(self, idx):
        user = self.users[idx]
        movie = self.movies[idx]
        rating = self.ratings[idx]

        return {
            "user":torch.tensor(user,dtype=torch.long),
            "movie":torch.tensor(movie,dtype=torch.long),
            "rating":torch.tensor(rating,dtype=torch.float),
        }
