import os
import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        self.data = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        return self.data

    def check_missing_values(self):
        print("Missing values per column:")
        print(self.data.isnull().sum())

    def fill_missing_values(self):
        self.data = self.data.fillna(method='ffill').fillna(method='bfill')

    def check_date_range(self):
        print(f"Data index range: {self.data.index.min()} to {self.data.index.max()}")

    def normalize_data(self):
        return self.data / self.data.max()

class VARModel:
    def __init__(self, data):
        self.data = data
        self.model = VAR(data)
        self.result = None

    def select_best_lag(self):
        lag_order = self.model.select_order()
        print(lag_order.summary())
        best_lag = lag_order.selected_orders['aic']
        print(f"Best lag order: {best_lag}")
        return best_lag

    def fit_model(self, best_lag):
        self.result = self.model.fit(best_lag)
        print(self.result.summary())

    def test_causality(self):
        for col in self.data.columns:
            if col != 'BTC-USD':
                test = self.result.test_causality('BTC-USD', col, kind='f')
                print(f"Causality of BTC-USD on {col}:")
                print(test.summary())

class Plotter:
    def __init__(self, data):
        self.data = data

    def plot_normalized_data(self, output_path):
        plt.figure(figsize=(12, 6))
        for col in self.data.columns:
            plt.plot(self.data.index, self.data[col], label=col)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.gcf().autofmt_xdate()

        plt.legend()
        plt.title('Normalized Asset Prices (BTC, AGG, GLD, SPY)')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")
        plt.show()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(parent_dir, 'data', 'processed_data', 'processed_data.csv')

    processor = DataProcessor(data_path)
    data = processor.load_data()
    processor.check_missing_values()
    processor.fill_missing_values()
    processor.check_date_range()
    normalized_data = processor.normalize_data()

    var_model = VARModel(data)
    best_lag = var_model.select_best_lag()
    var_model.fit_model(best_lag)
    var_model.test_causality()

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'normalized_asset_prices.png')

    plotter = Plotter(normalized_data)
    plotter.plot_normalized_data(output_path)

if __name__ == "__main__":
    main()
