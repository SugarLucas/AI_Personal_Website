PROJECTS = {
    "Churn Prediction": {
        "description": "Predicts customer churn using a simple interpretable model.",
        "demo_type": "slider",
        "skills": ["Logistic Regression", "EDA", "Model Interpretation"],
        "ai_context": """
This project predicts customer churn.

Model choice:
Logistic Regression was chosen for interpretability and clear coefficient explanations.

Features:
User tenure, usage frequency, and contract type.

Trade-offs:
The model is easy to explain but may underperform compared to tree-based models on complex patterns.

Use cases:
Best suited for early-stage analysis or stakeholder-facing insights.
"""
    },
    "Resume–JD Matcher": {
        "description": "Analyzes how well a resume matches a job description.",
        "demo_type": "text",
        "skills": ["NLP", "Text Similarity", "UX Design"],
        "ai_context": """
This project matches resumes to job descriptions.

Approach:
Text similarity and keyword overlap with a focus on transparency.

Trade-offs:
Not a deep learning model, but easier to understand and debug.

Use cases:
Helpful for applicants and recruiters who want quick feedback.
"""
    }
}
