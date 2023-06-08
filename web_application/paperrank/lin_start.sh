#!/bin/bash
echo "Ejecutando flask..."
if [ "$OS" == "Windows_NT" ]; then
  set FLASK_APP=app.py
else
  export FLASK_APP=app.py
fi
echo "Flask iniciado."
flask run

