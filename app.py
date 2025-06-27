from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Request body model
class PriceRequest(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
async def root():
    return {"message": "Verifier backend is live."}

@app.post("/check_price")
async def check_price(payload: PriceRequest):
    # Extract data
    product_name = payload.product_name
    mpn = payload.mpn

    # Example response
    return {
        "status": "success",
        "product_name": product_name,
        "mpn": mpn,
        "note": "This is a placeholder response."
    }
