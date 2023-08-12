# https://wendys.tistory.com/181
# https://www.youtube.com/watch?v=JAUVb_73RQY

from datetime import datetime
import numpy as np 
import pandas as pd 
import backtrader as bt

import matplotlib.pyplot as plt 
plt.rcParams['font.family'] = 'D2Coding'

class MyStratege(bt.Strategy):
    params = dict(
        period_short=5,
        period_long=20
    ) 

    def __init__(self):
        self.golden_crosses = [] 
        self.dead_crosses = []

        for data in self.datas:
            sma1 = bt.ind.SMA(data, period=self.p.period_short)
            sma2 = bt.ind.SMA(data, period=self.p.period_long)

            golden_cross = sma1 > sma2 
            dead_cross = sma1 < sma2 
            self.golden_crosses.append(golden_cross)
            self.dead_crosses.append(dead_cross)

        self.quantities = [0 for _ in self.datas]

    def next(self):
        for i, (data, golden, dead) in enumerate(zip(self.datas, self.golden_crosses, self.dead_crosses)):
            if golden:
                close = data.close[0]
                size = int(self.broker.getcash() / close)

                self.buy(data, size=size)
                if size:
                    print(f'BUY CREATE price={data.close[0]:.2f} size={size}')
            elif dead:
                self.close(data)



if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # 삼성전자 005930
    codes = ['035420', '005930']
    for i, (code,name) in enumerate(zip(codes, ['NAVER', '삼성전자'])):
        save_path = './data/stock/raw/{stock_code}.csv'.format(stock_code=code)
        df_dtype = {
            'stock_code':'object'
        }
        df = pd.read_csv(save_path, index_col='Date', dtype=df_dtype, parse_dates=['Date'])
        df = df.loc['2019-01-01':'2019-12-31']
        df = df.reset_index()
        df.columns = [ col.lower() for col in df.columns.to_list()]
        data = bt.feeds.PandasData(dataname=df, datetime='date')
        
        data.plotinfo.plot = False
        cerebro.adddata(data, name=name)

    cerebro.broker.setcash(1000000) # 초기 자본 설정
    cerebro.broker.setcommission(commission=0.00015)  # 매매 수수료는 0.015% 설정
    
    cerebro.addstrategy(MyStratege) # 자신만의 매매 전략 추가
    
    cerebro.run() # 백테스팅 시작
    
    cerebro.plot(stype='candlestick') # 그래프로 보여주기
