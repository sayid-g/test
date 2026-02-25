import requests
import json
import re
from bs4 import BeautifulSoup

def test_config_page():
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
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        text = response.text
        
        var_pattern = r'var config = ({.*?});'
        match = re.search(var_pattern, text, re.DOTALL)
        if match:
            print("\n找到config变量:")
            try:
                config = json.loads(match.group(1))
                print(f"config keys: {list(config.keys())[:10]}")
                if 'result' in config:
                    result = config['result']
                    print(f"result keys: {list(result.keys())[:10]}")
                    if 'paramtypeitems' in result:
                        params = result['paramtypeitems']
                        print(f"\n参数类型数量: {len(params)}")
                        for param in params[:3]:
                            print(f"  - {param.get('name', '')}: {list(param.keys())}")
            except:
                print(f"config内容片段: {match.group(1)[:500]}")
        
        spec_pattern = r'var spec = ({.*?});'
        match2 = re.search(spec_pattern, text, re.DOTALL)
        if match2:
            print("\n找到spec变量:")
            try:
                spec = json.loads(match2.group(1))
                print(f"spec keys: {list(spec.keys())[:10]}")
                if 'result' in spec:
                    result = spec['result']
                    print(f"result类型: {type(result)}")
                    if isinstance(result, list):
                        print(f"result长度: {len(result)}")
                        if result:
                            print(f"第一个元素: {json.dumps(result[0], ensure_ascii=False, indent=2)[:500]}")
            except:
                print(f"spec内容片段: {match2.group(1)[:500]}")
        
        print("\n查找所有var变量...")
        all_vars = re.findall(r'var\s+(\w+)\s*=\s*({[^;]+});', text[:10000])
        for var_name, var_value in all_vars[:5]:
            print(f"  - {var_name}: {var_value[:100]}...")

if __name__ == '__main__':
    test_config_page()
