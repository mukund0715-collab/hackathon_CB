import json
import random
import google.generativeai as genai
from textblob import TextBlob
from django.conf import settings
# Make sure you have the keywords.py file we created earlier
from .keywords import DANGER_KEYWORDS, COMPLAINT_KEYWORDS, FINANCE_KEYWORDS

# ---------------------------------------------------------
# CONFIGURATION: API SETUP (Only for Drafting)
# ---------------------------------------------------------
GOOGLE_API_KEY = "AIzaSyDGsKNjOPjFQkuQub0vyz-2V3R-VN-4m64" # <--- PASTE KEY HERE
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_email_content(subject, body, history=[], agent_name="Support Team"):
    """
    HYBRID ENGINE: 
    1. LOCAL: Uses TextBlob & Keywords for Speed/Consistency (Risk/Sentiment).
    2. CLOUD: Uses Gemini API for Creative Drafting (suggested_reply).
    """
    
    # ============================================================
    # PART A: LOCAL ANALYSIS (Your existing code)
    # ============================================================
    text = f"{subject} {body}"
    blob = TextBlob(text)
    text_lower = text.lower()
    
    # --- 1. CALCULATE SENTIMENT (Math) ---
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # --- 2. CALCULATE TONE (Heuristics) ---
    if text.isupper() or body.count("!") > 3:
        tone = "Aggressive / Urgent"
    elif polarity < -0.3:
        tone = "Frustrated"
    elif polarity > 0.5:
        tone = "Excited"
    else:
        tone = "Professional"

    # --- 3. DETECT RISK & CATEGORY (Keyword Matching) ---
    risk_score = 10  # Base risk
    flagged = []
    category = "Inquiry" # Default

    # Check Danger
    for word in DANGER_KEYWORDS:
        if word in text_lower:
            risk_score += 30
            flagged.append(word)
            category = "Compliance Issue"

    # Check Complaints
    for word in COMPLAINT_KEYWORDS:
        if word in text_lower:
            risk_score += 10
            category = "Complaint"
            
    # Check Finance
    for word in FINANCE_KEYWORDS:
        if word in text_lower:
            category = "Finance"

    # Adjust risk based on sentiment
    if sentiment == "Negative":
        risk_score += 20
    
    # Cap risk
    if risk_score > 99: risk_score = 99

    # Format flagged words for display
    flagged_display = ", ".join(list(set(flagged))[:5])

    # ============================================================
    # PART B: API DRAFTING (The Change)
    # ============================================================
    
    # Format history for context
    history_text = "No previous context."
    if history:
        history_text = "\n".join([f"- {msg['sender']}: {msg['body']}" for msg in history])

    # Initialize Gemini
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    prompt = f"""
    Act as an Enterprise Email Assistant named '{agent_name}'.
    
    I have already analyzed this email. Use my data to set your tone:
    - DETECTED SENTIMENT: {sentiment}
    - DETECTED TONE: {tone}
    - RISK SCORE: {risk_score}/100
    - CATEGORY: {category}
    
    CONTEXT (Previous Emails):
    {history_text}
    
    INCOMING EMAIL:
    Subject: {subject}
    Body: {body}

    TASK:
    Write a professional email response signed by {agent_name}.
    - If Risk is High (>50), be very apologetic and reassuring.
    - If it is a 'Compliance Issue', mention that Management is reviewing it.
    - Keep it concise (under 100 words).
    
    Return ONLY the email body text.
    """

    try:
        response = model.generate_content(prompt)
        draft_reply = response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        # Fallback template if API fails (so app doesn't crash)
        draft_reply = f"Dear Sender,\n\nThank you for your email regarding '{subject}'. We are reviewing it now.\n\nBest,\n{agent_name}"

    # ============================================================
    # PART C: RETURN RESULTS
    # ============================================================
    return {
        "summary": f"Hybrid Analysis: {sentiment} sentiment with {len(flagged)} risk triggers.",
        "sentiment": sentiment,
        "tone": tone,
        "risk_score": risk_score,
        "flagged_keywords": flagged_display,
        "suggested_category": category,
        "suggested_reply": draft_reply # <--- This now comes from Gemini
    }