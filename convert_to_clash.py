#!/usr/bin/env python3
"""
Простой конвертер aggregated_rules.json → clash_rules.yaml
"""

import json
import yaml

def main():
    print("🔄 Конвертируем JSON в правила Clash...")
    
    # Читаем JSON
    try:
        with open('aggregated_rules.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON загружен, найдено direct: {len(data.get('direct', []))}, proxy: {len(data.get('proxy', []))}")
    except FileNotFoundError:
        print("❌ Файл aggregated_rules.json не найден!")
        return
    except json.JSONDecodeError:
        print("❌ Ошибка в формате JSON!")
        return
    
    # Создаём структуру для Clash
    clash_config = {
        'rules': []
    }
    
    # Добавляем direct правила
    for domain in data.get('direct', []):
        clash_config['rules'].append(f"DOMAIN-SUFFIX,{domain},DIRECT")
    
    # Добавляем proxy правила
    for domain in data.get('proxy', []):
        clash_config['rules'].append(f"DOMAIN-SUFFIX,{domain},Proxy")
    
    # Сохраняем в YAML
    try:
        with open('clash_rules.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(clash_config, f, allow_unicode=True, default_flow_style=False)
        print(f"✅ Готово! Создано {len(clash_config['rules'])} правил")
        print("📁 Файл: clash_rules.yaml")
        
        # Покажем первые несколько правил для проверки
        print("\n📋 Первые 5 правил:")
        for rule in clash_config['rules'][:5]:
            print(f"   {rule}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")

if __name__ == '__main__':
    main()
