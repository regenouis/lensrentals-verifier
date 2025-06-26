from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ProductInfo(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/check_price")
async def check_price(info: ProductInfo):
    try:
        prompt = f"""
You are a camera gear expert. A user is researching a product called "{info.product_name}" with MPN (Manufacturer Part Number) "{info.mpn}". 
Give a short list of what stores typically sell it (e.g., B&H, Adorama, eBay, MPB) and what its new and used prices usually are.
Only return concise, accurate pricing info without commentary.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # <- This was changed from gpt-4
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400
        )

        result = response['choices'][0]['message']['content'].strip()
        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
