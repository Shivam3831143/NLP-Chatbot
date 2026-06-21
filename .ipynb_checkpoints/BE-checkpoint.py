import pandas as pd
from deep_translator import GoogleTranslator

def load_data():
    """Loads the CSV datasets into memory."""
    symptoms_df = pd.read_csv('diseases.csv')
    hospitals_df = pd.read_csv('doctors.csv')
    return symptoms_df, hospitals_df

def process_triage(user_input, lang_code, symptoms_df):
    """Translates text and maps it to a medical department."""
    try:
        translated_text = GoogleTranslator(source=lang_code, target='en').translate(user_input).lower()
    except Exception as e:
        # Handles internet dropouts gracefully
        return None, "Translation Error", "General Medicine", "Basic Care", str(e)

    matched_disease = "Unclear / General Evaluation"
    matched_dept = "General Medicine"
    urgency = "Basic Care"

    for index, row in symptoms_df.iterrows():
        keyword = str(row['Core_Symptom']).lower().strip()
        if keyword in translated_text:
            matched_disease = row['Disease_Tag']
            matched_dept = row['Target_Department']
            urgency = row['Urgency_Level']
            break

    return translated_text, matched_disease, matched_dept, urgency, None
