"""
@Author: Rohan Vetale

@Date: 2024-01-28 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-01-28 19:22

@Title : Fundoo Notes using FastAPI
"""
from fastapi import FastAPI, Security, Depends, Request
from fastapi.security import APIKeyHeader
from core.utils import jwt_authentication, request_loger
from routes.user import router_user
from routes.notes import router_notes
from routes.labels import router_labels


app = FastAPI()
@app.middleware("http")
def addmiddleware(request: Request, call_next):
    response = call_next(request)
    request_loger(request)
    return response

app.include_router(router_user, prefix='/user')
# app.include_router(router_notes,prefix='/notes',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])
app.include_router(router_notes,prefix='/notes',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])
#router_labels
app.include_router(router_labels, prefix='/labels',dependencies=[Security(APIKeyHeader(name='authorization')),Depends(jwt_authentication)])
