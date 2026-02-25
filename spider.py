import requests
from bs4 import BeautifulSoup
import time
import json
import re
from typing import List, Dict, Optional
from models import CarInfo


class AutohomeSpider:
    def __init__(self):
        self.base_url = "https://car.autohome.com.cn"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.autohome.com.cn/',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_brands(self) -> List[Dict]:
        url = "https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=1"
        brands = []
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'branditems' in data['result']:
                    for item in data['result']['branditems']:
                        brand_id = item.get('id', '')
                        if isinstance(brand_id, int):
                            brand_id = str(brand_id)
                        brands.append({
                            'id': brand_id,
                            'name': item.get('name', ''),
                            'letter': item.get('bfirstletter', '')
                        })
            
            if not brands:
                brands = self._get_brands_from_api_v2()
            
            return brands
        except Exception as e:
            print(f"获取品牌列表失败: {e}")
            return self._get_brands_from_api_v2()
    
    def _get_brands_from_api_v2(self) -> List[Dict]:
        url = "https://car.autohome.com.cn/javascript/NewSpecCompare.js"
        brands = []
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                text = response.text
                brand_pattern = r'var listCompare\s*=\s*(\[.*?\]);'
                match = re.search(brand_pattern, text, re.DOTALL)
                if match:
                    try:
                        data = json.loads(match.group(1))
                        for item in data:
                            if 'id' in item and 'name' in item:
                                brands.append({
                                    'id': str(item.get('id', '')),
                                    'name': item.get('name', ''),
                                    'letter': item.get('letter', '')
                                })
                    except json.JSONDecodeError as e:
                        print(f"JSON解析失败: {e}")
            
            if not brands:
                brands = self._get_brands_from_page()
            
            return brands
        except Exception as e:
            print(f"从API v2获取品牌列表失败: {e}")
            return self._get_brands_from_page()
    
    def _get_brands_from_page(self) -> List[Dict]:
        url = "https://www.autohome.com.cn/car/"
        brands = []
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                brand_items = soup.select('.cartree-letter .list-dl')
                
                for item in brand_items:
                    links = item.select('dt a')
                    for link in links:
                        brand_name = link.get_text(strip=True)
                        brand_url = link.get('href', '')
                        brand_id = ''
                        if brand_url:
                            match = re.search(r'/(\d+)/', brand_url)
                            if match:
                                brand_id = match.group(1)
                        
                        if brand_name and brand_id:
                            brands.append({
                                'id': brand_id,
                                'name': brand_name,
                                'url': brand_url
                            })
            
            return brands
        except Exception as e:
            print(f"从页面获取品牌列表失败: {e}")
            return []
    
    def get_series_by_brand(self, brand_id) -> List[Dict]:
        brand_id = str(brand_id)
        url = f"https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=3&value={brand_id}"
        series_list = []
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    if isinstance(result_data, dict) and 'factoryitems' in result_data:
                        factory_items = result_data['factoryitems']
                        if isinstance(factory_items, list):
                            for factory in factory_items:
                                if isinstance(factory, dict):
                                    factory_name = factory.get('name', '')
                                    series_items = factory.get('seriesitems', [])
                                    if isinstance(series_items, list):
                                        for series in series_items:
                                            if isinstance(series, dict):
                                                series_id = series.get('id', '')
                                                series_name = series.get('name', '')
                                                if series_id and series_name:
                                                    series_list.append({
                                                        'id': str(series_id),
                                                        'name': series_name,
                                                        'brand_id': brand_id,
                                                        'factory': factory_name,
                                                        'year': ''
                                                    })
            
            if not series_list:
                series_list = self._get_series_by_brand_from_page(brand_id)
            
            return series_list
        except Exception as e:
            print(f"获取品牌 {brand_id} 的车系列表失败: {e}")
            return self._get_series_by_brand_from_page(brand_id)
    
    def _get_series_by_brand_from_page(self, brand_id: str) -> List[Dict]:
        if not brand_id:
            return []
        
        first_letter = brand_id[0].upper() if brand_id else 'A'
        url = f"https://www.autohome.com.cn/grade/carhtml/{first_letter}/{brand_id}.html"
        series_list = []
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                rows = soup.select('tr')
                
                current_series = None
                for row in rows:
                    series_cell = row.select_one('td[valign="top"] a')
                    if series_cell:
                        series_name = series_cell.get_text(strip=True)
                        series_url = series_cell.get('href', '')
                        series_id = ''
                        if series_url:
                            match = re.search(r'/(\d+)/', series_url)
                            if match:
                                series_id = match.group(1)
                        
                        if series_name and series_id:
                            current_series = {
                                'id': series_id,
                                'name': series_name,
                                'brand_id': brand_id
                            }
                    
                    year_cells = row.select('td[valign="top"]:not(:first-child)')
                    for cell in year_cells:
                        year_link = cell.select_one('a')
                        if year_link and current_series:
                            year_text = year_link.get_text(strip=True)
                            year_url = year_link.get('href', '')
                            
                            series_info = current_series.copy()
                            series_info['year'] = year_text
                            series_info['year_url'] = year_url
                            series_list.append(series_info)
            
            return series_list
        except Exception as e:
            print(f"从页面获取品牌 {brand_id} 的车系列表失败: {e}")
            return []
    
    def _get_series_config(self, series_id: str) -> Dict:
        if not series_id:
            return {}
        
        series_id = str(series_id)
        url = f"https://car.autohome.com.cn/config/series/{series_id}.html"
        config_data = {}
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
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
                            ## 打印param_types
                            print(f"param_types: {param_types}")
                            
                            for param_type in param_types:
                                type_name = param_type.get('name', '')
                                param_items = param_type.get('paramitems', [])
                                
                                for item in param_items:
                                    item_name_raw = item.get('name', '')
                                    item_name = re.sub(r'<[^>]+>', '', item_name_raw)
                                    ##
                                


                                    value_items = item.get('valueitems', [])
                                    
                                    if not value_items:
                                        continue
                                    
                                    if '车型' in item_name or '销售' in item_name:
                                        # 打印item_name和value_items
                                        print(f"item_name: {item_name}, value_items: {value_items}")
                                        for vi in value_items:
                                            spec_id = vi.get('specid', '')
                                            value_raw = vi.get('value', '')
                                            value = re.sub(r'<[^>]+>', '', value_raw)
                                            if str(spec_id) not in config_data:
                                                config_data[str(spec_id)] = {}
                                            config_data[str(spec_id)]['sales_name'] = value
                                    
                                    # 只匹配发动机部分的排量字段
                                    if ('排量' in item_name or '(L)' in item_name) and '发动机' in type_name:
                                        for vi in value_items:
                                            spec_id = vi.get('specid', '')
                                            value = vi.get('value', '')
                                            if str(spec_id) not in config_data:
                                                config_data[str(spec_id)] = {}
                                            config_data[str(spec_id)]['displacement'] = value
                                    
                                    if '能源类型' in item_name:
                                        for vi in value_items:
                                            spec_id = vi.get('specid', '')
                                            value = vi.get('value', '')
                                            if str(spec_id) not in config_data:
                                                config_data[str(spec_id)] = {}
                                            config_data[str(spec_id)]['energy_type'] = value
            
            return config_data
        except Exception as e:
            print(f"获取车系 {series_id} 的配置信息失败: {e}")
            return {}
    
    def get_cars_by_series(self, series_id: str, brand_name: str = '', series_name: str = '', year: str = '') -> List[CarInfo]:
        if not series_id:
            return []
        
        series_id = str(series_id)
        url = f"https://www.autohome.com.cn/ashx/AjaxIndexCarFind.ashx?type=5&value={series_id}"
        cars = []
        
        config_data = self._get_series_config(series_id)
        
        try:
            response = self.session.get(url, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'yearitems' in data['result']:
                    year_items = data['result']['yearitems']
                    if isinstance(year_items, list):
                        for year_item in year_items:
                            if isinstance(year_item, dict):
                                year_name = year_item.get('name', '')
                                spec_items = year_item.get('specitems', [])
                                
                                if isinstance(spec_items, list):
                                    for spec in spec_items:
                                        if isinstance(spec, dict):
                                            spec_id = spec.get('id', '')
                                            spec_name = spec.get('name', '')
                                            min_price = spec.get('minprice', 0)
                                            max_price = spec.get('maxprice', 0)
                                            
                                            if spec_id and spec_name:
                                                price = ''
                                                if min_price and max_price:
                                                    if min_price == max_price:
                                                        price = f"{min_price/10000:.2f}万"
                                                    else:
                                                        price = f"{min_price/10000:.2f}-{max_price/10000:.2f}万"
                                                elif min_price:
                                                    price = f"{min_price/10000:.2f}万起"
                                                
                                                spec_config = config_data.get(str(spec_id), {})
                                                sales_name = spec_config.get('sales_name', '')
                                                displacement = spec_config.get('displacement', '')
                                                energy_type = spec_config.get('energy_type', '')
                                                
                                                car = CarInfo(
                                                    car_id=str(spec_id),
                                                    brand=brand_name,
                                                    series=series_name,
                                                    year=year_name,
                                                    model=spec_name,
                                                    price=price,
                                                    sales_name=sales_name,
                                                    displacement=displacement,
                                                    energy_type=energy_type
                                                )
                                                cars.append(car)
            
            return cars
        except Exception as e:
            print(f"获取车系 {series_id} 的车型列表失败: {e}")
            return []
    
    def crawl_all_cars(self, max_brands: Optional[int] = None) -> List[CarInfo]:
        all_cars = []
        
        print("正在获取品牌列表...")
        brands = self.get_brands()
        
        if max_brands:
            brands = brands[:max_brands]
        
        print(f"共找到 {len(brands)} 个品牌")
        
        for i, brand in enumerate(brands):
            print(f"\n[{i+1}/{len(brands)}] 正在处理品牌: {brand['name']}")
            
            series_list = self.get_series_by_brand(brand['id'])
            print(f"  找到 {len(series_list)} 个车系")
            
            processed_series = set()
            for j, series in enumerate(series_list):
                series_key = series['id']
                if series_key in processed_series:
                    continue
                processed_series.add(series_key)
                
                print(f"  [{j+1}/{len(series_list)}] 正在处理车系: {series['name']} - {series.get('year', '')}")
                
                cars = self.get_cars_by_series(
                    series['id'],
                    brand['name'],
                    series['name'],
                    series.get('year', '')
                )
                
                all_cars.extend(cars)
                print(f"    获取到 {len(cars)} 个车型")
                
                time.sleep(0.3)
            
            time.sleep(0.5)
        
        print(f"\n爬取完成，共获取 {len(all_cars)} 个车型信息")
        return all_cars
