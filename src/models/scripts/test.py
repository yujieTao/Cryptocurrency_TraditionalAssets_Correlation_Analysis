import os
import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取 src 所在的目录
parent_dir = os.path.dirname(os.path.dirname(current_dir))

# 构造相对路径
data_path = os.path.join(parent_dir, 'data', 'processed_data', 'processed_data.csv')

# 加载数据并解析时间列为日期类型
data = pd.read_csv(data_path, index_col=0, parse_dates=True)

# 检查是否有缺失值
print("Missing values per column:")
print(data.isnull().sum())

# 填充缺失值（前向填充）
data = data.fillna(method='ffill').fillna(method='bfill')

# 检查时间范围是否对齐
print(f"Data index range: {data.index.min()} to {data.index.max()}")

# 归一化数据以解决波动范围差异问题
normalized_data = data / data.max()

# 初始化 VAR 模型
model = VAR(data)

# 选择最佳滞后阶数
lag_order = model.select_order()
print(lag_order.summary())

# 获取最佳滞后阶数
best_lag = lag_order.selected_orders['aic']
print(f"Best lag order: {best_lag}")

# 使用最佳滞后阶数拟合模型
var_result = model.fit(best_lag)

# 打印模型结果
print(var_result.summary())

# 检查 BTC 对其他变量的因果关系
for col in data.columns:
    if col != 'BTC':
        test = var_result.test_causality('BTC', col, kind='f')
        print(f"Causality of BTC on {col}:")
        print(test.summary())

# 绘制归一化后的时间序列图
plt.figure(figsize=(12, 6))
for col in normalized_data.columns:
    plt.plot(normalized_data.index, normalized_data[col], label=col)

# 设置 x 轴日期格式为年/月，并以月为单位递增
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # 每月显示一个标签

# 自动调整日期标签以避免重叠
plt.gcf().autofmt_xdate()

plt.legend()
plt.title('Normalized Asset Prices (BTC, AGG, GLD, SPY)')

# 保存图片到 output 目录
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，则创建
output_path = os.path.join(output_dir, 'normalized_asset_prices.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {output_path}")

# 显示图片
plt.show()
