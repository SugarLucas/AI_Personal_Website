# 文件名: pdf_processor.py
import google.genai as genai # 注意这里用新版库
import os
from dotenv import load_dotenv
import PyPDF2
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 初始化 Gemini
client = genai.Client(api_key=api_key)

def extract_text_from_pdf(uploaded_file):
    """从上传的 PDF 文件中提取纯文本"""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def analyze_project_with_ai(text_content):
    """
    让 Gemini 从杂乱的文本中提取结构化的项目信息 (JSON)
    """
    prompt = f"""
    You are a Data Science Portfolio Manager.
    Extract details about a SINGLE project from the following text.
    
    TEXT CONTENT:
    {text_content[:10000]}  # 限制长度防止 Token 溢出

    INSTRUCTIONS:
    1. Identify the main project described.
    2. Extract the Title, a Short Description, Skills used, and a Detailed Context for AI.
    3. Return ONLY a valid JSON object. Do not add Markdown formatting (```json).
    
    JSON FORMAT:
    {{
        "title": "Project Name",
        "description": "One sentence summary.",
        "skills": "Python, SQL, Machine Learning (Comma separated string)",
        "ai_context": "Detailed explanation of the problem, solution, model, and results. This will be used by an AI chatbot to answer questions."
    }}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        
        # 清理返回结果，确保是纯 JSON
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
        
    except Exception as e:
        print(f"AI Extraction Error: {e}")
        return None
