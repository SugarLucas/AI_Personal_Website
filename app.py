import streamlit as st
from projects import PROJECTS
from ai_explainer import explain_project

st.set_page_config(page_title="AI Portfolio", layout="wide")

st.title("🚀 Interactive AI Project Portfolio")

# ---- Sidebar: Project Selection ----
st.sidebar.header("Projects")

project_name = st.sidebar.selectbox(
    "Choose a project",
    list(PROJECTS.keys())
)

project = PROJECTS[project_name]

# ---- Main Content ----
st.header(project_name)
st.write(project["description"])

st.subheader("Skills Demonstrated")
st.write(", ".join(project["skills"]))

# ---- Demo Placeholder ----
st.subheader("Live Demo")

if project["demo_type"] == "slider":
    value = st.slider("User tenure (months)", 0, 60, 12)
    st.write(f"Churn probability (demo): {round(value / 60, 2)}")

elif project["demo_type"] == "text":
    text = st.text_area("Paste text here")
    if text:
        st.write("Match score (demo): 72%")

st.divider()
st.subheader("💬 Ask AI about this project")

question = st.text_input("Ask a question (e.g. Why this model?)")

if st.button("Ask AI"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = explain_project(
                question,
                project["ai_context"]
            )
        st.write(answer)
