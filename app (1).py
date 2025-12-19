import streamlit as st
import plotly.graph_objects as go


st.set_page_config(
    page_title="Cardio AI - Clinical Decision Support",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    
    div[data-testid="metric-container"] label {
        color: #555555 !important;
        font-weight: 500;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 700;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    h1, h2, h3 {
        color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 4px;
        color: white;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ef4444;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


def calculate_cardiovascular_risk(age, gender, height, weight, systolic, diastolic, 
                                  cholesterol, glucose, smoke, alcohol, active):
    bmi = weight / ((height / 100) ** 2)
    risk_score = 0.0
    reasons = []
    
    if age > 60:
        risk_score += 0.25
        reasons.append("Age >60 (+25%)")
    elif age > 50:
        risk_score += 0.15
        reasons.append("Age >50 (+15%)")
    elif age > 40:
        risk_score += 0.08
        reasons.append("Age >40 (+8%)")
    
    systolic_risk = 0
    diastolic_risk = 0
    
    if systolic >= 180:
        systolic_risk = 0.30
        reasons.append("⚠️ Critical Systolic BP ≥180 (+30%)")
    elif systolic >= 160:
        systolic_risk = 0.25
        reasons.append("Severe Systolic BP ≥160 (+25%)")
    elif systolic >= 140:
        systolic_risk = 0.18
        reasons.append("Stage 2 Systolic BP ≥140 (+18%)")
    elif systolic >= 130:
        systolic_risk = 0.10
        reasons.append("Stage 1 Systolic BP ≥130 (+10%)")
    elif systolic >= 120:
        systolic_risk = 0.05
        reasons.append("Elevated Systolic BP ≥120 (+5%)")
    
    if diastolic >= 110:
        diastolic_risk = 0.28
        reasons.append("⚠️ Critical Diastolic BP ≥110 (+28%)")
    elif diastolic >= 100:
        diastolic_risk = 0.22
        reasons.append("Severe Diastolic BP ≥100 (+22%)")
    elif diastolic >= 90:
        diastolic_risk = 0.16
        reasons.append("Stage 2 Diastolic BP ≥90 (+16%)")
    elif diastolic >= 85:
        diastolic_risk = 0.09
        reasons.append("Stage 1 Diastolic BP ≥85 (+9%)")
    elif diastolic >= 80:
        diastolic_risk = 0.04
        reasons.append("Elevated Diastolic BP ≥80 (+4%)")
    
    risk_score += systolic_risk + diastolic_risk
    
    if systolic_risk >= 0.18 and diastolic_risk >= 0.16:
        risk_score += 0.10
        reasons.append("⚠️ Both BP Values Critical (+10%)")
    
    if bmi >= 35:
        risk_score += 0.20
        reasons.append("Severe Obesity BMI ≥35 (+20%)")
    elif bmi >= 30:
        risk_score += 0.15
        reasons.append("Obesity BMI ≥30 (+15%)")
    elif bmi >= 25:
        risk_score += 0.08
        reasons.append("Overweight BMI ≥25 (+8%)")
    
    if cholesterol == 'Very High':
        risk_score += 0.18
        reasons.append("Very High Cholesterol (+18%)")
    elif cholesterol == 'Above Normal':
        risk_score += 0.10
        reasons.append("Above Normal Cholesterol (+10%)")
    
    if glucose == 'Very High':
        risk_score += 0.16
        reasons.append("Very High Glucose (+16%)")
    elif glucose == 'Above Normal':
        risk_score += 0.09
        reasons.append("Above Normal Glucose (+9%)")
    
    if smoke:
        risk_score += 0.20
        reasons.append("⚠️ Smoking (+20%)")
    
    if alcohol:
        risk_score += 0.10
        reasons.append("⚠️ Alcohol Use (+10%)")
    
    if not active:
        risk_score += 0.12
        reasons.append("⚠️ Physical Inactivity (+12%)")
    
    if gender == 'Male':
        risk_score += 0.05
        reasons.append("Male Gender (+5%)")
    
    risk_score = min(max(risk_score, 0.01), 0.99)
    
    if risk_score > 0.70:
        risk_level = 'CRITICAL'
        risk_color = 'darkred'
    elif risk_score > 0.50:
        risk_level = 'SEVERE'
        risk_color = 'red'
    elif risk_score > 0.35:
        risk_level = 'HIGH'
        risk_color = 'orange'
    elif risk_score > 0.20:
        risk_level = 'MODERATE'
        risk_color = 'yellow'
    else:
        risk_level = 'LOW'
        risk_color = 'green'
    
    return {
        'score': risk_score,
        'percentage': risk_score * 100,
        'bmi': bmi,
        'reasons': reasons,
        'risk_level': risk_level,
        'risk_color': risk_color
    }


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=70)
    st.title("Patient Data")
    st.markdown("Enter clinical details below.")
    st.markdown("---")
    
    st.subheader("📋 Demographics")
    age = st.slider('Age', 30, 90, 50)
    gender = st.radio('Gender', ('Male', 'Female'), horizontal=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        height = st.number_input('Height (cm)', 140, 210, 175)
    with col_s2:
        weight = st.number_input('Weight (kg)', 40, 160, 80)
    
    st.markdown("---")
    
    st.subheader("🩺 Clinical Vitals")
    systolic = st.slider('Systolic BP (High)', 80, 240, 120)
    diastolic = st.slider('Diastolic BP (Low)', 40, 140, 80)
    
    cholesterol = st.selectbox('Cholesterol', ['Normal', 'Above Normal', 'Very High'])
    glucose = st.selectbox('Glucose', ['Normal', 'Above Normal', 'Very High'])
    
    st.markdown("---")
    
    st.subheader("🚬 Lifestyle")
    smoke = st.checkbox('Smoker', value=False)
    alcohol = st.checkbox('Alcohol', value=False)
    active = st.checkbox('Active Sport', value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    calculate_btn = st.button('🚀 START ANALYSIS', type="primary", use_container_width=True)


st.title("🥼 Clinical Decision Support System")
st.markdown("**AI Engine Status:** ✅ Online (Enhanced Risk Model v2)")


bmi = weight / ((height / 100) ** 2)


col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1:
    st.metric(label="BMI Score", value=f"{bmi:.1f}")
with col_k2:
    st.metric(label="Blood Pressure", value=f"{systolic}/{diastolic}")
with col_k3:
    st.metric(label="Patient Age", value=f"{age}")
with col_k4:
    metabolic_risk = "Elevated" if (cholesterol != 'Normal' or glucose != 'Normal') else "Normal"
    st.metric(label="Metabolic Risk", value=metabolic_risk)

st.divider()


if calculate_btn:
    with st.spinner("Processing clinical data..."):
        result = calculate_cardiovascular_risk(
            age, gender, height, weight, systolic, diastolic,
            cholesterol, glucose, smoke, alcohol, active
        )
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result['percentage'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Cardiovascular Risk Probability", 'font': {'size': 24, 'color': "white"}},
        number={'suffix': "%", 'font': {'size': 48, 'color': "white"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "white"},
            'bar': {'color': result['risk_color']},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': '#1b4332'},
                {'range': [20, 35], 'color': '#52b788'},
                {'range': [35, 50], 'color': '#fbbf24'},
                {'range': [50, 70], 'color': '#f97316'},
                {'range': [70, 100], 'color': '#dc2626'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': result['percentage']
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=400,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    res_col1, res_col2 = st.columns([1.2, 1])
    
    with res_col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with res_col2:
        st.subheader("Analysis Conclusion")
        
        if result['risk_level'] == 'CRITICAL':
            st.error(f"🔴 **{result['risk_level']} RISK - EMERGENCY**")
            st.markdown(f"""
            <div style='background-color: #3b1e1e; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #dc2626; color: #ffcccc;'>
                <p style='margin: 0 0 15px 0;'>
                    Patient requires immediate medical attention.
                </p>
                <p style='margin: 10px 0 5px 0; font-weight: bold;'>Immediate Action Required:</p>
                <p style='margin: 5px 0;'>• Emergency Cardiology Consultation</p>
                <p style='margin: 5px 0;'>• Hospitalization May Be Required</p>
                <p style='margin: 5px 0;'>• Full Cardiac Workup</p>
                <p style='margin: 5px 0;'>• Immediate Medication Initiation</p>
            </div>
            """, unsafe_allow_html=True)
        elif result['risk_level'] == 'SEVERE':
            st.error(f"🔴 **{result['risk_level']} RISK - URGENT**")
            st.markdown(f"""
            <div style='background-color: #3b1e1e; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #ef4444; color: #ffcccc;'>
                <p style='margin: 0 0 15px 0;'>
                    Patient has multiple critical risk factors.
                </p>
                <p style='margin: 10px 0 5px 0; font-weight: bold;'>Urgent Action Required:</p>
                <p style='margin: 5px 0;'>• Cardiology Referral Within 48 Hours</p>
                <p style='margin: 5px 0;'>• Comprehensive Blood Work</p>
                <p style='margin: 5px 0;'>• ECG and Stress Test</p>
                <p style='margin: 5px 0;'>• Aggressive Lifestyle Changes</p>
            </div>
            """, unsafe_allow_html=True)
        elif result['risk_level'] == 'HIGH':
            st.warning(f"🟠 **{result['risk_level']} RISK**")
            st.markdown(f"""
            <div style='background-color: #3b2e1e; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #f97316; color: #fde68a;'>
                <p style='margin: 0 0 15px 0;'>
                    Patient shows significant cardiovascular risk indicators.
                </p>
                <p style='margin: 10px 0 5px 0; font-weight: bold;'>Recommended Action:</p>
                <p style='margin: 5px 0;'>• Cardiology Consultation Advised</p>
                <p style='margin: 5px 0;'>• Full Blood Panel Required</p>
                <p style='margin: 5px 0;'>• Lifestyle Modification Program</p>
                <p style='margin: 5px 0;'>• Monthly Follow-up</p>
            </div>
            """, unsafe_allow_html=True)
        elif result['risk_level'] == 'MODERATE':
            st.warning(f"🟡 **{result['risk_level']} RISK**")
            st.markdown(f"""
            <div style='background-color: #3b2e1e; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #fbbf24; color: #fde68a;'>
                <p style='margin: 0 0 15px 0;'>
                    Patient has some risk factors that should be addressed.
                </p>
                <p style='margin: 10px 0 5px 0; font-weight: bold;'>Recommended Action:</p>
                <p style='margin: 5px 0;'>• Follow-up in 3-6 months</p>
                <p style='margin: 5px 0;'>• Lifestyle Modification Program</p>
                <p style='margin: 5px 0;'>• Regular Monitoring</p>
                <p style='margin: 5px 0;'>• Diet and Exercise Plan</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"🟢 **{result['risk_level']} RISK / HEALTHY**")
            st.markdown(f"""
            <div style='background-color: #1e3b26; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #22c55e; color: #ccffdd;'>
                <p style='margin: 0 0 15px 0;'>
                    Patient's values are within healthy range.
                </p>
                <p style='margin: 10px 0 5px 0; font-weight: bold;'>Recommended Action:</p>
                <p style='margin: 5px 0;'>• Routine Annual Check-up</p>
                <p style='margin: 5px 0;'>• Maintain Healthy Diet</p>
                <p style='margin: 5px 0;'>• Regular Exercise</p>
                <p style='margin: 5px 0;'>• Continue Healthy Habits</p>
            </div>
            """, unsafe_allow_html=True)
        
        if result['reasons']:
            st.markdown("---")
            st.markdown("**🔍 Risk Contributors:**")
            for reason in result['reasons']:
                st.write(f"• {reason}")

else:
    st.info("👈 Please enter patient data in the sidebar and click 'START ANALYSIS'.")


st.markdown("---")
with st.expander("🧠 Technical Details & Risk Model Information"):
    st.markdown("""
    ### Enhanced Risk Calculation Model v2
    
    **Blood Pressure Risk (Separate Assessment):**
    
    Systolic:
    - ≥180: +30% (Critical)
    - ≥160: +25% (Severe)
    - ≥140: +18% (Stage 2)
    - ≥130: +10% (Stage 1)
    - ≥120: +5% (Elevated)
    
    Diastolic:
    - ≥110: +28% (Critical)
    - ≥100: +22% (Severe)
    - ≥90: +16% (Stage 2)
    - ≥85: +9% (Stage 1)
    - ≥80: +4% (Elevated)
    
    **Combination Bonus:**
    - Both systolic and diastolic in critical range: +10% additional
    
    **Other Major Risk Factors:**
    - 🚬 Smoking: +20%
    - 👴 Age >60: +25%
    - ⚖️ Severe Obesity (BMI ≥35): +20%
    - 📊 Very High Cholesterol: +18%
    - � Very High Glucose: +16%
    - ⚖️ Obesity (BMI ≥30): +15%
    - 🛋️ Physical Inactivity: +12%
    - � Alcohol Use: +10%
    
    **Risk Level Classification:**
    - 🟢 LOW: 0-20% - Routine care
    - 🟡 MODERATE: 20-35% - Lifestyle changes
    - 🟠 HIGH: 35-50% - Medical intervention
    - 🔴 SEVERE: 50-70% - Urgent care
    - 🔴 CRITICAL: 70%+ - Emergency attention
    
    **Model Improvements v2:**
    - ✅ Separate systolic and diastolic assessment
    - ✅ More granular BP risk levels
    - ✅ Combination bonus for dual critical BP
    - ✅ 5-level risk classification
    - ✅ Higher weights for critical values
    """)
    
    st.markdown("---")
    st.markdown("**Note:** This tool is for educational purposes. Always consult healthcare professionals for medical decisions.")
