import streamlit as st
import BE # We are now importing your Coder's modular backend!

# --- UI Configuration ---
st.set_page_config(page_title="AI Healthcare Triage", page_icon="🏥", layout="wide")

# --- Load Data via BE ---
symptoms_df, hospitals_df = BE.load_data()

# --- THE UI LEAD'S SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Triage Settings")
    st.markdown("Configure your regional and language parameters here.")

    lang_dict = {"Marathi (मराठी)": "mr", "Hindi (हिन्दी)": "hi", "English (en)": "en"}
    selected_lang = st.selectbox("Language / भाषा:", list(lang_dict.keys()))
    lang_code = lang_dict[selected_lang]

    districts = hospitals_df['City'].unique().tolist()
    selected_district = st.selectbox("Target District:", districts)

    st.markdown("---")
    st.caption("")

# --- THE MAIN DASHBOARD ---
st.title("🏥 E-Vaidya Assistant")
st.markdown("Describe how the patient is feeling. Our NLP engine will translate the input and route the patient to the correct specialist.")

user_input = st.text_area("Patient Symptoms / रुग्णाची लक्षणे:", height=100, placeholder="Example: मला खूप ताप आहे आणि खोकला येत आहे")

# --- EXECUTION ---
if st.button("Run AI Triage 🚀", type="primary"):

    # DATA LEAD: Handling empty inputs
    if not user_input.strip():
        st.warning("⚠️ Please enter the symptoms before running the analysis.")
    else:
        with st.spinner("Analyzing symptoms and scanning hospital databases..."):

            # CODER: Using the modular engine
            translated_text, matched_disease, matched_dept, urgency, error = BE.process_triage(user_input, lang_code, symptoms_df)

            # DATA LEAD: Handling network dropouts
            if error:
                st.error("🚨 Network connection failed during translation. Please check your internet.")
            else:
                # UI LEAD: Clean Tabs Presentation
                tab1, tab2,  = st.tabs(["🩺 Diagnosis Report", "📍 Hospital Routing", ])

                with tab1:
                    st.subheader("AI Assessment Results")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Suspected Condition", matched_disease)
                    c2.metric("Target Department", matched_dept)

                    if urgency == "Emergency":
                        c3.error(f"Urgency: {urgency} 🚨")
                        st.error("🚨 **CRITICAL PRIORITY:** This looks like a medical emergency. Route patient to the nearest casualty ward immediately.")
                    else:
                        c3.success(f"Urgency: {urgency} ✅")
                        st.info("ℹ️ Proceed to standard OPD booking.")

                with tab2:
                    st.subheader(f"Recommended Doctors in {selected_district}")
                    local_hospitals = hospitals_df[(hospitals_df['City'] == selected_district) & (hospitals_df['Department'] == matched_dept)]

                    if local_hospitals.empty:
                        st.warning(f"No specific '{matched_dept}' data found for {selected_district}. Recommending General Medicine at the main Civil Hospital.")
                    else:
                        for idx, row in local_hospitals.iterrows():
                            # Creating a clean card layout for each hospital
                            st.success(f"👨‍⚕️ **{row['Doctor_Name']}** | 🏥 **{row['Hospital_Name']}**\n\n📍 *Address:* {row['Floor_Address']}")


