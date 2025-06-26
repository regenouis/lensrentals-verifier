import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI
import logging

app = FastAPI()

# OpenAI client initialization (using Render-stored API key)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pydantic model for the request body
class ProductRequest(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/check_price")
async def check_price(request: ProductRequest):
    try:
        # Replace this prompt with your desired logic
        prompt = (
            f"Check the average resale price and availability online for the product "
            f"{request.product_name} with MPN {request.mpn}. Return findings in bullet format."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can switch to gpt-4 if your API key has access
            messages=[
                {"role": "system", "content": "You are a product analyst helping verify gear prices."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        result = response.choices[0].message.content.strip()
        return {"response": result}

    except Exception as e:
        logging.exception("Error in /check_price")
        return {"error": str(e)}
