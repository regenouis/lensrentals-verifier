from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Use Render environment variable (set in Render dashboard)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Define request body schema
class PriceCheckRequest(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/check_price")
async def check_price(request: PriceCheckRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # GPT-4 can be re-enabled if account supports it
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a pricing analyst assistant. Given a product name and MPN, "
                        "return a JSON object with suggested retail price and resale price range based on current market data."
                    )
                },
                {
                    "role": "user",
                    "content": f"Product: {request.product_name}\nMPN: {request.mpn}"
                }
            ],
            temperature=0.3,
            timeout=30
        )

        reply = response.choices[0].message.content.strip()
        return {"result": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
