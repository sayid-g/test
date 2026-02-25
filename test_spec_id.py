import requests
import json
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.autohome.com.cn/',
})

series_id = '6388'  # 问界M5

# 获取API返回的车型
url = f"https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value={series_id}"
response = session.get(url, timeout=15)

print("API返回的车型:")
if response.status_code == 200:
    data = response.json()
    if 'result' in data and 'yearitems' in data['result']:
        year_items = data['result']['yearitems']
        for year_item in year_items[:2]:
            year_name = year_item.get('name', '')
            print(f"\n{year_name}:")
            spec_items = year_item.get('specitems', [])
            for spec in spec_items[:3]:
                spec_id = spec.get('id', '')
                spec_name = spec.get('name', '')
                print(f"  spec_id={spec_id}, name={spec_name}")

print("\n" + "="*60)

# 获取配置页面的spec_id
url2 = f"https://car.autohome.com.cn/config/series/{series_id}.html"
response2 = session.get(url2, timeout=15)

if response2.status_code == 200:
    text = response2.text
    
    var_pattern = r'var spec = ({.*?});'
    match = re.search(var_pattern, text, re.DOTALL)
    if match:
        spec_data = json.loads(match.group(1))
        if 'result' in spec_data:
            result = spec_data['result']
            print("配置页面的spec_list:")
            if isinstance(result, list):
                for item in result[:5]:
                    specid = item.get('specid', '')
                    showstate = item.get('showstate', '')
                    specstate = item.get('specstate', '')
                    print(f"  specid={specid}, showstate={showstate}, specstate={specstate}")
