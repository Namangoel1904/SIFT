#!/bin/bash
# Production start script for Render
# Uses PORT environment variable set by Render

exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}

