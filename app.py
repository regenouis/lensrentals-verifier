from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

# Initialize modern OpenAI client
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

        prompt = (
            f"You are a pricing analyst. Search B&H, Adorama, MPB, and eBay "
            f"for the product '{product_name}' with MPN '{mpn}'. "
            f"Provide a JSON object listing each site with URL, new price, used price, and stock status."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        return JSONResponse(
            content={
                "ai_response": answer
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )
