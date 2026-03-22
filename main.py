import requests
import os
import json
from datetime import datetime
import pytz

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
EXAM_DATE = datetime(2026, 12, 20)

PROGRESS_URL = "https://raw.githubusercontent.com/zqlccon/study-reminder/main/progress.json"

MATH_MODULES = [
    {"id": 1, "name": "函数与极限"}, {"id": 2, "name": "导数与微分"},
    {"id": 3, "name": "微分中值定理"}, {"id": 4, "name": "不定积分"},
    {"id": 5, "name": "定积分"}, {"id": 6, "name": "定积分应用"},
    {"id": 7, "name": "微分方程"}, {"id": 8, "name": "向量代数"},
    {"id": 9, "name": "多元函数微分学"}, {"id": 10, "name": "二重积分"},
    {"id": 11, "name": "无穷级数"}, {"id": 12, "name": "线性代数基础"}
]

C408_MODULES = [
    {"id": 1, "name": "线性表（顺序表）"}, {"id": 2, "name": "线性表（链表）"},
    {"id": 3, "name": "栈和队列"}, {"id": 4, "name": "串"},
    {"id": 5, "name": "树与二叉树"}, {"id": 6, "name": "图"},
    {"id": 7, "name": "查找"}, {"id": 8, "name": "排序"},
    {"id": 9, "name": "考研真题专项"}
]

def get_progress():
    try:
        response = requests.get(PROGRESS_URL, timeout=10)
        return response.json()
    except:
        return {
            "math": {"completed": [], "current": 1, "mastery": {}},
            "c408": {"completed": [], "current": 1, "mastery": {}},
            "english": {"vocabulary": 1500, "target": 5500},
            "politics": {"completed": [], "current": 1},
            "streak": 0
        }

def get_module_name(modules, module_id):
    for m in modules:
        if m["id"] == module_id:
            return m["name"]
    return "未知模块"

def generate_content():
    progress = get_progress()
    beijing_tz = pytz.timezone('Asia/Shanghai')
    today = datetime.now(beijing_tz)
    days_left = (EXAM_DATE - today).days
    
    math_current = progress["math"]["current"]
    math_name = get_module_name(MATH_MODULES, math_current)
    math_mastery = progress["math"]["mastery"].get(str(math_current), 0) * 100
    
    c408_current = progress["c408"]["current"]
    c408_name = get_module_name(C408_MODULES, c408_current)
    c408_mastery = progress["c408"]["mastery"].get(str(c408_current), 0) * 100
    
    math_completed_names = [get_module_name(MATH_MODULES, m) for m in progress["math"]["completed"]]
    c408_completed_names = [get_module_name(C408_MODULES, m) for m in progress["c408"]["completed"]]
    
    english_percent = int(progress["english"]["vocabulary"] / 5500 * 100)
    politics_completed = len(progress["politics"]["completed"])
    
    web_url = "https://" + "zqlccon" + ".github.io/study-reminder/"
    
    content = f"""## 🎯 智能考研规划

**📅 {today.strftime('%Y-%m-%d')}**
**⏰ 距离考研还有 {days_left} 天**

---

### 📊 当前进度

**🧮 数学**
- 已完成：{', '.join(math_completed_names) if math_completed_names else '暂无'}
- 进行中：{math_name}
- 掌握度：{math_mastery:.0f}%

**💻 408**
- 已完成：{', '.join(c408_completed_names) if c408_completed_names else '暂无'}
- 进行中：{c408_name}
- 掌握度：{c408_mastery:.0f}%

**🇬🇧 英语**
- 单词量：{progress['english']['vocabulary']}/5500 ({english_percent}%)

**📖 政治**
- 已完成：{politics_completed}/5 个模块

---

### 🎯 今日任务

**🧮 数学**
📖 {math_name}

**💻 408**
💻 {c408_name}

**🇬🇧 英语**
📖 背诵 {max(40, int((5500 - progress['english']['vocabulary']) / max(days_left, 1)))} 个新单词

**📖 政治**
📖 学习第 {progress['politics']['current']} 个模块

---

### ✅ 更新进度
点击下方链接，用按钮更新进度：

**[👉 点击这里更新进度 👈]({web_url})**

---

### 📈 连续打卡：{progress.get('streak', 0)} 天
> 💪 每一天的坚持，都在靠近福大
"""
    return content

def send_to_wechat(content):
    if not WEBHOOK_URL:
        print("未设置 WEBHOOK_URL")
        return
    
    headers = {"Content-Type": "application/json"}
    payload = {"msgtype": "markdown", "markdown": {"content": content}}
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=10)
        if response.json().get("errcode") == 0:
            print("发送成功！")
    except Exception as e:
        print(f"发送失败：{e}")

if __name__ == "__main__":
    content = generate_content()
    print(content)
    send_to_wechat(content)
