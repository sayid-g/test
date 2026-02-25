import requests
import json

def test_spec_info():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.autohome.com.cn/',
    })
    
    spec_id = 73339
    series_id = 5998
    
    print(f"测试车型信息API...")
    
    urls = [
        f"https://www.autohome.com.cn/ashx/series/spec-{series_id}-{spec_id}.ashx",
        f"https://www.autohome.com.cn/ashx/series/GetSeriesSpecList.ashx?seriesid={series_id}",
        f"https://www.autohome.com.cn/ashx/series/GetSpecList.ashx?seriesid={series_id}",
        f"https://car.autohome.com.cn/javascript/NewSpecCompare.js",
    ]
    
    for url in urls:
        print(f"\n尝试: {url}")
        response = session.get(url, timeout=15)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            text = response.text[:1500]
            print(f"响应: {text}")
    
    print("\n" + "="*60)
    print("测试车型配置页面...")
    url = f"https://www.autohome.com.cn/spec/{spec_id}/#pvareaid=2042006"
    print(f"URL: {url}")
    response = session.get(url, timeout=15)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"响应片段: {response.text[:2000]}")

if __name__ == '__main__':
    test_spec_info()
