# Setup and launch
1. Install Python 3.11+ and FFmpeg.
2. Add 2-3 licensed vertical gym clips to `assets/clips/`.
3. Copy `.env.example` to `.env` and add `OPENAI_API_KEY`.
4. Run `pip install -r requirements.txt `then `python -m app.main`.
5. Open `http://localhost:8000` and generate a draft Reel.
6. Review the MP4 and caption.
7. Only then configure Meta credentials and set `PUBLISH_TO_INSTAGRAM=true`.

GitHub Actions secrets: OPENAI_API_KEY, optional OPENAI_BASE_URL OPENAI_MODEL, CLIPS_BASE64 (base64 zip of licensed clips), PUBLISH_TO_INSTAGRAM, INSTAGRAM_BUSINESS_ACCOUNT_ID, META ACCESS TOKEN, PUBLIC_VIDEO_BASE_URL PUBLIC_VIDEO_DIR.
