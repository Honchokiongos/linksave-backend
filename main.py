from fastapi import FastAPI
from pydantic import BaseModel
from yt_dlp import YoutubeDL

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "LinkSave backend running"}

@app.post("/extract")
def extract_video(data: VideoRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "nocheckcertificate": True
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=False)

        formats = []

        for f in info.get("formats", []):
            if f.get("ext") == "mp4" and f.get("url"):
       formats.append({
    "quality": f.get("format_note", "unknown"),
    "url": f.get("url")
})

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats[:5]
        }

    except Exception as e:
        return {"error": str(e)}
