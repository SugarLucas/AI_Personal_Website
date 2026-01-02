# 文件名: data_tracker.py
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DB_URL)
except Exception as e:
    print(f"Database Connection Error: {e}")
    engine = None

def init_db():
    """初始化数据库"""
    if engine is None: return

    # 1. 访客记录表
    create_interactions = """
    CREATE TABLE IF NOT EXISTS interactions (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        project_name TEXT,
        question TEXT
    );
    """
    
    # 2. 项目存储表
    create_projects = """
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        title TEXT UNIQUE,
        description TEXT,
        skills TEXT,
        demo_type TEXT,
        ai_context TEXT
    );
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(create_interactions))
            conn.execute(text(create_projects))
            conn.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")

# --- 访客记录功能 ---
def log_interaction(project_name, question):
    if engine is None: return
    try:
        with engine.connect() as conn:
            query = text("INSERT INTO interactions (project_name, question) VALUES (:p, :q)")
            conn.execute(query, {"p": project_name, "q": question})
            conn.commit()
    except Exception as e:
        print(f"Log Error: {e}")

def load_data():
    """✅ 修复版：读取数据并重命名列，解决 KeyError"""
    if engine is None: 
        return pd.DataFrame()
    
    try:
        # 读取原始数据
        df = pd.read_sql("SELECT * FROM interactions ORDER BY timestamp DESC", engine)
        
        # 🔴 关键修复：把数据库列名映射回前端需要的名字
        if not df.empty:
            df = df.rename(columns={
                "project_name": "Project",
                "question": "Question",
                "timestamp": "Timestamp"
            })
        return df
    except Exception as e:
        print(f"Load Data Error: {e}")
        return pd.DataFrame()

# --- 项目管理功能 ---
def add_project_to_db(title, description, skills, demo_type, ai_context):
    if engine is None: return False
    
    # 确保 skills 是字符串
    if isinstance(skills, list):
        skills = ", ".join(skills)
        
    query = text("""
        INSERT INTO projects (title, description, skills, demo_type, ai_context)
        VALUES (:t, :d, :s, :demo, :ai)
        ON CONFLICT (title) DO NOTHING
    """)
    
    try:
        with engine.connect() as conn:
            conn.execute(query, {
                "t": title, "d": description, "s": skills, 
                "demo": demo_type, "ai": ai_context
            })
            conn.commit()
        return True
    except Exception as e:
        print(f"Add Project Error: {e}")
        return False

def fetch_all_projects():
    """获取所有项目"""
    db_projects = {}
    if engine:
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM projects"))
                for row in result:
                    # ✅ 修复：通过 row[索引] 或 getattr 安全获取
                    # 不同的 SQLAlchemy 版本获取方式不同，这里用通用写法
                    db_projects[row.title] = {
                        "description": row.description,
                        "skills": row.skills.split(",") if row.skills else [],
                        "demo_type": row.demo_type,
                        "ai_context": row.ai_context
                    }
        except Exception as e:
            print(f"Fetch Error: {e}")
            
    return db_projects

init_db()
