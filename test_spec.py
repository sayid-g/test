import requests
import json

def test_spec_detail():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.autohome.com.cn/',
    })
    
    spec_id = 73339
    print(f"测试车型详情API (车型ID: {spec_id})...")
    
    urls = [
        f"https://www.autohome.com.cn/ashx/spec/GetSpecDetail.ashx?specid={spec_id}",
        f"https://www.autohome.com.cn/ashx/spec/GetSpecConfigBySpecId.ashx?specid={spec_id}",
        f"https://www.autohome.com.cn/ashx/spec/GetSpecParamBySpecId.ashx?specid={spec_id}",
        f"https://www.autohome.com.cn/ashx/spec/GetSpecParameterBySpecId.ashx?specid={spec_id}",
    ]
    
    for url in urls:
        print(f"\n尝试: {url}")
        response = session.get(url, timeout=15)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.text[:500]}")
    
    print("\n" + "="*60)
    print("测试另一个API...")
    url = "https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=6&value=73339"
    print(f"URL: {url}")
    response = session.get(url, timeout=15)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"响应: {response.text[:2000]}")

if __name__ == '__main__':
    test_spec_detail()
