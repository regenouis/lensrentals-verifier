import os
import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()  # Loads OPENAI_API_KEY from .env

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class ProductInfo(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/check_price")
def check_price(info: ProductInfo):
    try:
        prompt = f"""
You are a product research assistant. Find current pricing information for this item:
Product Name: {info.product_name}
MPN: {info.mpn}

Return only the most relevant details from B&H, Adorama, eBay (sold and active listings), and MPB.
Structure the results clearly.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful product pricing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return {"results": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
