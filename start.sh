#!/usr/bin/env bash
# AIMATRY (AAK.AI) Local Launch Script
# Department of Computer Science & Engineering, NITRA Technical Campus

echo "============================================================="
echo "🧬 Launching AIMATRY: Materials Informatics & Polymer Designer"
echo "============================================================="

cd "$(dirname "$0")"

# Check dependencies
if ! command -v streamlit &> /dev/null; then
    echo "⚠️ Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

echo "🚀 Starting server on http://localhost:8501 ..."
echo "💡 Press Ctrl+C in this terminal window to stop the server."
echo ""

python3 run_app.py
