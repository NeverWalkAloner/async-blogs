#!/usr/bin/env bash

alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload