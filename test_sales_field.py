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
                    param_items = param_type.get('paramitems', [])
                    
                    for item in param_items:
                        item_name_raw = item.get('name', '')
                        item_name = re.sub(r'<[^>]+>', '', item_name_raw)
                        
                        if '车型' in item_name:
                            print(f"\n找到车型字段: {item_name}")
                            print(f"  完整字段名: {item_name_raw}")
                            value_items = item.get('valueitems', [])
                            print(f"  valueitems数量: {len(value_items)}")
                            
                            if value_items:
                                for i, vi in enumerate(value_items[:5]):
                                    spec_id = vi.get('specid', '')
                                    value_raw = vi.get('value', '')
                                    value = re.sub(r'<[^>]+>', '', value_raw)
                                    sublist = vi.get('sublist', [])
                                    print(f"  [{i}] spec_id={spec_id}, value={value}, sublist长度={len(sublist)}")
