"""
@Author: Rohan Vetale

@Date: 2024-01-28 19:44

@Last Modified by: Rohan Vetale

@Last Modified time: 2024-01-28 19:22

@Title : Fundoo Notes using FastAPI
"""
from fastapi import FastAPI, Security, Depends, Request
from fastapi.security import APIKeyHeader
from routes.user import router_user
from routes.notes import router_notes
import warnings

app = FastAPI()
app.include_router(router_user, prefix='/user')
app.include_router(router_notes, prefix='/notes')
