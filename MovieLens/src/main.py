from fastapi import FastAPI
from model import RecSysModel


app = FastAPI()
MODEL_PATH = " "


model = RecSysModel(num_users=len(user_lbler.classes_), num_movies=len(movie_lbler.classes_))
model.load_state_dict(MODEL_PATH)
@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/")
async def predict(user_id, movie_id):
    dataset = MovieDataset([user_id], [movie_id], [-1])

    data = dataset.__getitems__(-1)
    output, _, _ = model(data["user"], data['movie'])
    return {
        "ouput" : output
    }



