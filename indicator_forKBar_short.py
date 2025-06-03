# 載入必要套件
import requests, datetime, os, time
import numpy as np
import matplotlib.dates as mdates
# from talib.abstract import *  # 載入技術指標函數

# 算K棒
class KBar():  # 設定初始化變數
    def __init__(self, date, cycle=1):
        # K棒的頻率（分鐘）
        self.TAKBar = {
            'time': np.array([]),
            'open': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
            'close': np.array([]),
            'volume': np.array([])
        }
        self.current = datetime.datetime.strptime(date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.cycle = datetime.timedelta(minutes=cycle)

    # 更新最新報價
    def AddPrice(self, time, open_price, close_price, low_price, high_price, volume):
        if time <= self.current:
            if self.TAKBar['close'].size > 0:
                self.TAKBar['volume'][-1] += volume  # 更新成交量
                self.TAKBar['high'][-1] = max(self.TAKBar['high'][-1], high_price)  # 更新最高價
                self.TAKBar['low'][-1] = min(self.TAKBar['low'][-1], low_price)     # 更新最低價
            else:
                # 如果資料為空，初始化第一筆資料
                self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
                self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
                self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
                self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
                self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
                self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            return 0
        else:
            while time > self.current:
                self.current += self.cycle
                self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
                self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
                self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
                self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
                self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
                self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            return 1

    # 以下為資料取得函式（記得都要縮排在 class 裡）
    def GetTime(self):
        return self.TAKBar['time']

    def GetOpen(self):
        return self.TAKBar['open']

    def GetHigh(self):
        return self.TAKBar['high']

    def GetLow(self):
        return self.TAKBar['low']

    def GetClose(self):
        return self.TAKBar['close']

    def GetVolume(self):
        return self.TAKBar['volume']
