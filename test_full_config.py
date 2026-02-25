import requests
import json
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://car.autohome.com.cn/',
})

series_id = '6388'  # 问界M5
url = f"https://car.autohome.com.cn/config/series/{series_id}.html"
response = session.get(url, timeout=15)

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
                    print(f"\n{type_name}:")
                    param_items = param_type.get('paramitems', [])
                    
                    for item in param_items:
                        item_name_raw = item.get('name', '')
                        item_name = re.sub(r'<[^>]+>', '', item_name_raw)
                        value_items = item.get('valueitems', [])
                        
                        if value_items and len(value_items) > 0:
                            first_value = value_items[0]
                            spec_id = first_value.get('specid', '')
                            value_raw = first_value.get('value', '')
                            value = re.sub(r'<[^>]+>', '', value_raw)
                            print(f"  {item_name}: spec_id={spec_id}, value={value[:50]}")
