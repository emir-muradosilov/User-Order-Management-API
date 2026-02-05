from fastapi import FastAPI
from db.db_session import init_db

app = FastAPI(debug = True,)


from api.v1.auth import router as auth
from api.v1.orders import router as orders
from api.v1.products import router as products
from api.v1.users import router as user

app.include_router(auth)
app.include_router(user)
app.include_router(orders)
app.include_router(products)


@app.on_event("startup")
async def on_startup():
    await init_db()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = '127.0.0.1', port = 8082, reload=True)


