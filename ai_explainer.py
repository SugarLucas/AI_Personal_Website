# 文件名: ai_explainer.py
import os
from dotenv import load_dotenv
from google import genai

# 1. 加载环境变量
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. 配置我们测试成功的模型
# 注意：我们使用刚才测试成功的通用别名
MODEL_NAME = "gemini-flash-latest"

def explain_project(question, context):
    """
    接收用户问题和项目背景，返回 AI 的回答
    """
    try:
        # 初始化客户端
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a professional AI assistant for a Data Science Portfolio.
        
        Project Context:
        {context}
        
        User Question:
        {question}
        
        Please provide a concise, friendly, and professional answer.
        """
        
        # 调用模型
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=prompt
        )
        
        return response.text

    except Exception as e:
        return f"⚠️ AI Service Unavailable: {str(e)}"
