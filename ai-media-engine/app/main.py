import os,threading
from flask import Flask,redirect,render_template_string,url_for,send_file,abort
from . import db,config
from .generator import generate_reel
from .render import render_reel
from .publisher import publish_reel
app=Flask(__name__); db.init(); RUNNING=False; LAST_ERROR=""
HTML="""
<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>
<title>Coach Gado AI Media Engine</title><style>
body{margin:0;background:#111;color:#eee;font:16px Arial}header{background:#1a1a1b;padding:24px;border-bottom:3px solid #db2126}
main{max-width:960px;margin:28px auto;padding:0 16px}.card{background:#202022;border:1px solid #393939;border-radius:12px;padding:18px;margin:16px 0}
button{background:#db2126;color:white;border:0;padding:13px 20px;border-radius:8px;font-weight:bold}small,.muted{color:#aaa}a{color:#ff7777}.err{color:#ff7777}
</style></head><body><header><h1>COACH GADO <span style='color:#db2126'>AI MEDIA ENGINE</span></h1><small>Independent Instagram Reel production</small></header><main>
<div class=card><h2>Production control</h2><p>Generate one Egyptian Arabic fitness Reel using your own footage.</p>
<form method=post action=/run><button {% if running %}disabled{% endif %}>{{'Producingâ¦' if running else 'Generate todayâs Reel'}}</button></form>
<p class=muted>Publishing: {{mode}}. Review a test video before enabling live publishing.</p>{% if error %}<p class=err>{{error}}</p>{% endif %}</div>
<h2>Recent jobs</h2>{% for j in jobs %}<div class=card><b>#{{j.id}} â {{j.topic}}</b><p>{{j.status}} Â· {{j.created_at}}</p><p>{{j.caption}}</p>{% if j.video_path %}<a href=/video/{{j.id}}>Download video</a>{% endif %}{% if j.error %}<p class=err>{{j.error}}</p>{% endif %}</div>{% else %}<p class=muted>No jobs yet.</p>{% endfor %}
</main></body></html>
"""
def pipeline():
    global RUNNING,LAST_ERROR
    RUNNING=True
    try:
        d=generate_reel(); video=render_reel(d["narration"]); pid,status=publish_reel(video,d["caption"])
        db.add(d.get("topic","fitness"),d["narration"],d["caption"],video,status,pid); LAST_ERROR=""
    except Exception as e:
        LAST_ERROR=str(e); db.add("production","","","","failed","",LAST_ERROR)
    finally: RUNNING=False
@app.get("/")
def home():
    return render_template_string(HTML,*obs=db.recent(),running=RUNNING,error=LAST_ERROR,mode="LIVE" if config.enabled("PUBLISH_TO_INSTAGRAM") else "DRAFT ONLY")
@app.post("/run")
def run_now():
    if not RUNNING: threading.Thread(target=pipeline,daemon=True).start()
    return redirect(url_for("home"))
@app.get("/video/<int:jid>")
def video(jid):
    job=next((x for x in db.recent(100) if x["id"]==jid),None)
    if not job or not job["video_path"] or not os.path.exists(job["video_path"]): abort(404)
    return send_file(job["video_path"],as_attachment=True)
if __name__=="__main__": app.run(host=config.get("APP_HOST","0.0.0.0"),port=int(config.get("APP_PORT","8000")))
