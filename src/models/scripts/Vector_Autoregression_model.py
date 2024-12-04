import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

# 检查平稳性
def check_stationarity(series, name="Time Series"):
    try:
        result = adfuller(series)
        print(f"{name} ADF Statistic: {result[0]}")
        print(f"{name} p-value: {result[1]}")
        if result[1] < 0.05:
            print(f"{name} is stationary.")
        else:
            print(f"{name} is not stationary. Consider differencing.")
    except Exception as e:
        print(f"Error checking stationarity for {name}: {e}")

# 构建 VAR 模型
def build_var_model(data, lags=5):
    model = VAR(data)
    var_result = model.fit(lags)
    print(var_result.summary())
    return var_result

# 选择滞后期
def select_lag(data):
    model = VAR(data)
    lag_order = model.select_order(maxlags=10)
    print("Optimal Lag Order:")
    print(lag_order.summary())
    return lag_order

# 预测
def forecast_var(model, steps=10, start_date=None):
    """
    使用 VAR 模型预测未来值，并生成时间索引
    """
    last_values = model.endog[-model.k_ar:]  # 提取最后 k_ar 条记录（滞后期）
    forecast = model.forecast(last_values, steps=steps)

    forecast_df = pd.DataFrame(forecast, columns=model.names)

    # 设置时间索引
    if start_date:
        forecast_dates = pd.date_range(start=start_date, periods=steps, freq='D')
        forecast_df.index = forecast_dates
    else:
        raise ValueError("start_date must be provided for generating forecast dates.")

    print(f"Forecast data starts from: {forecast_df.index[0]}")
    print(f"Forecast data ends at: {forecast_df.index[-1]}")
    return forecast_df


# 可视化预测结果
def plot_forecast(forecast, data, steps=10, save_path="output/forecast_plot.png"):
    """
    可视化预测结果，与实际值对比
    """
    plt.figure(figsize=(12, 6))

    for column in data.columns:
        # 绘制预测值
        plt.plot(forecast.index, forecast[column], label=f"Forecast {column}")

        # 提取实际值的最后时间范围，与预测对齐
        actual_slice = data.loc[forecast.index]  # 直接使用预测的时间范围
        plt.plot(actual_slice.index, actual_slice[column], label=f"Actual {column}", linestyle='--')

    plt.legend()
    plt.title("VAR Model Forecast vs Actual Values")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid()
    plt.tight_layout()
    # 保存图像
    plt.savefig(save_path)
    plt.show()
    print(f"Forecast plot saved at {save_path}")

# 因果关系检验
def granger_causality(data, variables, maxlag=5):
    """
    对指定变量进行 Granger 因果关系检验
    """
    for var in variables:
        try:
            print(f"\nTesting causality between {var[0]} and {var[1]}:")
            grangercausalitytests(data[[var[0], var[1]]], maxlag=maxlag, verbose=True)
        except Exception as e:
            print(f"Error testing Granger causality for {var}: {e}")

# 主流程
def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造相对路径
    csv_file_path = os.path.join(script_dir, "../../data/processed_data/processed_data.csv")
    
    # 加载数据
    try:
        returns = pd.read_csv(csv_file_path, index_col=0, parse_dates=True).pct_change().dropna()
        print(f"Returns data starts from: {returns.index[0]}")
        print(f"Returns data ends at: {returns.index[-1]}")
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 检查平稳性
    for col in returns.columns:
        check_stationarity(returns[col], name=f"{col} Returns")

    # 构建 VAR 模型
    var_result = build_var_model(returns, lags=5)

    # Granger 因果关系
    granger_causality(returns, [("BTC", "SPY"), ("SPY", "BTC")])

    # 预测与可视化
    last_date = returns.index[-1]  # 获取历史数据的最后一个日期
    forecast = forecast_var(var_result, steps=10, start_date=last_date + timedelta(days=1))
    if not forecast.empty:
        plot_forecast(forecast, returns, steps=10)
    print(f"Forecast data starts from: {forecast.index[0]}")
    print(f"Forecast data ends at: {forecast.index[-1]}")

if __name__ == "__main__":
    main()
