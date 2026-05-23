import os, json, urllib.request, urllib.parse

KEY = os.environ["DEEPSEEK_API_KEY"]
BARK = os.environ["BARK_URL"].rstrip("/")

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

push_url = f"{BARK}/{urllib.parse.quote('早安')}/{urllib.parse.quote(greeting)}"
urllib.request.urlopen(push_url)
print("已推送")
