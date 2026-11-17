import asyncio,glob,os,random,subprocess
from pathlib import Path
import edge_tts
from . import config
def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-2500:])
async def voice(text,path):
    await edge_tts.Communicate(text,config.get("TTS_VOICE","ar-EG-ShakirNeural")).save(str(path))
def render_reel(narration):
    clips=glob.glob(config.get("CLIPS_DIR","assets/clips")+"/*.mp4")+glob.glob(config.get("CLIPS_DIR","assets/clips")+"/*.mov")
    if not clips: raise RuntimeError("Add licensed .mp4/.mov footage to assets/clips/ first.")
    out=Path(config.get("OUTPUT_DIR","output")); out.mkdir(parents=True,exist_ok=True)
    audio=out/"voice.mp3"; asyncio.run(voice(narration,audio)); source=random.choice(clips); final=out/"coach-gado-daily-reel.mp4"
    w=config.get("VIDEO_WIDTH","1080"); h=config.get("VIDEO_HEIGHT","1920"); fps=config.get("VIDEO_FPS","30")
    run(["ffmpeg","-y","-stream_loop","-1","-i",source,"-i",str(audio),"-t",str(config.get("REEL_DURATION_SECONDS","35")),
      "-vf",f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps={fps},format=yuv420p",
      "-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","veryfast","-crf","22","-c:a","aac","-b:a","160k",
      "-shortest","-movflags","+faststart",str(final)])
    return str(final)
