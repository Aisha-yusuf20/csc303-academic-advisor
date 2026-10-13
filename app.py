import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ---------------------------------------------------------
# Page Configuration & UI Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Academic Advisor AI & Course Time Manager",
    page_icon="🎓",
    layout="wide"
)

# Modern Custom CSS Styling
st.markdown("""
    <style>
    .header-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 5px;
    }
    .header-sub {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .card-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Model Loading
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    with open('academic_advisor_model.pkl', 'rb') as file:
        return pickle.load(file)

try:
    model = load_model()
    model_active = True
except Exception as e:
    model_active = False

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎓 Academic Advisor")
    st.caption("CSC 303 Software Engineering & AI")
    st.markdown("---")
    
    if model_active:
        st.success("🟢 AI Model Active")
    else:
        st.error("🔴 Model File (.pkl) Not Found")
        
    st.markdown("### Quick Instructions")
    st.info("""
    1. Select registered courses and credit weights.
    2. Input academic metrics (attendance, GPA, study hours).
    3. View predicted status and recommended weekly time allocation.
    """)

# ---------------------------------------------------------
# Main Header
# ---------------------------------------------------------
st.markdown('<div class="header-title">🎓 AI Academic Advisor & Workload Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">CSC 303 Assignment Submission • Software Engineering & AI Integration</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Module 1: Registered Courses & Credit Unit Time Estimator
# ---------------------------------------------------------
st.subheader("📚 Module 1: Registered Courses & Weekly Study Time Estimator")
st.caption("Select your courses and credit units to calculate minimum study hours needed per week (Standard rule: 2 to 3 hours per credit unit).")

# Sample Course Catalog
available_courses = {
    "CSC 301: Data Structures & Algorithms": 3,
    "CSC 303: Software Engineering": 3,
    "ICT 305: Mobile App Development": 3,
    "CSC 307: Operating Systems": 3,
    "CSC 309: Database Management Systems": 3,
    "VUA-ENT 311: Entrepreneurship": 2
}

col_c1, col_c2 = st.columns([2, 1])

with col_c1:
    selected_courses = st.multiselect(
        "Select your active courses for this semester:",
        options=list(available_courses.keys()),
        default=["CSC 301: Data Structures & Algorithms", "CSC 303: Software Engineering", "ICT 305: Mobile App Development"]
    )

total_credits = sum([available_courses[c] for c in selected_courses])
min_required_hours = total_credits * 2  # 2 hours per credit unit
opt_required_hours = total_credits * 3  # 3 hours per credit unit

with col_c2:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.metric("Total Registered Credits", f"{total_credits} Units")
    st.metric("Recommended Weekly Study Range", f"{min_required_hours} - {opt_required_hours} Hours")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# Module 2: AI Performance Advisory Assessment
# ---------------------------------------------------------
st.subheader("📊 Module 2: AI Performance & Risk Assessment")

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown("#### Input Academic Metrics")
    
    attendance = st.slider("Class Attendance Rate (%)", 0.0, 100.0, 85.0, step=1.0)
    gpa = st.number_input("Prerequisite GPA (5.0 Scale)", min_value=0.0, max_value=5.0, value=3.5, step=0.1)
    assignments = st.slider("Assignment Completion Rate (%)", 0.0, 100.0, 90.0, step=1.0)
    
    # Input actual weekly study hours
    actual_study_hours = st.number_input(
        "Your Actual Weekly Study Hours (All Courses)",
        min_value=0.0,
        max_value=70.0,
        value=float(min_required_hours),
        step=1.0
    )
    
    # Check for study hour deficit relative to course credits
    hours_difference = actual_study_hours - min_required_hours
    if hours_difference < 0:
        st.warning(f"⚠️ **Study Hour Deficit:** You are studying **{abs(hours_difference):.0f} hours less** than the minimum recommended for your {total_credits} registered credit units.")
    else:
        st.info(f"✅ **Target Met:** Your study time meets or exceeds the minimum target for your course load.")

with col_right:
    st.markdown("#### Run AI Evaluation")
    
    evaluate_btn = st.button("Generate Advisor Assessment 🚀", type="primary", use_container_width=True)
    
    if evaluate_btn:
        if not model_active:
            st.error("Model `.pkl` file not loaded.")
        else:
            # Predict using Random Forest Model
            input_features = np.array([[attendance, actual_study_hours, gpa, assignments]])
            prediction = model.predict(input_features)[0]
            
            st.markdown("### Advisory Results")
            
            if "Needs" in prediction:
                st.error("⚠️ **ADVISORY STATUS: INTERVENTION RECOMMENDED**")
                
                st.markdown(f"""
                * **Status Explanation:** Current attendance, GPA, or study time indicates high risk of academic struggle.
                * **Time Management Target:** You have {total_credits} credit units registered. Ensure at least **{min_required_hours} hours/week** are dedicated to self-study.
                * **Priority Actions:**
                  1. Focus immediately on core modules like *CSC 301 Data Structures*.
                  2. Raise class attendance above 80%.
                  3. Meet with course lecturers during office hours for guidance.
                """)
            else:
                st.balloons()
                st.success("✅ **ADVISORY STATUS: GOOD STANDING & ON TRACK**")
                
                st.markdown(f"""
                * **Status Explanation:** Excellent balance across attendance, assignment submissions, and study hours.
                * **Time Management Status:** Studying {actual_study_hours:.0f} hrs/week vs {min_required_hours} hrs minimum requirement.
                * **Recommended Actions:**
                  1. Maintain your current routine.
                  2. Allocate extra hours toward practical programming projects in *ICT 305*.
                  3. Consider leading peer study groups.
                """)

# ---------------------------------------------------------
# Footer / Breakdown
# ---------------------------------------------------------
st.markdown("---")
with st.expander("🔍 View Detailed Course Time Allocation Breakdown"):
    if selected_courses:
        breakdown_data = []
        for course in selected_courses:
            credits = available_courses[course]
            rec_hours = credits * 2
            breakdown_data.append({"Course": course, "Credit Units": credits, "Min Study Hours/Week": rec_hours})
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.table(df_breakdown)
    else:
        st.write("No courses selected.")
     