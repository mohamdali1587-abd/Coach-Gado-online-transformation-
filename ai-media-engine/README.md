# Coach Gado AI Media Engine
Standalone daily Instagram Reels pipeline. Independent from all existing Coach Gado apps, databases, Vercel and Supabase projects.

## Features
- Generates Egyptian Arabic fitness/nutrition scripts and captions using an OpenAI-compatible API.
- Creates Egyptian Arabic voiceover using Edge TTS.
- Renders vertical 1080x1920 MP4 from your licensed clips using FFmpeg.
- Keeps production history in its own SQLite database.
- Optional Instagram Graph API Reels publishing.
- Manual dashboard and daily GitHub Actions workflow.

## Requirements before live use
- AI API key and model endpoint.
- FFmpeg.
- Your own/licensed clips in `assets/clips/`.
- For live Instagram: professional Instagram account linked to a Facebook Page, Meta app, publishing permissions, long-lived token and Instagram Business Account ID.
- A public HTTPS video host for the MP4 before Meta can ingest it.

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env; add licensed clips to assets/clips/
python -m app.main
```
Open http://127.0.0.1:8000.

Keep `PUBLISH_TO_INSTAGRAM=false` until a test Reel is reviewed. Never commit `.env` or access tokens.

## GitHub Actions
The included workflow runs daily at 07:00 UTC (09:00 Cairo in Egypt standard time; adjust seasonally). Add required values as GitHub repository secrets. For clips, provide `CLIPS_BASE64` as a base64 ZIP of licensed source clips. Generated MP4 is uploaded as a workflow artifact.

## Publishing
The publisher calls Meta Graph API `/{ig-user-id}/media` with `media_type=REELS`, then `/{container-id}/media_publish` after processing completes. Configure `PUBLIC_VIDEO_BASE_URL` and `PUBLIC_VIDEO_DIR` to a public HTTPS location containing the generated MP4. Verify current Meta permissions and API version before enabling.

## Known v1 scope
This is a functional starter pipeline, not a fully connected SaAS. It selects one of your supplied clips as the visual background and adds generated voiceover. It does not generate AI B-roll or burn Arabic subtitles into the video in v1. Instagram publishing requires external credentials and public video hosting.
