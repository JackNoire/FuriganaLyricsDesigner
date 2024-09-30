from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import FileResponse

from sudachipy import dictionary
from JMdict_json import JMdict_json
from string_processing_utils import analyse_original_text

api = FastAPI()

sudachi_dict = dictionary.Dictionary()
jmdict_json = JMdict_json()

class AnalyzeRequest(BaseModel):
    string: str

@api.post("/analyze")
async def analyze(request: AnalyzeRequest):
    return analyse_original_text(request.string, sudachi_dict, jmdict_json)

app = FastAPI()

# For vue-project npm run dev
if False:
    origins = [
        "http://localhost:5173"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/api", api)
app.mount("/", StaticFiles(directory="static", html=True))

@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return FileResponse("static/index.html")
    else:
        # Just use FastAPI's built-in handler for other errors
        return await http_exception_handler(request, exc)
