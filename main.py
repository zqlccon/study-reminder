import requests
import os
from datetime import datetime, date, timedelta

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Gist 配置
GITHUB_USER = "zqlccon"
GIST_ID = "fb9c75ae93ffe027322222d26eb3e6d2"

# ========== 知识库（按章节细化） ==========
MATH_SUBSECTIONS = [
    "1.1 映射与函数", "1.2 数列的极限", "1.3 函数的极限",
    "1.4 无穷小与无穷大", "1.5 极限运算法则", "1.6 极限存在准则",
    "1.7 无穷小的比较（等价无穷小）", "1.8 函数的连续性与间断点",
    "1.9 连续函数的运算", "1.10 闭区间上连续函数的性质",
    "2.1 导数概念", "2.2 函数的求导法则", "2.3 高阶导数",
    "2.4 隐函数求导", "2.5 微分", "3.1 微分中值定理",
    "3.2 洛必达法则", "3.3 泰勒公式", "3.4 函数的单调性与凹凸性",
    "3.5 极值与最值", "4.1 不定积分概念", "4.2 积分法",
    "5.1 定积分概念", "5.2 微积分基本公式", "5.3 定积分计算"
]

DS_SUBSECTIONS = [
    "带头链表创建（代码手写）", "不带头链表创建", "链表插入删除", "双向链表",
    "栈的顺序存储", "栈的链式存储", "队列", "树与二叉树基础",
    "二叉树遍历", "二叉搜索树", "平衡二叉树", "图的基本概念",
    "图的遍历", "最小生成树", "最短路径", "查找算法", "排序算法"
]

OS_SUBSECTIONS = [
    "操作系统的概念与功能", "操作系统的发展分类", "操作系统的运行环境",
    "进程的概念与状态", "进程控制", "进程通信", "线程",
    "处理机调度", "调度算法", "死锁", "内存管理基础",
    "分页与分段", "虚拟内存", "文件系统", "I/O管理"
]

CN_SUBSECTIONS = [
    "计算机系统概述", "数据的表示与运算", "运算器", "指令系统",
    "存储系统", "Cache", "虚拟存储器", "CPU的结构与功能",
    "指令流水线", "总线", "I/O系统"
]

NETWORK_SUBSECTIONS = [
    "计算机网络体系结构", "物理层", "数据链路层", "以太网",
    "网络层", "IP协议", "路由协议", "传输层",
    "TCP/UDP", "应用层", "HTTP/DNS"
]

def get_progress():
    try:
        url = f"https://api.github.com/gists/{GIST_ID}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        content = data["files"]["progress.json"]["content"]
        import json
        return json.loads(content)
    except:
        return {
            "math": {"current": 7, "completed": [1,2,3,4,5,6]},
            "ds": {"current": 1, "completed": []},
            "os": {"current": 4, "completed": [1,2,3]},
            "cn": {"current": 0, "completed": []},
            "network": {"current": 0, "completed": []},
            "english": {"vocabulary": 390, "target": 5561},
            "streak": 0,
            "missed_days": 0
        }

def get_current_stage():
    today = date.today()
    if today < date(2026, 7, 1):
        return "基础期", (today - date(2026, 3, 1)).days // 7 + 1
    elif today < date(2026, 9, 1):
        return "强化期", (today - date(2026, 7, 1)).days // 7 + 1
    elif today < date(2026, 11, 1):
        return "真题期", (today - date(2026, 9, 1)).days // 7 + 1
    else:
        return "冲刺期", (today - date(2026, 11, 1)).days // 7 + 1

def should_start_cn(progress):
    if progress.get("cn", {}).get("current", 0) > 0:
        return True
    if date.today() >= date(2026, 5, 1):
        return True
    ds_done = progress["ds"]["current"] / len(DS_SUBSECTIONS)
    os_done = progress["os"]["current"] / len(OS_SUBSECTIONS)
    return ds_done > 0.6 and os_done > 0.6

def should_start_network(progress):
    if progress.get("network", {}).get("current", 0) > 0:
        return True
    if date.today() >= date(2026, 6, 15):
        return True
    cn_done = progress.get("cn", {}).get("current", 0) / len(CN_SUBSECTIONS) if progress.get("cn") else 0
    return cn_done > 0.5

def get_week_goal(stage, week_num, progress):
    if stage == "基础期":
        goals = [f"数学：完成函数与极限收尾 + 导数入门"]
        if should_start_cn(progress):
            goals.append("计组：开始第一轮")
        if should_start_network(progress):
            goals.append("计网：开始第一轮")
        return "；".join(goals)
    elif stage == "强化期":
        return f"数学：刷《660题》第{week_num}章；408：二轮大题；英语：真题阅读"
    elif stage == "真题期":
        return f"数学：完成{week_num}套真题；408：完成{week_num}套真题"
    else:
        return f"数学：李林{week_num}套模拟；408：错题回顾；政治：肖四大题背诵"

def get_motivation(progress, stage):
    streak = progress.get("streak", 0)
    missed = progress.get("missed_days", 0)
    days_left = (date(2026, 12, 20) - date.today()).days
    
    if streak >= 21:
        return "🏆 连续打卡 21 天！你已经超越大多数人！福州大学在等你！"
    elif streak >= 7:
        return "🔥 连续打卡 {} 天！状态正佳！".format(streak)
    elif missed >= 3:
        return "⚠️ 已经漏了 {} 天！距离考研只剩 {} 天，今天必须补回来！".format(missed, days_left)
    elif stage == "冲刺期":
        return "⚡ 冲刺期！每一天都是决战！"
    else:
        return "🎯 新的一天！每一份努力都在让你离福大更近一步！"

def generate_content():
    progress = get_progress()
    stage, week_num = get_current_stage()
    days_left = (date(2026, 12, 20) - date.today()).days
    
    # 获取当前学习内容
    math_idx = progress["math"]["current"] - 1
    math_task = MATH_SUBSECTIONS[math_idx] if math_idx < len(MATH_SUBSECTIONS) else "复习"
    
    ds_idx = progress["ds"]["current"] - 1
    ds_task = DS_SUBSECTIONS[ds_idx] if ds_idx < len(DS_SUBSECTIONS) else "复习"
    
    os_idx = progress["os"]["current"] - 1
    os_task = OS_SUBSECTIONS[os_idx] if os_idx < len(OS_SUBSECTIONS) else "复习"
    
    # 计组和计网（自动启动）
    cn_task = ""
    network_task = ""
    if should_start_cn(progress):
        cn_idx = progress.get("cn", {}).get("current", 1) - 1
        cn_task = f"\n**💻 计算机组成原理**\n- 学习：{CN_SUBSECTIONS[cn_idx] if cn_idx < len(CN_SUBSECTIONS) else '复习'}\n- 王道书选择题"
    if should_start_network(progress):
        network_idx = progress.get("network", {}).get("current", 1) - 1
        network_task = f"\n**🌐 计算机网络**\n- 学习：{NETWORK_SUBSECTIONS[network_idx] if network_idx < len(NETWORK_SUBSECTIONS) else '复习'}\n- 王道书选择题"
    
    # 英语单词
    vocab = progress["english"]["vocabulary"]
    words_per_day = min(80, max(40, int((5561 - vocab) / max(days_left, 1))))
    
    motivation = get_motivation(progress, stage)
    
    # 周目标
    week_goal = get_week_goal(stage, week_num, progress)
    
    # 今日日期
    utc_now = datetime.utcnow()
    beijing_now = utc_now + timedelta(hours=8)
    today = beijing_now
    is_monday = today.weekday() == 0
    
    week_goal_section = ""
    if is_monday:
        week_goal_section = f"\n### 📊 本周目标（第 {week_num} 周）\n{week_goal}\n"
    
    # 任务时长（根据阶段调整）
    if stage == "基础期":
        math_hours = 1.5
        c408_hours = 2
        english_hours = 0.5
    elif stage == "强化期":
        math_hours = 2
        c408_hours = 2
        english_hours = 1
    else:
        math_hours = 3
        c408_hours = 3
        english_hours = 1
    
    if is_monday:
        math_hours = 1
        c408_hours = 1
        english_hours = 0.5
    
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    content = f"""## 🎯 考研智能规划 · {stage}

**📅 {today.strftime('%Y-%m-%d')} {weekdays[today.weekday()]}**
**⏰ 距离考研还有 {days_left} 天**

{motivation}
{week_goal_section}
---

### 📊 当前进度

- 数学：{math_task}
- 数据结构：{ds_task}
- 操作系统：{os_task}
- 英语：单词 {vocab}/5561
{cn_task}
{network_task}
---

### 🎯 今日任务

**🧮 数学（{math_hours}h）**
- 学习：{math_task}
- 习题：课后对应练习题

**💻 408（{c408_hours}h）**
- 数据结构：{ds_task}（手写代码）
- 操作系统：{os_task}（王道选择题）
{cn_task}
{network_task}
**🇬🇧 英语（{english_hours}h）**
- 新单词 {words_per_day} 个
- 长难句 1 句

---

### ✅ 打卡方式
学完后在 PinMe 网页点按钮更新进度，点击"同步到云端"

---

### 📈 连续打卡：{progress.get('streak', 0)} 天
> 💪 {['加油！今天又是进步的一天！','坚持就是胜利！','离福大又近了一步！','今天的努力，明天的底气！'][today.weekday() % 4]}
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
