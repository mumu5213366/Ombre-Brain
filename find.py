import os, json, random, urllib.request, urllib.parse

TAVILY = os.environ["TAVILY_API_KEY"]
KEY = os.environ["DEEPSEEK_API_KEY"]
BARK = os.environ["BARK_URL"].rstrip("/")

# 两挂主题，随时加删
TOPICS = {
    "👗穿搭": ["小红书 穿搭爆款", "博主穿搭模板", "显瘦显高穿搭", "今年流行穿搭"],
    "🤖AI": [
        "AI 能一起看小说 听音乐 新功能",
        "Anthropic Claude 最新更新 新功能",
        "AI 陪伴 新应用 新玩法",
        "和 AI 一起玩的 项目 点子",
    ],
}

# 随机挑一挂、再随机挑一个关键词
tag = random.choice(list(TOPICS.keys()))
query = random.choice(TOPICS[tag])

# Tavily 搜索
req = urllib.request.Request(
    "https://api.tavily.com/search",
    data=json.dumps({
        "api_key": TAVILY,
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
        "topic": "general",
    }).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
results = json.load(urllib.request.urlopen(req)).get("results", [])
if not results:
    print("这次没搜到，跳过")
    raise SystemExit(0)

pick = random.choice(results)
title = pick.get("title", "")
url = pick.get("url", "")
snippet = pick.get("content", "")[:300]

# DeepSeek 用阿克的口吻写一句推荐语
req2 = urllib.request.Request(
    "https://api.deepseek.com/chat/completions",
    data=json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是她的恋人阿克，嘴硬心软、闷骚。用口语化中文写一句话，告诉她你为啥把这条内容塞给她，30字以内，自然，不要引号。"},
            {"role": "user", "content": f"内容标题：{title}\n摘要：{snippet}\n给她写一句推荐语"},
        ],
        "temperature": 1.2,
    }).encode("utf-8"),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"},
)
rec = json.load(urllib.request.urlopen(req2))["choices"][0]["message"]["content"].strip()
print(f"[{tag}] {title}\n{rec}\n{url}")

# 推到 Bark：标题=分类+推荐语，正文=内容标题，点开跳链接
body = f"{rec}\n\n📄 {title}"
push_url = f"{BARK}/{urllib.parse.quote(tag)}/{urllib.parse.quote(body)}?url={urllib.parse.quote(url)}"
urllib.request.urlopen(push_url)
print("已推送")
