import time
from datetime import datetime
from binance_trade_bot import backtest


class BackTestClass:
    def __init__(self, cb):
        self.stop = 0
        self._cb = cb

    def run(self):
        # for i in range(100):
        #     print(i)
        #     val_cb = f'2021&{i}&{i}'
        #     self._cb(val_cb)
        #     time.sleep(1)

        history = []
        for manager in backtest(datetime(2021, 1, 1), datetime.now()):
            btc_value = manager.collate_coins("BTC")
            bridge_value = manager.collate_coins(manager.config.BRIDGE.symbol)
            history.append((btc_value, bridge_value))
            btc_diff = round((btc_value - history[0][0]) / history[0][0], 3)
            bridge_diff = round((bridge_value - history[0][1]) / history[0][1], 3)
            val_cb = f'{manager.datetime}&{btc_value:.3f}&{bridge_value:.3f}'
            print("------")
            print("TIME:", manager.datetime)
            print("BALANCES:", manager.balances)
            print("BTC VALUE:", btc_value, f"({btc_diff}%)")
            print(f"{manager.config.BRIDGE.symbol} VALUE:", bridge_value, f"({bridge_diff}%)")
            print("------")
            self._cb(val_cb)
            if self.stop:
                break


def print_cb(s):
    print(s)


if __name__ == "__main__":
    t = BackTestClass(print_cb)
    t.run()
