#!/bin/bash

source venv/bin/activate
echo "start auto scrawl novel from kyks"

for ((i=2000; i<4000; i++))
do
    export NOVEL_PAGE=$i
    python manage.py get_novel_from_kyks
done

echo "end auto scrawl novel from kyks"