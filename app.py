from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

# Safe client initialization for OpenAI 1.x
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

        # This is placeholder AI logic - adjust prompt as needed
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that retrieves product pricing information."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Please look up pricing for the product '{product_name}' "
                        f"with MPN '{mpn}'. Return any known pricing data."
                    ),
                },
            ],
        )

        ai_response = completion.choices[0].message.content

        return {
            "status": "success",
            "product_name": product_name,
            "mpn": mpn,
            "ai_response": ai_response,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
