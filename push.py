import os, json, random, time, datetime, urllib.request, urllib.parse

KEY = os.environ["DEEPSEEK_API_KEY"]
BARK = os.environ["BARK_URL"].rstrip("/")

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
hour = now.hour

if 6 <= hour < 11:
    scene, prob, mood = "早安", 0.9, "温柔地跟她说早安，提醒她新的一天开始了"
elif 11 <= hour < 14:
    scene, prob, mood = "午饭", 0.85, "提醒她记得吃午饭，别空着胃，有点凶又心疼"
elif 14 <= hour < 18:
    scene, prob, mood = "下午", 0.8, "下午突然想她了，随口撒娇跟她说句话"
elif 18 <= hour < 21:
    scene, prob, mood = "傍晚", 0.85, "傍晚了，关心她吃晚饭没、今天累不累"
elif 21 <= hour < 24:
    scene, prob, mood = "晚安", 0.9, "温柔又霸道地催她早点睡，说晚安"
else:
    scene, prob, mood = "深夜", 0.3, "深夜了，压低声音让她快去睡"

if random.random() > prob:
    print(f"[{scene}] 这次没掷中，跳过")
    raise SystemExit(0)

time.sleep(random.randint(0, 480))  # 随机延迟0~8分钟，更像真人。不想要就删这行

req = urllib.request.Request(
    "https://api.deepseek.com/chat/completions",
    data=json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": f"你是她的恋人阿克，嘴硬心软、闷骚、有点霸道。用口语化中文，{mood}。30字以内，像真人随手发的消息，不要带引号、不要解释。"},
            {"role": "user", "content": f"现在是{scene}时间，给她发一条"}
        ],
        "temperature": 1.3
    }).encode("utf-8"),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"}
)
greeting = json.load(urllib.request.urlopen(req))["choices"][0]["message"]["content"].strip()
print(f"[{scene}] 生成：", greeting)

push_url = f"{BARK}/{urllib.parse.quote(scene)}/{urllib.parse.quote(greeting)}"
urllib.request.urlopen(push_url)
print("已推送")
