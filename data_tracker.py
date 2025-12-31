# 文件名: data_tracker.py
import pandas as pd
import os
from datetime import datetime

LOG_FILE = "visitor_logs.csv"

def log_interaction(project_name, question):
    """
    将用户的提问记录到 CSV 文件中
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_data = pd.DataFrame({
        "Timestamp": [timestamp],
        "Project": [project_name],
        "Question": [question]
    })

    # 如果文件不存在，写入表头；如果存在，追加数据
    if not os.path.exists(LOG_FILE):
        new_data.to_csv(LOG_FILE, index=False)
    else:
        new_data.to_csv(LOG_FILE, mode='a', header=False, index=False)

def load_data():
    """
    读取日志数据，用于 Dashboard 展示
    """
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    else:
        # 如果没有数据，返回一个空的 DataFrame 防止报错
        return pd.DataFrame(columns=["Timestamp", "Project", "Question"])
