import json,random
from openai import OpenAI
from . import config
def generate_reel():
    if not config.get("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY is missing; configure .env.")
    client=OpenAI(api_key=config.get("OPENAI_API_KEY"),base_url=config.get("OPENAI_BASE_URL","https://api.openai.com/v1"))
    pillars=[x.strip() for x in config.get("CONTENT_PILLARS","fat loss,muscle building,nutrition").split(",") if x.strip()]
    topic=random.choice(pillars)
    prompt=f"""
Create one original Instagram Reel about {topic} for Coach Gado.
Audience: {config.get("TARGET_AUDIENCE","Egyptian adults")}.
Write natural Egyptian colloquial Arabic, not formal Arabic and not robotic advertising.
Return ONLY JSON keys: narration (90-120 spoken Arabic words), caption (helpful CTA), hashtags (array of 5-8),
topic, on_screen_title (short).
Avoid guaranteed results, diagnosis, unsafe advice, fabricated client stories or medical claims.
Include one practical actionable takeaway.
"""
    r=client.chat.completions.create(model=config.get("OPENAI_MODEL","gpt-4.1-mini"),
      messages=[{"role":"system","content":"Return valid JSON only."},{"role":"user","content":prompt}],temperature=.8)
    raw=r.choices[0].message.content.strip()
    if raw.startswith("```"): raw=raw.split("\n",1)[1].rsplit("```",1)[0]
    d=json.loads(raw); d["caption"]=d.get("caption","")+"\n\n"+" ".join(d.get("hashtags",[])); return d
