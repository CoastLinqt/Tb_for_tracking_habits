#!/bin/bash

cd src

alembic upgrade head


uvicorn main:app --host 0.0.0.0