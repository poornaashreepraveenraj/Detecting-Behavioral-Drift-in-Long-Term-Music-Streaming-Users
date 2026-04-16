from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from recommender import recommender
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    genres: List[str]
    artists: List[str]
    time_of_day: str  # morning | afternoon | evening | night
    energy_preference: float  # 0 to 100
    mood_preference: float  # 0 to 100 (Valence)

@app.post("/recommend")
async def recommend(data: RecommendRequest):
    # The new recommender handles the pandas-based similarity search
    recs = recommender.get_recommendations(
        genres=data.genres,
        artists=data.artists,
        time_of_day=data.time_of_day,
        energy_pref=data.energy_preference,
        mood_pref=data.mood_preference
    )
    return {"recommendations": recs}

@app.get("/")
async def read_index():
    return FileResponse('index.html')

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
