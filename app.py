from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

# Legacy client initialization compatible with openai==0.28.1
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "Verifier backend is live."}

@app.post("/check_price")
async def check_price(request: Request):
    try:
        payload = await request.json()
        product_name = payload.get("product_name")
        mpn = payload.get("mpn")

        # Just confirming payload received — actual lookup logic goes here
        return {
            "status": "success",
            "product_name": product_name,
            "mpn": mpn,
            "note": "This is a placeholder response. Price logic not implemented in this file."
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
