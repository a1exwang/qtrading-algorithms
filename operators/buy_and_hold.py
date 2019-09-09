import numpy as np

class BuyAndHold:
    def __call__(self, t, price, shares, cash, service_charge_rate):
        if t == 0:
            return 0.95 * (cash / price)
        return 0
