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
    return templates.TemplateResponse('config.html', {'request': request, 'cfg': cfg})


@app.post('/config')
async def save_config(request: Request):
    cfg_data = await request.form()
    _save_config(cfg_data)
    return RedirectResponse(url="/config", status_code=303)


@app.get('/history', response_class=HTMLResponse)
async def history(request: Request):
    keep_last_50_records()
    hsy = HistoryModel.select()
    return templates.TemplateResponse('history.html', {
        'request': request,
        'history': hsy
    })


def _save_config(cfg_data):
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


def keep_last_50_records():
    total_count = HistoryModel.select().count()
    if total_count > 50:
        query = HistoryModel.delete().where(HistoryModel.id.in_(
            HistoryModel.select(HistoryModel.id).order_by(HistoryModel.create_time).limit(total_count - 50)
        ))
        query.execute()


def start_web():
    SqliteDB.connect()
    SqliteDB.create_tables([ConfigModel, HistoryModel])
    uvicorn.run('backend.web:app', port=SETTINGS_PORT, host=SETTINGS_HOST, reload=False)
