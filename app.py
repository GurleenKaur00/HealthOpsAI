import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data" / "processed"
MODEL_DIR = BASE_DIR / "models"

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "processed_hospital_data.csv")

df = load_data()

# ==========================================================
# LOAD MODEL
# ==========================================================

@st.cache_resource
def load_model():

    package = joblib.load(
        MODEL_DIR / "readmission_model.pkl"
    )

    model = package["model"]
    preprocessor = package["preprocessor"]
    threshold = package["threshold"]

    return model, preprocessor, threshold

model, preprocessor, threshold = load_model()
# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="HealthOps AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "role" not in st.session_state:
    st.session_state.role = ""

if "hospital" not in st.session_state:
    st.session_state.hospital = ""

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* ------------------------------------------------ */
/* Hide Streamlit Components */
/* ------------------------------------------------ */

#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}

/* ------------------------------------------------ */
/* App Background */
/* ------------------------------------------------ */

.stApp{
background:linear-gradient(
135deg,
#F6FAFF 0%,
#EEF6FF 45%,
#FFFFFF 100%);
}

/* ------------------------------------------------ */
/* Main Container */
/* ------------------------------------------------ */

.block-container{
padding-top:1rem;
padding-left:4rem;
padding-right:4rem;
padding-bottom:2rem;
}

/* ------------------------------------------------ */
/* Headings */
/* ------------------------------------------------ */

h1,h2,h3{
color:#1565C0;
font-family:Arial;
}

/* ------------------------------------------------ */
/* Buttons */
/* ------------------------------------------------ */

.stButton>button{

width:100%;

background:#1565C0;

color:white;

border:none;

border-radius:12px;

padding:12px;

font-size:16px;

font-weight:600;

transition:0.3s;

}

.stButton>button:hover{

background:#0D47A1;

color:white;

transform:translateY(-3px);

box-shadow:0px 12px 25px rgba(0,0,0,0.18);

}

/* ------------------------------------------------ */
/* Version Badge */
/* ------------------------------------------------ */

.version-badge{

display:inline-block;

background:#E8F3FF;

color:#1565C0;

padding:10px 22px;

border-radius:30px;

font-size:15px;

font-weight:600;

}

/* ------------------------------------------------ */
/* Section Heading */
/* ------------------------------------------------ */

.section-title{

font-size:38px;

font-weight:700;

color:#1565C0;

margin-bottom:15px;

}

.section-subtitle{

font-size:18px;

color:#555;

line-height:1.8;

}
/* ======================================================
STATISTICS CARDS
====================================================== */

.stats-heading{

text-align:center;

margin-top:50px;

margin-bottom:30px;

}

.stats-card{

background:white;

border-radius:18px;

padding:28px 20px;

text-align:center;

border:1px solid #E6EEF7;

box-shadow:0px 8px 18px rgba(0,0,0,0.08);

transition:0.35s;

height:230px;

}

.stats-card:hover{

transform:translateY(-8px);

box-shadow:0px 18px 35px rgba(0,0,0,0.18);

border:1px solid #1565C0;

}

.stats-icon{

font-size:45px;

margin-bottom:15px;

}

.stats-number{

font-size:36px;

font-weight:700;

color:#1565C0;

margin-bottom:10px;

}

.stats-title{

font-size:20px;

font-weight:600;

margin-bottom:10px;

}

.stats-desc{

font-size:15px;

color:#666;

line-height:1.6;

}
/* ======================================================
LOGIN CARDS
====================================================== */

.portal-heading{

text-align:center;

margin-top:40px;

margin-bottom:30px;

}

.portal-card{

background:white;

border-radius:20px;

padding:30px 25px;

text-align:center;

border:1px solid #E7EEF7;

box-shadow:0px 8px 20px rgba(0,0,0,0.08);

transition:0.35s;

height:420px;

}

.portal-card:hover{

transform:translateY(-8px);

box-shadow:0px 18px 35px rgba(0,0,0,0.16);

border:1px solid #1565C0;

}

.portal-icon{

font-size:70px;

margin-bottom:18px;

}

.portal-title{

font-size:24px;

font-weight:700;

color:#1565C0;

margin-bottom:15px;

}

.portal-desc{

font-size:15px;

color:#666;

line-height:1.7;

margin-bottom:20px;

}
/* ======================================================
SERVICES
====================================================== */

.service-card{

background:white;

border-radius:18px;

padding:28px;

text-align:center;

height:280px;

border:1px solid #E7EEF7;

box-shadow:0px 8px 20px rgba(0,0,0,0.08);

transition:0.35s;

}

.service-card:hover{

transform:translateY(-8px);

border:1px solid #1565C0;

box-shadow:0px 20px 40px rgba(0,0,0,0.15);

}

.service-icon{

font-size:55px;

margin-bottom:20px;

}

.service-title{

font-size:24px;

font-weight:700;

color:#1565C0;

margin-bottom:15px;

}

.service-desc{

font-size:15px;

line-height:1.8;

color:#666;

}
/* ======================================================
WHY CHOOSE US
====================================================== */

.feature-card{

background:white;

border-radius:18px;

padding:25px;

height:220px;

text-align:center;

border:1px solid #E7EEF7;

box-shadow:0px 8px 18px rgba(0,0,0,0.08);

transition:0.35s;

}

.feature-card:hover{

transform:translateY(-8px);

border:1px solid #1565C0;

box-shadow:0px 18px 35px rgba(0,0,0,0.15);

}

.feature-icon{

font-size:48px;

margin-bottom:18px;

}

.feature-title{

font-size:22px;

font-weight:700;

color:#1565C0;

margin-bottom:12px;

}

.feature-desc{

font-size:15px;

line-height:1.7;

color:#666;

}
/* ======================================================
FOOTER
====================================================== */

.footer{

background:#0F172A;

color:white;

padding:45px 30px;

border-radius:20px 20px 0px 0px;

margin-top:50px;

}

.footer-title{

font-size:28px;

font-weight:700;

margin-bottom:15px;

color:white;

}

.footer-subtitle{

font-size:15px;

line-height:1.8;

color:#CBD5E1;

}

.footer-heading{

font-size:18px;

font-weight:600;

margin-bottom:15px;

color:white;

}

.footer-link{

color:#CBD5E1;

margin-bottom:10px;

font-size:15px;

}

.footer-bottom{

text-align:center;

margin-top:30px;

padding-top:20px;

border-top:1px solid rgba(255,255,255,0.15);

font-size:14px;

color:#94A3B8;

}
/* ======================================================
DOCTOR LOGIN
====================================================== */

.login-box{

background:white;

padding:40px;

border-radius:20px;

box-shadow:0px 10px 30px rgba(0,0,0,0.10);

margin-top:40px;

}

.login-title{

font-size:34px;

font-weight:700;

color:#1565C0;

margin-bottom:10px;

}

.login-subtitle{

font-size:16px;

color:#666;

margin-bottom:30px;

line-height:1.7;

}

.login-icon{

font-size:120px;

text-align:center;

margin-top:50px;

}
/* ======================================================
DOCTOR DASHBOARD
====================================================== */

.dashboard-header{

background:linear-gradient(135deg,#1565C0,#1E88E5);

padding:25px;

border-radius:18px;

color:white;

margin-bottom:30px;

box-shadow:0px 8px 20px rgba(0,0,0,0.12);

}

.dashboard-title{

font-size:34px;

font-weight:700;

}

.dashboard-subtitle{

font-size:17px;

opacity:0.95;

margin-top:8px;

}

.metric-card{

background:white;

padding:22px;

border-radius:18px;

text-align:center;

box-shadow:0px 8px 18px rgba(0,0,0,0.08);

border:1px solid #E6EEF7;

transition:0.3s;

}

.metric-card:hover{

transform:translateY(-5px);

}

.metric-number{

font-size:34px;

font-weight:bold;

color:#1565C0;

}

.metric-label{

margin-top:10px;

font-size:16px;

color:#666;

}
</style>
""", unsafe_allow_html=True)


def home_page():

    # ======================================================
    # HEADER
    # ======================================================

    col1, col2 = st.columns([4,1])

    with col1:

        st.markdown("""
        <h1 style="margin-bottom:0;">
        🏥 HealthOps AI
        </h1>

        <p style="
        margin-top:0;
        font-size:20px;
        color:#555;">
        AI-Powered Hospital Decision Support System
        </p>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div style="text-align:right;margin-top:18px;">
        <span class="version-badge">
        Version 1.0
        </span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ======================================================
    # HERO
    # ======================================================

    left, right = st.columns([1.15,1])

    with left:

        st.markdown("""
        <div class="section-title">
        Transforming Healthcare
        <br>
        with Artificial Intelligence
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-subtitle">

        HealthOps AI is an AI-powered hospital decision support
        platform that helps doctors predict patient readmission,
        generate personalized recommendations, monitor hospital
        performance and assist healthcare administrators through
        intelligent analytics.

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.write("")

        st.markdown(
        """
        <div style="
        background:#E8F3FF;
        padding:15px;
        border-radius:12px;
        border-left:5px solid #1565C0;
        font-size:17px;
        color:#333;
        margin-bottom:15px;
        ">
        ℹ️ <b>Want to know more about this project?</b><br>
        Click the <b>About</b> button below to explore the project overview, workflow, technologies, and implementation details.
        </div>
        """,
        unsafe_allow_html=True
        )

        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()

            st.write("")

        f1, f2 = st.columns(2)

        with f1:
            st.success("🧠 Readmission Prediction")
            st.success("📊 Hospital Analytics")

        with f2:
            st.success("💡 AI Recommendation")
            st.success("🔒 Secure Access")

    with right:

        st.image(
            "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1200",
            use_container_width=True
        )

    # ======================================================
    # STATISTICS
    # ======================================================

    st.markdown("""
    <div class="stats-heading">

    <h2 style="color:#1565C0;">
    HealthOps AI at a Glance
    </h2>

    <p style="color:#666;">
    Empowering smarter healthcare with Artificial Intelligence.
    </p>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    cards = [

        ("🧠","30","Days","Readmission prediction window."),

        ("🏥","50+","KPIs","Operational, clinical and financial analytics."),

        ("🤖","Clinical","Assistant","Clinical decision support."),

        ("🔒","100%","Secure","Role-based secure access system.")

    ]

    columns = [c1, c2, c3, c4]

    for col, card in zip(columns, cards):

        with col:

            st.markdown(f"""
            <div class="stats-card">

            <div class="stats-icon">{card[0]}</div>

            <div class="stats-number">{card[1]}</div>

            <div class="stats-title">{card[2]}</div>

            <div class="stats-desc">{card[3]}</div>

            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # ======================================================
    # LOGIN PORTALS
    # ======================================================

    st.markdown("""
    <div class="portal-heading">

    <h2 style="color:#1565C0;">
    Choose Your Portal
    </h2>

    <p style="color:#666;">
    Secure role-based access for every healthcare stakeholder.
    </p>

    </div>
    """, unsafe_allow_html=True)

    doctor,ministry = st.columns(2)

    # ------------------------------------------------------
    # DOCTOR
    # ------------------------------------------------------

    with doctor:

        st.markdown("""

        <div class="portal-card">

        <div class="portal-icon">
        👨‍⚕️
        </div>

        <div class="portal-title">
        Doctor Portal
        </div>

        <div class="portal-desc">

        • Predict patient readmission

        <br><br>

        • View patient profile

        <br><br>

        • AI recommendations

        <br><br>

        • Clinical decision support

        </div>

        </div>

        """, unsafe_allow_html=True)

        if st.button("Login as Doctor", use_container_width=True):

            st.session_state.page = "doctor_login"

            st.rerun()

    # ------------------------------------------------------
    # MINISTRY
    # ------------------------------------------------------

    with ministry:

        st.markdown("""

        <div class="portal-card">

        <div class="portal-icon">
        🏛️
        </div>

        <div class="portal-title">
        Health Ministry
        </div>

        <div class="portal-desc">

        • Nationwide analytics

        <br><br>

        • Hospital comparison

        <br><br>

        • Policy monitoring

        <br><br>

        • Healthcare Intelligence

        </div>

        </div>

        """, unsafe_allow_html=True)

        if st.button(
            "Login as Ministry",
            key="ministry",
            use_container_width=True
        ):
            st.session_state.page="ministry_login"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    # ======================================================
    # SERVICES
    # ======================================================

    st.markdown("""

    <div style="text-align:center; margin-top:40px;">

    <h2 style="color:#1565C0;">
    Our Intelligent Services
    </h2>

    <p style="color:#666;">
    AI-powered solutions designed to improve healthcare outcomes.
    </p>

    </div>

    """, unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        st.markdown("""

        <div class="service-card">

        <div class="service-icon">
        🧠
        </div>

        <div class="service-title">
        Readmission Prediction
        </div>

        <div class="service-desc">

        Predicts 30-day patient readmission using
        Machine Learning models to help clinicians
        identify high-risk patients early.

        </div>

        </div>

        """, unsafe_allow_html=True)

    with row1_col2:

        st.markdown("""

        <div class="service-card">

        <div class="service-icon">
        💡
        </div>

        <div class="service-title">
        Recommendation Engine
        </div>

        <div class="service-desc">

        Generates personalized patient care
        recommendations using diagnosis,
        age, admission details and AI insights.

        </div>

        </div>

        """, unsafe_allow_html=True)

    st.write("")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:

        st.markdown("""

        <div class="service-card">

        <div class="service-icon">
        📊
        </div>

        <div class="service-title">
        Hospital Analytics
        </div>

        <div class="service-desc">

        Interactive dashboards providing
        clinical, operational and financial
        performance insights.

        </div>

        </div>

        """, unsafe_allow_html=True)

    with row2_col2:

        st.markdown("""

        <div class="service-card">

        <div class="service-icon">
        
        </div>

        <div class="service-title">
        Clinical Decision Support
        </div>

        <div class="service-desc">

        Evidence-based recommendations to support patient discharge planning

        </div>

        </div>

        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # ======================================================
    # WHY CHOOSE HEALTHOPS AI
    # ======================================================

    st.markdown("""
    <div style="text-align:center; margin-top:40px;">

    <h2 style="color:#1565C0;">
    Why Choose HealthOps AI?
    </h2>

    <p style="color:#666;">
    A complete AI-powered platform designed for modern healthcare organizations.
    </p>

    </div>
    """, unsafe_allow_html=True)

    # ---------------- First Row ----------------

    c1, c2, c3 = st.columns(3)

    cards = [

    ("🔐","Secure Access",
    "Role-based authentication for Doctors, Managers and Health Ministry officials."),

    ("🧠","AI Prediction",
    "Machine Learning model predicts 30-day patient readmission risk."),

    ("📊","Smart Analytics",
    "Clinical, operational and financial dashboards powered by Power BI.")

    ]

    for col, card in zip([c1,c2,c3], cards):

        with col:

            st.markdown(f"""
            <div class="feature-card">

            <div class="feature-icon">{card[0]}</div>

            <div class="feature-title">{card[1]}</div>

            <div class="feature-desc">{card[2]}</div>

            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # ---------------- Second Row ----------------

    c4, c5, c6 = st.columns(3)

    cards = [

    ("⚡","Real-Time Decisions",
    "Instant predictions and recommendations to support clinical decisions."),

    ("🏥","Hospital Intelligence",
    "Monitor hospital performance through integrated analytics and KPIs."),

    ("💡","Clinical Decision Support",
    "Evidence-based recommendations to support patient discharge planning.")

    ]

    for col, card in zip([c4,c5,c6], cards):

        with col:

            st.markdown(f"""
            <div class="feature-card">

            <div class="feature-icon">{card[0]}</div>

            <div class="feature-title">{card[1]}</div>

            <div class="feature-desc">{card[2]}</div>

            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    # ======================================================
    # FOOTER
    # ======================================================

    st.markdown("""

    <div class="footer">

    <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:40px;">

    <div style="flex:1; min-width:280px;">

    <div class="footer-title">
    🏥 HealthOps AI
    </div>

    <div class="footer-subtitle">
    An AI-powered healthcare intelligence platform that helps doctors,
    hospital administrators, and healthcare authorities make smarter,
    data-driven decisions through predictive analytics and intelligent dashboards.
    </div>

    </div>

    <div style="flex:1; min-width:220px;">

    <div class="footer-heading">
    Modules
    </div>

    <div class="footer-link">• Readmission Prediction</div>

    <div class="footer-link">• Recommendation Engine</div>

    <div class="footer-link">• Hospital Analytics</div>

    </div>

    <div style="flex:1; min-width:220px;">

    <div class="footer-heading">
    User Portals
    </div>

    <div class="footer-link">• Doctor</div>

    <div class="footer-link">• Health Ministry</div>

    <div class="footer-link">• Secure Role-Based Access</div>

    </div>

    </div>

    <div class="footer-bottom">

    © Gurleen Kaur | Major Project | Built with AI, Machine Learning, SQL, Power BI & Streamlit

    </div>

    </div>

    """, unsafe_allow_html=True)


def doctor_login_page():

    st.markdown("<h1 style='text-align:center;color:#1565C0;'>Doctor Portal</h1>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1,1])

    # ---------------- LEFT ----------------

    with left:

        st.markdown("""
        <div class="login-box">

        <div class="login-title">
        Welcome Doctor
        </div>

        <div class="login-subtitle">
        Login to access patient records, AI-powered predictions,
        treatment recommendations, and healthcare analytics.
        </div>

        """, unsafe_allow_html=True)

        hospital = st.selectbox(
            "Hospital",
            sorted(df["hospital_name"].dropna().astype(str).unique())
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Login", use_container_width=True):

            if username == "doctor" and password == "doctor123":

                st.success("Login Successful")
                st.session_state.hospital = hospital

                st.session_state.page = "doctor_dashboard"

                st.rerun()

            else:

                st.error("Invalid Username or Password")

        if st.button("← Back to Home", use_container_width=True):

            st.session_state.page = "home"

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- RIGHT ----------------

    with right:

        st.markdown("""
        <div class="login-icon">
        👨‍⚕️
        </div>

        <h2 style="text-align:center;color:#1565C0;">
        HealthOps AI
        </h2>

        <p style="text-align:center;color:#666;font-size:18px;">
        Secure AI-powered healthcare platform
        for doctors and clinicians.
        </p>
        """, unsafe_allow_html=True)

def doctor_dashboard_page():

    st.markdown(f"""
    <div class="dashboard-header">

    <div class="dashboard-title">
    👨‍⚕️ Doctor Dashboard
    </div>

    <div class="dashboard-subtitle">
    Hospital : <b>{st.session_state.hospital}</b>
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📝 Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        patient_id = st.text_input("Patient ID")

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=45
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        admit_type = st.selectbox(
            "Admission Type",
            sorted(df["admit_type"].dropna().astype(str).unique())
        )

        primary_diag_category = st.selectbox(
        "Primary Diagnosis Category",
            sorted(df["primary_diag_category"].dropna().astype(str).unique())
        )

        los_days = st.number_input(
            "Length of Stay (Days)",
            min_value=1,
            max_value=60,
            value=5
        )
        admit_date = st.date_input(
        "Admission Date"
        )

        total_diagnoses = st.number_input(
        "Total Diagnoses",
        min_value=1,
        max_value=20,
        value=2
        )

    with col2:

        ward_type = st.selectbox(
            "Ward Type",
            sorted(df["ward_type"].dropna().astype(str).unique())
        )

        insurance_type = "Unknown"  # Default value

        total_cost = st.number_input(
            "Estimated Cost (₹)",
            min_value=0.0,
            value=50000.0
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
    "🧠 Predict Readmission",
    use_container_width=True
    ):

            st.session_state.patient_data = {

                "patient_id": patient_id,

                "age": age,

                "gender": gender,

                "admit_type": admit_type,

                "primary_diag_category": primary_diag_category,

                "los_days": los_days,

                "ward_type": ward_type,

                "insurance_type": insurance_type,

                "total_diagnoses": total_diagnoses,

                "admit_date": admit_date,

                "total_cost_inr": total_cost,

                "hospital_name": st.session_state.hospital

            }

            st.session_state.page = "prediction"

            st.rerun()

    with c2:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.page = "home"

            st.session_state.hospital = ""

            st.rerun()
from datetime import datetime

def prepare_patient_features(patient):

    hospital_row = df[
        df["hospital_name"] == patient["hospital_name"]
    ].iloc[0]

    admit_date = pd.to_datetime(patient["admit_date"])

    feature = {}

    # =====================================================
    # Raw Features
    # =====================================================

    feature["admit_type"] = patient["admit_type"]
    feature["ward_type"] = patient["ward_type"]
    feature["los_days"] = patient["los_days"]
    feature["age"] = patient["age"]
    feature["gender"] = patient["gender"]
    feature["patient_state"] = hospital_row["hospital_state"]
    feature["insurance_type"] = patient["insurance_type"]

    feature["hospital_state"] = hospital_row["hospital_state"]
    feature["hospital_tier"] = hospital_row["hospital_tier"]
    feature["beds"] = hospital_row["beds"]
    feature["teaching"] = hospital_row["teaching"]

    feature["primary_diag_category"] = patient["primary_diag_category"]

    feature["total_diagnoses"] = patient["total_diagnoses"]

    feature["total_cost_inr"] = patient["total_cost_inr"]

    # =====================================================
    # Date Features
    # =====================================================

    feature["admit_year"] = admit_date.year
    feature["admit_month"] = admit_date.month
    feature["admit_day"] = admit_date.day
    feature["admit_weekday"] = admit_date.day_name()
    feature["admit_quarter"] = admit_date.quarter

    feature["discharge_year"] = admit_date.year
    feature["discharge_month"] = admit_date.month

    feature["weekend_admission"] = int(
        feature["admit_weekday"] in ["Saturday", "Sunday"]
    )

    # =====================================================
    # Cost Category
    # =====================================================

    q1 = df["total_cost_inr"].quantile(0.25)
    q3 = df["total_cost_inr"].quantile(0.75)

    if feature["total_cost_inr"] <= q1:
        feature["cost_category"] = "Low"

    elif feature["total_cost_inr"] >= q3:
        feature["cost_category"] = "High"

    else:
        feature["cost_category"] = "Medium"

    # =====================================================
    # Engineered Numerical Features
    # =====================================================

    feature["stay_per_bed"] = (
        feature["los_days"] /
        feature["beds"]
    )

    feature["cost_per_day"] = (
        feature["total_cost_inr"] /
        (feature["los_days"] + 1)
    )

    feature["cost_per_bed"] = (
        feature["total_cost_inr"] /
        feature["beds"]
    )

    feature["num_diagnosis_categories"] = 1

    feature["diagnosis_density"] = (
        feature["total_diagnoses"] /
        (feature["los_days"] + 1)
    )

    feature["cost_per_diagnosis"] = (
        feature["total_cost_inr"] /
        (feature["total_diagnoses"] + 1)
    )

    feature["diagnosis_per_bed"] = (
        feature["total_diagnoses"] /
        feature["beds"]
    )

    feature["elderly"] = int(feature["age"] >= 65)

    feature["very_elderly"] = int(feature["age"] >= 80)

    feature["long_stay"] = int(feature["los_days"] >= 7)

    feature["very_long_stay"] = int(feature["los_days"] >= 14)

    feature["multiple_diagnoses"] = int(
        feature["total_diagnoses"] >= 5
    )

    feature["age_diagnosis"] = (
        feature["age"] *
        feature["total_diagnoses"]
    )

    feature["large_hospital"] = int(
        feature["beds"] >= df["beds"].median()
    )

    feature["low_cost"] = int(
        feature["total_cost_inr"] <= q1
    )

    feature["high_cost"] = int(
        feature["total_cost_inr"] >= q3
    )

    feature["bed_cost_ratio"] = (
        feature["beds"] /
        (feature["total_cost_inr"] + 1)
    )

    feature["bed_los_ratio"] = (
        feature["beds"] /
        (feature["los_days"] + 1)
    )

    if feature["admit_month"] in [12, 1, 2]:
        feature["season"] = "Winter"
    elif feature["admit_month"] in [3, 4, 5]:
        feature["season"] = "Spring"
    elif feature["admit_month"] in [6, 7, 8]:
        feature["season"] = "Summer"
    else:
        feature["season"] = "Autumn"

    feature["age_los"] = (
        feature["age"] *
        feature["los_days"]
    )

    feature["age_cost"] = (
        feature["age"] *
        feature["total_cost_inr"]
    )

    feature["diagnosis_cost"] = (
        feature["total_diagnoses"] *
        feature["total_cost_inr"]
    )

    feature["teaching_long_stay"] = int(
        feature["teaching"] == 1 and
        feature["los_days"] >= 7
    )

    feature["has_cardiovascular"] = int(
        feature["primary_diag_category"] == "Cardiovascular"
    )

    feature["has_respiratory"] = int(
        feature["primary_diag_category"] == "Respiratory"
    )

    feature["has_neurological"] = int(
        feature["primary_diag_category"] == "Neurological"
    )

    feature["has_endocrine"] = int(
        feature["primary_diag_category"] == "Endocrine"
    )

    feature["has_infectious"] = int(
        feature["primary_diag_category"] == "Infectious"
    )

    feature["has_neoplasm"] = int(
        feature["primary_diag_category"] == "Neoplasm"
    )

    feature["has_gastrointestinal"] = int(
        feature["primary_diag_category"] == "Gastrointestinal"
    )

    return pd.DataFrame([feature])
            
def prediction_page():

    patient = st.session_state.patient_data
    st.markdown("""
    <div class="dashboard-header">

        <div class="dashboard-title">
        🧠 Readmission Risk Prediction
        </div>

        <div class="dashboard-subtitle">
        Evaluate the likelihood of 30-day hospital readmission.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("Patient Summary")

    c1, c2 = st.columns(2)

    with c1:

        st.info(f"**Hospital**\n\n{patient['hospital_name']}")

        st.info(f"**Age**\n\n{patient['age']} Years")

        st.info(f"**Gender**\n\n{patient['gender']}")

        st.info(f"**Admission Type**\n\n{patient['admit_type']}")

    with c2:

        st.info(f"**Diagnosis Category**\n\n{patient['primary_diag_category']}")

        st.info(f"**Length of Stay**\n\n{patient['los_days']} Days")

        st.info(f"**Ward Type**\n\n{patient['ward_type']}")

        st.info(f"**Insurance**\n\n{patient['insurance_type']}")

    st.divider()

    predict = st.button(
        "🧠 Predict Readmission Risk",
        use_container_width=True
    )

    if predict:

        try:

            input_df = prepare_patient_features(patient)

            input_df = input_df[preprocessor.feature_names_in_]

            X_processed = preprocessor.transform(input_df)

            probability = model.predict_proba(
             X_processed
            )[0][1]

            prediction = int(
            probability >= threshold
            )

        except Exception as e:

            st.error(f"Prediction Error: {e}")

            st.stop()

        st.markdown("## Prediction Result")

        st.progress(probability)

        if prediction == 1:

            st.error(
                f"🔴 HIGH RISK ({probability*100:.2f}%)"
            )

            st.warning(
                "This patient has a high probability of readmission within 30 days."
            )

        else:

            st.success(
                f"🟢 LOW RISK ({probability*100:.2f}%)"
            )

            st.success(
                "The patient is unlikely to be readmitted within 30 days."
            )

        st.session_state.prediction = prediction

        st.session_state.probability = probability

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            st.session_state.page = "doctor_dashboard"

            st.rerun()

    with col2:

        if st.button(
            "Treatment Recommendations →",
            use_container_width=True,
            disabled=("prediction" not in st.session_state)
        ):

            st.session_state.page = "recommendation"

            st.rerun()

def ministry_login_page():

    st.title("🏛️ Health Ministry Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        if username == "ministry" and password == "ministry123":

            st.session_state.page = "ministry_dashboard"
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    if st.button("← Back", use_container_width=True):

        st.session_state.page = "home"
        st.rerun()


def ministry_dashboard_page():

    st.title("🏛️ Health Ministry Dashboard")

    st.write(
        """
National Healthcare Analytics Dashboard

The following Power BI dashboard provides an overview of
hospital performance, readmission trends and healthcare
analytics across multiple hospitals.
"""
    )

    st.divider()

    st.image(
        "powerbi/images/z1.png",
        caption="Dashboard 1",
        use_container_width=True
    )

    st.image(
        "powerbi/images/z2.png",
        caption="Dashboard 2",
        use_container_width=True
    )

    st.image(
        "powerbi/images/z3.png",
        caption="Dashboard 3",
        use_container_width=True
    )

    st.image(
        "powerbi/images/z4.png",
        caption="Dashboard 4",
        use_container_width=True
    )
    st.image(
            "powerbi/images/z5.png",
            caption="Dashboard 5",
            use_container_width=True
        )

    st.divider()

    if st.button("🏠 Back to Home", use_container_width=True):

        st.session_state.page = "home"
        st.rerun()

def about_page():

    st.title("📖 About HealthOps AI")

    st.markdown("""
### 🏥 Problem Statement

Hospital readmissions place a significant burden on healthcare systems by increasing treatment costs, reducing resource availability, and affecting patient outcomes. Identifying patients at high risk of readmission can help healthcare providers plan timely interventions and improve the quality of care.

---

### 💡 Our Solution

HealthOps AI is an AI-powered Hospital Decision Support System that predicts the probability of 30-day patient readmission using Machine Learning. It also provides clinical recommendations and healthcare analytics through interactive dashboards.

---

### 📌 Project Overview

This project combines Artificial Intelligence, Machine Learning, SQL, Power BI and Streamlit to support data-driven healthcare decisions.

#### Target Variable

- **30-Day Hospital Readmission**
  - High Risk
  - Low Risk

---

### 📋 Features Used

- Patient Age
- Gender
- Admission Type
- Admission Date
- Primary Diagnosis Category
- Length of Stay
- Ward Type
- Insurance Type
- Total Diagnoses
- Estimated Treatment Cost
- Hospital Tier
- Hospital State
- Number of Beds
- Teaching Hospital Status

Along with multiple engineered features including:

- Cost Category
- Cost per Day
- Cost per Diagnosis
- Stay per Bed
- Diagnosis Density
- Seasonal Features
- Elderly Indicators
- Long Stay Indicators
- Diagnosis Category Flags

---

### ⚙️ Steps Performed

1. Data Cleaning & Preprocessing
2. Exploratory Data Analysis (EDA)
3. Feature Engineering
4. Machine Learning Model Development
5. Model Evaluation & Threshold Optimization
6. SQL-based Data Analysis
7. Power BI Dashboard Development
8. Streamlit Web Application

---

### 🛠️ Tools & Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- LightGBM
- Streamlit
- SQL
- Power BI
- Git & GitHub

---

### 👩‍🎓 Submitted By

**Gurleen Kaur**

B.Tech Electronics & Computer Engineering (2023–2027)

Guru Nanak Dev University

CGPA: **8.59** (Till 6th Semester)

---

### 💼 Skills

- Python
- Java
- SQL
- Machine Learning
- Artificial Intelligence
- Data Analytics
- Power BI
- Streamlit
- Git & GitHub
- IoT
- Motion Graphic Designing
""")

    st.markdown("### 🔗 Connect")

    st.markdown(
    "- **GitHub:** https://github.com/GurleenKaur00"
)

    st.markdown(
    "- **LinkedIn:** https://www.linkedin.com/in/gurleen-kaur-sandhu/"
)
    st.divider()

    if st.button("🏠 Back to Home", use_container_width=True):

        st.session_state.page = "home"
        st.rerun()

# ==========================================================
# ROUTER
# ==========================================================
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "about":
    about_page()

elif st.session_state.page == "doctor_login":
    doctor_login_page()

elif st.session_state.page == "doctor_dashboard":
    doctor_dashboard_page()

elif st.session_state.page == "prediction":
    prediction_page()

elif st.session_state.page == "recommendation":

    patient = st.session_state.patient_data
    prediction = st.session_state.prediction
    probability = st.session_state.probability

    st.title("💡 Clinical Recommendations")

    st.subheader("Prediction Summary")

    st.write(f"**Patient ID:** {patient['patient_id']}")
    st.write(f"**Hospital:** {patient['hospital_name']}")
    st.write(f"**Risk Probability:** {probability*100:.2f}%")

    st.divider()

    if prediction == 1:

        st.error("🔴 High Risk of Readmission")

        st.markdown("""
- Schedule follow-up within 7 days
- Review medications before discharge
- Provide discharge counselling
- Educate patient and family
- Monitor symptoms after discharge
""")

    else:

        st.success("🟢 Low Risk of Readmission")

        st.markdown("""
- Continue standard discharge process
- Routine follow-up
- Continue prescribed medication
- Maintain healthy lifestyle
""")

    st.divider()

    if st.button("🏠 Back to Home", use_container_width=True):

        st.session_state.page = "home"
        st.rerun()
elif st.session_state.page == "ministry_login":
    ministry_login_page()

elif st.session_state.page == "ministry_dashboard":
    ministry_dashboard_page()