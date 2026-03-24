import requests
import os
from datetime import date

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

GIST_ID = "fb9c75ae93ffe027322222d26eb3e6d2"

MATH_MODULES = [
    "函数与极限", "导数与微分", "微分中值定理", "不定积分",
    "定积分", "定积分应用", "微分方程", "向量代数",
    "多元函数微分学", "二重积分", "无穷级数", "线性代数基础"
]

C408_MODULES = [
    "线性表（顺序表）", "线性表（链表）", "栈和队列", "串",
    "树与二叉树", "图", "查找", "排序", "考研真题专项"
]

def get_progress():
    try:
        url = f"https://api.github.com/gists/{GIST_ID}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        content = data["files"]["progress.json"]["content"]
        import json
        return json.loads(content)
    except Exception as e:
        print(f"读取 Gist 失败：{e}")
        # 默认进度
        return {
            "math": {"current": 1},
            "c408": {"current": 1},
            "english": {"vocabulary": 390, "target": 5500},
            "politics": {"current": 1},
            "streak": 0
        }

def generate_content():
    progress = get_progress()
    
    # 倒计时
    exam_date = date(2026, 12, 20)
    today_date = date.today()
    days_left = (exam_date - today_date).days
    
    # 获取当前模块名称
    math_current = progress["math"]["current"]
    math_name = MATH_MODULES[math_current - 1] if 1 <= math_current <= 12 else "函数与极限"
    
    c408_current = progress["c408"]["current"]
    c408_name = C408_MODULES[c408_current - 1] if 1 <= c408_current <= 9 else "线性表"
    
    english_vocab = progress["english"]["vocabulary"]
    words_per_day = max(40, int((5500 - english_vocab) / max(days_left, 1)))
    
    politics_current = progress["politics"]["current"]
    politics_list = ["马原", "毛中特", "史纲", "思修", "形策"]
    politics_name = politics_list[politics_current - 1] if 1 <= politics_current <= 5 else "已完成"
    
    content = f"""## 🎯 考研智能规划

**📅 {today_date.strftime('%Y-%m-%d')}**
**⏰ 距离考研还有 {days_left} 天**

---

### 📊 当前进度

- 数学：{math_name}
- 408：{c408_name}
- 英语：单词 {english_vocab}/5500
- 政治：{politics_name}

---

### 🎯 今日任务

**🧮 数学**
继续学习：{math_name}

**💻 408**
继续学习：{c408_name}

**🇬🇧 英语**
背诵 {words_per_day} 个新单词

**📖 政治**
学习 {politics_name}

---

### ✅ 打卡方式
打开 PinMe 网页 → 点按钮更新进度 → 点"同步到云端"

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
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if resp.json().get("errcode") == 0:
            print("发送成功！")
        else:
            print(f"发送失败：{resp.json()}")
    except Exception as e:
        print(f"请求异常：{e}")

if __name__ == "__main__":
    content = generate_content()
    print(content)
    send_to_wechat(content)
