import streamlit as st
import pandas as pd
from projects import PROJECTS as DEFAULT_PROJECTS 
from ai_explainer import explain_project
from data_tracker import log_interaction, load_data, add_project_to_db, fetch_all_projects
from pdf_processor import extract_text_from_pdf, analyze_project_with_ai

st.set_page_config(page_title="Lucas's Portfolio", layout="wide")

# --- 数据加载逻辑 ---
db_projects = fetch_all_projects()
ALL_PROJECTS = {**DEFAULT_PROJECTS, **db_projects}

st.title("🚀 Lucas Liu - Data Science Portfolio")

tab1, tab2, tab3 = st.tabs(["📂 Project Showcase", "📊 Analytics Dashboard", "➕ Add Project (Admin)"])

# ==========================================
# TAB 1: Project Showcase
# ==========================================
with tab1:
    st.sidebar.header("Select Project")
    project_name = st.sidebar.selectbox("Choose a project:", list(ALL_PROJECTS.keys()))
    project = ALL_PROJECTS[project_name]

    st.header(f"Project: {project_name}")
    st.write(project["description"])
    
    skills_display = project["skills"]
    if isinstance(skills_display, list):
        skills_display = " · ".join(skills_display)
    st.markdown(f"**Skills:** `{skills_display}`")
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("💡 Demo / Artifacts")
        d_type = project.get("demo_type", "text")
        if d_type == "slider":
            val = st.slider("Input Value", 0, 100, 50)
            st.info(f"Prediction: {val * 1.5}")
        else:
            st.info("This project contains text/code analysis.")
            st.code("print('Hello World') # Placeholder code")

    with col2:
        st.subheader("🤖 Ask AI about this")
        user_question = st.text_input("Question:", key="q1")
        if st.button("Ask Gemini"):
            if user_question:
                with st.spinner("Thinking..."):
                    ans = explain_project(user_question, project["ai_context"])
                    st.write(ans)
                    log_interaction(project_name, user_question)

# ==========================================
# TAB 2: Analytics Dashboard
# ==========================================
with tab2:
    st.header("📊 Visitor Analytics")
    df = load_data()
    if not df.empty:
        st.dataframe(df.tail(5))
        try:
            st.bar_chart(df['Project'].value_counts())
        except KeyError:
            st.warning("Not enough data to map columns yet.")
    else:
        st.info("No data yet.")

# ==========================================
# TAB 3: 管理员上传区域 (🔴 修复了这里的逻辑)
# ==========================================
with tab3:
    st.header("⚡ AI Project Extractor")
    uploaded_file = st.file_uploader("Upload Project PDF", type=["pdf"])
    
    # 🔴 1. 初始化 Session State (内存)
    if "ai_data" not in st.session_state:
        st.session_state["ai_data"] = None

    # 🔴 2. 点击分析按钮：只负责提取数据并存入内存
    if uploaded_file is not None:
        if st.button("Analyze & Extract"):
            with st.spinner("Reading PDF and asking Gemini..."):
                raw_text = extract_text_from_pdf(uploaded_file)
                extracted_data = analyze_project_with_ai(raw_text)
                
                if extracted_data:
                    # 把数据存进“永久内存”，这样刷新页面也不会丢
                    st.session_state["ai_data"] = extracted_data
                    st.success("Extraction Successful! Please review below.")
                else:
                    st.error("AI extraction failed.")

    # 🔴 3. 只要内存里有数据，就一直显示表单
    if st.session_state["ai_data"]:
        data = st.session_state["ai_data"]
        
        with st.form("edit_project"):
            st.subheader("Review Extracted Data")
            # 使用内存里的数据填充默认值
            new_title = st.text_input("Title", data['title'])
            new_desc = st.text_area("Description", data['description'])
            new_skills = st.text_input("Skills", data['skills'])
            new_context = st.text_area("AI Context", data['ai_context'], height=150)
            
            submitted = st.form_submit_button("Save to Database")
            
            if submitted:
                # 4. 保存到数据库
                success = add_project_to_db(new_title, new_desc, new_skills, "text", new_context)
                if success:
                    st.success(f"✅ Project '{new_title}' saved successfully!")
                    # 可选：清空内存，重置状态
                    st.session_state["ai_data"] = None
                    # 强制刷新页面，让新项目立刻出现在 Tab 1
                    st.rerun() 
                else:
                    st.error("Failed to save to database. Check terminal for SQL errors.")
