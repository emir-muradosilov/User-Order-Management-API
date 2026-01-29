from fastapi import FastAPI
from db.db_session import init_db

app = FastAPI(debug = True,)


from api.v1.auth import router as auth
app.include_router(auth)


@app.on_event("startup")
async def on_startup():
    await init_db()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8082, reload=True)


