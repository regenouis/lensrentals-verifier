import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import logging

app = FastAPI()

# Initialize OpenAI client (no proxies, matches openai==1.25.1+)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ProductRequest(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/check_price")
async def check_price(request: ProductRequest):
    try:
        prompt = (
            f"Find current pricing and availability for {request.product_name} "
            f"with MPN {request.mpn}. Summarize the results in bullet points."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful product analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return {"response": response.choices[0].message.content.strip()}

    except Exception as e:
        logging.exception("Error occurred in /check_price")
        return {"error": str(e)}
