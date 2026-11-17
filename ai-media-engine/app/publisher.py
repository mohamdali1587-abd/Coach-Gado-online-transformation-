import os,time,requests
from . import config
def publish_reel(video_path,caption):
    if not config.enabled("PUBLISH_TO_INSTAGRAM"): return "","draft_only"
    ig=config.get("INSTAGRAM_BUSINESS_ACCOUNT_ID"); token=config.get("META_ACCESS_TOKEN")
    base=config.get("PUBLIC_VIDEO_BASE_URL").rstrip("/"); folder=config.get("PUBLIC_VIDEO_DIR","").strip("/")
    if not all([ig,token,base,folder]): raise RuntimeError("Missing Instagram ID/token or public video hosting settings.")
    url=f"{base}/{folder}/{os.path.basename(video_path)}"; ver=config.get("META_GRAPH_API_VERSION","v23.0")
    api=f"https://graph.facebook.com/{ver}/{ig}"
    r=requests.post(api+"/media",data={"media_type":"REELS","video_url":url,"caption":caption,"access_token":token},timeout=60); r.raise_for_status()
    cid=r.json()["id"]
    for _ in range(30):
        s=requests.get(f"https://graph.facebook.com/{ver}/{cid}",params={"fields":"status_code","access_token":token},timeout=30); s.raise_for_status()
        status=s.json().get("status_code")
        if status=="FINISHED": break
        if status=="ERROR": raise RuntimeError("Meta Reel processing failed.")
        time.sleep(10)
    else: raise RuntimeError("Meta Reel processing timed out.")
    p=requests.post(api+"/media_publish",data={"creation_id":cid,"access_token":token},timeout=60); p.raise_for_status()
    return p.json().get("id",""),"published"
