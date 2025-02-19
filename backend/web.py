import os

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from backend import *

SETTINGS_HOST = 'localhost'
SETTINGS_PORT = 17888
work_path = os.getcwd()
app = FastAPI()

templates = Jinja2Templates(work_path + '/backend/templates')
app.mount('/static', StaticFiles(directory=work_path + '/backend/templates'), name='static')


@app.get('/config', response_class=HTMLResponse)
async def config(request: Request):
    cfg = ConfigModel.select().first()
    if cfg:
        return templates.TemplateResponse('config.html', {'request': request, 'cfg': cfg})
    else:
        return templates.TemplateResponse('config.html', {'request': request, 'cfg': None})


@app.post('/config')
async def index(request: Request):
    cfg_data = await request.form()
    cfg = ConfigModel.select().first()
    if cfg:
        cfg.base_url = cfg_data['base_url']
        cfg.api_key = cfg_data['api_key']
        cfg.model = cfg_data['model']
        cfg.button_time = cfg_data['button_time']
        cfg.button_select = cfg_data['button_select']
        cfg.save()
    else:
        ConfigModel.create(base_url=cfg_data['base_url'], api_key=cfg_data['api_key'], model=cfg_data['model'],
                           button_time=cfg_data['button_time'], button_select=cfg_data['button_select'])
    return RedirectResponse(url="/config", status_code=303)


@app.get('/history', response_class=HTMLResponse)
async def history(request: Request):
    keep_last_50_records()
    hsy = HistoryModel.select()
    return templates.TemplateResponse('history.html', {
        'request': request,
        'history': hsy
    })


def keep_last_50_records():
    total_count = HistoryModel.select().count()
    if total_count > 50:
        records_to_delete = total_count - 50
        query = HistoryModel.select().order_by(HistoryModel.create_time).limit(records_to_delete)
        query.delete().execute()


def start_web():
    SqliteDB.connect()
    SqliteDB.create_tables([ConfigModel, HistoryModel])
    uvicorn.run('backend.web:app', port=SETTINGS_PORT, host=SETTINGS_HOST, reload=False)
