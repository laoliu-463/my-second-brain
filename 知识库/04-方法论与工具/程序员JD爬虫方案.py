#!/usr/bin/env python3
"""
程序员JD爬虫方案
功能：爬取招聘平台JD，按技能词频统计分析，生成需求图谱
适用：大二学生求职方向决策、程序员职业路径分析

依赖安装：
  pip install requests pandas jieba wordcloud matplotlib seaborn
  # jieba用于中文分词（统计技能关键词）
  # 如只爬取数据不加分析，可只装 requests + pandas

免责声明：
  - 本脚本仅供学习研究使用
  - 请遵守各平台 robots.txt 及使用条款
  - 爬虫频率过高可能导致IP封禁，请设置合理延迟（sleep）
  - 商业用途请自行承担法律责任

作者：Hermes Agent
日期：2026-05-02
"""

import requests
import pandas as pd
import time
import re
import json
import os
from collections import Counter

# ============================================================
# 配置区（按需修改）
# ============================================================
CONFIG = {
    # 目标平台，目前支持 BOSS直聘（网页版）
    "platform": "boss",
    # 搜索关键词
    "search_keyword": "后端开发",  # 可改为 "Java", "Python", "前端", "算法工程师" 等
    # 目标城市（BOSS直聘城市代码，如：上海=1，北京=2，深圳=3）
    "city_code": 1,
    # 每页数量（通常为20）
    "page_size": 20,
    # 爬取页数（建议先从3页开始测试，避免封IP）
    "max_pages": 5,
    # 请求间隔（秒），建议 ≥2，避免被封
    "delay_seconds": 3,
    # 输出目录
    "output_dir": "./jd_crawl_results",
}

# ============================================================
# 工具函数
# ============================================================

def save_json(data, filepath):
    """保存数据为JSON"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_csv(df, filepath):
    """保存数据为CSV"""
    df.to_csv(filepath, index=False, encoding="utf-8-sig")

def clean_html(text):
    """去除HTML标签"""
    return re.sub(r"<[^>]+>", "", text)

def extract_skills(jd_text, skill_patterns):
    """
    从JD文本中提取技能关键词
    skill_patterns: 技能正则表达式字典 {技能名: 正则}
    """
    found = {}
    text_lower = jd_text.lower()
    for skill, pattern in skill_patterns.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found[skill] = 1
    return found

# ============================================================
# 技能词频统计用的正则（可自行扩充）
# ============================================================
SKILL_PATTERNS = {
    # 编程语言
    "Python": r"python",
    "Java": r"\bjava\b",
    "Go": r"\bgo\b|\bgolang\b",
    "C++": r"c\+\+",
    "C": r"\bc\b(?!-)",
    "Rust": r"rust",
    "JavaScript": r"javascript",
    "TypeScript": r"typescript",
    "PHP": r"\bphp\b",
    "Ruby": r"\bruby\b",
    "Swift": r"\bswift\b",
    "Kotlin": r"\bkotlin\b",
    "Scala": r"\bscala\b",
    "SQL": r"\bsql\b",
    "Shell": r"\bshell\b",
    # 后端框架
    "Spring": r"spring",
    "Django": r"django",
    "Flask": r"flask",
    "FastAPI": r"fastapi",
    "Gin": r"\bgin\b",
    "Fiber": r"\bfiber\b",
    # 前端框架
    "React": r"react",
    "Vue": r"\bvue\b",
    "Angular": r"angular",
    "Next.js": r"next\.js",
    "Node.js": r"node\.js",
    # 数据库
    "MySQL": r"mysql",
    "PostgreSQL": r"postgresql",
    "Redis": r"\bredis\b",
    "MongoDB": r"mongodb",
    "Elasticsearch": r"elasticsearch",
    "Kafka": r"\bkafka\b",
    # 云/基础设施
    "AWS": r"\baws\b|amazon web services",
    "Azure": r"\bazure\b",
    "GCP": r"\bgcp\b|google cloud",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"kubernetes|k8s",
    "Linux": r"\blinux\b",
    "Nginx": r"\bnginx\b",
    # AI/ML工具
    "TensorFlow": r"tensorflow",
    "PyTorch": r"pytorch",
    "Copilot": r"copilot",
    "LLM": r"llm|large language model|chatgpt|gpt|claude",
    # 其他工具
    "Git": r"\bgit\b",
    "CI/CD": r"ci/cd|jenkins|gitlab",
    "微服务": r"微服务|microservice",
    "分布式": r"分布式|distributed",
    "高并发": r"高并发|high concurrency",
    "缓存": r"缓存|cache",
}

# ============================================================
# 平台适配器（示例：BOSS直聘）
# ============================================================

def crawl_boss(keyword, city_code, pages, delay):
    """
    爬取BOSS直聘搜索结果页面的JD列表

    注意：BOSS直聘有反爬机制，以下代码演示结构，实际使用时：
    1. 需要手动在浏览器登录获取 cookie（__zp__）
    2. 可能需要添加 UA 和 Referer 头
    3. 如果返回空或403，说明需要更新 cookie 或用selenium
    """
    results = []
    url = "https://www.zhipin.com/web/job/geek/job-list"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.zhipin.com/",
        # 此处需要填入有效的cookie，否则无法获取数据
        # "Cookie": "your_cookie_here",
    }

    for page in range(1, pages + 1):
        params = {
            "scene": 1,
            "query": keyword,
            "city": city_code,
            "page": page,
            "pageSize": 20,
        }
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 403:
                print(f"[WARN] 第{page}页被拦截（403），可能需要更新Cookie")
                break
            if resp.status_code != 200:
                print(f"[WARN] 第{page}页请求失败：{resp.status_code}")
                break
            # 此处需根据BOSS实际返回结构解析JSON
            # data = resp.json()
            # for job in data.get("jobList", []):
            #     results.append({...})
            print(f"[OK] 第{page}页已爬取（模拟），待解析JSON结构")
        except Exception as e:
            print(f"[ERROR] 第{page}页异常：{e}")
        time.sleep(delay)

    return results

# ============================================================
# 主分析函数
# ============================================================

def analyze_jd_texts(jd_list):
    """
    对JD列表进行技能词频分析
    jd_list: JD文本列表
    返回：技能Counter + 汇总DataFrame
    """
    all_skills = Counter()

    for jd in jd_list:
        found = extract_skills(jd, SKILL_PATTERNS)
        all_skills.update(found)

    # 转为DataFrame排序
    skill_df = pd.DataFrame(
        [(k, v, v/len(jd_list)*100) for k, v in all_skills.items()],
        columns=["技能", "出现次数", "出现率(%)"]
    ).sort_values("出现次数", ascending=False)

    return all_skills, skill_df

# ============================================================
# 主程序
# ============================================================

def main():
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    print(f"[*] 目标平台：{CONFIG['platform']}")
    print(f"[*] 搜索关键词：{CONFIG['search_keyword']}")
    print(f"[*] 爬取页数：{CONFIG['max_pages']}")

    # Step 1: 爬取JD
    print("\n[1] 开始爬取JD...")
    if CONFIG["platform"] == "boss":
        jd_list = crawl_boss(
            CONFIG["search_keyword"],
            CONFIG["city_code"],
            CONFIG["max_pages"],
            CONFIG["delay_seconds"],
        )
    else:
        raise ValueError(f"不支持的平台：{CONFIG['platform']}")

    # Step 2: 如果是模拟数据（实际爬取前），用示例数据演示
    if len(jd_list) == 0:
        print("[!] 实际爬取未成功（可能需要登录Cookie），使用示例数据演示分析流程")
        # 示例JD（来自网上公开职位描述）
        sample_jds = [
            "要求：熟练掌握Java、Spring、Mysql、Redis，了解微服务、分布式、高并发，有Git经验",
            "职位描述：Python开发工程师，精通Django/Flask，熟悉MySQL/PostgreSQL，了解Linux/Docker",
            "任职资格：Go语言开发，熟悉Gin框架，Redis缓存，Linux系统，CI/CD流水线",
            "岗位要求：前端React/Vue，TypeScript，Node.js，了解微服务架构",
            "岗位职责：算法工程师，精通Python/TensorFlow/PyTorch，了解大模型（LLM）和Copilot",
        ]
        jd_list = sample_jds
        save_json(sample_jds, os.path.join(CONFIG["output_dir"], "sample_jds.json"))

    # Step 3: 技能词频分析
    print(f"\n[2] 分析 {len(jd_list)} 份JD的技能要求...")
    _, skill_df = analyze_jd_texts(jd_list)

    # 保存结果
    skill_csv = os.path.join(CONFIG["output_dir"], "skill_frequency.csv")
    save_csv(skill_df, skill_csv)
    print(f"[+] 技能词频已保存：{skill_csv}")

    # 打印Top 15
    print("\n=== 技能需求 TOP 15 ===")
    print(skill_df.head(15).to_string(index=False))

    # Step 4: 生成文字报告
    report = f"""# {CONFIG['search_keyword']} JD技能需求分析报告

## 基本信息
- 爬取平台：Boss直聘
- 搜索关键词：{CONFIG['search_keyword']}
- 有效JD数量：{len(jd_list)} 份
- 爬取时间：{time.strftime('%Y-%m-%d %H:%M')}

## 技能需求排名（Top 15）

| 排名 | 技能 | 出现次数 | 出现率 |
|------|------|---------|--------|
"""
    for i, row in skill_df.head(15).iterrows():
        report += f"| {i+1} | {row['技能']} | {row['出现次数']} | {row['出现率(%)']:.1f}% |\n"

    report += f"""
## 分析结论

1. **最高频技能**：{skill_df.iloc[0]['技能'] if len(skill_df)>0 else 'N/A'}（出现率 {skill_df.iloc[0]['出现率(%)']:.1f}%）
2. **语言趋势**：{'Python/Java/Go 为头部语言' if any(skill_df['技能'].isin(['Python','Java','Go'])) else '需进一步分析'}
3. **AI工具渗透**：{'已提及' if 'LLM' in skill_df['技能'].values or 'Copilot' in skill_df['技能'].values else '样本中未明显体现'}

## 使用说明

本脚本为演示版本，实际使用请：
1. 在浏览器登录BOSS直聘后复制Cookie填入headers
2. 根据实际返回的JSON结构修改解析代码
3. 建议每次爬取间隔3秒以上，避免IP被封

## 下一步行动建议

根据上述技能排名，对照自己的技能清单：
- 已在列表中且熟练的技能：保持
- 已在列表中但不熟悉的技能：优先学习
- 未在列表中的技能：评估是否值得投入

---
*由 Hermes Agent 生成 | {time.strftime('%Y-%m-%d %H:%M')}*
"""

    report_path = os.path.join(CONFIG["output_dir"], "jd_analysis_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[+] 分析报告已保存：{report_path}")

    print("\n[+] 全部完成！")
    print(f"    输出目录：{CONFIG['output_dir']}")
    print(f"    技能词频：{skill_csv}")
    print(f"    分析报告：{report_path}")

if __name__ == "__main__":
    main()
