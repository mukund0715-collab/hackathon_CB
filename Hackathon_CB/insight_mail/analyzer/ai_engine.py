import json
# import openai  # Uncomment this when you have your API Key

def analyze_email_content(subject, body):
    """
    This function simulates an LLM analysis.
    Later, we replace the dummy data with a real OpenAI call.
    """
    
    # --- REAL AI CODE (Commented out for now) ---
    # prompt = f"Analyze this email. Subject: {subject}. Body: {body}. Return JSON with sentiment, risk_score (0-100), summary, tone, suggested_reply."
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    # return json.loads(response.choices[0].message.content)
    # ---------------------------------------------

    # --- SIMULATION MODE (So you can build the UI fast) ---
    # Simple keywords to fake intelligence for testing
    subject_lower = subject.lower()
    body_lower = body.lower()
    
    risk_score = 10
    tone = "Neutral"
    sentiment = "Neutral"
    
    if "angry" in body_lower or "stupid" in body_lower:
        sentiment = "Negative"
        tone = "Aggressive"
        risk_score = 80
    elif "refund" in body_lower:
        sentiment = "Negative"
        tone = "Frustrated"
        risk_score = 40
    elif "thank" in body_lower:
        sentiment = "Positive"
        tone = "Appreciative"
        risk_score = 0

    return {
        "summary": f"User is writing about {subject}. Detected tone is {tone}.",
        "sentiment": sentiment,
        "tone": tone,
        "risk_score": risk_score,
        "suggested_category": "Complaint" if risk_score > 50 else "Inquiry",
        "suggested_reply": f"Dear Customer, thank you for your email regarding '{subject}'. We are looking into it immediately."
    }