from spider import AutohomeSpider

spider = AutohomeSpider()

# 测试问界M5
series_id = '6388'
brand_name = 'AITO 问界'
series_name = '问界M5'

print(f"测试问界M5 (series_id={series_id})...")
cars = spider.get_cars_by_series(series_id, brand_name, series_name)

print(f"获取到 {len(cars)} 个车型")
for car in cars[:5]:
    print(f"\n车型: {car.model}")
    print(f"  销售名称: {car.sales_name}")
    print(f"  排量: {car.displacement}")
    print(f"  能源类型: {car.energy_type}")
