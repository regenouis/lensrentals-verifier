from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client (free-tier compatible)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request schema for validation
class PriceRequest(BaseModel):
    product_name: str
    mpn: str

@app.get("/")
async def root():
    return {"message": "AI Pricing Verifier backend is live."}

@app.post("/check_price")
async def check_price(request: PriceRequest):
    try:
        # Build a strong, clear prompt
        prompt = (
            f"You are a professional photography equipment pricing analyst.\n\n"
            f"Given the product below, find the most likely current retail price range in USD.\n\n"
            f"Requirements:\n"
            f"- Cite reputable sources you draw from (even if approximate)\n"
            f"- Rate your confidence (high, medium, low)\n"
            f"- Never hallucinate or invent data. If unsure, say so clearly.\n\n"
            f"Product Name: {request.product_name}\n"
            f"MPN: {request.mpn}\n\n"
            f"Respond in JSON with keys: price_estimate, confidence, sources (array), note.\n"
        )

        # Create the completion
        completion = client.chat.completions.create(
            model="gpt-4o",  # Or "gpt-3.5-turbo" for cheaper cost
            messages=[
                {"role": "system", "content": "You are a pricing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0  # Keep deterministic
        )

        # Parse the text response
        raw_response = completion.choices[0].message.content

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "raw_response": raw_response
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )
