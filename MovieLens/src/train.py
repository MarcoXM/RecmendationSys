import pandas as pd  
from dataset import MovieDataset
from sklearn.model_selection import train_test_split
from sklearn import metrics,preprocessing
from model import RecSysModel
import torch.optim as optim
import torch
from tqdm import tqdm 


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EPOCH = 10
TRAINING_BATCH_SIZE = 32
TEST_BATCH_SIZE = 16
debug = True

def train(dataloader,model,optimizer):
    model.train()
    for bi,data in tqdm(enumerate(dataloader)):
        user = data["user"]
        movie = data["movie"]
        rating = data["rating"]

        optimizer.zero_grad()
        output, loss , metrics = model(user, movie,rating)
        loss.backward()
        optimizer.step()

def evaluate(dataloader,model):
    model.eval()
    final_loss = 0
    counter = 0
    for bi,data in tqdm(enumerate(dataloader)):
        user = data["user"]
        movie = data["movie"]
        rating = data["rating"]


        output, loss , metrics = model(user, movie,rating)
        final_loss += loss  
    return final_loss/counter 



def run():
    df = pd.read_csv("data/MovieLens20M/rating.csv")
    
    user_lbler = preprocessing.LabelEncoder()
    movie_lbler = preprocessing.LabelEncoder()

    ## user is dense but not movies
    print(len(df.userId.unique()), max(df.userId.unique()),len(df.movieId.unique()), max(df.movieId.unique()))
    df.userId = user_lbler.fit_transform(df.userId.values)
    df.movieId = movie_lbler.fit_transform(df.movieId.values)

    if debug:
        df = df.head(10000)

    df_train, df_test = train_test_split(df,test_size=0.1,stratify=df.rating.values)
    df_train , df_valid = train_test_split(df_train,test_size=0.2,stratify=df_train.rating.values)

    train_dataset = MovieDataset(df_train.userId.values,df_train.movieId.values,df_train.rating.values )
    valid_dataset = MovieDataset(df_valid.userId.values,df_valid.movieId.values,df_valid.rating.values )


    train_loader = torch.utils.data.DataLoader(
        dataset = train_dataset,
        batch_size=TRAINING_BATCH_SIZE,
        shuffle=True,
        num_workers=4,
    )

    valid_loader = torch.utils.data.DataLoader(
        dataset = valid_dataset,
        batch_size=TEST_BATCH_SIZE,
        shuffle=False,
        num_workers=4,
    )

    model = RecSysModel(num_users=len(user_lbler.classes_), num_movies=len(movie_lbler.classes_))
    
    optimizer = optim.Adam(model.parameters(),lr = 1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer,mode="max",patience=5,factor=0.3,verbose=True)
    model.to(DEVICE)
    

    for e in range(EPOCH):
        train(dataloader = train_loader,model = model,optimizer = optimizer)
        score = evaluate(dataloader=valid_loader,model=model)
        scheduler.step(score)
        print("In the epoch {}, the loss in validation is {}".format(e,score))
        torch.save(model.state_dict(),"{}.pth".format("BASE_MODEL"))

if __name__ == "__main__":
    run()