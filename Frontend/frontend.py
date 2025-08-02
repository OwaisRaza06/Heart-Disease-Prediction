import streamlit as st
import requests
from PIL import Image
import base64

# Set page config
st.set_page_config(
    page_title="Heart Disease Risk Assessment",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")  # Create a style.css file with the CSS below

# Sidebar
with st.sidebar:
    st.header("About This Tool")
    st.markdown("""
    This tool predicts the 10-year risk of Coronary Heart Disease (CHD) 
    using advanced machine learning models. Fill in the patient details 
    and get instant risk assessment.
    """)
    
    st.markdown("---")
    st.markdown("""
    **Instructions:**
    1. Fill all patient information
    2. Click 'Predict Risk'
    3. View results
    """)
    
    st.markdown("---")
    st.markdown("Built with ❤ by Owais")

# Main content
st.title("❤️ Coronary Heart Disease Risk Prediction")
st.markdown("Assess a patient's 10-year risk of developing coronary heart disease")

# Form container with card-like appearance
with st.container():
    st.markdown("""
    <div class="card">
        <h3>Patient Information</h3>
    """, unsafe_allow_html=True)
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🧑 Demographic Information")
            sex_options = ["Female", "Male"]
            male = st.radio("Sex", options=sex_options, index=0, horizontal=True)
            male = 1 if male == "Male" else 0
            age = st.number_input("Age (years)", min_value=20, max_value=100, value=50)
            education = st.selectbox(
                "Education Level", 
                options=[("Some High School", 1), ("High School/GED", 2), 
                         ("Some College/Vocational School", 3), ("College", 4)],
                format_func=lambda x: x[0]
            )[1]
            
            st.markdown("#### 🚬 Smoking Information")
            currentSmoker = st.checkbox("Current Smoker", value=False)
            currentSmoker = 1 if currentSmoker else 0
            cigsPerDay = st.slider("Cigarettes per Day", min_value=0, max_value=100, value=0, 
                                  disabled=not currentSmoker)
        
        with col2:
            st.markdown("#### 🏥 Medical History")
            BPMeds = st.checkbox("On BP Medication", value=False)
            BPMeds = 1 if BPMeds else 0
            prevalentStroke = st.checkbox("History of Stroke", value=False)
            prevalentStroke = 1 if prevalentStroke else 0
            prevalentHyp = st.checkbox("Prevalent Hypertension", value=False)
            prevalentHyp = 1 if prevalentHyp else 0
            diabetes = st.checkbox("Diabetes", value=False)
            diabetes = 1 if diabetes else 0
            
            st.markdown("#### 💓 Clinical Measurements")
            totChol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
            sysBP = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=250, value=120)
            diaBP = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80)
        
        st.markdown("#### ⚖️ Additional Measurements")
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        height = st.number_input("Height (meters)", min_value=1.0, max_value=2.5, value=1.7, step=0.01)
        heartRate = st.slider("Heart Rate (bpm)", min_value=40, max_value=150, value=72)
        glucose = st.number_input("Glucose (mg/dL)", min_value=50, max_value=300, value=90)
        
        # Centered submit button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            submitted = st.form_submit_button("🔍 Predict Risk", use_container_width=True)

# Results section
if submitted:
    st.markdown("---")
    with st.spinner("Analyzing patient data..."):
        # Prepare the data
        data = {
            "male": male,
            "age": age,
            "education": education,
            "currentSmoker": currentSmoker,
            "cigsPerDay": cigsPerDay,
            "BPMeds": BPMeds,
            "prevalentStroke": prevalentStroke,
            "prevalentHyp": prevalentHyp,
            "diabetes": diabetes,
            "totChol": totChol,
            "sysBP": sysBP,
            "diaBP": diaBP,
            "weight": weight,
            "height": height,
            "heartRate": heartRate,
            "glucose": glucose
        }
        
        # Make request to your FastAPI endpoint
        api_url = "http://localhost:8000/predict"
        
        try:
            response = requests.post(api_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("chances of Ten year CHD", 0)
                
                # Animated result display
                with st.container():
                    st.markdown("## 📊 Risk Assessment Results")
                    
                    if prediction == 1:
                        st.error("""
                        ## ❗ High Risk of CHD
                        This patient has a **high risk** of developing coronary heart disease 
                        within 10 years. Consider preventive measures and regular monitoring.
                        """)
                    else:
                        st.success("""
                        ## ✅ Low Risk of CHD
                        This patient has a **low risk** of developing coronary heart disease 
                        within 10 years. Maintain healthy lifestyle practices.
                        """)
                    
                    # Additional space
                    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
                    
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the API: {str(e)}")
