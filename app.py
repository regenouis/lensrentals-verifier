from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai

app = FastAPI()

# Use environment variable directly
openai.api_key = os.environ["OPENAI_API_KEY"]

class ProductRequest(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/check_price")
async def check_price(request: ProductRequest):
    try:
        query = f"What is the average used and new price for a {request.product_name} with MPN {request.mpn}?"

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful product price researcher."},
                {"role": "user", "content": query}
            ]
        )

        result = response.choices[0].message.content.strip()
        return {"response": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
