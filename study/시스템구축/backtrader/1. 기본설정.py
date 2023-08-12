# https://stockfinancediary.tistory.com/113

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime 
import os.path
import sys 

import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Set our desired cash start 
    cerebro.broker.setcash(100000.0)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'data', 'orcl-1995-2014.txt')
    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)
    
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())