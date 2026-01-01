# 文件名: app.py
import streamlit as st
import pandas as pd
from projects import PROJECTS
from ai_explainer import explain_project
from data_tracker import log_interaction, load_data

# 设置页面配置（必须是第一行 Streamlit 命令）
st.set_page_config(page_title="Lucas's Portfolio", layout="wide")

st.title("🚀 Lucas Liu - Data Science Portfolio")
st.markdown("Welcome! This is an AI-powered portfolio. Ask questions about my projects!")

# 创建两个标签页
tab1, tab2 = st.tabs(["📂 Project Showcase", "📊 Analytics Dashboard"])

# ==========================================
# TAB 1: 项目展示
# ==========================================
with tab1:
    # 侧边栏：选择项目
    st.sidebar.header("Select a Project")
    project_name = st.sidebar.selectbox("Choose a project to explore:", list(PROJECTS.keys()))
    
    # 获取项目数据
    project = PROJECTS[project_name]

    # 主区域：显示项目详情
    st.header(f"Project: {project_name}")
    st.write(project["description"])
    
    # 展示技能
    st.markdown("**Skills:**")
    st.write(" · ".join([f"`{skill}`" for skill in project["skills"]]))

    st.divider()
    
    # 左右分栏：左边是 Demo，右边是 AI 问答
    col1, col2 = st.columns([1, 1])
    
    # --- 左边: Interactive Demo ---
    with col1:
        st.subheader("💡 Interactive Demo")
        
        if project["demo_type"] == "slider":
            st.write("Adjust the slider to see how the model predicts churn:")
            tenure = st.slider("User Tenure (months)", 0, 60, 12)
            # 简单的模拟逻辑
            prob = max(0, 1 - (tenure / 60)) 
            st.info(f"Predicted Churn Probability: **{prob:.2%}**")
            
        elif project["demo_type"] == "text":
            text_input = st.text_area("Paste a job description or resume snippet:")
            if text_input:
                st.success("Match Score: **85%** (Simulated Output)")
            else:
                st.caption("Waiting for input...")

    # --- 右边: AI Q&A ---
    with col2:
        st.subheader("🤖 Ask Gemini about this")
        st.markdown(f"Ask anything about **{project_name}** (e.g., 'Why use this model?')")
        
        user_question = st.text_input("Your Question:")
        
        if st.button("Ask AI"):
            if user_question.strip():
                with st.spinner("Gemini is thinking..."):
                    # 1. 调用 AI 回答
                    answer = explain_project(user_question, project["ai_context"])
                    st.write(answer)
                    
                    # 2. 记录数据到后台
                    log_interaction(project_name, user_question)
            else:
                st.warning("Please enter a question first.")

# ==========================================
# TAB 2: 数据看板 (给面试官的亮点)
# ==========================================
with tab2:
    st.header("📊 Visitor Analytics")
    st.markdown("This dashboard tracks user engagement data in real-time.")
    
    # 加载数据
    df = load_data()
    
    if not df.empty:
        # 显示关键指标
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Interactions", len(df))
        m2.metric("Most Popular Project", df['Project'].mode()[0] if not df['Project'].empty else "N/A")
        
        # 🔴 修复点在这里：使用 strftime 格式化时间对象
        try:
            latest_time = df['Timestamp'].iloc[-1].strftime("%H:%M:%S")
        except AttributeError:
            #以此防守：万一它有时候还是字符串（比如空数据时），做个兼容
            latest_time = str(df['Timestamp'].iloc[-1]).split(" ")[-1]
            
        m3.metric("Latest Query", latest_time)
        
        st.divider()

        # 图表区域
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("🔥 Project Interest")
            # 统计每个项目被问的次数
            project_counts = df['Project'].value_counts()
            st.bar_chart(project_counts)
            
        with c2:
            st.subheader("📝 Recent Questions Log")
            st.dataframe(df[['Project', 'Question']].tail(5), hide_index=True)
            
    else:
        st.info("No data yet. Go to the 'Project Showcase' tab and ask some questions to generate data!")
