import requests
import json
import re

def test_sales_name():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://car.autohome.com.cn/',
    })
    
    series_id = 5998
    url = f"https://car.autohome.com.cn/config/series/{series_id}.html"
    print(f"获取配置页面: {url}")
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
                        
                        for item in param_items:
                            item_name_raw = item.get('name', '')
                            item_name = re.sub(r'<[^>]+>', '', item_name_raw)
                            value_items = item.get('valueitems', [])
                            
                            if '车型' in item_name:
                                print(f"\n找到车型字段: {item_name}")
                                print(f"前3个值:")
                                for vi in value_items[:3]:
                                    spec_id = vi.get('specid', '')
                                    value_raw = vi.get('value', '')
                                    value = re.sub(r'<[^>]+>', '', value_raw)
                                    print(f"  spec_id={spec_id}, value={value}")

if __name__ == '__main__':
    test_sales_name()
