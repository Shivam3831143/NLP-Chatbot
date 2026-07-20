# 🩺 Multilingual AI Healthcare Triage Bot

> An intelligent Natural Language Processing (NLP)-based healthcare assistant that analyzes user-reported symptoms in multiple languages, identifies the appropriate medical department, recommends a suitable specialist, and provides hospital location details for faster healthcare access.

---

## 📖 Overview

The **Multilingual AI Healthcare Triage Bot** is an NLP-powered healthcare assistance system designed to simplify the initial medical consultation process. The application accepts symptoms in **English, Hindi, and Marathi**, processes them using Natural Language Processing techniques, and recommends the most relevant medical department along with an appropriate doctor and hospital.

The system bridges the communication gap between patients and healthcare providers by enabling multilingual interaction while assisting users in locating nearby healthcare facilities.

---

## ✨ Key Features

- 🌐 **Multilingual Support**
  - English
  - Hindi
  - Marathi

- 🤖 NLP-based symptom understanding

- 🌍 Automatic language translation for standardized symptom processing

- 🩺 Disease category prediction based on reported symptoms

- 👨‍⚕️ Intelligent recommendation of the appropriate medical department

- 🏥 Doctor recommendation based on specialization

- 📍 Hospital recommendation with complete address and city

- 💻 Interactive and responsive web application using Streamlit

- ⚡ Simple, lightweight, and user-friendly interface

---

## 🏗️ System Architecture

```
                 User Input
                     │
                     ▼
        Multilingual Symptom Entry
                     │
                     ▼
      Language Translation (if required)
                     │
                     ▼
      Natural Language Processing (NLP)
                     │
                     ▼
        Symptom Pattern Recognition
                     │
                     ▼
        Disease Category Identification
                     │
                     ▼
      Medical Department Recommendation
                     │
                     ▼
 Doctor & Hospital Recommendation Engine
                     │
                     ▼
      Hospital Address & Location Display
```

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Frontend | Streamlit |
| Data Processing | Pandas |
| Translation | Deep Translator |
| Dataset | CSV |
| Development Environment | Jupyter Notebook, VS Code |

---

## 📚 Python Libraries Used

- Streamlit
- Pandas
- Deep Translator
- CSV
- OS
- JSON
- Datetime
- Regular Expressions (re)
- Additional Python Standard Libraries

> *The project also utilizes various built-in Python modules required for data processing and application functionality.*

---

## 📂 Project Structure

```
Multilingual-AI-Healthcare-Triage-Bot
│
├── FE.py                  # Frontend implementation
├── BE.py                  # Backend logic
├── 44.py                  # Main Streamlit application
├── main.py
│
├── diseases.csv           # Disease and symptom dataset
├── doctors.csv            # Doctor and hospital dataset
│
├── LOGIC.ipynb            # Model development notebook
├── BEF.ipynb
├── FEF.ipynb
│
├── README.md
└── requirements.txt
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/Multilingual-AI-Healthcare-Triage-Bot.git
```

### Navigate to the Project Directory

```bash
cd Multilingual-AI-Healthcare-Triage-Bot
```

### Install Required Dependencies

```bash
pip install -r requirements.txt
```

If a requirements file is unavailable:

```bash
pip install streamlit pandas deep-translator
```

### Run the Application

```bash
streamlit run 44.py
```

---

## 💡 Working Principle

1. The user selects a preferred language.
2. Symptoms are entered in natural language.
3. The application translates non-English input into English.
4. NLP techniques analyze the symptom text.
5. Symptoms are matched against the medical dataset.
6. The relevant disease category is identified.
7. The corresponding medical department is determined.
8. A suitable doctor is recommended.
9. Hospital details including address and city are displayed.

---

## 🎯 Applications

- Healthcare Triage Systems
- Rural Healthcare Assistance
- Telemedicine Platforms
- Hospital Information Systems
- Patient Navigation Services
- Digital Healthcare Solutions
- AI-powered Clinical Assistance

---

## 📈 Future Enhancements

- Integration with Machine Learning models for improved prediction accuracy
- Large Language Model (LLM)-powered conversational assistant
- Voice-based symptom interaction
- Google Maps API integration for live navigation
- Online appointment booking
- Emergency response recommendations
- Electronic Health Record (EHR) integration
- Support for additional regional languages

---

## 🤝 Contributing

Contributions are welcome.

If you would like to improve this project:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Submit a Pull Request.

---

## 👩‍💻 Author

**Manasi Deshmukh**

**B.Tech Artificial Intelligence & Data Science**

Passionate about Artificial Intelligence, Natural Language Processing, Healthcare Technology, and developing intelligent systems that create meaningful real-world impact.

---

## 📜 License

This project is intended for educational, research, and academic purposes.

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

Your support helps improve the project and motivates future development.
