from spider import AutohomeSpider

spider = AutohomeSpider()

# 测试问界M5
series_id = '6388'

print(f"测试配置数据获取 (series_id={series_id})...")
config_data = spider._get_series_config(series_id)

print(f"配置数据大小: {len(config_data)}")
print("前5个配置数据:")
for spec_id, config in list(config_data.items())[:5]:
    print(f"  spec_id={spec_id}: {config}")
