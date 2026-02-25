import requests
import json

def test_detail_api():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.autohome.com.cn/',
    })
    
    series_id = 5998
    print(f"测试车型API完整数据 (车系ID: {series_id})...")
    
    url = f"https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value={series_id}"
    response = session.get(url, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        if 'result' in data and 'yearitems' in data['result']:
            year_items = data['result']['yearitems']
            if year_items:
                print(f"\n年款数据结构:")
                print(json.dumps(year_items[0], ensure_ascii=False, indent=2))
                
                if year_items[0].get('specitems'):
                    print(f"\n车型数据结构:")
                    print(json.dumps(year_items[0]['specitems'][0], ensure_ascii=False, indent=2))
    
    print("\n" + "="*60)
    spec_id = 73339
    print(f"测试车型详情API (车型ID: {spec_id})...")
    
    url2 = f"https://www.autohome.com.cn/ashx/spec/specparams.ashx?seriesid={series_id}&specid={spec_id}"
    response2 = session.get(url2, timeout=15)
    print(f"状态码: {response2.status_code}")
    if response2.status_code == 200:
        print(f"响应: {response2.text[:2000]}")
    
    print("\n" + "="*60)
    url3 = f"https://car.autohome.com.cn/config/spec/{spec_id}"
    print(f"测试车型配置页面...")
    response3 = session.get(url3, timeout=15)
    print(f"状态码: {response3.status_code}")
    if response3.status_code == 200:
        print(f"响应片段: {response3.text[:1500]}")

if __name__ == '__main__':
    test_detail_api()
