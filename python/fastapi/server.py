import random

from fastapi import FastAPI, HTTPException, Response

# CORS or "Cross-Origin Resource Sharing" refers to the situations when 
# a frontend running # in a browser has JavaScript code that communicates with a backend, 
# and the backend is in a different "origin" than the frontend.
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

import prometheus_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*",], allow_methods=["*",], allow_headers=["*",], 
)

heads_count = prometheus_client.Counter(
    "heads_count", 
    "Number of heads",
)

tails_count = prometheus_client.Counter(
    "tails_count", 
    "Number of tails",
)

flip_count = prometheus_client.Counter(
    "flip_count", 
    "Number of flips",
)


@app.get("/flip-coins")
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(
            status_code=400,
            detail="times must be set in request and an integer"
        )

    # flipping coins    
    times_as_int = int(times)
    
    heads = 0
    for _ in range(times_as_int):
        # this will be 0 or 1, if 1, it evaluates to True
        if random.randint(0,1):
            heads += 1
    tails = times_as_int - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flip_count.inc(times_as_int)


    return {
        "heads" : heads,
        "tails" : tails,
    }

@app.get("/metrics")
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest(),
    )

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.140.102", port=5000)



