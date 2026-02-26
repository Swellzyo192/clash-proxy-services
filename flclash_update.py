#!/usr/bin/env python3
"""
Скрипт для генерации flclash_rules.yaml из aggregated_rules.json и extra_domains.txt
"""

import json
import yaml
import os
from pathlib import Path

def load_json_rules(json_path):
    """Загружает правила из JSON файла"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Файл {json_path} не найден")
        return {"direct": [], "proxy": []}
    except json.JSONDecodeError:
        print(f"❌ Ошибка парсинга {json_path}")
        return {"direct": [], "proxy": []}

def load_extra_domains(txt_path):
    """Загружает дополнительные домены из текстового файла"""
    extra = {"direct": [], "proxy": []}
    
    if not os.path.exists(txt_path):
        print(f"ℹ️ Файл {txt_path} не найден, пропускаем")
        return extra
    
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            current_category = None
            for line in f:
                line = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                
                # Проверяем категории
                if line.lower() == '[direct]':
                    current_category = 'direct'
                    continue
                elif line.lower() == '[proxy]':
                    current_category = 'proxy'
                    continue
                
                # Добавляем домен в текущую категорию
                if current_category and line:
                    extra[current_category].append(line)
        
        print(f"✅ Загружено доп. доменов: direct={len(extra['direct'])}, proxy={len(extra['proxy'])}")
    except Exception as e:
        print(f"❌ Ошибка при чтении {txt_path}: {e}")
    
    return extra

def merge_rules(json_rules, extra_rules):
    """Объединяет правила из JSON и доп. домены, убирая дубликаты"""
    merged = {
        "direct": list(set(json_rules.get("direct", []) + extra_rules.get("direct", []))),
        "proxy": list(set(json_rules.get("proxy", []) + extra_rules.get("proxy", [])))
    }
    
    # Сортируем для красоты
    merged["direct"].sort()
    merged["proxy"].sort()
    
    print(f"📊 После объединения: direct={len(merged['direct'])}, proxy={len(merged['proxy'])}")
    return merged

def generate_yaml(rules, yaml_path):
    """Генерирует YAML файл для FlClash"""
    
    # Структура для FlClash
    flclash_config = {
        "payload": [
            # Сначала direct (обычно их меньше, удобнее проверять)
            {"DOMAIN-SUFFIX": domain} for domain in rules["direct"]
        ] + [
            # Потом proxy
            {"DOMAIN-SUFFIX": domain} for domain in rules["proxy"]
        ]
    }
    
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(flclash_config, f, allow_unicode=True, sort_keys=False)
        print(f"✅ YAML файл создан: {yaml_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании YAML: {e}")
        return False

def main():
    print("🚀 Запуск генерации FlClash правил...")
    
    # Пути к файлам
    base_dir = Path(__file__).parent
    json_path = base_dir / "aggregated_rules.json"
    txt_path = base_dir / "extra_domains.txt"
    yaml_path = base_dir / "flclash_rules.yaml"
    
    # Загружаем правила
    json_rules = load_json_rules(json_path)
    extra_rules = load_extra_domains(txt_path)
    
    # Объединяем
    merged_rules = merge_rules(json_rules, extra_rules)
    
    # Генерируем YAML
    success = generate_yaml(merged_rules, yaml_path)
    
    if success:
        print("🎉 Готово! Файл flclash_rules.yaml создан/обновлён")
    else:
        print("❌ Что-то пошло не так")
        exit(1)

if __name__ == "__main__":
    main()
