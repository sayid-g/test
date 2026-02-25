import requests
import json
import re

def test_config_detail():
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
                
                print("speclist信息:")
                if 'speclist' in result:
                    speclist = result['speclist']
                    print(f"speclist长度: {len(speclist)}")
                    if speclist:
                        print(f"第一个spec: {json.dumps(speclist[0], ensure_ascii=False, indent=2)}")
                
                print("\n参数信息:")
                if 'paramtypeitems' in result:
                    params = result['paramtypeitems']
                    for param_type in params:
                        type_name = param_type.get('name', '')
                        param_items = param_type.get('paramitems', [])
                        print(f"\n{type_name}:")
                        for item in param_items[:5]:
                            item_name = item.get('name', '')
                            valueitems = item.get('valueitems', [])
                            if valueitems:
                                print(f"  {item_name}: {valueitems[0] if valueitems else 'N/A'}")

if __name__ == '__main__':
    test_config_detail()
