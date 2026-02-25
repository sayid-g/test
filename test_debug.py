import requests
import json
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://car.autohome.com.cn/',
})

series_id = '6388'

config_data = {}
url = f"https://car.autohome.com.cn/config/series/{series_id}.html"
print(f"获取配置页面: {url}")
response = session.get(url, timeout=15)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    text = response.text
    
    var_pattern = r'var config = ({.*?});'
    match = re.search(var_pattern, text, re.DOTALL)
    if match:
        config = json.loads(match.group(1))
        if 'result' in config:
            result = config['result']
            
            if 'paramtypeitems' in result:
                param_types = result['paramtypeitems']
                
                for param_type in param_types:
                    type_name = param_type.get('name', '')
                    param_items = param_type.get('paramitems', [])
                    
                    for item in param_items:
                        item_name_raw = item.get('name', '')
                        item_name = re.sub(r'<[^>]+>', '', item_name_raw)
                        value_items = item.get('valueitems', [])
                        
                        if not value_items:
                            continue
                        
                        print(f"\n检查字段: {item_name}")
                        
                        if '车型' in item_name or '销售' in item_name:
                            print(f"  匹配到销售名称字段!")
                            for vi in value_items[:3]:
                                spec_id = vi.get('specid', '')
                                value_raw = vi.get('value', '')
                                value = re.sub(r'<[^>]+>', '', value_raw)
                                print(f"    spec_id={spec_id}, value={value}")
                                if spec_id not in config_data:
                                    config_data[str(spec_id)] = {}
                                config_data[str(spec_id)]['sales_name'] = value
                        
                        if '排量' in item_name or 'mL' in item_name:
                            print(f"  匹配到排量字段!")
                            for vi in value_items[:3]:
                                spec_id = vi.get('specid', '')
                                value = vi.get('value', '')
                                print(f"    spec_id={spec_id}, value={value}")
                                if spec_id not in config_data:
                                    config_data[str(spec_id)] = {}
                                if 'displacement' not in config_data[str(spec_id)]:
                                    config_data[str(spec_id)]['displacement'] = value

print(f"\n最终config_data: {json.dumps(config_data, ensure_ascii=False, indent=2)[:500]}")
