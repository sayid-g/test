import requests
import json

def test_car_config():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://car.autohome.com.cn/',
    })
    
    spec_id = 73339
    series_id = 5998
    
    print(f"测试车型配置API...")
    
    urls = [
        f"https://car.autohome.com.cn/config/spec/{spec_id}",
        f"https://car.autohome.com.cn/javascript/NewSpecCompare.js",
        f"https://car.autohome.com.cn/dealer/spec/{spec_id}",
    ]
    
    for url in urls:
        print(f"\n尝试: {url}")
        try:
            response = session.get(url, timeout=15)
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                if 'javascript' in url:
                    import re
                    text = response.text
                    
                    spec_pattern = f'"I":{spec_id}[^}}]+}}'
                    match = re.search(spec_pattern, text)
                    if match:
                        print(f"找到车型数据: {match.group()[:500]}")
                    
                    all_specs = re.findall(r'"I":(\d+),"N":"([^"]+)"', text)
                    print(f"找到 {len(all_specs)} 个车型")
                    if all_specs:
                        print(f"前5个: {all_specs[:5]}")
                else:
                    print(f"响应片段: {response.text[:1000]}")
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n" + "="*60)
    print("测试车型参数API...")
    url = f"https://car.autohome.com.cn/config/series/{series_id}.html"
    print(f"URL: {url}")
    response = session.get(url, timeout=15)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"响应片段: {response.text[:2000]}")

if __name__ == '__main__':
    test_car_config()
