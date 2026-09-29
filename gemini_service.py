import json
import base64
from typing import Optional
from google import genai
from google.genai import types
from app.config import settings

def _fallback(planner: str, data: dict):
    budget = float(data["budget"])
    if planner == "home":
        rows = [
            ("Lighting set", budget * .12, "Amazon", "Useful lighting option within the planned budget."),
            ("Ceiling fan", budget * .18, "Flipkart", "Balances utility and budget."),
            ("Storage unit", budget * .30, "IKEA", "Adds practical storage for the room."),
            ("Decor items", budget * .15, "Amazon", "Adds style without consuming the full budget."),
        ]
    elif planner == "party":
        rows = [
            ("Catering", budget * .45, "Swiggy", "Largest allocation for food."),
            ("Decoration", budget * .20, "Amazon", "Keeps the venue visually appealing."),
            ("Venue", budget * .25, "OYO", "Example venue/accommodation allocation."),
            ("Entertainment", budget * .10, "Local vendor", "Small flexible reserve."),
        ]
    else:
        rows = [
            ("Earrings", budget * .18, "Amazon", "Easy-to-match accessory."),
            ("Necklace", budget * .42, "Flipkart", "Main statement piece."),
            ("Bangles", budget * .20, "Amazon", "Complements the overall look."),
            ("Hair accessory", budget * .10, "Flipkart", "Optional finishing touch."),
        ]
    return {
        "planner": planner,
        "budget": budget,
        "summary": "Fallback recommendations are shown because Gemini is not configured or did not return usable data.",
        "recommendations": [
            {"category": r[0], "item": r[0], "estimated_price": round(r[1], 2), "platform": r[2], "reason": r[3]}
            for r in rows
        ],
    }

def _client():
    if not settings.gemini_api_key:
        return None
    return genai.Client(api_key=settings.gemini_api_key)

def generate_recommendation(planner: str, data: dict, image_bytes: Optional[bytes] = None, image_mime: Optional[str] = None):
    client = _client()
    if client is None:
        return _fallback(planner, data)

    prompt = f"""
You are PocketSmart AI, a budget-aware recommendation assistant.
Planner: {planner}
User input:
{json.dumps(data, indent=2)}

Return ONLY valid JSON with this shape:
{{
  "planner": "{planner}",
  "budget": number,
  "summary": "short summary",
  "recommendations": [
    {{
      "category": "string",
      "item": "string",
      "estimated_price": number,
      "platform": "Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO/Other",
      "reason": "short reason"
    }}
  ]
}}

Rules:
- Keep the sum of estimated_price values at or below the user's budget.
- Give 4 to 8 useful recommendations.
- Do not claim live price or stock verification.
- Platform names are suggestions only unless real API data is supplied.
"""
    contents = [prompt]
    if image_bytes and image_mime:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime))

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.4,
            ),
        )
        parsed = json.loads(response.text)
        return parsed
    except Exception:
        return _fallback(planner, data)
