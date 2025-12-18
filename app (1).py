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
    
    /* Metric containers */
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
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
    }
    
    /* Tabs */
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
    """
    Calculates cardiovascular risk with proper weighting for lifestyle factors
    """
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
    
    
    if systolic >= 140 or diastolic >= 90:
        risk_score += 0.22
        reasons.append("Hypertension Stage 2 (+22%)")
    elif systolic >= 130 or diastolic >= 85:
        risk_score += 0.12
        reasons.append("Elevated BP (+12%)")
    elif systolic >= 120 or diastolic >= 80:
        risk_score += 0.05
        reasons.append("Prehypertension (+5%)")
    
   
    if bmi >= 30:
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
    
  
    if risk_score > 0.60:
        risk_level = 'CRITICAL'
        risk_color = 'red'
    elif risk_score > 0.40:
        risk_level = 'HIGH'
        risk_color = 'orange'
    elif risk_score > 0.25:
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
st.markdown("**AI Engine Status:** ✅ Online (Improved Risk Model)")


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
                {'range': [0, 25], 'color': '#1b4332'},    # Dark Green
                {'range': [25, 40], 'color': '#52b788'},   # Light Green
                {'range': [40, 60], 'color': '#fbbf24'},   # Yellow
                {'range': [60, 75], 'color': '#f97316'},   # Orange
                {'range': [75, 100], 'color': '#dc2626'}   # Red
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
        
        if result['risk_level'] in ['CRITICAL', 'HIGH']:
            st.error(f"🔴 **{result['risk_level']} RISK DETECTED**")
            st.markdown(f"""
            <div style='background-color: #3b1e1e; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #dc2626; color: #ffcccc;'>
                <p style='margin: 0 0 15px 0;'>
                    The patient shows strong indicators of cardiovascular disease.
                </p>
                <p style='margin: 10px 0 5px 0; font-weight: bold;'>Recommended Action:</p>
                <p style='margin: 5px 0;'>• Urgent Cardiology Referral</p>
                <p style='margin: 5px 0;'>• Full Blood Panel Required</p>
                <p style='margin: 5px 0;'>• Immediate Lifestyle Intervention</p>
                <p style='margin: 5px 0;'>• Consider Medication Review</p>
            </div>
            """, unsafe_allow_html=True)
        elif result['risk_level'] == 'MODERATE':
            st.warning(f"🟡 **{result['risk_level']} RISK**")
            st.markdown(f"""
            <div style='background-color: #3b2e1e; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #fbbf24; color: #fde68a;'>
                <p style='margin: 0 0 15px 0;'>
                    The patient has some risk factors that should be addressed.
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
                    The patient's values are within the manageable range.
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
    ### Improved Risk Calculation Model
    
    This version uses evidence-based risk weighting:
    
    **Major Risk Factors:**
    - 🚬 **Smoking**: +20% (Leading preventable cause)
    - 🩸 **Hypertension (Stage 2)**: +22% (BP ≥140/90)
    - 👴 **Age >60**: +25% (Natural aging effect)
    
    **Significant Risk Factors:**
    - 📊 **Very High Cholesterol**: +18%
    - 🍬 **Very High Glucose**: +16%
    - ⚖️ **Obesity (BMI ≥30)**: +15%
    - 🍺 **Alcohol Use**: +10%
    
    **Moderate Risk Factors:**
    - 🛋️ **Physical Inactivity**: +12%
    - 📈 **Above Normal Cholesterol**: +10%
    - 🍬 **Above Normal Glucose**: +9%
    - ⚖️ **Overweight (BMI ≥25)**: +8%
    
    **Model Improvements:**
    - ✅ Lifestyle factors (smoking, alcohol, exercise) now properly weighted
    - ✅ Clinically accurate BP thresholds (140/90 for Stage 2)
    - ✅ Cumulative risk calculation (factors add up realistically)
    - ✅ Risk capped at 99% to avoid unrealistic predictions
    
    **Risk Level Classification:**
    - 🟢 **LOW**: 0-25% - Routine care recommended
    - 🟡 **MODERATE**: 25-40% - Lifestyle changes needed
    - 🟠 **HIGH**: 40-60% - Medical intervention advised
    - 🔴 **CRITICAL**: 60%+ - Urgent cardiology referral
    """)
    
    st.markdown("---")
    st.markdown("**Note:** This tool is for educational purposes. Always consult healthcare professionals for medical decisions.")

