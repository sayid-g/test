import argparse
import pandas as pd
from datetime import datetime
from spider import AutohomeSpider
from models import CarInfo


def save_to_excel(cars: list, filename: str = None):
    if not filename:
        filename = f"cars_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    data = [car.to_dict() for car in cars]
    df = pd.DataFrame(data)
    
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"数据已保存到: {filename}")
    return filename


def save_to_csv(cars: list, filename: str = None):
    if not filename:
        filename = f"cars_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    data = [car.to_dict() for car in cars]
    df = pd.DataFrame(data)
    
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"数据已保存到: {filename}")
    return filename


def main():
    parser = argparse.ArgumentParser(description='汽车之家车辆信息爬虫')
    parser.add_argument('--max-brands', type=int, default=None, help='最大爬取品牌数量（用于测试）')
    parser.add_argument('--output', type=str, default='excel', choices=['excel', 'csv'], help='输出格式')
    parser.add_argument('--filename', type=str, default=None, help='输出文件名')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("汽车之家车辆信息爬虫")
    print("=" * 60)
    
    spider = AutohomeSpider()
    
    cars = spider.crawl_all_cars(max_brands=args.max_brands)
    
    if cars:
        if args.output == 'excel':
            save_to_excel(cars, args.filename)
        else:
            save_to_csv(cars, args.filename)
        
        print("\n" + "=" * 60)
        print("爬取统计:")
        print(f"  总车型数: {len(cars)}")
        
        brands = set(car.brand for car in cars)
        print(f"  品牌数: {len(brands)}")
        
        series = set((car.brand, car.series) for car in cars)
        print(f"  车系数: {len(series)}")
        print("=" * 60)
    else:
        print("未获取到任何车辆信息")


if __name__ == '__main__':
    main()
