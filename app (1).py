import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# ---------------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Klinik Karar Destek Sistemi",
    page_icon="❤️",
    layout="wide"
)

st.title("🏥 Clinical Decision System")
st.markdown("Yapay Zeka ve Tıbbi Kuralların birleşimiyle çalışan hibrit risk analiz sistemi Hybrid analysis system.")

@st.cache_resource
def train_and_get_stats():
    # Dosya okuma işlemi: Hem local hem cloud uyumlu olması için düzenlendi
    # Eğer dosya GitHub'da app.py ile aynı klasördeyse direkt ismini yazarız.
    file_path = "cardio_train.csv" 
    
    # Eğer bilgisayarındaki local yol hala lazımsa, onu da alternatif olarak ekliyorum:
    local_path = "archive/cardio_train.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep=';')
    elif os.path.exists(local_path):
        df = pd.read_csv(local_path, sep=';')
    else:
        st.error("Hata: Veri seti bulunamadı. Lütfen 'cardio_train.csv' dosyasını GitHub reponuza yüklediğinizden emin olun.")
        st.stop()

    df.drop('id', axis=1, inplace=True)
    df['age'] = (df['age'] / 365).round().astype('int')
    df = df[(df['ap_hi'] > 50) & (df['ap_hi'] < 250)]
    df = df[(df['ap_lo'] > 30) & (df['ap_lo'] < 150)]

    df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

    X = df.drop('cardio', axis=1)
    y = df['cardio']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    # --- HATA DÜZELTİLDİ: Boşluk hatası giderildi ---
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Effect (importance Degree)': model.feature_importances_
    }).sort_values(by='Effect (importance Degree)', ascending=False)
    # -----------------------------------------------

    # İstatistikleri bir sözlük olarak döndür
    return {
        'model': model,
        'accuracy': acc,
        'data_count': len(df),
        'feature_importance': importance_df
    }

with st.spinner('Training the model and calculating the statistics...'):
    stats = train_and_get_stats()
    model = stats['model']

tab1, tab2 = st.tabs(["🏥 RİSK Analysis (Doctor Screen)", "🧠 MODEL DETAILS & TRAINING"])

with tab1:
    col_input, col_result = st.columns([1, 1.5])

    with col_input:
        st.subheader("Patient Information")
        age = st.slider('Age', 30, 90, 50)
        gender = st.radio('Gender', ('Male', 'Female'), horizontal=True)
        gender_val = 2 if gender == 'Male' else 1

        height = st.slider('Height (cm)', 140, 210, 175)
        weight = st.slider('Weight (kg)', 40, 160, 80)

        st.markdown("---")
        col_t1, col_t2 = st.columns(2)
        with col_t1: ap_hi = st.number_input('systolic blood pressure', 80, 240, 120)
        with col_t2: ap_lo = st.number_input('Diastolic Blood Pressure', 40, 140, 80)

        cholesterol = st.selectbox('Cholesterol', ['Normal', 'Above Normal', 'Very High'])
        chol_map = {'Normal': 1, 'Above Normal': 2, 'Very High': 3}

        gluc = st.selectbox('Glucose ', ['Normal', 'Above Normal', 'Very High'])
        gluc_map = {'Normal': 1, 'Above Normal': 2, 'Very High': 3}

        st.markdown("---")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1: smoke = st.checkbox('Smoke')
        with col_c2: alco = st.checkbox('Alcohol')
        with col_c3: active = st.checkbox('Sport')

        bmi = weight / ((height / 100) ** 2)

        # DataFrame Hazırlığı
        input_data = {
            'age': age, 'gender': gender_val, 'height': height, 'weight': weight,
            'ap_hi': ap_hi, 'ap_lo': ap_lo, 'cholesterol': chol_map[cholesterol],
            'gluc': gluc_map[gluc], 'smoke': int(smoke), 'alco': int(alco),
            'active': int(active), 'bmi': bmi
        }
        input_df = pd.DataFrame(input_data, index=[0])

    with col_result:
        st.subheader("analysis Result")
        st.info(f"**Calculated BMI:** {bmi:.1f}")

        if st.button('Calculate the Risk', type="primary"):

            base_prob = model.predict_proba(input_df)[0][1]
            risk_score = base_prob
            reasons = []

            if input_df['smoke'][0] == 1:
                risk_score += 0.10
                reasons.append("Smoking (+%10 Risk)")
            if input_df['alco'][0] == 1:
                risk_score += 0.05
                reasons.append("Alcohol usage (+%5 Risk)")
            if input_df['active'][0] == 0:
                risk_score += 0.05
                reasons.append("inactive lifestyle (+%5 Risk)")
            if input_df['gluc'][0] == 3:
                risk_score += 0.07
                reasons.append("high Glucose/Diabetes (+%7 Risk)")

            risk_score = min(max(risk_score, 0.01), 0.99)

            # GÖRSELLEŞTİRME
            st.write("---")
            if risk_score > 0.50:
                st.error(f"🔴 HIGH RISK: %{risk_score * 100:.1f}")
                st.metric(label="Raw Prediction of Artificial Intelligence", value=f"%{base_prob * 100:.1f}")
                if reasons:
                    st.warning("⚠️ Risk-Increasing Factors:")
                    for r in reasons: st.write(f"- {r}")
                st.write("👉 **Recommendation:** Referral to cardiology is recommended..")
            else:
                st.success(f"🟢 LOW RISK: %{risk_score * 100:.1f}")
                st.metric(label="Raw Prediction of Artificial Intelligence", value=f"%{base_prob * 100:.1f}")
                if reasons:
                    st.info("💡 Things to consider:")
                    for r in reasons: st.write(f"- {r}")
                st.write("👉 **Suggestion: Routine check-up.")

with tab2:
    st.header("🧠 Technical Details of AI")
    st.markdown("In this tab, you can see the statistics behind the decision-making system..")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="The used Dataset", value=f"{stats['data_count']:,} Patient")
        st.caption("Data Set:: Cardiovascular Disease Dataset")

    with col2:
        st.metric(label="Model Accuracy ", value=f"%{stats['accuracy'] * 100:.2f}")
        st.caption("Success rate on test data")

    with col3:
        st.metric(label="Used Algorithm", value="Random Forest")
        st.caption("Ensemble Learning")

    st.divider()

    st.subheader("📊 How much weight does AI give to specific features when making a decision?")
    st.markdown(
        "The following graph illustrates the feature importance for the model's prediction of whether a patient is 'Sick' or 'Healthy'.")

    chart_data = stats['feature_importance'].set_index('Feature')

    en_map = {
        'age': 'Age', 'ap_hi': 'high blood pressure', 'weight': 'Weight',
        'bmi': 'Vücut Kitle İndeksi', 'height': 'Boy', 'ap_lo': 'Low blood pressure',
        'cholesterol': 'Cholosterol', 'gluc': 'Glucose', 'gender': 'Gender',
        'active': 'Active', 'smoke': 'Smoke', 'alco': 'Alcohol'
    }
    chart_data.index = chart_data.index.map(en_map)

    st.bar_chart(chart_data, color="#FF4B4B")

    st.info("""
    **Chart Analysis: The longer the bar, the more decisive the criterion is for the diagnosis. 
    Generally, 'Systolic Blood Pressure' and 'Age' appear as the dominant predictors..
    The low ranking of Smoking and Alcohol in the graph stems from data inconsistencies, which justifies our use of a hybrid rule system.
    """)
