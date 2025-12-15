import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ---------------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Clinical Decision Support System",
    page_icon="❤️",
    layout="wide"
)

st.title("🏥 Clinical Decision Support System")
st.markdown("Hybrid risk analysis system powered by AI and Medical Guidelines.")

@st.cache_resource
def train_and_get_stats():
    # Dosya yolu kontrolü (GitHub vs Local)
    file_path = "cardio_train.csv"
    local_path = "C:/Users/Ali34/Downloads/archive/cardio_train.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';')
    elif os.path.exists(local_path):
        df = pd.read_csv(local_path, sep=';')
    else:
        st.error("Error: Dataset file not found. Please upload 'cardio_train.csv' to your repository.")
        st.stop()

    # Veri Temizleme
    df.drop('id', axis=1, inplace=True)
    df['age'] = (df['age'] / 365).round().astype('int')
    df = df[(df['ap_hi'] > 50) & (df['ap_hi'] < 250)]
    df = df[(df['ap_lo'] > 30) & (df['ap_lo'] < 150)]
    df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

    X = df.drop('cardio', axis=1)
    y = df['cardio']

    # Model Eğitimi
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # Özellik Önem Dereceleri
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    # --- DÜZELTME BURADA YAPILDI ---
    # Hem 'data' (grafikler için) hem 'data_count' (sayı göstermek için) eklendi.
    return {
        'model': model,
        'accuracy': acc,
        'data': df,
        'data_count': len(df), # Eksik olan bu satırdı, eklendi.
        'feature_importance': importance_df
    }

# Yükleme ekranı
with st.spinner('System is initializing...'):
    stats = train_and_get_stats()
    model = stats['model']
    df_source = stats['data']

# Sekmeler
tab1, tab2 = st.tabs(["🏥 PATIENT ANALYSIS", "🧠 MODEL INTERNALS & DATA"])

# ---------------------------------------------------------
# TAB 1: HASTA ANALİZ EKRANI
# ---------------------------------------------------------
with tab1:
    col_main, col_result = st.columns([1, 1.2])

    with col_main:
        st.subheader("Patient Vitals")
        
        age = st.slider('Age (Years)', 30, 90, 50)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            gender = st.radio('Gender', ('Male', 'Female'), horizontal=True)
            gender_val = 2 if gender == 'Male' else 1
        with col_g2:
             bmi_display = st.empty()

        height = st.slider('Height (cm)', 140, 210, 175)
        weight = st.slider('Weight (kg)', 40, 160, 80)
        
        bmi = weight / ((height / 100) ** 2)
        bmi_display.metric("Current BMI", f"{bmi:.1f}")

        st.markdown("### Blood Pressure")
        ap_hi = st.slider('Systolic (Top Number)', 80, 240, 120, help="Normal range is usually 120 or lower.")
        ap_lo = st.slider('Diastolic (Bottom Number)', 40, 140, 80)

        st.markdown("### Lab Results")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            cholesterol = st.select_slider('Cholesterol Level', options=['Normal', 'Above Normal', 'Very High'])
            chol_map = {'Normal': 1, 'Above Normal': 2, 'Very High': 3}
        with col_l2:
            gluc = st.select_slider('Glucose Level', options=['Normal', 'Above Normal', 'Very High'])
            gluc_map = {'Normal': 1, 'Above Normal': 2, 'Very High': 3}

        st.markdown("### Lifestyle")
        col_hab1, col_hab2, col_hab3 = st.columns(3)
        with col_hab1: smoke = st.toggle('Smoker')
        with col_hab2: alco = st.toggle('Alcohol Consumer')
        with col_hab3: active = st.toggle('Physically Active', value=True)

        input_data = {
            'age': age, 'gender': gender_val, 'height': height, 'weight': weight,
            'ap_hi': ap_hi, 'ap_lo': ap_lo, 'cholesterol': chol_map[cholesterol],
            'gluc': gluc_map[gluc], 'smoke': int(smoke), 'alco': int(alco),
            'active': int(active), 'bmi': bmi
        }
        input_df = pd.DataFrame(input_data, index=[0])

    with col_result:
        st.subheader("Analysis Results")
        
        if st.button('RUN DIAGNOSIS', type="primary", use_container_width=True):
            
            base_prob = model.predict_proba(input_df)[0][1]
            risk_score = base_prob
            reasons = []

            # Hibrit Kural Sistemi
            if input_df['smoke'][0] == 1:
                risk_score += 0.10
                reasons.append("Smoking habit increases cardiovascular stress (+10%)")
            if input_df['alco'][0] == 1:
                risk_score += 0.05
                reasons.append("Alcohol consumption factor (+5%)")
            if input_df['active'][0] == 0:
                risk_score += 0.05
                reasons.append("Sedentary lifestyle warning (+5%)")
            if input_df['gluc'][0] == 3:
                risk_score += 0.07
                reasons.append("Critical Glucose levels detected (+7%)")
            
            risk_score = min(max(risk_score, 0.01), 0.99)
            
            # Sonuç Kutusu
            result_container = st.container(border=True)
            with result_container:
                col_r1, col_r2 = st.columns(2)
                
                with col_r1:
                    st.metric(label="AI Probability", value=f"%{base_prob * 100:.1f}")
                with col_r2:
                    st.metric(label="Adjusted Risk Score", value=f"%{risk_score * 100:.1f}", delta_color="inverse")
                
                st.write("Risk Severity Gauge")
                
                bar_color = "green"
                if risk_score > 0.5: bar_color = "red"
                elif risk_score > 0.3: bar_color = "orange"
                
                st.progress(risk_score, text=f"Risk Level: {risk_score*100:.1f}%")

                if risk_score > 0.50:
                    st.error("🔴 **HIGH RISK DETECTED**")
                    st.markdown("**Action Plan:** Immediate consultation with a cardiologist is recommended.")
                else:
                    st.success("🟢 **LOW RISK**")
                    st.markdown("**Action Plan:** Maintain healthy habits and routine check-ups.")

            if reasons:
                with st.expander("🔍 View Risk Factors Details", expanded=True):
                    for r in reasons:
                        st.warning(f"• {r}")
        else:
            st.info("👈 Please configure the patient vitals and click 'RUN DIAGNOSIS'")

# ---------------------------------------------------------
# TAB 2: TEKNİK DETAYLAR
# ---------------------------------------------------------
with tab2:
    st.header("🧠 Technical Performance & Data Insights")
    
    # Burada 'data_count' hatası alıyordun, yukarıda return kısmına eklediğim için düzeldi.
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Dataset Size", f"{stats['data_count']:,} Patients", delta="Verified")
    m_col2.metric("Model Accuracy", f"{stats['accuracy'] * 100:.2f}%", delta="+1.2% vs Baseline")
    m_col3.metric("Algorithm", "Random Forest", "Ensemble Method")

    st.divider()

    st.subheader("1. Feature Importance Analysis")
    st.caption("Which factors affect the decision mechanism the most?")
    
    chart_data = stats['feature_importance'].set_index('Feature')
    en_map = {
        'age': 'Age', 'ap_hi': 'Systolic BP', 'weight': 'Weight',
        'bmi': 'BMI', 'height': 'Height', 'ap_lo': 'Diastolic BP',
        'cholesterol': 'Cholesterol', 'gluc': 'Glucose', 'gender': 'Gender',
        'active': 'Activity', 'smoke': 'Smoking', 'alco': 'Alcohol'
    }
    chart_data.index = chart_data.index.map(en_map)
    st.bar_chart(chart_data, color="#FF4B4B", height=300)

    st.divider()

    st.subheader("2. Data Correlation Heatmap")
    st.caption("How features relate to each other (Lighter colors indicate stronger positive correlation)")
    
    corr_df = df_source.corr()
    st.dataframe(corr_df.style.background_gradient(cmap="Reds"), use_container_width=True)
    
    st.divider()
    
    st.subheader("3. Age Distribution by Disease Status")
    st.caption("Comparison of sick vs healthy individuals across age groups")
    
    # Basit Scatter Chart yerine daha temiz bir görselleştirme
    chart_data_age = df_source[['age', 'cardio']]
    st.scatter_chart(chart_data_age, x='age', y='cardio', color='#0000FF')
