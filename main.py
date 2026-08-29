from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from api.routes import router
from config.settings import settings

app=FastAPI(title=settings.app_name,description="RoboLab | SynapseX Robotics & Technologies",version="2.0.0")
app.add_middleware(SessionMiddleware,secret_key=settings.secret_key,same_site="lax",https_only=False,max_age=60*60*24*7)
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
app.mount("/static",StaticFiles(directory="web/static"),name="static")

@app.get("/",include_in_schema=False)
def home(): return FileResponse("web/templates/index.html")
@app.get("/health",include_in_schema=False)
def health(): return {"status":"healthy","service":settings.app_name,"version":app.version}
