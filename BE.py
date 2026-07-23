import pandas as pd
from deep_translator import GoogleTranslator



# DATA LOADING


def load_data():
    """Loads the CSV datasets into memory."""
    symptoms_df = pd.read_csv('diseases.csv')
    hospitals_df = pd.read_csv('doctors.csv')
    return symptoms_df, hospitals_df



# CORE NLP TRIAGE ENGINE


def process_triage(user_input, lang_code, symptoms_df):
    """
    Translates the user's input to English (if needed) and
    matches it against the symptom keyword database.
    Returns: (translated_text, disease, dept, urgency, keyword, error)
    """
    try:
        if lang_code == 'en':
            translated_text = user_input.lower()
        else:
            translated_text = GoogleTranslator(source=lang_code, target='en').translate(user_input).lower()
    except Exception as e:
        return None, "Translation Error", "General Medicine", "Basic Care", "None", str(e)

    matched_disease  = "Unclear / General Evaluation"
    matched_dept     = "General Medicine"
    urgency          = "Basic Care"
    matched_keyword  = "None"

    for _, row in symptoms_df.iterrows():
        keyword = str(row['Core_Symptom']).lower().strip()
        if keyword in translated_text:
            matched_disease = row['Disease_Tag']
            matched_dept    = row['Target_Department']
            urgency         = row['Urgency_Level']
            matched_keyword = keyword
            break

    return translated_text, matched_disease, matched_dept, urgency, matched_keyword, None



# AI RESPONSE TEXT GENERATOR


def get_ai_response_text(disease, dept, urgency, matched_keyword, user_input):
    """
    Generates a friendly, context-aware AI response intro and follow-up advice.
    Returns: (intro_text, advice_text)
    """
    if urgency == "Emergency":
        intro  = (f"⚠️ **Urgent attention needed!** Based on your description, I've detected symptoms "
                  f"that may indicate **{disease}**. This is classified as a **medical emergency**. "
                  f"Please seek immediate care right away!")
        advice = ("Do NOT delay — go to the nearest Emergency Room or call **108** (Ambulance) immediately. "
                  "While waiting, stay calm, sit or lie down comfortably, and avoid strenuous activity. "
                  "If you are alone, unlock your door so help can reach you.")

    elif matched_keyword == "None":
        intro  = ("I've carefully reviewed your description. While I couldn't match your exact symptoms "
                  "to a specific condition in my database, I recommend visiting a **General Physician** "
                  "for a thorough in-person evaluation.")
        advice = ("Your symptoms may have multiple possible causes, and an accurate diagnosis requires a "
                  "proper physical examination and diagnostic tests. The doctor listings below are "
                  "the closest General Medicine practitioners in your selected area.")
        disease = "General Evaluation Needed"

    elif urgency == "Specialized Care":
        intro  = (f"Based on your symptoms, my analysis indicates a possible **{disease}**. "
                  f"I'm routing you to the **{dept}** department for specialized evaluation.")
        advice = ("Your condition requires attention from a **specialist**. I recommend booking an appointment "
                  "as soon as possible — don't ignore persistent or worsening symptoms. In the meantime, "
                  "note your symptoms, their frequency, and any triggers to share with your doctor.")

    else:  # Basic Care
        intro  = (f"I've analyzed your symptoms and the pattern suggests a possible **{disease}**. "
                  f"This is being routed to the **{dept}** department.")
        advice = ("This appears to be a **manageable condition** with proper care and medication. "
                  "Rest well, stay hydrated, and monitor your symptoms. If symptoms worsen or persist "
                  "beyond 3–5 days, please consult the recommended specialists below.")

    return intro, advice



# EMERGENCY CONTACTS


def get_emergency_contacts():
    """Returns a list of emergency contact dictionaries."""
    return [
        {
            "name": "National Emergency",
            "number": "112",
            "icon": "🚨",
            "desc": "Police · Fire · Ambulance — all emergencies",
            "color": "#ef4444",
            "bg": "rgba(239,68,68,0.10)",
        },
        {
            "name": "Ambulance Service",
            "number": "108",
            "icon": "🚑",
            "desc": "Free 24/7 emergency ambulance service",
            "color": "#ef4444",
            "bg": "rgba(239,68,68,0.10)",
        },
        {
            "name": "Police Control Room",
            "number": "100",
            "icon": "👮",
            "desc": "Law enforcement — crime & safety",
            "color": "#6366f1",
            "bg": "rgba(99,102,241,0.10)",
        },
        {
            "name": "Fire Brigade",
            "number": "101",
            "icon": "🔥",
            "desc": "Fire emergency & rescue services",
            "color": "#f59e0b",
            "bg": "rgba(245,158,11,0.10)",
        },
        {
            "name": "National Health Helpline",
            "number": "104",
            "icon": "🩺",
            "desc": "Free medical advice & health guidance",
            "color": "#0ea5e9",
            "bg": "rgba(14,165,233,0.10)",
        },
        {
            "name": "Women Safety Helpline",
            "number": "1091",
            "icon": "👩",
            "desc": "24/7 women's safety & support line",
            "color": "#ec4899",
            "bg": "rgba(236,72,153,0.10)",
        },
        {
            "name": "Child Helpline",
            "number": "1098",
            "icon": "👶",
            "desc": "Child abuse reporting & emergency help",
            "color": "#10b981",
            "bg": "rgba(16,185,129,0.10)",
        },
        {
            "name": "Blood Bank Helpline",
            "number": "104",
            "icon": "🩸",
            "desc": "Emergency blood supply & donation info",
            "color": "#ef4444",
            "bg": "rgba(239,68,68,0.07)",
        },
    ]


# HEALTH TIPS


def get_health_tips():
    """Returns a curated list of health insight cards for the dashboard."""
    return [
        {
            "title": "Stay Hydrated",
            "tip":   "Drink 8–10 glasses of water daily. Proper hydration improves metabolism, skin clarity, and brain function by up to 14%.",
            "icon":  "💧",
            "color": "#0ea5e9",
            "bg":    "rgba(14,165,233,0.07)",
        },
        {
            "title": "Quality Sleep",
            "tip":   "Adults need 7–9 hours of quality sleep. Poor sleep increases risk of heart disease, obesity, and mental health issues.",
            "icon":  "😴",
            "color": "#8b5cf6",
            "bg":    "rgba(139,92,246,0.07)",
        },
        {
            "title": "Daily Exercise",
            "tip":   "Just 30 minutes of moderate exercise daily reduces chronic disease risk by 35% and significantly boosts mood.",
            "icon":  "🏃",
            "color": "#10b981",
            "bg":    "rgba(16,185,129,0.07)",
        },
        {
            "title": "Balanced Nutrition",
            "tip":   "Fill half your plate with colorful vegetables and fruits. Limit ultra-processed foods and added sugars.",
            "icon":  "🥗",
            "color": "#f59e0b",
            "bg":    "rgba(245,158,11,0.07)",
        },
        {
            "title": "Stress Management",
            "tip":   "Practice deep breathing or meditation for 10 minutes daily. Chronic stress suppresses your immune system.",
            "icon":  "🧘",
            "color": "#14b8a6",
            "bg":    "rgba(20,184,166,0.07)",
        },
        {
            "title": "Regular Checkups",
            "tip":   "Annual health screenings catch problems early. Preventive care is always more effective than reactive treatment.",
            "icon":  "🩺",
            "color": "#ef4444",
            "bg":    "rgba(239,68,68,0.07)",
        },
    ]
