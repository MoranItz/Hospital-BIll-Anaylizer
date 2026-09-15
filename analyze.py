import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_ai_review(message):
    if not message:
        return "No message provided."

    text = message
    print(text)

    prompt = f"""
You are a careful hospital-bill review assistant. Analyze the image below and
create a professional, PDF-ready HTML report for the patient.

IMPORTANT ACCURACY RULES:
1. First decide whether the text is a hospital bill or receipt. If it is not, return
    only this exact HTML: <p>The PDF file provided does not appear to be a valid receipt.</p>
2. Include every identifiable line item from the bill. Preserve each original charged
    price exactly as shown; never replace, round, or silently omit it.
3. For each line item, put the original charged price and the estimated fair price
    next to each other in the same table row. Use "Not available" when a fair price
    cannot be responsibly estimated.
4. Clearly label all suggested prices as estimates, explain the source or reasoning,
    and state that prices vary by location, insurer, facility, and patient condition.
    Do not invent a location, insurance adjustment, medical code, or market price.
5. Separate facts read from the bill from assumptions and estimates. Flag unclear OCR,
    duplicate charges, missing quantities, unexplained fees, and arithmetic errors.
6. Compare subtotals and totals when they are visible. Do not claim fraud or wrongdoing;
    describe an amount as potentially high, unclear, or needing verification instead.
7. End with practical next steps, such as requesting an itemized bill, asking the
    provider to explain codes, checking the insurer's explanation of benefits, and
    requesting an appeal or correction when appropriate.

REPORT STRUCTURE:
- A title: "Hospital Bill Review"
- A short overall assessment with a confidence level
- A table with these columns, in this order: Service or charge, Quantity, Original
  charged price, Estimated fair price, Difference, Assessment
- A totals section with original total and estimated total when calculable
- "How the estimates were determined"
- "Items needing verification"
- "Recommended next steps"

HTML OUTPUT RULES:
- Return only a complete HTML fragment inside <article>...</article>.
- Do not use Markdown, code fences, scripts, external images, or external stylesheets.
- Use semantic tags such as <h1>, <h2>, <p>, <table>, <thead>, <tbody>, <tr>, <th>,
  and <td>. Keep text concise enough to fit on printed pages.
- Use class names "summary", "good", "warning", "bad", and "muted" when helpful.
- Use plain text for all prices and preserve currency symbols when they are present.

OCR IMAGE BINARY FROM THE BILL:
{text}
"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"