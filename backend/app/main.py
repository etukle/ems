from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.routers import user_router, auth_router
from app.database import Base, engine, db_dependency as db

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "OK", "message": "Application is running properly"}


@app.get("/db-check")
def db_check(db: db):
    try:
        result = db.execute(text("SELECT 1"))
        return {"status": "OK", "message": "Database is healthy", "result": result}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


app.include_router(user_router.router)
app.include_router(auth_router.router)
