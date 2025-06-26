from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
import re
import os
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductRequest(BaseModel):
    product_name: str
    mpn: str

class GPTResponse(BaseModel):
    raw_output: str
    valid: bool
    score: int
    issues: list
    manual_links: dict

def build_prompt(product_name, mpn):
    return f"""
    Search the following platforms for a product with these details:
    - Name: {product_name}
    - MPN: {mpn}

    Return your results in this exact format:
    {{
      "product_found": true/false,
      "platforms": {{
        "B&H": {{"price": "$XXX.XX", "stock_status": "In Stock / Out of Stock / Unknown", "link": "full URL or null"}},
        "Adorama": {{...}},
        "eBay": {{...}}
      }},
      "resale_suggestion": "$XXX.XX"
    }}

    Do not estimate or fabricate data. Say "not found" if necessary.
    """

def validate_gpt_output(data):
    score = 100
    reasons = []
    try:
        output = json.loads(data)
    except json.JSONDecodeError:
        return {"valid": False, "score": 0, "issues": ["Invalid JSON format"]}

    required_keys = ["product_found", "platforms", "resale_suggestion"]
    for key in required_keys:
        if key not in output:
            score -= 25
            reasons.append(f"Missing key: {key}")

    platforms = output.get("platforms", {})
    for site, info in platforms.items():
        if not re.match(r"\$\d+(?:\.\d{2})?", info.get("price", "")):
            score -= 10
            reasons.append(f"Invalid price format at {site}")
        if not info.get("link", "").startswith("https://"):
            score -= 10
            reasons.append(f"Invalid or missing link at {site}")
        if "stock_status" not in info:
            score -= 5
            reasons.append(f"Missing stock_status at {site}")

    resale_price = output.get("resale_suggestion", "")
    if not re.match(r"\$\d+(?:\.\d{2})?", resale_price):
        score -= 10
        reasons.append("Invalid resale suggestion format")

    return {
        "valid": score >= 70,
        "score": max(score, 0),
        "issues": reasons
    }

def get_gpt_output(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )
    return response.choices[0].message["content"]

def get_manual_search_links(product_name, mpn):
    encoded_name = quote_plus(product_name)
    return {
        "B&H Search": f"https://www.bhphotovideo.com/c/search?Ntt={mpn}",
        "Adorama Search": f"https://www.adorama.com/l/?searchinfo={mpn}",
        "eBay Used": f"https://www.ebay.com/sch/i.html?_nkw={mpn}+used",
        "eBay Sold": f"https://www.ebay.com/sch/i.html?_nkw={mpn}+used&_sop=13&LH_Complete=1&LH_Sold=1"
    }

@app.post("/check_price", response_model=GPTResponse)
def check_price(request: ProductRequest):
    prompt = build_prompt(request.product_name, request.mpn)
    try:
        raw_output = get_gpt_output(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    validation = validate_gpt_output(raw_output)
    manual_links = get_manual_search_links(request.product_name, request.mpn)

    return GPTResponse(
        raw_output=raw_output,
        valid=validation["valid"],
        score=validation["score"],
        issues=validation["issues"],
        manual_links=manual_links
    )

@app.get("/")
def root():
    return {"status": "ok"}
