import numpy as np
import math
import matplotlib.pyplot as plt



class MyOperator:
    def __init__(self):
        self.init_price = 0
        self.expected_return_rate = 0.8
        self.max_return_rate = 0.8
        self.max_last_prices = 100
        self.last_prices = []
        self.sell_percent = 0.5
        self.buy_percent = 0.2
        self.min_trade_period = 10
        self.last_trade_time = -self.min_trade_period

    def sell(self, t, shares):
        self.last_trade_time = t
        return -shares * self.sell_percent

    def buy_in_cash(self, t, cash, price):
        self.last_trade_time = t
        print(cash)
        return math.floor(cash / price) * self.buy_percent

    def __call__(self, t, price, shares, cash, service_charge_rate):
        self.last_prices.append(price)
        if len(self.last_prices) > self.max_last_prices:
            self.last_prices = self.last_prices[1:]

        if t - self.last_trade_time >= self.min_trade_period:
            if shares > 100:
                if price < sum(self.last_prices) / len(self.last_prices) * 0.95:
                    return self.sell(t, shares)
            if cash > 100:
                if price < sum(self.last_prices) / len(self.last_prices) * 1.3:
                    return self.buy_in_cash(t, cash, price)

            
        return 0


def simulate(init_price, init_cash, deltas, operator):
    current_price = init_price
    current_shares = (init_cash / 2) / current_price
    current_cash = init_cash / 2 
    total_assets = []
    prices = []
    total_trade_values = []
    total_cash = []
    service_charge_rate = 0.001
    for t, d in enumerate(deltas):
        # > 0, buy x shares
        # < 0, sell x shares
        traded_shares = operator(t, current_price, current_shares, current_cash, service_charge_rate)
        current_shares += traded_shares
        current_cash -= traded_shares * current_price

        service_charge = abs(traded_shares) * current_price * service_charge_rate
        current_cash -= service_charge

        total_assets.append(current_cash + current_shares * current_price)
        prices.append(current_price)
        total_trade_values.append(traded_shares * current_price)
        total_cash.append(current_cash)

        current_price = current_price * (1+d)
    return np.array(total_assets), np.array(prices), total_trade_values, np.array(total_cash)



def run(your_operator, name):
    deltas = np.concatenate((
        np.random.uniform(-0.09, 0.11, 100),
        np.random.uniform(-0.11, 0.09, 100),
        np.random.uniform(-0.09, 0.10, 100),
        np.random.uniform(-0.10, 0.09, 100),
        np.random.uniform(-0.10, 0.10, 100),
    ))
    init_price = 10.0
    principle = 10000

    total_assets, total_prices, total_trade_values, total_cash = simulate(init_price, principle, deltas, MyOperator())
    total_assets2, _, total_trade_values2, total_cash2 = simulate(init_price, principle, deltas, your_operator)

    plt.subplot('211')
    plt.plot(total_assets, label='Asset(%s)' % 'trend')
    plt.plot(total_assets2, label='Asset(%s)' % name)
    plt.plot(total_prices/init_price * principle, label='Price')
    plt.legend()

    plt.subplot('212')
    plt.plot(total_trade_values, label='Traded(%s)' % 'Trend')
    plt.plot(total_trade_values2, label='Traded2(%s)' % name)
    plt.plot(total_cash, label='Cash')
    plt.legend()
    plt.show()
