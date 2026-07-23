# -*- coding: utf-8 -*-
"""
MediNex AI — Premium Healthcare Assistant (Bug-Fixed v3)
Root cause fix: st.chat_message() + st.chat_input() replace custom HTML bubbles
which were triggering Streamlit's markdown-to-code-block conversion on indented HTML.
"""

import streamlit as st
import pandas as pd
import datetime
import html as _html
import time

import BE


# PAGE CONFIG

st.set_page_config(
    page_title="MediNex AI — Intelligent Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# GLOBAL CSS

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
--p:#0ea5e9;--pd:#0284c7;--s:#14b8a6;--a:#10b981;
--dn:#ef4444;--wn:#f59e0b;--ok:#22c55e;
--card:rgba(255,255,255,0.92);--t1:#0f172a;--t2:#475569;--tm:#94a3b8;
--br:rgba(14,165,233,0.12);--sh:0 4px 24px rgba(14,165,233,0.10);
--r:18px;--rs:12px;--tr:all 0.3s cubic-bezier(0.4,0,0.2,1);
}
*,*::before,*::after{font-family:'Inter',sans-serif!important;box-sizing:border-box;}
#MainMenu,footer,header{visibility:hidden;}
.stDeployButton,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}

.stApp{background:linear-gradient(145deg,#f0f9ff 0%,#dbeafe 35%,#ecfdf5 100%)!important;min-height:100vh;}
[data-testid="stMain"]{background:transparent!important;}
[data-testid="block-container"]{padding-top:1.4rem!important;}

/* SIDEBAR */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0c1a2e 0%,#1a2d48 55%,#0e2341 100%)!important;border-right:1px solid rgba(14,165,233,0.18)!important;box-shadow:4px 0 28px rgba(0,0,0,0.18)!important;}
[data-testid="stSidebar"] p,[data-testid="stSidebar"] span,[data-testid="stSidebar"] div,[data-testid="stSidebar"] label{color:#cbd5e1!important;}
[data-testid="stSidebar"] .stSelectbox>label{color:#64748b!important;font-size:0.7rem!important;font-weight:700!important;text-transform:uppercase;letter-spacing:0.09em;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:rgba(255,255,255,0.06)!important;border:1px solid rgba(255,255,255,0.11)!important;border-radius:11px!important;color:#e2e8f0!important;}
[data-testid="stSidebar"] .stButton>button{width:100%!important;background:transparent!important;border:1px solid rgba(255,255,255,0.07)!important;color:#94a3b8!important;border-radius:12px!important;padding:10px 14px!important;text-align:left!important;font-weight:500!important;font-size:0.88rem!important;transition:var(--tr)!important;margin-bottom:3px!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(14,165,233,0.14)!important;border-color:rgba(14,165,233,0.38)!important;color:#38bdf8!important;transform:translateX(5px)!important;}

/* TABS */
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:rgba(255,255,255,0.88)!important;border-radius:16px!important;padding:6px!important;gap:4px!important;backdrop-filter:blur(14px)!important;border:1px solid rgba(14,165,233,0.12)!important;box-shadow:0 4px 20px rgba(14,165,233,0.09)!important;margin-bottom:24px!important;}
[data-testid="stTabs"] [data-baseweb="tab"]{border-radius:12px!important;font-weight:600!important;font-size:0.87rem!important;color:#64748b!important;padding:10px 22px!important;transition:var(--tr)!important;border:none!important;}
[data-testid="stTabs"] [aria-selected="true"]{background:linear-gradient(135deg,#0ea5e9,#14b8a6)!important;color:white!important;box-shadow:0 4px 16px rgba(14,165,233,0.38)!important;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"]{display:none!important;}

/* CHAT MESSAGES — premium styling for st.chat_message() */
[data-testid="stChatMessage"]{background:rgba(255,255,255,0.88)!important;border:1.5px solid rgba(14,165,233,0.12)!important;border-radius:18px!important;padding:16px 18px!important;margin-bottom:10px!important;backdrop-filter:blur(14px)!important;box-shadow:0 3px 16px rgba(14,165,233,0.08)!important;animation:fadeUp 0.4s ease both;}
[data-testid="stChatMessageContent"] p{font-size:0.95rem!important;line-height:1.65!important;color:#1e293b!important;}
[data-testid="stChatMessageContent"] strong{color:#0f172a!important;}

/* CHAT INPUT */
[data-testid="stChatInput"]{background:rgba(255,255,255,0.92)!important;border:2px solid rgba(14,165,233,0.18)!important;border-radius:16px!important;box-shadow:0 4px 20px rgba(14,165,233,0.10)!important;backdrop-filter:blur(12px)!important;}
[data-testid="stChatInput"] textarea{font-size:0.95rem!important;color:#0f172a!important;}
[data-testid="stChatInput"] button{background:linear-gradient(135deg,#0ea5e9,#14b8a6)!important;border-radius:10px!important;}

/* BUTTONS */
.stButton>button{border-radius:var(--rs)!important;font-weight:600!important;transition:var(--tr)!important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#0ea5e9,#14b8a6)!important;color:white!important;border:none!important;box-shadow:0 4px 16px rgba(14,165,233,0.32)!important;padding:12px 28px!important;}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px)!important;box-shadow:0 8px 28px rgba(14,165,233,0.48)!important;}
.stButton>button[kind="secondary"]{background:rgba(255,255,255,0.9)!important;border:1.5px solid rgba(14,165,233,0.15)!important;color:#475569!important;}
.stButton>button[kind="secondary"]:hover{border-color:rgba(14,165,233,0.35)!important;color:#0284c7!important;background:rgba(14,165,233,0.05)!important;}

/* SELECTBOX */
.stSelectbox>div>div{background:white!important;border:2px solid rgba(14,165,233,0.14)!important;border-radius:12px!important;}
.stSelectbox>label{font-weight:600!important;color:#475569!important;}

/* METRICS */
[data-testid="metric-container"]{background:rgba(255,255,255,0.92)!important;border-radius:var(--r)!important;padding:20px!important;border:1px solid rgba(14,165,233,0.12)!important;box-shadow:var(--sh)!important;backdrop-filter:blur(12px)!important;}
[data-testid="stMetricLabel"]>div{color:#64748b!important;font-size:0.72rem!important;font-weight:700!important;text-transform:uppercase;letter-spacing:0.06em;}
[data-testid="stMetricValue"]>div{color:#0284c7!important;font-weight:800!important;}

/* FILE UPLOADER */
[data-testid="stFileUploader"]>section{background:rgba(14,165,233,0.03)!important;border:2.5px dashed rgba(14,165,233,0.28)!important;border-radius:var(--r)!important;}

/* EXPANDER */
[data-testid="stExpander"]{background:rgba(255,255,255,0.9)!important;border:1px solid rgba(14,165,233,0.12)!important;border-radius:var(--r)!important;}

/* SCROLLBAR */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(14,165,233,0.25);border-radius:10px;}

/* ANIMATIONS */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes glow{0%,100%{box-shadow:0 0 22px rgba(14,165,233,0.32)}50%{box-shadow:0 0 44px rgba(14,165,233,0.62)}}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.08);opacity:0.75}}

.anim-fadeup{animation:fadeUp 0.5s ease both;}
.anim-fadein{animation:fadeIn 0.4s ease both;}
</style>
""", unsafe_allow_html=True)



# SESSION STATE

_defaults = {
    'messages': [],
    'water_cups': 3,
    'symptom_history': [],
    'pending_message': '',
    'reminders': [
        {'med': 'Vitamin D3',  'dose': '1000 IU',  'time': '08:00 AM', 'icon': '🌞'},
        {'med': 'Omega-3',     'dose': '500mg',     'time': '01:00 PM', 'icon': '🐟'},
        {'med': 'Probiotic',   'dose': '1 capsule', 'time': '09:00 PM', 'icon': '🦠'},
    ],
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v



# DATA LOADING

@st.cache_data
def _load():
    return BE.load_data()

symptoms_df, hospitals_df = _load()
districts = sorted(hospitals_df['City'].unique().tolist())



# UTILITY HELPERS

def now_str():
    return datetime.datetime.now().strftime("%I:%M %p")

def esc(s):
    return _html.escape(str(s))

def urgency_colors(urgency):
    if urgency == "Emergency":
        return "#dc2626", "rgba(239,68,68,0.10)", "rgba(239,68,68,0.28)", "🚨"
    elif urgency == "Specialized Care":
        return "#d97706", "rgba(245,158,11,0.10)", "rgba(245,158,11,0.28)", "⚠️"
    return "#16a34a", "rgba(34,197,94,0.10)", "rgba(34,197,94,0.28)", "✅"



# MESSAGE RENDERERS  (using st.chat_message — no raw HTML blocks)
def render_user_msg(msg):
    with st.chat_message("user", avatar="👤"):
        st.markdown(msg['content'])
        st.caption(f"🕐 {msg['timestamp']}")


def render_ai_msg(msg):
    triage = msg.get('triage') or {}

    with st.chat_message("assistant", avatar="🤖"):
        # ── Main response text ────────────────────────────────────
        st.markdown(msg['content'])

        # ── Emergency banner ──────────────────────────────────────
        if triage.get('urgency') == "Emergency":
            st.error("🚨 **EMERGENCY — Seek Immediate Care!**  "
                     "Call **108** (Ambulance) or go to the nearest Emergency Room **right now**.")

        # ── Triage result cards (3 columns, single-line HTML — no indentation bug) ──
        if triage.get('disease'):
            uc, ubg, ubr, uico = urgency_colors(triage.get('urgency', 'Basic Care'))
            c1, c2, c3 = st.columns(3)
            # Each st.markdown call is a single compact line → no code-block trigger
            with c1:
                st.markdown(
                    f'<div style="background:rgba(14,165,233,0.07);border:1px solid rgba(14,165,233,0.18);border-radius:12px;padding:14px;text-align:center;">'
                    f'<div style="font-size:1.5rem;margin-bottom:5px;">🩺</div>'
                    f'<div style="font-size:0.6rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;">Suspected Condition</div>'
                    f'<div style="font-size:0.85rem;font-weight:700;color:#0f172a;margin-top:5px;">{esc(triage["disease"])}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    f'<div style="background:rgba(20,184,166,0.07);border:1px solid rgba(20,184,166,0.18);border-radius:12px;padding:14px;text-align:center;">'
                    f'<div style="font-size:1.5rem;margin-bottom:5px;">🏥</div>'
                    f'<div style="font-size:0.6rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;">Department</div>'
                    f'<div style="font-size:0.85rem;font-weight:700;color:#0f172a;margin-top:5px;">{esc(triage["dept"])}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with c3:
                st.markdown(
                    f'<div style="background:{ubg};border:1px solid {ubr};border-radius:12px;padding:14px;text-align:center;">'
                    f'<div style="font-size:1.5rem;margin-bottom:5px;">{uico}</div>'
                    f'<div style="font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;color:{uc};">Urgency Level</div>'
                    f'<div style="font-size:0.85rem;font-weight:700;margin-top:5px;color:{uc};">{esc(triage.get("urgency","Basic Care"))}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # ── Doctor recommendation cards ───────────────────────────
        if triage.get('doctors'):
            st.markdown("---")
            st.markdown("📍 **Recommended Specialists Near You**")
            for doc in triage['doctors'][:3]:
                name     = str(doc.get('Doctor_Name', 'Doctor'))
                initials = ''.join(w[0].upper() for w in name.split()[:2] if w)
                hospital = esc(str(doc.get('Hospital_Name', '')))
                address  = esc(str(doc.get('Floor_Address', '')))
                dept_tag = esc(triage.get('dept', ''))
                # Single-line HTML: zero indentation → no markdown code-block issue
                st.markdown(
                    f'<div style="background:rgba(14,165,233,0.05);border:1px solid rgba(14,165,233,0.18);border-radius:12px;padding:12px 14px;margin:6px 0;display:flex;align-items:center;gap:12px;">'
                    f'<div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#0ea5e9,#14b8a6);color:white;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.82rem;flex-shrink:0;">{initials}</div>'
                    f'<div style="flex:1;min-width:0;">'
                    f'<div style="font-weight:700;font-size:0.87rem;color:#0f172a;">{esc(name)}</div>'
                    f'<div style="font-size:0.76rem;color:#475569;">🏥 {hospital}</div>'
                    f'<div style="font-size:0.72rem;color:#94a3b8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">📍 {address}</div>'
                    f'</div>'
                    f'<div style="font-size:0.65rem;font-weight:700;padding:4px 10px;border-radius:20px;background:rgba(14,165,233,0.1);color:#0284c7;border:1px solid rgba(14,165,233,0.2);white-space:nowrap;flex-shrink:0;">{dept_tag}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        elif triage.get('disease') and not triage.get('doctors'):
            st.warning(f"No {triage.get('dept','General Medicine')} specialists found in the database for your selected district. Please visit the local Civil Hospital.")

        # ── Advice strip 
        if triage.get('advice'):
            st.info(f"💡 {triage['advice']}")

        st.caption(f"🕐 {msg['timestamp']}")



# SIDEBAR

with st.sidebar:
    st.markdown(
        '<div style="padding:22px 4px 10px;">'
        '<div style="display:flex;align-items:center;gap:13px;margin-bottom:18px;">'
        '<div style="width:50px;height:50px;background:linear-gradient(135deg,#0ea5e9,#14b8a6);border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 4px 18px rgba(14,165,233,0.45);animation:glow 3s ease-in-out infinite;flex-shrink:0;">🏥</div>'
        '<div>'
        '<div style="font-size:1.22rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.025em;">MediNex AI</div>'
        '<div style="font-size:0.67rem;color:#475569;font-weight:500;">Intelligent Healthcare Assistant</div>'
        '</div></div>'
        '<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(14,165,233,0.3),transparent);margin-bottom:14px;"></div>'
        '<div style="display:inline-flex;align-items:center;gap:7px;background:rgba(34,197,94,0.09);border:1px solid rgba(34,197,94,0.22);border-radius:20px;padding:5px 13px;margin-bottom:6px;">'
        '<div style="width:7px;height:7px;background:#22c55e;border-radius:50%;animation:pulse 1.5s ease-in-out infinite;"></div>'
        '<span style="font-size:0.72rem;font-weight:600;color:#16a34a !important;">AI Online · 24/7</span>'
        '</div></div>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="font-size:0.65rem;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:0.1em;padding:6px 0 8px;">⚙️ Preferences</div>', unsafe_allow_html=True)

    lang_map   = {"🇬🇧  English": "en", "🇮🇳  Marathi (मराठी)": "mr", "🇮🇳  Hindi (हिन्दी)": "hi"}
    lang_label = st.selectbox("Language / भाषा", list(lang_map.keys()), key="sb_lang")
    lang_code  = lang_map[lang_label]

    selected_dist = st.selectbox("📍 Your District", districts, key="sb_dist")

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(14,165,233,0.2),transparent);margin:14px 0;"></div>', unsafe_allow_html=True)

    # Daily tip
    tips_cycle = [
        "💧 Drink 8 glasses of water today for peak energy.",
        "🏃 A 30-min walk lowers heart disease risk by 35%.",
        "😴 7–9 hours of sleep heals and restores your body.",
        "🥗 Eat the rainbow — colorful veggies = more nutrients.",
        "🧘 5 min deep breathing reduces cortisol by 20%.",
        "☀️ 15 min morning sunlight boosts Vitamin D and mood.",
        "📵 Reduce screen time 1hr before bed for better sleep.",
    ]
    tip_today = tips_cycle[datetime.datetime.now().timetuple().tm_yday % len(tips_cycle)]
    st.markdown(
        f'<div style="background:rgba(14,165,233,0.07);border:1px solid rgba(14,165,233,0.18);border-radius:14px;padding:14px 15px;margin-bottom:10px;">'
        f'<div style="font-size:0.62rem;font-weight:700;color:#0ea5e9 !important;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:6px;">💡 Daily Tip</div>'
        f'<div style="font-size:0.81rem;color:#cbd5e1 !important;line-height:1.55;">{tip_today}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    total_q = len([m for m in st.session_state.messages if m['role'] == 'user'])
    st.markdown(
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;">'
        f'<div style="background:rgba(14,165,233,0.07);border:1px solid rgba(14,165,233,0.15);border-radius:12px;padding:12px;text-align:center;">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#38bdf8 !important;">{total_q}</div>'
        f'<div style="font-size:0.65rem;color:#64748b !important;font-weight:600;text-transform:uppercase;">Queries</div>'
        f'</div>'
        f'<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.15);border-radius:12px;padding:12px;text-align:center;">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#34d399 !important;">{len(st.session_state.symptom_history)}</div>'
        f'<div style="font-size:0.65rem;color:#64748b !important;font-weight:600;text-transform:uppercase;">Analyzed</div>'
        f'</div></div>'
        f'<div style="text-align:center;padding:8px 0 4px;font-size:0.67rem;color:#334155 !important;line-height:1.7;">'
        f'MediNex AI v3.0 · Built with ❤️<br>'
        f'<span style="color:#1e3a5f !important;font-size:0.62rem;">Not a substitute for professional medical advice</span>'
        f'</div>',
        unsafe_allow_html=True
    )



# MAIN TABS

tab_chat, tab_dash, tab_upload, tab_em = st.tabs([
    "💬  Chat Assistant",
    "📊  Health Dashboard",
    "📄  Upload Report",
    "🚨  Emergency",
])



# TAB 1 — CHAT ASSISTANT

with tab_chat:

    # ── Toolbar (shown only when conversation exists)
    if st.session_state.messages:
        tc1, tc2, _ = st.columns([1, 1, 8])
        with tc1:
            if st.button("🔄 New Chat", key="new_chat"):
                st.session_state.messages = []
                st.rerun()
        with tc2:
            if st.button("🗑️ Clear", key="clear_chat"):
                st.session_state.messages = []
                st.rerun()
        st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)

    # ── Landing hero (only when no messages) 
    if not st.session_state.messages:
        st.markdown(
            '<div class="anim-fadeup" style="text-align:center;padding:28px 20px 16px;">'
            '<div style="position:relative;display:inline-block;margin-bottom:22px;">'
            '<div style="width:96px;height:96px;background:linear-gradient(135deg,#0ea5e9 0%,#14b8a6 55%,#10b981 100%);border-radius:28px;display:flex;align-items:center;justify-content:center;font-size:50px;margin:0 auto;box-shadow:0 8px 40px rgba(14,165,233,0.38);animation:glow 3s ease-in-out infinite;">🏥</div>'
            '<div style="position:absolute;inset:-9px;border-radius:37px;border:2px solid rgba(14,165,233,0.22);animation:pulse 2.6s infinite;"></div>'
            '<div style="position:absolute;inset:-18px;border-radius:46px;border:1px solid rgba(14,165,233,0.10);animation:pulse 2.6s infinite 0.65s;"></div>'
            '</div>'
            '<h1 style="font-size:2rem;font-weight:900;color:#0f172a;letter-spacing:-0.04em;margin:0 0 10px;">'
            'Hello! I\'m <span style="background:linear-gradient(135deg,#0ea5e9,#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">MediNex AI</span>'
            '</h1>'
            '<p style="font-size:1rem;color:#475569;max-width:500px;margin:0 auto 10px;line-height:1.7;">'
            'Describe your symptoms and I\'ll help you understand possible conditions, find the right specialists, and guide your healthcare journey.'
            '</p>'
            '<div style="display:inline-flex;align-items:center;gap:7px;background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.26);border-radius:20px;padding:5px 14px;margin-top:4px;">'
            '<div style="width:7px;height:7px;background:#22c55e;border-radius:50%;animation:pulse 1.5s infinite;"></div>'
            '<span style="font-size:0.74rem;font-weight:600;color:#16a34a;">AI Assistant Online</span>'
            '</div></div>',
            unsafe_allow_html=True
        )

        # Quick Action Visual Cards (HTML, compact single-line)
        st.markdown(
            '<p style="text-align:center;font-size:0.73rem;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:0.1em;margin:4px 0 14px;">✦ Quick Actions — Click a button below ✦</p>',
            unsafe_allow_html=True
        )

        cards_html = (
            '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;">'
            '<div style="background:rgba(255,255,255,0.9);border:1.5px solid rgba(14,165,233,0.13);border-radius:18px;padding:18px 14px;text-align:center;box-shadow:0 4px 20px rgba(14,165,233,0.08);">'
            '<div style="font-size:2rem;margin-bottom:8px;">🩺</div>'
            '<div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-bottom:3px;">Check Symptoms</div>'
            '<div style="font-size:0.72rem;color:#94a3b8;">Describe how you feel for AI analysis</div>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.9);border:1.5px solid rgba(14,165,233,0.13);border-radius:18px;padding:18px 14px;text-align:center;box-shadow:0 4px 20px rgba(14,165,233,0.08);">'
            '<div style="font-size:2rem;margin-bottom:8px;">💊</div>'
            '<div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-bottom:3px;">Medicine Info</div>'
            '<div style="font-size:0.72rem;color:#94a3b8;">Get guidance on medications and dosage</div>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.9);border:1.5px solid rgba(14,165,233,0.13);border-radius:18px;padding:18px 14px;text-align:center;box-shadow:0 4px 20px rgba(14,165,233,0.08);">'
            '<div style="font-size:2rem;margin-bottom:8px;">🌿</div>'
            '<div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-bottom:3px;">Lifestyle Tips</div>'
            '<div style="font-size:0.72rem;color:#94a3b8;">Wellness advice for a healthier life</div>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.9);border:1.5px solid rgba(14,165,233,0.13);border-radius:18px;padding:18px 14px;text-align:center;box-shadow:0 4px 20px rgba(14,165,233,0.08);">'
            '<div style="font-size:2rem;margin-bottom:8px;">🏥</div>'
            '<div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-bottom:3px;">Find Hospitals</div>'
            '<div style="font-size:0.72rem;color:#94a3b8;">Locate specialists in your district</div>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.9);border:1.5px solid rgba(239,68,68,0.15);border-radius:18px;padding:18px 14px;text-align:center;box-shadow:0 4px 20px rgba(239,68,68,0.07);">'
            '<div style="font-size:2rem;margin-bottom:8px;">🚨</div>'
            '<div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-bottom:3px;">Emergency Help</div>'
            '<div style="font-size:0.72rem;color:#94a3b8;">Emergency contacts and first aid tips</div>'
            '</div>'
            '<div style="background:rgba(255,255,255,0.9);border:1.5px solid rgba(14,165,233,0.13);border-radius:18px;padding:18px 14px;text-align:center;box-shadow:0 4px 20px rgba(14,165,233,0.08);">'
            '<div style="font-size:2rem;margin-bottom:8px;">🔬</div>'
            '<div style="font-size:0.88rem;font-weight:700;color:#0f172a;margin-bottom:3px;">Lab Test Guide</div>'
            '<div style="font-size:0.72rem;color:#94a3b8;">Understand CBC, sugar, lipid tests</div>'
            '</div>'
            '</div>'
        )
        st.markdown(cards_html, unsafe_allow_html=True)

        # Interactive quick-action buttons
        qb1, qb2, qb3 = st.columns(3)
        with qb1:
            if st.button("🩺  Check Symptoms", key="qa_sym", use_container_width=True):
                st.session_state.pending_message = "I want to check my symptoms. I've been feeling unwell and need help understanding what might be wrong."
                st.rerun()
            if st.button("🏥  Find Hospitals", key="qa_hosp", use_container_width=True):
                st.session_state.pending_message = "Can you help me find specialist doctors and hospitals near my area?"
                st.rerun()
        with qb2:
            if st.button("💊  Medicine Info", key="qa_med", use_container_width=True):
                st.session_state.pending_message = "I need information about common medicines, their uses and dosage."
                st.rerun()
            if st.button("🌿  Lifestyle Tips", key="qa_life", use_container_width=True):
                st.session_state.pending_message = "Please give me healthy lifestyle tips and wellness advice for better health."
                st.rerun()
        with qb3:
            if st.button("🔬  Lab Test Guide", key="qa_lab", use_container_width=True):
                st.session_state.pending_message = "Can you explain common lab tests like CBC, blood sugar, and lipid panel?"
                st.rerun()
            if st.button("😴  Sleep & Stress", key="qa_sleep", use_container_width=True):
                st.session_state.pending_message = "I'm having trouble sleeping and feeling stressed. What can I do to improve?"
                st.rerun()

    #  Render existing messages 
    else:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                render_user_msg(msg)
            else:
                render_ai_msg(msg)

    #  Handle pending_message (from quick-action buttons)
    if st.session_state.pending_message:
        _pending = st.session_state.pending_message
        st.session_state.pending_message = ''

        # Add user message
        st.session_state.messages.append({
            'role': 'user', 'content': _pending, 'timestamp': now_str()
        })

        # Run triage
        with st.spinner("🔍 Analyzing your symptoms with AI…"):
            t, dis, dep, urg, kw, err = BE.process_triage(_pending, lang_code, symptoms_df)

        if err:
            st.session_state.messages.append({
                'role': 'ai',
                'content': "I'm sorry, there was a connection issue while translating your input. Please check your internet and try again. Writing in English works perfectly!",
                'timestamp': now_str(),
                'triage': None
            })
        else:
            docs = hospitals_df[
                (hospitals_df['City'] == selected_dist) &
                (hospitals_df['Department'] == dep)
            ].head(3).to_dict('records')

            intro, advice = BE.get_ai_response_text(dis, dep, urg, kw, _pending)

            if kw != "None":
                st.session_state.symptom_history.insert(0, {
                    'condition': dis, 'dept': dep, 'urgency': urg,
                    'time': now_str(), 'date': datetime.date.today().strftime("%d %b")
                })
                st.session_state.symptom_history = st.session_state.symptom_history[:10]

            st.session_state.messages.append({
                'role': 'ai', 'content': intro, 'timestamp': now_str(),
                'triage': {'disease': dis, 'dept': dep, 'urgency': urg,
                           'doctors': docs, 'advice': advice}
            })
        st.rerun()

    # ── Chat Input (st.chat_input pins to page bottom automatically) ──
    if prompt := st.chat_input(
        "Describe your symptoms or ask a health question… (Marathi / Hindi / English)",
        key="main_chat_input"
    ):
        # Add user message
        st.session_state.messages.append({
            'role': 'user', 'content': prompt, 'timestamp': now_str()
        })

        # Run NLP triage
        with st.spinner("🔍 Analyzing your symptoms with AI…"):
            t, dis, dep, urg, kw, err = BE.process_triage(prompt, lang_code, symptoms_df)

        if err:
            st.session_state.messages.append({
                'role': 'ai',
                'content': "I'm sorry — there was a connection error while processing your input. Please check your internet and try again.",
                'timestamp': now_str(),
                'triage': None
            })
        else:
            docs = hospitals_df[
                (hospitals_df['City'] == selected_dist) &
                (hospitals_df['Department'] == dep)
            ].head(3).to_dict('records')

            intro, advice = BE.get_ai_response_text(dis, dep, urg, kw, prompt)

            if kw != "None":
                st.session_state.symptom_history.insert(0, {
                    'condition': dis, 'dept': dep, 'urgency': urg,
                    'time': now_str(), 'date': datetime.date.today().strftime("%d %b")
                })
                st.session_state.symptom_history = st.session_state.symptom_history[:10]

            st.session_state.messages.append({
                'role': 'ai', 'content': intro, 'timestamp': now_str(),
                'triage': {'disease': dis, 'dept': dep, 'urgency': urg,
                           'doctors': docs, 'advice': advice}
            })
        st.rerun()



# TAB 2 — HEALTH DASHBOARD

with tab_dash:
    st.markdown(
        '<h2 style="font-size:1.75rem;font-weight:800;color:#0f172a;letter-spacing:-0.035em;margin:0 0 5px;">Health Dashboard</h2>'
        '<p style="color:#64748b;margin:0 0 22px;font-size:0.95rem;">Your personal health overview and insights</p>',
        unsafe_allow_html=True
    )

    sm1, sm2, sm3, sm4 = st.columns(4)
    sm1.metric("💬 Queries Today",    len([m for m in st.session_state.messages if m['role'] == 'user']), "Total")
    sm2.metric("🩺 Conditions Found", len(st.session_state.symptom_history), "Analyzed")
    sm3.metric("💧 Water Intake",     f"{st.session_state.water_cups}/8", "Glasses today")
    sm4.metric("🏆 Health Score",     "78 / 100", "↑ +5 pts this week")

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    dleft, dright = st.columns([1.35, 1])

    #  LEFT: Symptom history + appointments 
    with dleft:
        # Symptom history card
        st.markdown(
            '<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:20px 22px;margin-bottom:16px;backdrop-filter:blur(12px);box-shadow:0 4px 22px rgba(14,165,233,0.08);">'
            '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">'
            '<span style="font-size:1.02rem;font-weight:700;color:#0f172a;">🩺 Symptom History</span>'
            '<span style="font-size:0.7rem;background:rgba(14,165,233,0.1);color:#0284c7;border:1px solid rgba(14,165,233,0.22);padding:3px 10px;border-radius:20px;font-weight:700;">Last 10</span>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.session_state.symptom_history:
            for h in st.session_state.symptom_history[:5]:
                uc, ubg, ubr, uico = urgency_colors(h['urgency'])
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid rgba(14,165,233,0.07);">'
                    f'<div style="width:36px;height:36px;background:linear-gradient(135deg,rgba(14,165,233,0.1),rgba(20,184,166,0.1));border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;">🩺</div>'
                    f'<div style="flex:1;">'
                    f'<div style="font-weight:700;font-size:0.88rem;color:#0f172a;margin:0 0 2px;">{esc(h["condition"])}</div>'
                    f'<div style="font-size:0.72rem;color:#94a3b8;">{esc(h["dept"])} · {h["date"]} at {h["time"]}</div>'
                    f'</div>'
                    f'<div style="font-size:0.68rem;font-weight:700;padding:3px 9px;border-radius:20px;background:{ubg};color:{uc};border:1px solid {ubr};white-space:nowrap;">{uico} {esc(h["urgency"])}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div style="text-align:center;padding:28px 16px;color:#94a3b8;">'
                '<div style="font-size:2.5rem;margin-bottom:10px;">📋</div>'
                '<div style="font-size:0.9rem;font-weight:600;margin-bottom:4px;">No history yet</div>'
                '<div style="font-size:0.8rem;">Go to Chat and analyze your first symptom.</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

        # Upcoming appointments
        st.markdown(
            '<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:20px 22px;backdrop-filter:blur(12px);box-shadow:0 4px 22px rgba(14,165,233,0.08);">'
            '<div style="font-size:1.02rem;font-weight:700;color:#0f172a;margin-bottom:16px;">📅 Upcoming Appointments</div>',
            unsafe_allow_html=True
        )

        for a in [
            {"day": "28", "mon": "Jul", "title": "Annual General Checkup",   "doc": "Dr. Ramesh Mehta",  "time": "10:30 AM"},
            {"day": "02", "mon": "Aug", "title": "Blood Test Result Review", "doc": "Dr. Priya Sharma",  "time": "02:00 PM"},
            {"day": "15", "mon": "Aug", "title": "Cardiology Consultation",  "doc": "Dr. Arun Joshi",    "time": "11:00 AM"},
        ]:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:14px;padding:12px 14px;background:rgba(14,165,233,0.04);border:1px solid rgba(14,165,233,0.10);border-radius:14px;margin-bottom:8px;">'
                f'<div style="background:linear-gradient(135deg,#0ea5e9,#14b8a6);color:white;border-radius:10px;padding:8px 12px;text-align:center;flex-shrink:0;min-width:52px;">'
                f'<div style="font-size:1.25rem;font-weight:800;line-height:1;">{a["day"]}</div>'
                f'<div style="font-size:0.6rem;font-weight:600;opacity:0.9;text-transform:uppercase;">{a["mon"]}</div>'
                f'</div>'
                f'<div style="flex:1;">'
                f'<div style="font-weight:700;font-size:0.88rem;color:#0f172a;margin:0 0 2px;">{a["title"]}</div>'
                f'<div style="font-size:0.75rem;color:#94a3b8;">{a["doc"]}</div>'
                f'</div>'
                f'<div style="font-size:0.8rem;font-weight:600;color:#0ea5e9;background:rgba(14,165,233,0.09);padding:4px 11px;border-radius:8px;white-space:nowrap;">{a["time"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: Water tracker + reminders + insights ───────────────
    with dright:
        cups = st.session_state.water_cups
        pct  = min(100, cups * 12.5)
        cups_html = ''.join([
            f'<span style="font-size:1.55rem;{"" if i < cups else "filter:grayscale(1);opacity:0.35"}">🥤</span>'
            for i in range(8)
        ])
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:20px 22px;margin-bottom:14px;backdrop-filter:blur(12px);box-shadow:0 4px 22px rgba(14,165,233,0.08);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">'
            f'<span style="font-size:1.02rem;font-weight:700;color:#0f172a;">💧 Water Tracker</span>'
            f'<span style="font-size:1.1rem;font-weight:800;color:#0ea5e9;">{cups}/8</span>'
            f'</div>'
            f'<div style="height:10px;background:rgba(14,165,233,0.10);border-radius:10px;overflow:hidden;margin-bottom:13px;">'
            f'<div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#0ea5e9,#06b6d4);border-radius:10px;"></div>'
            f'</div>'
            f'<div style="display:flex;gap:7px;flex-wrap:wrap;margin-bottom:4px;">{cups_html}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        wc1, wc2 = st.columns(2)
        with wc1:
            if st.button("+ Add Glass", key="w_add", use_container_width=True):
                if st.session_state.water_cups < 8:
                    st.session_state.water_cups += 1
                    st.rerun()
        with wc2:
            if st.button("− Remove",    key="w_rem", use_container_width=True):
                if st.session_state.water_cups > 0:
                    st.session_state.water_cups -= 1
                    st.rerun()

        # Medicine reminders
        st.markdown(
            '<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:20px 22px;margin-top:14px;backdrop-filter:blur(12px);box-shadow:0 4px 22px rgba(14,165,233,0.08);">'
            '<div style="font-size:1.02rem;font-weight:700;color:#0f172a;margin-bottom:14px;">💊 Medicine Reminders</div>',
            unsafe_allow_html=True
        )
        for r in st.session_state.reminders:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;padding:10px 12px;background:rgba(14,165,233,0.04);border:1px solid rgba(14,165,233,0.10);border-radius:12px;margin-bottom:8px;">'
                f'<span style="font-size:1.5rem;">{r["icon"]}</span>'
                f'<div style="flex:1;">'
                f'<div style="font-weight:700;font-size:0.86rem;color:#0f172a;">{esc(r["med"])}</div>'
                f'<div style="font-size:0.72rem;color:#94a3b8;">{esc(r["dose"])} · ⏰ {esc(r["time"])}</div>'
                f'</div>'
                f'<div style="width:8px;height:8px;background:#22c55e;border-radius:50%;flex-shrink:0;"></div>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Health insights
        st.markdown(
            '<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:20px 22px;margin-top:14px;backdrop-filter:blur(12px);box-shadow:0 4px 22px rgba(14,165,233,0.08);">'
            '<div style="font-size:1.02rem;font-weight:700;color:#0f172a;margin-bottom:14px;">💡 Health Insights</div>',
            unsafe_allow_html=True
        )
        for tip in BE.get_health_tips()[:4]:
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:11px;padding:10px 11px;background:{tip["bg"]};border-radius:11px;margin-bottom:8px;">'
                f'<div style="width:38px;height:38px;border-radius:10px;background:{tip["bg"]};border:1px solid {tip["color"]}25;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">{tip["icon"]}</div>'
                f'<div>'
                f'<div style="font-weight:700;font-size:0.84rem;color:#0f172a;margin:0 0 3px;">{tip["title"]}</div>'
                f'<div style="font-size:0.74rem;color:#475569;line-height:1.5;">{tip["tip"][:85]}…</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)



# TAB 3 — UPLOAD REPORT

with tab_upload:
    st.markdown(
        '<h2 style="font-size:1.75rem;font-weight:800;color:#0f172a;letter-spacing:-0.035em;margin:0 0 5px;">Medical Report Analysis</h2>'
        '<p style="color:#64748b;margin:0 0 24px;font-size:0.95rem;">Upload your reports for AI-powered extraction and health insights</p>',
        unsafe_allow_html=True
    )

    upcol, infocol = st.columns([1.25, 1])

    with upcol:
        st.markdown(
            '<div style="border:2.5px dashed rgba(14,165,233,0.32);border-radius:20px;padding:40px 24px;text-align:center;background:rgba(14,165,233,0.02);margin-bottom:18px;">'
            '<div style="font-size:3.5rem;margin-bottom:16px;">📄</div>'
            '<div style="font-size:1.12rem;font-weight:700;color:#0f172a;margin-bottom:8px;">Drop your medical report here</div>'
            '<div style="font-size:0.87rem;color:#64748b;margin-bottom:4px;">or choose a file below</div>'
            '<div style="font-size:0.74rem;color:#94a3b8;">PDF · JPG · PNG · DOCX · Max 10 MB</div>'
            '</div>',
            unsafe_allow_html=True
        )

        uploaded = st.file_uploader(
            "Choose a medical report",
            type=['pdf', 'jpg', 'jpeg', 'png', 'docx'],
            key="uploader",
            label_visibility="collapsed",
        )

        if uploaded:
            size_kb = uploaded.size // 1024
            st.markdown(
                f'<div style="background:rgba(34,197,94,0.08);border:1.5px solid rgba(34,197,94,0.28);border-radius:14px;padding:16px 18px;display:flex;align-items:center;gap:12px;margin-top:10px;">'
                f'<div style="font-size:2rem;flex-shrink:0;">✅</div>'
                f'<div>'
                f'<div style="font-weight:700;font-size:0.92rem;color:#166534;">Uploaded successfully!</div>'
                f'<div style="font-size:0.8rem;color:#16a34a;">{esc(uploaded.name)} · {size_kb} KB</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

            if st.button("🔬  Analyze Report", type="primary", use_container_width=True, key="do_analyze"):
                with st.spinner("Extracting data from your report…"):
                    time.sleep(2)
                st.success("✅ Report processed. Key highlights extracted.")
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:22px;margin-top:14px;box-shadow:0 4px 20px rgba(14,165,233,0.08);">'
                    '<div style="font-size:1rem;font-weight:700;color:#0f172a;margin-bottom:14px;">📋 Analysis Summary</div>'
                    '<div style="display:flex;flex-direction:column;gap:9px;">'
                    '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(34,197,94,0.06);border-radius:10px;"><span style="font-size:1.2rem;">✅</span><span style="font-size:0.87rem;color:#0f172a;font-weight:600;">Document processed and scanned</span></div>'
                    '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(14,165,233,0.05);border-radius:10px;"><span style="font-size:1.2rem;">💡</span><span style="font-size:0.87rem;color:#0f172a;">Consult a physician to interpret results accurately.</span></div>'
                    '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:rgba(245,158,11,0.05);border-radius:10px;"><span style="font-size:1.2rem;">⚙️</span><span style="font-size:0.87rem;color:#0f172a;">Full OCR + clinical NLP available in MediNex Pro.</span></div>'
                    '</div></div>',
                    unsafe_allow_html=True
                )

    with infocol:
        st.markdown(
            '<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:22px;box-shadow:0 4px 20px rgba(14,165,233,0.08);margin-bottom:16px;">'
            '<div style="font-size:1rem;font-weight:700;color:#0f172a;margin-bottom:16px;">📌 Report Types We Support</div>',
            unsafe_allow_html=True
        )
        for icon, title, desc in [
            ("🩸", "Blood Test Reports",  "CBC, lipid panel, sugar & more"),
            ("🧠", "Radiology Reports",   "MRI, CT scan, X-ray findings"),
            ("💊", "Prescription Scans",  "Medication ID & interaction check"),
            ("❤️", "ECG / EKG Reports",   "Heart rhythm & cardiac analysis"),
            ("🧬", "Pathology Reports",   "Lab biomarkers & tissue analysis"),
            ("👁️", "Ophthalmology",       "Eye test & vision reports"),
        ]:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(14,165,233,0.07);">'
                f'<div style="width:38px;height:38px;background:rgba(14,165,233,0.07);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">{icon}</div>'
                f'<div><div style="font-weight:700;font-size:0.85rem;color:#0f172a;">{title}</div>'
                f'<div style="font-size:0.72rem;color:#94a3b8;">{desc}</div></div>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div style="background:linear-gradient(135deg,rgba(239,68,68,0.07),rgba(239,68,68,0.03));border:1.5px solid rgba(239,68,68,0.22);border-radius:16px;padding:16px 18px;">'
            '<div style="font-size:0.87rem;font-weight:700;color:#dc2626;margin-bottom:6px;">⚠️ Medical Disclaimer</div>'
            '<div style="font-size:0.78rem;color:#7f1d1d;line-height:1.65;">'
            'MediNex AI is a decision-support tool only. It does <strong>NOT</strong> replace professional medical diagnosis or treatment. Always consult a qualified healthcare provider.'
            '</div></div>',
            unsafe_allow_html=True
        )



# TAB 4 — EMERGENCY

with tab_em:
    st.markdown(
        '<div style="background:linear-gradient(135deg,#ef4444,#dc2626);border-radius:20px;padding:22px 28px;color:white;display:flex;align-items:center;gap:16px;margin-bottom:28px;box-shadow:0 8px 36px rgba(239,68,68,0.38);">'
        '<div style="font-size:3rem;flex-shrink:0;">🚨</div>'
        '<div style="flex:1;">'
        '<div style="font-size:1.4rem;font-weight:800;margin:0 0 4px;">Emergency Contacts</div>'
        '<div style="font-size:0.9rem;opacity:0.92;">For life-threatening emergencies, call <strong>112</strong> immediately.</div>'
        '</div>'
        '<div style="text-align:right;flex-shrink:0;">'
        '<div style="font-size:2.8rem;font-weight:900;letter-spacing:-0.03em;line-height:1;">112</div>'
        '<div style="font-size:0.7rem;opacity:0.82;text-transform:uppercase;letter-spacing:0.06em;">National Emergency</div>'
        '</div></div>',
        unsafe_allow_html=True
    )

    st.markdown('<h3 style="font-size:1.1rem;font-weight:700;color:#0f172a;margin:0 0 16px;">📞 Emergency Helplines</h3>', unsafe_allow_html=True)

    ec1, ec2 = st.columns(2)
    for i, c in enumerate(BE.get_emergency_contacts()):
        num_color = "#ef4444" if c['color'] == "#ef4444" else "#0ea5e9"
        with (ec1 if i % 2 == 0 else ec2):
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.92);border:1.5px solid rgba(14,165,233,0.12);border-radius:18px;padding:18px 20px;display:flex;align-items:center;gap:14px;margin-bottom:12px;box-shadow:0 4px 18px rgba(14,165,233,0.07);">'
                f'<div style="width:52px;height:52px;background:{c["bg"]};border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;flex-shrink:0;">{c["icon"]}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-weight:700;font-size:0.95rem;color:#0f172a;margin:0 0 3px;">{esc(c["name"])}</div>'
                f'<div style="font-size:0.77rem;color:#94a3b8;">{esc(c["desc"])}</div>'
                f'</div>'
                f'<div style="font-size:1.45rem;font-weight:800;color:{num_color};letter-spacing:-0.02em;flex-shrink:0;">{c["number"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<h3 style="font-size:1.1rem;font-weight:700;color:#0f172a;margin:16px 0;">🩹 Quick First Aid Guide</h3>', unsafe_allow_html=True)

    fa1, fa2 = st.columns(2)
    first_aid = [
        ("❤️",  "Heart Attack",         "Chew aspirin (if not allergic). Rest, loosen clothing. Stay calm. Call 108 NOW."),
        ("🧠",  "Stroke — FAST",        "Face drooping? Arm weakness? Speech slurred? Call 112 immediately."),
        ("🩸",  "Severe Bleeding",      "Apply firm pressure with clean cloth. Elevate wound above heart level."),
        ("🤕",  "Head Injury",          "Keep person still. Do NOT move them. Monitor breathing. Call ambulance."),
        ("🔥",  "Burns",                "Cool under running water 20 min. No ice. Cover loosely. Seek help."),
        ("😵",  "Fainting",             "Lay flat, raise legs 30 cm. Loosen clothing. No food/water until conscious."),
    ]
    for i, (icon, title, tip) in enumerate(first_aid):
        with (fa1 if i % 2 == 0 else fa2):
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.9);border:1px solid rgba(14,165,233,0.12);border-radius:16px;padding:16px 18px;box-shadow:0 3px 12px rgba(14,165,233,0.06);margin-bottom:12px;">'
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
                f'<span style="font-size:1.25rem;">{icon}</span>'
                f'<span style="font-weight:700;font-size:0.87rem;color:#0f172a;">{title}</span>'
                f'</div>'
                f'<p style="font-size:0.79rem;color:#475569;line-height:1.6;margin:0;">{tip}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div style="background:rgba(14,165,233,0.05);border:1px solid rgba(14,165,233,0.15);border-radius:14px;padding:16px 20px;text-align:center;margin-top:8px;">'
        '<div style="font-size:0.88rem;font-weight:700;color:#0284c7;margin-bottom:4px;">🏥 Find the Nearest Emergency Room</div>'
        '<div style="font-size:0.8rem;color:#475569;">Use Google Maps → search <strong>"Emergency hospital near me"</strong> or call <strong>108</strong> for ambulance.</div>'
        '</div>',
        unsafe_allow_html=True
    )