%%writefile 44.py
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Maharashtra AI Triage", page_icon="🏥", layout="centered")
st.title("🏥 Maharashtra Healthcare AI Triage")
st.markdown("Enter your symptoms in Marathi, Hindi, or English. The AI will map you to the correct department and local doctor.")
st.markdown("---")

# --- 2. LOAD DATABASES (The Data Lead & UI Lead's Work) ---
@st.cache_data
def load_datasets():
    try:
        # Load the 100-row symptom dictionary
        symptoms_df = pd.read_csv('diseases.csv')
        # Load the 200-row hospital directory
        hospitals_df = pd.read_csv('doctors.csv')
        return symptoms_df, hospitals_df
    except FileNotFoundError:
        st.error("⚠️ Error: Missing CSV files. Please ensure 'diseases.csv' and 'doctors.csv' are in the same folder.")
        st.stop()

symptoms_df, hospitals_df = load_datasets()

# --- 3. UI INPUT CONTROLS ---
col1, col2 = st.columns(2)
with col1:
    lang_dict = {"Marathi (मराठी)": "mr", "Hindi (हिन्दी)": "hi", "English (en)": "en"}
    selected_lang = st.selectbox("Select Language / भाषा निवडा:", list(lang_dict.keys()))
    lang_code = lang_dict[selected_lang]

with col2:
    # Get unique districts from the hospital database automatically
    districts = hospitals_df['City'].unique().tolist()
    selected_district = st.selectbox("Select Your District:", districts)

user_input = st.text_area("Describe your physical symptoms / तुमची लक्षणे लिहा:", 
                          placeholder="Example: मला दोन दिवसांपासून छातीत खूप दुखत आहे")

# --- 4. CORE NLP & ROUTING ENGINE (Phase 2 Logic) ---
if st.button("Analyze & Route Patient", type="primary"):
    if not user_input.strip():
        st.warning("Please describe your symptoms first.")
    else:
        with st.spinner("Processing language and matching medical tokens..."):
            try:
                # STEP A: Pre-Processing & Translation
                translated_text = GoogleTranslator(source=lang_code, target='en').translate(user_input).lower()
                
                # STEP B: The Token Matcher Engine
                # Set default fallback values (If the bot doesn't understand, send to General Medicine)
                matched_disease = "Ambiguous / General Sickness"
                matched_dept = "General Medicine"
                urgency = "Basic Care"
                matched_keyword = "None"
                
                # Loop through the symptom database to find a keyword match
                for index, row in symptoms_df.iterrows():
                    keyword = str(row['Core_Symptom']).lower().strip()
                    if keyword in translated_text:
                        matched_disease = row['Disease_Tag']
                        matched_dept = row['Target_Department']
                        urgency = row['Urgency_Level']
                        matched_keyword = keyword
                        break # Stop searching once we find the first match

                # STEP C: Display NLP Results
                st.success("✅ AI Analysis Complete")
                
                m1, m2, m3 = st.columns(3)
                m1.metric(label="Suspected Issue", value=matched_disease)
                m2.metric(label="Target Department", value=matched_dept)
                m3.metric(label="Urgency Level", value=urgency)
                
                if urgency == "Emergency":
                    st.error("🚨 EMERGENCY: Please seek immediate medical attention.")
                elif matched_keyword == "None":
                    st.info("ℹ️ We couldn't map a specific specialist to your text. Recommending a General Physician for a primary checkup.")

                # STEP D: Database Filtering (Map to correct District and Department)
                st.markdown("---")
                st.markdown(f"### 📍 Recommended Specialists in **{selected_district}**")
                
                # Filter the Pandas dataframe based on user selections
                local_hospitals = hospitals_df[
                    (hospitals_df['City'] == selected_district) & 
                    (hospitals_df['Department'] == matched_dept)
                ]
                
                if local_hospitals.empty:
                    st.warning(f"No specific {matched_dept} specialists found in our prototype database for {selected_district}. Please visit the local Civil Hospital.")
                else:
                    # Loop through the filtered results and display them nicely
                    for index, row in local_hospitals.iterrows():
                        with st.expander(f"🏥 {row['Hospital_Name']}", expanded=True):
                            st.write(f"👨‍⚕️ **Doctor:** {row['Doctor_Name']}")
                            st.write(f"🏢 **Floor/Address:** {row['Floor_Address']}")

                # STEP E: System Logs (Crucial for showing professors how it works)
                with st.expander("System Debug Logs (For Presentation)"):
                    st.write(f"**Source Language:** {lang_code.upper()}")
                    st.write(f"**Raw Input:** {user_input}")
                    st.write(f"**Translated Context (English):** {translated_text}")
                    st.write(f"**Keyword Matched:** {matched_keyword}")

            except Exception as e:
                st.error("Translation API Error. Please check your internet connection or try again.")