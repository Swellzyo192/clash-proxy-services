#!/usr/bin/env python3
"""
Простой конвертер aggregated_rules.json → clash_rules.yaml
"""

import json
import yaml

def main():
    print("🔄 Конвертируем JSON в правила Clash...")
    
    # Читаем JSON
    with open('aggregated_rules.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Создаём структуру для Clash
    clash_config = {
        'rules': []
    }
    
    # Добавляем direct правила (обычно их меньше, ставим первыми)
    for domain in data.get('direct', []):
        clash_config['rules'].append(f"DOMAIN-SUFFIX,{domain},DIRECT")
    
    # Добавляем proxy правила
    for domain in data.get('proxy', []):
        clash_config['rules'].append(f"DOMAIN-SUFFIX,{domain},Proxy")  # Proxy - имя вашего прокси в конфиге
    
    # Сохраняем в YAML
    with open('clash_rules.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(clash_config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ Готово! Создано {len(clash_config['rules'])} правил")
    print("📁 Файл: clash_rules.yaml")

if __name__ == '__main__':
    main()
