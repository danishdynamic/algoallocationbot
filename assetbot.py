#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 02:05:37 2020

@author: ali
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 14:35:38 2020

@author: Administrator

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

        
class Backtest(object):
    def __init__(self,account_id,symbol,initial_money=100000):

        self.id = account_id
        self.symbol = symbol
        self.fee_rate = 0.001
        self.weight = [0]
        self.share = [0]
        self.account_value = [initial_money]
        self.position_value = [0]
        self.account_balance = [initial_money]

    
        self.transaction_record ={'date':[],'order':[],'symbol':[],'price':[],'value':[],'fee':[],'label':[]}
        self.get_history_data()
            
    def get_history_data(self):
        # downloading historical data
        self.history_data = yf.download(self.symbol,interval = "1d")['Adj Close'].dropna()
        self.ACWI_data =  yf.download("ACWI",interval = "1d")['Adj Close'].dropna()
    
    def get_last_price(self,date):
        return self.history_data[self.history_data.index<=date].iloc[-1]
    
    def get_MA(self,price_series,date,obs_n=100):
        return np.average(price_series[price_series.index<date][-obs_n])

    def plt_account_info(self):
            account_info = ['account_value','position_value','account_balance','share','weight']
            #plot dataframe by each of col individually
            plt.figure(figsize=(12,10))
            num_plot=len(account_info)
            plt_x=5
            plt_y=1
            plt.subplots_adjust(left=0.15,bottom=0.1,top=1.1,right=0.95,hspace=1.25,wspace=0.75)
            
            for i in range(0,num_plot,1):
                plt.subplot(plt_x,plt_y,i+1)
                title=self.symbol+' : '+account_info[i]
                plt.title(title)
                plt.xticks(rotation=90)
                plt.plot(self.backtest_date,getattr(self,account_info[i]),'blue')
                
            plt.show()
            print('                     Backtesing : Account Info ')
            print('sharpe ratio : '+str(self.sharpe))
            print('volatility   : '+str(self.volatility))

    def daily_update(self,date):
        self.share.append(self.share[-1])
        self.account_balance.append(self.account_balance[-1])
        self.position_value.append(self.share[-1]*self.get_last_price(date))
        self.account_value.append(self.account_balance[-1]+self.position_value[-1])
        self.weight.append(self.position_value[-1]/self.account_value[-1])
        
        
    def order_update(self,date,weight,label=''):
        if weight == np.round(self.weight[-1],2):
            self.daily_update(date)
            return
        price = self.get_last_price(date)
        bs = 'buy' if weight-self.weight[-1]>0 else 'sell'
        
        self.transaction_record['date'].append(date)
        self.transaction_record['order'].append(bs)
        self.transaction_record['symbol'].append(self.symbol)
        self.transaction_record['price'].append(price)
        self.transaction_record['value'].append(self.account_value[-1]*(weight-self.weight[-1]))
        fee = np.abs(self.account_value[-1]*(weight-self.weight[-1])*self.fee_rate)
        self.transaction_record['fee'].append(fee)
        self.transaction_record['label'].append(label)
     
        self.weight.append(weight)
        self.position_value.append(self.weight[-1]*self.account_value[-1])
        self.account_value.append(self.account_value[-1] - fee)
        self.account_balance.append( self.account_value[-1] - self.position_value[-1])
        self.share.append(self.position_value[-1]/price)
        

    def backtest_momentum(self,MA_n1=50, MA_n2=200, ACWI_MA_obs_n=100, start_date='2019-01-01', end_date='2019-12-30'):
        date = self.history_data.index[(self.history_data.index>=start_date)&(self.history_data.index<end_date)]
        self.backtest_date = date
        length  = len(date)
        for i in range(1,length,1):
            #define stop loss 
            
            #stop loss extra
            #if we want stoploss , we can add code here 
            ACWI_MA_n          =self.get_MA(self.ACWI_data,date[i],obs_n=ACWI_MA_obs_n)
            ACWI_price          =self.ACWI_data[self.ACWI_data.index<date[i]].iloc[-1]
            ACWI_MA_n_delay1   =self.get_MA(self.ACWI_data,date[i-1],obs_n=ACWI_MA_obs_n)
            ACWI_price_delay1   =self.ACWI_data[self.ACWI_data.index<date[i-1]].iloc[-1]

            if ACWI_price> ACWI_MA_n and ACWI_price_delay1<ACWI_MA_n_delay1:
                self.order_update(date[i],0.99,label='Rule0')
                continue
            elif ACWI_price< ACWI_MA_n and ACWI_price_delay1>ACWI_MA_n_delay1:
                self.order_update(date[i],0.91,label='Rule0')
                continue
            else: #
                pass
            
            # SYMBOL RULE
            symbol_MA_n1         = self.get_MA(self.history_data,date[i],obs_n=MA_n1)
            symbol_MA_n2        = self.get_MA(self.history_data,date[i],obs_n=MA_n2)
            symbol_MA_n1_delay1  = self.get_MA(self.history_data,date[i-1],obs_n=MA_n1)
            symbol_MA_n2_delay1 = self.get_MA(self.history_data,date[i-1],obs_n=MA_n2)

            if symbol_MA_n1 > symbol_MA_n2 and  symbol_MA_n1_delay1 < symbol_MA_n2_delay1:
                self.order_update(date[i],0.99,label='Rule1')
                continue
            elif symbol_MA_n1 < symbol_MA_n2 and  symbol_MA_n1_delay1 > symbol_MA_n2_delay1:
                self.order_update(date[i],0.00,label='Rule1')    
                continue
            else:
                pass
            
            self.daily_update(date[i])
        
        self.transaction_record = pd.DataFrame(self.transaction_record)
        self.get_performance()
        return self.sharpe,self.volatility
    
    def get_performance(self):
        price = pd.Series(self.account_value) 
        ret = (np.log(price)-np.log(price).shift(1)).dropna()*252
        self.volatility = ret.std()
        self.sharpe = (ret.mean() - 0.02)/self.volatility

# single -asset allocation
by = Backtest('ali','AAPL',initial_money=100000)
by.backtest_momentum()
by.plt_account_info()
by.transaction_record




#optimum MA parameters : MA_n1=50, MA_n2=200, ACWI_MA_obs_n=100

def get_best_MA(symbol):
	result = {'MAn1':[],'MAn2':[],'ACWI_MA':[],'sharpe':[],'volatility':[]}
	for i in range(5,200,5):
		for j in range(2,20):
			by = Backtest('ali',symbol)
			sharpe,volatility = by.backtest_momentum(MA_n1=i, MA_n2=i*j, ACWI_MA_obs_n=100)
			result['MAn1'].append(i)
			result['MAn2'].append(i*j)
			result['ACWI_MA'].append(100)
			result['sharpe'].append(sharpe)
			result['volatility'].append(volatility)
	df = pd.DataFrame(result)
	print('max sharpe :')
	print(df[df.sharpe == df.sharpe.max()])
	print('min volatility :')
	print(df[df.volatility == df.volatility.min()])
	
	return df

get_best_MA('AAPL')





