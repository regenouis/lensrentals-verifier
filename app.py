from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

# Initialize OpenAI client (no arguments if OPENAI_API_KEY is in environment)
client = OpenAI()

@app.get("/")
async def root():
    return {"message": "Verifier backend is live."}

@app.post("/check_price")
async def check_price(request: Request):
    try:
        payload = await request.json()
        product_name = payload.get("product_name")
        mpn = payload.get("mpn")

        # Construct prompt for AI
        prompt_text = (
            f"Find the average current price online for the product '{product_name}' "
            f"with MPN '{mpn}'. Return ONLY the price in USD, no extra text."
        )

        # Call OpenAI completion
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You provide pricing data in USD."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0
        )

        # Extract text response
        ai_response = completion.choices[0].message.content.strip()

        return {
            "status": "success",
            "product_name": product_name,
            "mpn": mpn,
            "price_estimate_usd": ai_response
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
