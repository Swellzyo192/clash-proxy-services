#!/usr/bin/env python3
"""
Генератор полноценного конфига Clash с балансировкой
Использует aggregated_rules.json для правил
"""

import json
import yaml
from datetime import datetime

def generate_clash_config():
    print("🔄 Генерация Clash конфига с балансировкой...")
    
    # Читаем JSON с правилами
    with open('aggregated_rules.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    direct_domains = data.get('direct', [])
    proxy_domains = data.get('proxy', [])
    
    print(f"📊 Загружено: DIRECT={len(direct_domains)}, PROXY={len(proxy_domains)}")
    
    # Базовый конфиг
    config = {
        "port": 7890,
        "socks-port": 7891,
        "allow-lan": true,
        "mode": "rule",
        "log-level": "info",
        "external-controller": "127.0.0.1:9090",
        
        # Прокси-серверы (ЗАМЕНИТЕ НА СВОИ!)
        "proxies": [
            {
                "name": "SERVER1",
                "type": "vmess",
                "server": "server1.example.com",
                "port": 443,
                "uuid": "your-uuid-here",
                "alterId": 0,
                "cipher": "auto",
                "tls": true,
                "skip-cert-verify": true,
                "network": "ws",
                "ws-path": "/path",
                "ws-headers": {
                    "Host": "server1.example.com"
                }
            },
            {
                "name": "SERVER2",
                "type": "vmess",
                "server": "server2.example.com",
                "port": 443,
                "uuid": "your-uuid-here",
                "alterId": 0,
                "cipher": "auto",
                "tls": true,
                "skip-cert-verify": true,
                "network": "ws",
                "ws-path": "/path",
                "ws-headers": {
                    "Host": "server2.example.com"
                }
            },
            {
                "name": "SERVER3",
                "type": "vmess",
                "server": "server3.example.com",
                "port": 443,
                "uuid": "your-uuid-here",
                "alterId": 0,
                "cipher": "auto",
                "tls": true,
                "skip-cert-verify": true,
                "network": "ws",
                "ws-path": "/path",
                "ws-headers": {
                    "Host": "server3.example.com"
                }
            },
            {
                "name": "SERVER4",
                "type": "vmess",
                "server": "server4.example.com",
                "port": 443,
                "uuid": "your-uuid-here",
                "alterId": 0,
                "cipher": "auto",
                "tls": true,
                "skip-cert-verify": true,
                "network": "ws",
                "ws-path": "/path",
                "ws-headers": {
                    "Host": "server4.example.com"
                }
            }
        ],
        
        # Прокси-группы
        "proxy-groups": [
            {
                "name": "🚀 LOAD_BALANCE",
                "type": "load-balance",
                "proxies": ["SERVER1", "SERVER2", "SERVER3", "SERVER4"],
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "strategy": "round-robin"  # round-robin или consistent-hashing
            },
            {
                "name": "🎯 SELECTOR",
                "type": "select",
                "proxies": [
                    "🚀 LOAD_BALANCE",
                    "SERVER1",
                    "SERVER2",
                    "SERVER3",
                    "SERVER4",
                    "DIRECT"
                ]
            },
            {
                "name": "🌍 DIRECT",
                "type": "select",
                "proxies": ["DIRECT"]
            }
        ],
        
        # Правила
        "rules": []
    }
    
    # Добавляем DIRECT правила (из aggregated_rules.json)
    for domain in direct_domains:
        config["rules"].append(f"DOMAIN-SUFFIX,{domain},🌍 DIRECT")
    
    # Добавляем PROXY правила (все через балансировку)
    for domain in proxy_domains:
        config["rules"].append(f"DOMAIN-SUFFIX,{domain},🚀 LOAD_BALANCE")
    
    # Добавляем стандартные правила
    config["rules"].extend([
        # LAN
        "IP-CIDR,192.168.0.0/16,🌍 DIRECT",
        "IP-CIDR,10.0.0.0/8,🌍 DIRECT", 
        "IP-CIDR,172.16.0.0/12,🌍 DIRECT",
        
        # Гео-правила
        "GEOIP,CN,🌍 DIRECT",
        "GEOSITE,CN,🌍 DIRECT",
        
        # Всё остальное
        "MATCH,🎯 SELECTOR"
    ])
    
    # Сохраняем
    output_file = "clash_config.yaml"
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Конфиг создан: {output_file}")
    print(f"📊 Всего правил: {len(config['rules'])}")
    
    # Считаем статистику
    balance_rules = sum(1 for r in config["rules"] if "🚀 LOAD_BALANCE" in r)
    direct_rules = sum(1 for r in config["rules"] if "🌍 DIRECT" in r)
    print(f"📈 Правил через балансировку: {balance_rules}")
    print(f"📉 Прямых правил: {direct_rules}")

if __name__ == "__main__":
    generate_clash_config()
