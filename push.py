import os, json, urllib.request

KEY = os.environ["DEEPSEEK_API_KEY"]
BARK = os.environ["BARK_URL"]

# 1. 让 DeepSeek 写一句问候
req = urllib.request.Request(
    "https://api.deepseek.com/chat/completions",
    data=json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你用温柔、口语化的中文写一句早安问候，30字以内，不要带引号。"},
            {"role": "user", "content": "给她写今天的早安"}
        ]
    }).encode("utf-8"),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"}
)
greeting = json.load(urllib.request.urlopen(req))["choices"][0]["message"]["content"].strip()
print("生成：", greeting)

# 2. 推到 Bark
push = urllib.request.Request(
    BARK,
    data=json.dumps({"title": "早安", "body": greeting}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
urllib.request.urlopen(push)
print("已推送")
