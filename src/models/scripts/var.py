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
        results = []
        for col in self.data.columns:
            if col != 'BTC':
                test = self.result.test_causality('BTC', col, kind='f')
                results.append({
                    'cause': 'BTC',
                    'effect': col,
                    'p_value': test.pvalue,
                    'f_stat': test.test_statistic
                })
                print(f"Causality of BTC on {col}:")
                print(test.summary())
        return results 

class Plotter:
    def __init__(self, data):
        self.data = data

    def plot_normalized_data_with_causality(self, output_path, causality_results):
        plt.figure(figsize=(12, 6))

        for col in self.data.columns:
            plt.plot(self.data.index, self.data[col], label=col)
        for result in causality_results:
            if result['p_value'] < 0.05: 
                effect = result['effect']
                max_date = self.data[effect].idxmax()
                max_value = self.data[effect].max()
                plt.annotate(
                    f"BTC → {effect}",
                    xy=(max_date, max_value),
                    xytext=(max_date, max_value + 0.1),
                    arrowprops=dict(facecolor='red', arrowstyle='->'),
                    fontsize=10,
                    color='red'
                )

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.gcf().autofmt_xdate()

        plt.legend()
        plt.title('Normalized Asset Prices with Significant Causality (BTC → Others)')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot with causality annotations saved to: {output_path}")
        plt.show()

    def plot_weak_correlation(self, output_path, threshold=0.2):
        correlation_matrix = self.data.corr()
        btc_correlations = correlation_matrix['BTC']
        weakly_correlated_assets = btc_correlations[btc_correlations.abs() < threshold].index

        if len(weakly_correlated_assets) == 0:
            print("No assets found with weak correlation to BTC.")
            return

        plt.figure(figsize=(12, 6))
        for asset in weakly_correlated_assets:
            plt.plot(self.data.index, self.data[asset], label=asset)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.gcf().autofmt_xdate()

        plt.legend()
        plt.title(f'Assets Weakly Correlated with BTC (|correlation| < {threshold})')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Weak correlation plot saved to: {output_path}")
        plt.show()
