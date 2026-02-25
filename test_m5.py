import requests
import json
import re

def test_m5_config():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://car.autohome.com.cn/',
    })
    
    series_id = 6388
    url = f"https://car.autohome.com.cn/config/series/{series_id}.html"
    print(f"获取问界M5配置页面: {url}")
    response = session.get(url, timeout=15)
    
    if response.status_code == 200:
        text = response.text
        
        var_pattern = r'var config = ({.*?});'
        match = re.search(var_pattern, text, re.DOTALL)
        if match:
            config = json.loads(match.group(1))
            if 'result' in config:
                result = config['result']
                
                print("查找销售名称字段...")
                if 'paramtypeitems' in result:
                    params = result['paramtypeitems']
                    for param_type in params:
                        type_name = param_type.get('name', '')
                        param_items = param_type.get('paramitems', [])
                        
                        print(f"\n{type_name}:")
                        for item in param_items[:5]:
                            item_name_raw = item.get('name', '')
                            item_name = re.sub(r'<[^>]+>', '', item_name_raw)
                            value_items = item.get('valueitems', [])
                            
                            if value_items:
                                first_value = value_items[0] if value_items else {}
                                spec_id = first_value.get('specid', '')
                                value_raw = first_value.get('value', '')
                                value = re.sub(r'<[^>]+>', '', value_raw)
                                print(f"  {item_name}: spec_id={spec_id}, value={value[:50] if value else 'N/A'}")

if __name__ == '__main__':
    test_m5_config()
