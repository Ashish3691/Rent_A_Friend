 # Entry point to start the FastAPI server
 
 
from fastapi import FastAPI


app = FastAPI(title="Rent A Friend")

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(verification.router, prefix="/verification", tags=["Verification"])
app.include_router(sos.router, prefix="/sos", tags=["SOS"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring"])
app.include_router(rating.router, prefix="/rating", tags=["Rating"])

@app.get("/")
def read_root():
    return {"message": "Welcom to this Platform"}

