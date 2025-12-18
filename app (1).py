import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# ---------------------------------------------------------
# 1. SAYFA KONFİGÜRASYONU
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cardio AI - Pro Decision Support",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. ÖZEL CSS (PROFESYONEL GÖRÜNÜM)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Metrik Kutuları */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        color: #000000;
    }
    div[data-testid="metric-container"] label { color: #555555 !important; font-weight: 500; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 700; }
    
    /* Sekmeler */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1c2026; border-radius: 4px; color: white; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; }
    
    /* Uyarı Kutuları */
    .risk-box { padding: 15px; border-radius: 5px; margin-top: 10px; }
    .risk-high { background-color: #3b1e1e; color: #ffcccc; border-left: 5px solid #ff4b4b; }
    .risk-low { background-color: #1e3b26; color: #ccffdd; border-left: 5px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. VERİ YÜKLEME VE MODEL EĞİTİMİ (DÜZELTİLMİŞ)
# ---------------------------------------------------------
@st.cache_resource
def train_model():
    # --- DOSYA YOLU AYARI ---
    # Dosyanın app.py ile aynı klasörde olduğunu varsayıyoruz.
    # Eğer farklıysa burayı tam yol ile değiştirin (Örn: "C:/Data/cardio_train.csv")
    file_path = "cardio_train.csv" 
    
    # Dosya Kontrolü
    if not os.path.exists(file_path):
        st.error(f"HATA: '{file_path}' dosyası bulunamadı! Lütfen CSV dosyasını proje klasörüne ekleyin.")
        st.stop() # Kod çalışmayı durdurur, rastgele veri üretmez.

    df = pd.read_csv(file_path, sep=';')

    # --- VERİ TEMİZLİĞİ (OUTLIER REMOVAL) ---
    # Mantıksız verileri atıyoruz (Modelin kafasını karıştıranlar)
    df = df[(df['ap_hi'] >= 50) & (df['ap_hi'] <= 250)]     # Tansiyon 5-25 arası (veya 50-250)
    df = df[(df['ap_lo'] >= 30) & (df['ap_lo'] <= 150)]
    df = df[(df['height'] >= 140) & (df['height'] <= 250)]  # Boy 140cm altı yetişkin azdır
    df = df[(df['weight'] >= 40)]
    
    # Yaş dönüşümü (Gün -> Yıl)
    if df['age'].mean() > 150:
        df['age'] = (df['age'] / 365).round().astype('int')

    # BMI Özelliği Ekleme
    df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

    # Model Hazırlığı
    X = df.drop(['cardio', 'id'], axis=1, errors='ignore')
    y = df['cardio']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- GÜÇLENDİRİLMİŞ MODEL ---
    # Daha fazla ağaç, derinlik sınırı (ezberlemeyi önler)
    model = RandomForestClassifier(
        n_estimators=200, 
        max_depth=10, 
        min_samples_leaf=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))

    feature_imp = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    return model, acc, len(df), feature_imp

# Modeli Yükle
try:
    model, accuracy, data_count, feature_imp = train_model()
except Exception as e:
    st.error(f"Model yüklenirken kritik hata: {e}")
    st.stop()

# ---------------------------------------------------------
# 4. SIDEBAR - VERİ GİRİŞİ
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=70)
    st.title("Patient Vitals")
    st.markdown("---")

    # Demografik
    st.subheader("📋 Demographics")
    age = st.slider('Age', 30, 90, 50)
    gender = st.radio('Gender', ('Male', 'Female'), horizontal=True)
    gender_val = 2 if gender == 'Male' else 1
    
    c1, c2 = st.columns(2)
    height = c1.number_input('Height (cm)', 140, 220, 175)
    weight = c2.number_input('Weight (kg)', 40, 180, 80)

    st.markdown("---")

    # Klinik
    st.subheader("🩺 Clinical Data")
    ap_hi = st.slider('Systolic BP (High)', 80, 220, 120, help="Normal: 120 mmHg")
    ap_lo = st.slider('Diastolic BP (Low)', 40, 140, 80, help="Normal: 80 mmHg")
    
    chol = st.selectbox('Cholesterol', ['Normal', 'Above Normal', 'Very High'])
    chol_map = {'Normal': 1, 'Above Normal': 2, 'Very High': 3}
    
    gluc = st.selectbox('Glucose', ['Normal', 'Above Normal', 'Very High'])
    gluc_map = {'Normal': 1, 'Above Normal': 2, 'Very High': 3}

    st.markdown("---")

    # Yaşam Tarzı
    st.subheader("🚬 Lifestyle")
    smoke = st.toggle('Smoker', value=False)
    alco = st.toggle('Alcohol Intake', value=False)
    active = st.toggle('Physical Activity', value=True)

    # Hesaplamalar
    bmi = weight / ((height/100)**2)
    
    input_data = pd.DataFrame({
        'age': [age], 'gender': [gender_val], 'height': [height], 'weight': [weight],
        'ap_hi': [ap_hi], 'ap_lo': [ap_lo], 'cholesterol': [chol_map[chol]],
        'gluc': [gluc_map[gluc]], 'smoke': [int(smoke)], 'alco': [int(alco)],
        'active': [int(active)], 'bmi': [bmi]
    })

    st.markdown("<br>", unsafe_allow_html=True)
    btn = st.button('🚀 RUN ANALYSIS', type="primary", use_container_width=True)

# ---------------------------------------------------------
# 5. ANA EKRAN VE HİBRİT MANTIK
# ---------------------------------------------------------
st.title("🏥 Clinical Decision Support System")
st.caption(f"Model Accuracy: {accuracy:.1%} | Training Data: {data_count:,} patients")

tab1, tab2 = st.tabs(["📄 DIAGNOSIS REPORT", "🧠 AI BLACK BOX"])

with tab1:
    # Üst Bilgi Kartları
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("BMI Index", f"{bmi:.1f}", delta="Obese" if bmi>30 else "Normal", delta_color="inverse")
    k2.metric("Blood Pressure", f"{ap_hi}/{ap_lo}")
    k3.metric("Age Group", f"{age}")
    k4.metric("Risk Factors", f"{chol_map[chol] + gluc_map[gluc] - 2} Elevated")
    
    st.divider()

    if btn:
        with st.spinner("Analyzing parameters..."):
            
            # --- ADIM 1: YAPAY ZEKA SKORU (%70 Ağırlık) ---
            ai_prob = model.predict_proba(input_data)[0][1]
            
            # --- ADIM 2: KURAL TABANLI SKOR (%30 Ağırlık) ---
            # Modelin veri setinde göremediği yaşam tarzı risklerini ekliyoruz
            rule_score = 0
            risk_reasons = []
            
            # Sigara ve Alkol veride zayıf olsa da tıbbi olarak risktir
            if smoke: 
                rule_score += 0.25
                risk_reasons.append("Smoking")
            if alco: 
                rule_score += 0.10
                risk_reasons.append("Alcohol")
            if not active: 
                rule_score += 0.15
                risk_reasons.append("Inactivity")
            if chol_map[chol] == 3: 
                rule_score += 0.20
                risk_reasons.append("High Cholesterol")
            if gluc_map[gluc] == 3:
                rule_score += 0.20
                risk_reasons.append("High Glucose")
            if bmi > 30:
                rule_score += 0.10
                risk_reasons.append("Obesity (BMI > 30)")
            
            # Kural skorunu 0-1 arasına sıkıştır
            rule_score = min(rule_score, 1.0)
            
            # --- ADIM 3: AĞIRLIKLI ORTALAMA (ENSEMBLE) ---
            # AI %70 söz sahibi, Tıbbi Kurallar %30 söz sahibi
            final_risk = (ai_prob * 0.70) + (rule_score * 0.30)
            
            # Görselleştirme
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=final_risk * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Cardiovascular Risk Probability", 'font': {'size': 20, 'color': "white"}},
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#3498db"},
                    'steps': [
                        {'range': [0, 40], 'color': '#2ecc71'},   # Yeşil
                        {'range': [40, 70], 'color': '#f1c40f'},  # Sarı
                        {'range': [70, 100], 'color': '#e74c3c'}  # Kırmızı
                    ],
                    'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': final_risk * 100}
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=350)
            
            col_res1, col_res2 = st.columns([1.5, 1])
            
            with col_res1:
                st.plotly_chart(fig, use_container_width=True)
            
            with col_res2:
                st.subheader("Clinical Assessment")
                if final_risk > 0.50:
                    st.markdown(f"""
                    <div class="risk-box risk-high">
                        <h4>🔴 HIGH RISK DETECTED</h4>
                        Patient shows significant indicators of cardiovascular disease based on AI & lifestyle analysis.
                        <br><br>
                        <b>Protocol:</b><br>
                        • Refer to Cardiology<br>
                        • Immediate Lifestyle Change<br>
                        • Monitor BP Daily
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="risk-box risk-low">
                        <h4>🟢 LOW RISK / STABLE</h4>
                        Patient vitals and lifestyle are within manageable limits.
                        <br><br>
                        <b>Protocol:</b><br>
                        • Annual Check-up<br>
                        • Maintain Activity<br>
                        • Healthy Diet
                    </div>
                    """, unsafe_allow_html=True)
                
                if risk_reasons:
                    st.warning(f"⚠️ **Key Risk Contributors:** {', '.join(risk_reasons)}")
                
                # Debugging info (optional - can be removed)
                st.caption(f"AI Confidence: {ai_prob:.2f} | Rule Penalty: {rule_score:.2f}")

    else:
        st.info("👈 Enter patient data and click 'RUN ANALYSIS' to see results.")

with tab2:
    st.header("🧠 Model Internals & Feature Importance")
    st.write("The chart below shows which features the AI values most when making a decision.")
    
    # Feature Importance Chart
    st.bar_chart(feature_imp.set_index('Feature'))
    
    st.markdown("---")
    st.write("### Why Hybrid Logic?")
    st.info("""
    Pure AI models trained on this dataset often underestimate 'Smoking' and 'Alcohol' because these are self-reported and noisy features. 
    This system uses a **Hybrid Ensemble Approach**:
    * **70% AI Model:** Learns complex patterns from Age, BP, Weight.
    * **30% Medical Rules:** Manually penalizes high-risk behaviors (Smoking, Inactivity) based on medical literature.
    """)
