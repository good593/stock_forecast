# https://wendys.tistory.com/181
# https://www.youtube.com/watch?v=JAUVb_73RQY

from datetime import datetime
import numpy as np 
import pandas as pd 
import backtrader as bt


class MyStratege(bt.Strategy):
    params = dict(
        period_short=5,
        period_long=20
    ) 

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.period_short)
        sma2 = bt.ind.SMA(period=self.p.period_long)

        self.golden_cross = sma1 > sma2 
        self.dead_cross = sma1 < sma2 

    def next(self):
        if not self.position:
            if self.golden_cross:
                close = self.data.close[0]
                size = int(self.broker.getcash() / close)
                self.buy(size=size)

        elif self.dead_cross:
            self.close()



if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # 삼성전자 005930
    save_path = './data/stock/raw/{stock_code}.csv'.format(stock_code='005930')
    df_dtype = {
        'stock_code':'object'
    }
    df = pd.read_csv(save_path, index_col='Date', dtype=df_dtype, parse_dates=['Date'])
    df = df.loc['2019-01-01':'2019-12-31']
    df = df.reset_index()
    df.columns = [ col.lower() for col in df.columns.to_list()]
    data = bt.feeds.PandasData(dataname=df, datetime='date')
    cerebro.adddata(data)
    cerebro.broker.setcash(1000000) # 초기 자본 설정
    cerebro.broker.setcommission(commission=0.00015)  # 매매 수수료는 0.015% 설정
    
    cerebro.addstrategy(MyStratege) # 자신만의 매매 전략 추가
    
    cerebro.run() # 백테스팅 시작
    
    cerebro.plot() # 그래프로 보여주기
