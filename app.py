from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Define request body model
class PriceRequest(BaseModel):
    product_name: str
    mpn: str

# Initialize OpenAI client
client = OpenAI()

@app.get("/")
async def root():
    return {"message": "Verifier backend is live."}

@app.post("/check_price")
async def check_price(request: PriceRequest):
    try:
        prompt_text = (
            f"You are an expert in camera gear pricing. "
            f"Estimate the current average used price in USD for the product '{request.product_name}' with MPN '{request.mpn}'. "
            f"Follow this process step by step:\n"
            f"1. Search your training data for pricing trends and typical ranges.\n"
            f"2. Check approximate pricing from reputable sources such as B&H, Adorama, Amazon, and MPB.\n"
            f"3. If you are unsure or cannot find data, clearly say 'unknown'.\n"
            f"4. Respond ONLY with a valid JSON object in this format:\n"
            f'{{"price_estimate_usd": "XXX.XX", "confidence": "high/medium/low"}}\n'
            f"Never include extra commentary or disclaimers."
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise pricing analyst for camera gear. "
                        "Always follow instructions carefully and never make up data."
                    )
                },
                {"role": "user", "content": prompt_text}
            ],
            temperature=0
        )

        ai_response = completion.choices[0].message.content.strip()

        return {
            "status": "success",
            "product_name": request.product_name,
            "mpn": request.mpn,
            "ai_raw_response": ai_response
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
