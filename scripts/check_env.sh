#!/bin/bash
echo "Проверка окружения..."
python --version
echo "Python установлен"
pip list | grep -q pytest && echo "pytest установлен" || echo "pytest не установлен (pip install pytest)"
echo "Текущая директория: $(pwd)"
