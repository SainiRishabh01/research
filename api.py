from fastapi import FastAPI
from utils import search_research_papers, summarize_paper, text_to_speech

app = FastAPI()

@app.get("/papers/{topic}")
def get_papers(topic: str):
    papers = search_research_papers(topic)
    for paper in papers:
        paper['summary'] = summarize_paper(paper['content'])
    return papers

@app.get("/tts/{text}")
def get_tts(text: str):
    audio_file = text_to_speech(text)
    return {"message": "TTS generated successfully", "audio_file": audio_file}
