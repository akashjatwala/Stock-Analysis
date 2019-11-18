from nsepy import get_history
from nsepy import get_quote
from nsepy.derivatives import get_expiry_date
from nsepy.history import get_price_list
import datetime
from pprint import pprint
from scipy.stats import norm
import numpy as np
from selenium import webdriver
import pandas as pd
from tabulate import tabulate
import os
import docx2txt
from tkinter import *
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from mpl_finance import candlestick_ohlc
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# %matplotlib inline

symbol=open("Symbols.txt","r")
symbol_list=symbol.read().split("\n")
names=open("Names.txt","r")
name_list=names.read().split("\n")
symbol_fno=open("Symbol_FnO.txt","r")
symbol_fno_list=symbol_fno.read().split("\n")
symbol_nifty_100=open("NIFTY100.txt","r")
symbol_nifty_100_list=symbol_nifty_100.read().split("\n")
symbol_nifty_50=open("NIFTY50.txt","r")
symbol_nifty_50_list=symbol_nifty_50.read().split("\n")
today_date=datetime.date.today()

def trading_day():
    day_value=datetime.date.today().weekday()
    weekdays={0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",7:"Sunday"}
    day=weekdays[day_value]
    if(day=="Saturday" or day=="Sunday"):
        return True
    else:
        return True

def trading_day_message():
    messagebox.showinfo("Error","Today is not a Trading Day",icon="warning")

def update_datasets():
    os.startfile("Update Datasets.pdf")

def message_datasets():
    messagebox.showinfo("Message","The Program run on Datasets, which consists of Stocks Symbols, and Names. \nThe Dtaset to be used can be th Pre-Saved, or can be Downloaded while running the Program. \nThe Pre-Saved Datasets are to be updated Frequently, so as to have the Updated Results")
    response=messagebox.askquestion("Update Datasets","Do you want to know the Procedure to Update the Datasets")
    if(response=='yes'):
        update_datasets()     
        
def disclaimer():
    messagebox.showinfo("Disclaimer","- The Data are from NSE \n- For Indices, only NIFTY and BANK NIFTY is available \n- The Data are available only on Trading Day\n- Expiries are available for Near Month and Far Month \n- Technical Screener only captures NIFTY100 Stocks \n- For Top Gainers/Losers, Maximum of 10 Stocks are Permitted")    

def name_input():
    name=simpledialog.askstring("Name","What is your Name")
    return name
    
def symbol_fno_error_message():
    messagebox.showinfo("Error","The Company you selected is not in F&O Segment",icon="warning")

def exp_year_input():
    exp_year=simpledialog.askstring("Expiry Year","Please enter the Expiry Year")
    return exp_year
    
def strike_input():
    strike=simpledialog.askstring("Strike Price","Please enter the Strike Price")
    return strike
    
def implied_vol_input():
    imp_vol=simpledialog.askstring("Implied Volatility","Please enter the Annualised Volatility from Other Informations")
    return imp_vol
    
def portfolio_no_stocks_input():
    no_stocks=simpledialog.askstring("Number of Stocks","Please enter the Total Number of Stocks in the Portfolio")
    return no_stocks
    
def gainer_loser_no_stocks_input():
    no_stocks=simpledialog.askstring("Number of Stocks","Please enter the Total Number of Stocks to be Displayed")
    return no_stocks

def option_strike_input(message):
    strike_price=simpledialog.askstring("Strike Price",message)
    return strike_price
    
def option_price_input(message):
    option_price=simpledialog.askstring("Option Price",message)
    return option_price
    
def pcr_oi_input(message):
    total_files=simpledialog.askstring("Total Files",message)
    return total_files 
    
def message(string):
    messagebox.showinfo("Message",string)
    
def choose_file_message(message):
    messagebox.showinfo("Choose File",message)
    
def save_message(message):
    messagebox.showinfo("File Saved",message)

def main_exit():
    response=messagebox.askquestion("Exit","Are you sure you want to Exit",icon="warning")
    if(response=='yes'):
        return True
    else:
        return False

def main_exit_message():
    messagebox.showinfo("Thank You","Thank you for Visiting.\nHave a Nice Day!!")

def date_entry_bhav():
    date=simpledialog.askstring("BhavCopy","Please enter the Date for which you want to see the BhavCopy in YYYY-MM-DD format")
    return date
    
def date_entry_start():
    date=simpledialog.askstring("Start Date","Please enter the Start Date in YYYY-MM-DD format")
    return date

def date_entry_end():
    date=simpledialog.askstring("End Date","Please enter the End Date in YYYY-MM-DD format")
    return date
    
def cont():
    response=messagebox.askquestion("Continue","Do you want to Continue",icon="warning")
    if(response=='yes'):
        return True
    else:
        return False

def continue_message_main():
    messagebox.showinfo("Exit","You will be re-directed to the Main Section")
    
def continue_message_sub():
    messagebox.showinfo("Exit","You will be re-directed to the Sub-Section")
    
def close_price_message(close_price):
    close_price=(int)(close_price)
    string="The Last Traded Value is: "+str(close_price)
    messagebox.showinfo("Closing Price",string)

def save():
    response=messagebox.askquestion("Save","Do you want to Save the Files")
    if(response=='yes'):
        return True
    else:
        return False    

def thank():
    print("\nThank youfor Visiting. \nHave a Nice Day!!\n")
    
def invalid():
    messagebox.showinfo("Error","You had entered an Invalid Data",icon="warning")        
            
def valid_date(year,month,day):
    valid=0
    isvaliddate=True
    try:
        datetime.date(int(year),int(month),int(day))
    except ValueError:
        isvaliddate=False
    if(isvaliddate):
        valid=1
    else:
        valid=0
    return valid

def invalid_date():
    messagebox.showinfo("Invalid Date","You had entered an Invalid Date")    

def expiry_date(year,month):
    exp=get_expiry_date(year=year,month=month)
    return exp
    
def date_entry():
    print("\nTime Period: 1. 1 Year")
    print("             2. 2 Year")
    print("             3. 3 Year")
    print("             4. 5 Year")
    print("             5. Custom Date Range")
    while(True):
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>0 and c<=5):
                break
            else:
                invalid()
        if(c==1):
            end=today_date
            dd=datetime.timedelta(days=365)
            start=end-dd
            break
        else: 
            if(c==2):
                end=today_date
                dd=datetime.timedelta(days=365*2)
                start=end-dd
                break
            else:
                if(c==3):
                    end=today_date
                    dd=datetime.timedelta(days=365*3)
                    start=end-dd
                    break
                else:
                    if(c==4):
                        end=today_date
                        dd=datetime.timedelta(days=365*5)
                        start=end-dd
                        break
                    else:
                        if(c==5):
                            while(True):
                                date_entry=date_entry_end()
                                year,month,day=map(int,date_entry.split('-'))
                                valid=valid_date(year,month,day)
                                if(valid==1):
                                    end=datetime.date(year,month,day)
                                    if(end<today_date):
                                        break
                                    else:
                                        invalid_date()
                                else:
                                    invalid_date()
                            while(True):
                                date_entry=date_entry_start()
                                year,month,day=map(int,date_entry.split('-'))
                                valid=valid_date(year,month,day)
                                if(valid==1):
                                    start=datetime.date(year,month,day)
                                    if(start<end):
                                        break
                                    else:
                                        invalid_date()
                                else:
                                    invalid_date()
                            break
                        else:
                            invalid()
    return start,end
    
def date_entry_fno():
    start_copy=str(today_date)
    datee=datetime.datetime.strptime(start_copy,"%Y-%m-%d").date()
    today_year=datee.year
    today_month=datee.month
    month_nos=[1,2,3,4,5,6,7,8,9,10,11,12]
    current_expiry_date=expiry_date(today_year,today_month)
    while(True):
        year=(int)(exp_year_input())
        if(year>=2000 and year<=today_year):
            break
        else:
            invalid_date()
    month_list=[]
    if(year<today_year):
        month_list=month_nos
    else:
        if(current_expiry_date>today_date):
            month_list=month_nos[today_month-1:today_month+1]
        else:
            month_list=month_nos[today_month:today_month+2]
    expiry_dates=[]
    for i in month_list:
        expiry_dates.append(expiry_date(year,i))
    string="Please select the Expiry Date"
    message(string)
    root=Tk()
    value=StringVar(root)
    value.set(expiry_dates[0])
    opt=OptionMenu(root,value,*expiry_dates)
    opt.pack()
    def ok():
        value.get()
        root.quit()
        root.destroy()
    button=Button(root,text="Ok",command=ok)
    button.pack()
    mainloop()
    expiry_str=value.get()
    exp_dt=datetime.datetime.strptime(expiry_str,'%Y-%m-%d')
    exp_dt=exp_dt.date()
    start_str=(str)(year)+"-01-01"           
    start=datetime.datetime.strptime(start_str,'%Y-%m-%d')
    start=start.date()
    end=today_date
    return start,end,exp_dt
    
def option_type_input():
    string="Please select the Option Type"
    message(string)
    opt_type=["CE","PE"]
    root=Tk()
    value=StringVar(root)
    value.set(opt_type[0])
    opt=OptionMenu(root,value,*opt_type)
    opt.pack()
    def ok():
        value.get()
        root.quit()
        root.destroy()
    button=Button(root,text="Ok",command=ok)
    button.pack()
    mainloop()
    option=value.get()    
    return option

def symbol_input():
    first=[]
    for i in name_list:
        first.append(i.split(' ')[0])
    while(True):
        word=(input("Please enter the first word of the Stock which you want to select (in UPPERCASE): "))
        if(word in first):
            break
        else:
            invalid()
    name=list(filter(lambda x: x.startswith(word), name_list))
    l=len(name)
    sno=list(range(1,l+1))
    name_sno=dict(zip(sno,name))
    pprint(name_sno)
    no=(int)(input("Please enter the desired Stock No: "))
    stock_name=name_sno[no]
    name_symbol=dict(zip(name_list,symbol_list))
    symbol=name_symbol[stock_name]
    return symbol
    
def symbol_input_fno():
    while(True):
        first=[]
        for i in name_list:
            first.append(i.split(' ')[0])
        while(True):
            word=(input("Please enter the first word of the Stock which you want to select (in UPPERCASE): "))
            if(word in first):
                break
            else:
                invalid()
        name=list(filter(lambda x: x.startswith(word), name_list))
        l=len(name)
        sno=list(range(1,l+1))
        name_sno=dict(zip(sno,name))
        pprint(name_sno)
        no=(int)(input("Please enter the desired Stock No: "))
        stock_name=name_sno[no]
        name_symbol=dict(zip(name_list,symbol_list))
        symbol=name_symbol[stock_name]
        if(symbol in symbol_fno_list):
            break;
        else:
            symbol_fno_error_message()       
    return symbol

def stock_quote(symbol):
    quote=get_quote(symbol)
    return quote

def stock_historical(symbol,start,end):
    historical=get_history(symbol=symbol,start=start,end=end)
    return historical

def stock_future(symbol,start,end,expiry):
    future=get_history(symbol=symbol,start=start,end=end,futures=True,expiry_date=expiry)
    return future
    
def stock_option(symbol,start,end,option_type,strike_price,expiry_date):
    option=get_history(symbol=symbol,start=start,end=end,option_type=option_type,strike_price=strike_price,expiry_date=expiry_date)
    return option
    
def index_historical(symbol,start,end):
    historical=get_history(symbol=symbol,start=start,end=end,index=True)
    return historical

def index_future(symbol,start,end,expiry):
    future=get_history(symbol=symbol,start=start,end=end,index=True,futures=True,expiry_date=expiry)
    return future
    
def index_option(symbol,start,end,option_type,strike_price,expiry_date):
    option=get_history(symbol=symbol,start=start,end=end,index=True,option_type=option_type,strike_price=strike_price,expiry_date=expiry_date)
    return option

def bhavcopy(date):
    bhav=get_price_list(dt=date)
    return bhav
 
def spot(symbol):
    quote=stock_quote(symbol)
    spot_price=quote['lastPrice']
    return spot_price
    
def browser(symbol):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    strike=(int)(strike_input())
    browser.close()
    return strike
    
def rate():
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.fbil.org.in/")
    r_element=browser.find_elements_by_xpath('//*[@id="grdMibor"]/tbody/tr[2]/td[4]')[0]
    r=r_element.text
    browser.close()
    r=float(r)
    r=r/100
    return r
    
def implied_vol(symbol,exp_date):
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying="+symbol+"&instrument=FUTSTK&expiry="+exp_date+"&type=-&strike=-")
    v=implied_vol_input()
    v=(float)(v)
    browser.close()
    return v
    
def delta_value(s,k,r,t,v):
    d1=(np.log(s/k))+((r+(v**2)/2)*t)
    nd1=norm.cdf(d1,0.0,1.0)
    delta_call=nd1
    delta_put=abs(nd1-1)
    return delta_call,delta_put
    
def ema_single(df,n,symbol):
    ema=pd.Series(df['Close'].ewm(span=n, min_periods=n).mean(), name='EMA_'+str(n))
    df=df.join(ema)
    plt.figure(figsize=(15,15))
    plt.plot(df['Close'],label="Close Prices")
    plt.plot(df['EMA_'+str(n)],label="EMA_"+str(n))
    plt.title("Single Crossover EMA",fontsize=18)
    plt.ylabel("Prices")
    plt.grid(True)
    plt.legend(loc="best",prop={'size':9})
    plt.show()
    return df
    
def ema_double(df,n1,n2,symbol):
    ema1=pd.Series(df['Close'].ewm(span=n1, min_periods=n1).mean(), name='EMA_'+str(n1))
    ema2=pd.Series(df['Close'].ewm(span=n2, min_periods=n2).mean(), name='EMA_'+str(n2))
    df=df.join(ema1)
    df=df.join(ema2)
    plt.figure(figsize=(15,15))
    plt.plot(df['Close'],label="Close Prices")
    plt.plot(df['EMA_'+str(n1)],label="EMA_"+str(n1))
    plt.plot(df['EMA_'+str(n2)],label="EMA_"+str(n2))
    plt.title("Double Crossover EMA",fontsize=18)
    plt.ylabel("Prices")
    plt.grid(True)
    plt.legend(loc="best",prop={'size':9})
    plt.show()
    return df
    
def ema_triple(df,n1,n2,n3,symbol):
    ema1=pd.Series(df['Close'].ewm(span=n1, min_periods=n1).mean(), name='EMA_'+str(n1))
    ema2=pd.Series(df['Close'].ewm(span=n2, min_periods=n2).mean(), name='EMA_'+str(n2))
    ema3=pd.Series(df['Close'].ewm(span=n3, min_periods=n3).mean(), name='EMA_'+str(n3))
    df=df.join(ema1)
    df=df.join(ema2)
    df=df.join(ema3)
    plt.figure(figsize=(15,15))
    plt.plot(df['Close'],label="Close Prices")
    plt.plot(df['EMA_'+str(n1)],label="EMA_"+str(n1))
    plt.plot(df['EMA_'+str(n2)],label="EMA_"+str(n2))
    plt.plot(df['EMA_'+str(n3)],label="EMA_"+str(n3))
    plt.title("Triple Crossover EMA",fontsize=18)
    plt.ylabel("Prices")
    plt.grid(True)
    plt.legend(loc="best",prop={'size':9})
    plt.show()
    return df

def momentum(df,symbol):
    n=14
    m=pd.Series(df['Close'].diff(n), name='Momentum_'+str(n))
    fig=plt.figure(figsize=(15,15))
    ax=fig.add_subplot(2,1,1)
    # ax.set_xticklabels([]) - to remove the x labels
    plt.plot(df['Close'],lw=1,linestyle='-',label="Close Price")
    plt.legend(loc='best',prop={'size':9})
    plt.title(symbol,fontsize=18)
    plt.ylabel("Close Price")
    plt.grid(True)
    bx=fig.add_subplot(2,1,2)
    # bx.set_xticklabels([]) - to remove the x labels
    plt.plot(m,'k',lw=1,linestyle='-',label='Momentum')
    plt.legend(loc='best',prop={'size':9})
    plt.title("Momentum Indicator",fontsize=18)
    plt.ylabel('Values')
    plt.grid(True)
    plt.setp(plt.gca().get_xticklabels(),rotation=30)
    plt.show()
    return df
    
def bollinger_bands(df,symbol):
    n=20
    ema=pd.Series(df['Close'].ewm(span=n, min_periods=n).mean(), name='MA')
    df=df.join(ema)
    sd=pd.Series(df['Close'].rolling(n, min_periods=n).std())
    b1=(df['MA']+2*sd)
    B1=pd.Series(b1,name="UpperBB")
    df=df.join(B1)
    b2=(df['MA']-2*sd)
    B2=pd.Series(b2,name="LowerBB")
    df=df.join(B2)
    plt.figure(figsize=(15,15))
    plt.plot(df['Close'],label="Close Prices")
    plt.plot(df['MA'],label="MA_20")
    plt.plot(df['UpperBB'],label="Upper Bollinger Bands")
    plt.plot(df['LowerBB'],label="Lower Bollinger Bands")
    plt.title(symbol,fontsize=18)
    plt.ylabel("Prices")
    plt.grid(True)
    plt.legend(loc="best",prop={'size':9})
    plt.show()
    return df
  
def ppsr(df,symbol):
    pp=pd.Series((df['High']+df['Low']+df['Close'])/3)
    r1=pd.Series(2*pp-df['Low'])
    s1=pd.Series(2*pp-df['High'])
    r2=pd.Series(pp+df['High']-df['Low'])
    s2=pd.Series(pp-df['High']+df['Low'])
    r3=pd.Series(df['High']+2*(pp-df['Low']))
    s3=pd.Series(df['Low']-2*(df['High']-pp))
    psr={'PP':pp,'R1':r1,'S1':s1,'R2':r2,'S2':s2,'R3':r3,'S3':s3}
    psr=pd.DataFrame(psr)
    df=df.join(psr)
    print("\n",symbol," Pivot Points, Support, & Resistance")
    print(tabulate([['Close Price',df.Close[-1:]],["Pivot Points",df.PP[-1:]],['Support 1',df.S1[-1:]],['Resistance 1',df.R1[-1:]],['Support 2',df.S2[-1:]],['Resistance 2',df.R2[-1:]],['Support 3',df.S3[-1:]],['Resistance 3',df.R3[-1:]]],headers=["Particulars","Prices"]))
    return df
    
def macd(df,symbol):
    n_fast=12
    n_slow=26
    emafast=pd.Series(df['Close'].ewm(span=n_fast,min_periods=n_slow).mean())
    emaslow=pd.Series(df['Close'].ewm(span=n_slow,min_periods=n_slow).mean())
    macd=pd.Series(emafast-emaslow,name='MACD_'+str(n_fast)+'_' + str(n_slow))
    macdsign=pd.Series(macd.ewm(span=9, min_periods=9).mean(),name='MACDsign_'+str(n_fast)+'_'+str(n_slow))
    macddiff=pd.Series(macd-macdsign,name='MACDdiff_'+str(n_fast)+'_'+str(n_slow))
    df=df.join(macd)
    df=df.join(macdsign)
    df=df.join(macddiff)
    fig=plt.figure(figsize=(15,15))
    ax=fig.add_subplot(2,1,1)
    # ax.set_xticklabels([]) - to remove the x labels
    plt.plot(df['Close'],lw=1,linestyle='-',label="Close Price")
    plt.legend(loc=2,prop={'size':9})
    plt.title(symbol,fontsize=18)
    plt.ylabel("Close Price")
    plt.grid(True)
    bx=fig.add_subplot(2,1,2)
    # bx.set_xticklabels([]) - to remove the x labels
    plt.plot(df['MACD_12_26'],lw=1,linestyle='-',label='MACD')
    plt.plot(df['MACDsign_12_26'],lw=1,linestyle='-',label='MACD Signal')
    plt.plot(df['MACDdiff_12_26'],lw=1,linestyle='-',label='MACD Difference')
    plt.legend(loc=2,prop={'size':9})
    plt.title("MACD",fontsize=18)
    plt.ylabel('Values')
    plt.grid(True)
    plt.setp(plt.gca().get_xticklabels(),rotation=30)
    plt.show()
    return df

def relative_strength_index(df,symbol):
    rsi_period=14
    chg=df['Close'].diff(1)
    gain=chg.mask(chg<0,0)
    df['Gain']=gain
    loss=chg.mask(chg>0,0)
    df['Loss']=loss
    avg_gain=gain.ewm(com=rsi_period-1,min_periods=rsi_period).mean()
    avg_loss=loss.ewm(com=rsi_period-1,min_periods=rsi_period).mean()
    df['Avg_Gain']=avg_gain
    df['Avg_Loss']=avg_loss
    rs=abs(avg_gain/avg_loss)
    rsi=100-(100/(1+rs))
    df['RSI']=rsi
    fig=plt.figure(figsize=(15,15))
    ax=fig.add_subplot(2,1,1)
    # ax.set_xticklabels([]) - to remove the x labels
    plt.plot(df['Close'],lw=1,linestyle='-',label="Close Price")
    plt.legend(loc='best',prop={'size':9})
    plt.title(symbol,fontsize=18)
    plt.ylabel("Close Price")
    plt.grid(True)
    bx=fig.add_subplot(2,1,2)
    # bx.set_xticklabels([]) - to remove the x labels
    plt.plot(df['RSI'],'k',lw=1,linestyle='-',label='RSI')
    plt.legend(loc='best',prop={'size':9})
    plt.title("RSI",fontsize=18)
    plt.ylabel('Values')
    plt.grid(True)
    plt.setp(plt.gca().get_xticklabels(),rotation=30)
    plt.show()
    return df
    
def fibonacci(df,symbol):
    price_max=df['Close'].max()
    price_min=df['Close'].min()
    diff=price_max-price_min
    level1=price_max-0.382*diff
    level2=price_max-0.5*diff
    level3=price_max-0.618*diff
    print(tabulate([['0%',price_max],['38.2%',level1],['50%',level2],['61.8%',level3],['100%',price_min]],headers=['Level','Price']))
    fig=plt.figure(figsize=(15,15))
    ax=fig.add_subplot(2,1,1)
    ax.plot(df.Close,color='black')
    ax.axhspan(level1,price_min,alpha=0.4,color='lightsalmon')
    ax.axhspan(level2,level1,alpha=0.5,color='palegoldenrod')
    ax.axhspan(level3,level2,alpha=0.5,color='palegreen')
    ax.axhspan(price_max,level3,alpha=0.5,color='powderblue')
    plt.title("Fibonacci Retrenchments",fontsize=18)
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend(loc="best")
    plt.show()
    return df
                                
def returns(df):
    df=np.log(df.Close)-np.log(df.Close.shift(1))
    return df
    
def aplha_beta_rsquared(symbol):
    end=today_date
    dd=datetime.timedelta(days=365*5)
    start=end-dd
    df_stock=stock_historical(symbol,start,end)
    df_index=index_historical("NIFTY",start,end)
    df_stock['Returns']=returns(df_stock)
    df_index['Returns']=returns(df_index)
    df_stock=df_stock.dropna()
    df_index=df_index.dropna()
    stock_ret=df_stock['Returns']
    index_ret=df_index['Returns']
    covmat=np.cov(stock_ret,index_ret)
    beta=covmat[0,1]/covmat[1,1]
    alpha=np.mean(stock_ret-beta*np.mean(index_ret))
    ypred=alpha+beta*index_ret
    ss_res=np.sum(np.power(ypred-stock_ret,2))
    ss_tot=covmat[0,0]*(len(df_stock)-1)
    r_squared=1-ss_res/ss_tot
    return alpha,beta,r_squared
    
def beta(symbol):
    end=today_date
    dd=datetime.timedelta(days=365*5)
    start=end-dd
    df_stock=stock_historical(symbol,start,end)
    df_index=index_historical("NIFTY",start,end)
    df_stock['Returns']=returns(df_stock)
    df_index['Returns']=returns(df_index)
    df_stock=df_stock.dropna()
    df_index=df_index.dropna()
    stock_ret=df_stock['Returns']
    index_ret=df_index['Returns']
    covmat=np.cov(stock_ret,index_ret)
    beta=covmat[0,1]/covmat[1,1]
    return beta
    
def portfolio_historical(symbol,start,end):
    historical=get_history(symbol=symbol,start=start,end=end)
    port_ret=returns(historical)
    close=historical.Close
    return port_ret,close
    
def sumproduct(lista,listb):
    lists=lista,listb
    sum_product=sum([x*y for x,y in zip(*lists)])
    return sum_product
    
def rsi_screen_stocks(df):
    rsi_period=14
    chg=df['Close'].diff(1)
    gain=chg.mask(chg<0,0)
    df['Gain']=gain
    loss=chg.mask(chg>0,0)
    df['Loss']=loss
    avg_gain=gain.ewm(com=rsi_period-1,min_periods=rsi_period).mean()
    avg_loss=loss.ewm(com=rsi_period-1,min_periods=rsi_period).mean()
    df['Avg_Gain']=avg_gain
    df['Avg_Loss']=avg_loss
    rs=abs(avg_gain/avg_loss)
    rsi=100-(100/(1+rs))
    df['RSI']=rsi
    return df['RSI']

def macd_screen_stocks(df):
    n_fast=12
    n_slow=26
    emafast=pd.Series(df['Close'].ewm(span=n_fast,min_periods=n_slow).mean())
    emaslow=pd.Series(df['Close'].ewm(span=n_slow,min_periods=n_slow).mean())
    macd=pd.Series(emafast-emaslow,name='MACD_'+str(n_fast)+'_' + str(n_slow))
    macdsign=pd.Series(macd.ewm(span=9, min_periods=9).mean(),name='MACDsign_'+str(n_fast)+'_'+str(n_slow))
    macddiff=pd.Series(macd-macdsign,name='MACDdiff')
    df=df.join(macd)
    df=df.join(macdsign)
    df=df.join(macddiff)
    return df['MACDdiff']
    
def ema_single_screen_stocks(df,n1):
    ema=pd.Series(df['Close'].ewm(span=n, min_periods=n).mean(), name='EMA')
    df=df.join(ema)
    return df['EMA']

def ema_double_screen_stocks(df,n1,n2):
    ema1=pd.Series(df['Close'].ewm(span=n1, min_periods=n1).mean(), name='EMA1')
    ema2=pd.Series(df['Close'].ewm(span=n2, min_periods=n2).mean(), name='EMA2')
    df=df.join(ema1)
    df=df.join(ema2)
    return df['EMA1'],df['EMA2']
    
def ema_triple_screen_stocks(df,n1,n2,n3):
    ema1=pd.Series(df['Close'].ewm(span=n1, min_periods=n1).mean(), name='EMA1')
    ema2=pd.Series(df['Close'].ewm(span=n2, min_periods=n2).mean(), name='EMA2')
    ema3=pd.Series(df['Close'].ewm(span=n3, min_periods=n3).mean(), name='EMA3')
    df=df.join(ema1)
    df=df.join(ema2)
    df=df.join(ema3)
    return df['EMA1'],df['EMA2'],df['EMA3']
    
def ema_single_screener():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    while(True):
        n1=(int)(input("Please enter the Time Period: "))
        if(n1>=4 and n1<=200):
            break
        else:
            invalid()
    print("\nFollowing are the Names of the Stocks which follows your Criteria:\n")
    for i in range(len(symbol_nifty_100_list)):
        df=stock_historical(symbol_nifty_100_list[i],start,end)
        ema=ema_single_screen_stocks(df,n1)
        ema=(int)(ema[-1:])
        spot_price=(int)(spot(symbol_nifty_100_list[i]))
        if(spot_price>ema):
            print(name_symbol[symbol_nifty_100_list[i]])
    
def ema_double_screener():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    while(True):
        n1=(int)(input("Please enter the Time Period 1: "))
        if(n1>=4 and n1<=200):
            n2=(int)(input("Please enter the Time Period 2: "))
            if(n2>n1 and n2<=200):
                break
        else:
            invalid()
    for i in range(len(symbol_nifty_100_list)):
        df=stock_historical(symbol_nifty_100_list[i],start,end)
        ema1,ema2=ema_double_screen_stocks(df,n1,n2)
        ema1=(int)(ema1[-1:])
        ema2=(int)(ema2[-1:])
        spot_price=(int)(spot(symbol_nifty_100_list[i]))
        if(ema1>ema2):
            if(spot_price>ema1):
                print(name_symbol[symbol_nifty_100_list[i]])
    
def ema_triple_screener():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    while(True):
        n1=(int)(input("Please enter the Time Period 1: "))
        if(n1>=4 and n1<=200):
            n2=(int)(input("Please enter the Time Period 2: "))
            if(n2>n1 and n2<=200):
                n3=(int)(input("Please enter the Time Period 3: "))
                if(n3>n2 and n3<=200):
                    break
        else:
            invalid()
    for i in range(len(symbol_nifty_100_list)):
        df=stock_historical(symbol_nifty_100_list[i],start,end)
        ema1,ema2,ema3=ema_triple_screen_stocks(df,n1,n2,n3)
        ema1=(int)(ema1[-1:])
        ema2=(int)(ema2[-1:])
        ema3=(int)(ema3[-1:])
        spot_price=(int)(spot(symbol_nifty_100_list[i]))
        if(ema1>ema2):
            if(ema2>ema3):
                if(spot_price>ema1):
                    print(name_symbol[symbol_nifty_100_list[i]])

def rsi_screener():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    tech_names=[]
    print("\nWe have the following following Levels in RSI:")
    print("1. 30-70")
    print("2. 20-80")
    while(True):
        c=(int)(input("Please enter your choice: "))
        if(c>=1 and c<=2):
            break
        else:
            invalid()
    if(c==1):
        lower=30
        upper=70
    else:
        if(c==2):
            lower=20
            upper=80
    while(True):
        limit=(int)(input("Please enter the RSI Limit: "))
        if(limit>=lower and limit<=upper):
            break
        else:
            invalid()
    for i in symbol_nifty_100_list:
        df=stock_historical(i,start,end)
        rsi=rsi_screen_stocks(df)
        rsi=(int)(rsi[-1:])
        if(rsi>lower and rsi<upper):
            if(rsi>limit):
                tech_names.append(i)
    print("\nFollowing are the Names of the Stocks which follows your Criteria:\n")
    for i in tech_names:
        print(name_symbol[i])

def macd_screener():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    tech_names=[]
    for i in symbol_nifty_100_list:
        df=stock_historical(i,start,end)
        macd=macd_screen_stocks(df)
        macd=(int)(macd[-1:])
        if(macd>0):
            tech_names.append(i)
    print("\nFollowing are the Names of the Stocks which follows your Criteria:\n")
    for i in tech_names:
        print(name_symbol[i])

def ema_screener():
    print("1. Single Period EMA")
    print("2. Double Period Crossover EMA")
    print("3. Triple Period Crossover EMA")
    while(True):
        c=(int)(input("Please enter your choice: "))
        if(c>=1 and c<=3):
            break
        else:
            invalid()
    if(c==1):
        ema_single_screener()
    else:
        if(c==2):
            ema_double_screener()
        else:
            if(c==3):
                ema_triple_screener()

def high_low(df):
    high=df['Close'].max()
    low=df['Close'].min()
    return high,low
    
def top_gainers_losers_nifty_50():
    end=today_date
    dd=datetime.timedelta(days=3)
    start=end-dd
    returns_list=[]
    l=len(symbol_nifty_50_list)
    for i in range(l):
        df=stock_historical(symbol_nifty_50_list[i],start,end)
        close=(int)(df.Close[-1:])
        spot_price=(int)(spot(symbol_nifty_50_list[i]))
        returns=np.log(spot_price/close)
        returns_list.append(returns)
    dict_ret=dict(zip(returns_list,symbol_nifty_50_list))
    returns_list.sort()
    while(True):
        no=gainer_loser_no_stocks_input()
        no=(int)(no)
        if(no>0 and no<=10):
            break
        else:
            invalid()
    top_loser=returns_list[:no]
    top_gainer=returns_list[-no:]
    print("\nFollowing are the Names of the  Top ",no," Losers in NIFTY50:\n")
    for i in range(no):
        print(dict_ret[top_loser[i]])    
    print("\nFollowing are the Names of the  Top ",no," Winners in NIFTY50:\n")
    for i in range(no):
        print(dict_ret[top_gainer[i]])

def top_gainers_losers_nifty_100():
    end=today_date
    dd=datetime.timedelta(days=3)
    start=end-dd
    returns_list=[]
    l=len(symbol_nifty_100_list)
    for i in range(l):
        df=stock_historical(symbol_nifty_100_list[i],start,end)
        close=(int)(df.Close[-1:])
        spot_price=(int)(spot(symbol_nifty_100_list[i]))
        returns=np.log(spot_price/close)
        returns_list.append(returns)
    dict_ret=dict(zip(returns_list,symbol_nifty_100_list))
    returns_list.sort()
    while(True):
        no=gainer_loser_no_stocks_input()
        no=(int)(no)
        if(no>0 and no<=10):
            break
        else:
            invalid()
    top_loser=returns_list[:no]
    top_gainer=returns_list[-no:]
    print("\nFollowing are the Names of the  Top ",no," Losers in NIFTY100:\n")
    for i in range(no):
        print(dict_ret[top_loser[i]])    
    print("\nFollowing are the Names of the  Top ",no," Winners in NIFTY100:\n")
    for i in range(no):
        print(dict_ret[top_gainer[i]])

def high_low_52_week_nifty_50():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    l=len(symbol_nifty_50_list)
    print("\nFollowing are the Names of the NIFTY50 Stocks which have formed new 52 Week High:\n")
    for i in range(l):
        df=stock_historical(symbol_nifty_50_list[i],start,end)
        high,low=high_low(df)
        high=(int)(high)
        low=(int)(low)
        spot_price=(int)(spot(symbol_nifty_50_list[i]))
        if(spot_price>high):
            print(name_symbol[symbol_nifty_50_list[i]])
    print("\nFollowing are the Names of the NIFTY50 Stocks which have formed new 52 Week Low:\n")
    for i in range(l):
        df=stock_historical(symbol_nifty_50_list[i],start,end)
        high,low=high_low(df)
        high=(int)(high)
        low=(int)(low)
        spot_price=(int)(spot(symbol_nifty_50_list[i]))
        if(spot_price<low):
            print(name_symbol[symbol_nifty_50_list[i]])

def high_low_52_week_nifty_100():
    end=today_date
    dd=datetime.timedelta(days=365)
    start=end-dd
    name_symbol=dict(zip(symbol_list,name_list))
    l=len(symbol_nifty_100_list)
    print("\nFollowing are the Names of the NIFTY100 Stocks which have formed new 52 Week High:\n")
    for i in range(l):
        df=stock_historical(symbol_nifty_100_list[i],start,end)
        high,low=high_low(df)
        high=(int)(high)
        low=(int)(low)
        spot_price=(int)(spot(symbol_nifty_100_list[i]))
        if(spot_price>high):
            print(name_symbol[symbol_nifty_100_list[i]])
    print("\nFollowing are the Names of the NIFTY100 Stocks which have formed new 52 Week Low:\n")
    for i in range(l):
        df=stock_historical(symbol_nifty_100_list[i],start,end)
        high,low=high_low(df)
        high=(int)(high)
        low=(int)(low)
        spot_price=(int)(spot(symbol_nifty_100_list[i]))
        if(spot_price<low):
            print(name_symbol[symbol_nifty_100_list[i]])

def symbol_input_custom():
    print("\nSelect Stocks:")
    print("1. Selecting the Stocks by Stock Name")
    print("2. Choosing a file containing Stock Symbols (The Symbols must be written in a 'word(.docx)' File")
    while(True):
        c=(int)(input("Please enter your choice: "))
        if(c==1 or c==2):
            break
        else:
            invalid()
    sym_list=[]
    sym_list_empty=[]
    count=0
    if(c==1):
        l=0
        while(True):
            l=(int)(input("Please enter the Maximum Number of Stocks: "))
            if(l>=2 or l<=100):
                break
            else:
                invalid()
        for i in range(l):
            sym=symbol_input()
            sym_list.append(sym)
    if(c==2):
        message="Please choose the File"
        choose_file_message(message)
        filename2=askopenfilename()
        text2=docx2txt.process(filename2) 
        text=text2.split("\n")
        text=list(filter(None,text))
        sym_list=text
        for i in sym_list:
            if(i not in symbol_list):
                print("Symbol",i,"is an invalid Symbol")
                count+=1
    if(count==0):   
        return sym_list
    else:
        return sym_list_empty
    return (sym_list)

def symbol_input_custom_fno():
    print("\nHow do you want to add Stocks?")
    print("1. Selecting the Stocks by Stock Name")
    print("2. Choosing a file containing Stock Symbols (The Symbols must be written in a 'word(.docx)' file")
    while(True):
        c=(int)(input("Please enter your choice: "))
        if(c==1 or c==2):
            break
        else:
            invalid()
    sym_list=[]
    sym_list_empty=[]
    count1=0
    count2=0
    if(c==1):
        l=0
        while(True):
            l=(int)(input("Please enter the maximum number of Stocks: "))
            if(l>=2 or l<=100):
                break
            else:
                invalid()
        for i in range(l):
            sym=symbol_input_fno()
            sym_list.append(sym)
    if(c==2):
        message="Please choose the File"
        choose_file_message(message)
        filename2=askopenfilename()
        text2=docx2txt.process(filename2) 
        text=text2.split("\n")
        text=list(filter(None,text))
        sym_list=text
        for i in sym_list:
            if(i not in symbol_list):
                print("Symbol",i,"is an invalid Symbol")
                count1+=1
        if(count1==0):
            for i in sym_list:
                if(i not in symbol_fno_list):
                    print("Symbol",i,"is not in F&O Segment")
                    count2+=1
    if(count1==0 and count2==0):   
        return sym_list
    else:
        return sym_list_empty

def stock_historical_returns(symbol,start,end):
    historical=get_history(symbol=symbol,start=start,end=end)
    historical['Returns']=returns(historical)
    historical[symbol]=historical['Returns']
    return historical[symbol]
    
def stock_future_oi(symbol,start,end,expiry):
    future=get_history(symbol=symbol,start=start,end=end,futures=True,expiry_date=expiry)
    future[symbol]=future['Open Interest']
    return future[symbol]
    
def call_payoff(s,k,call_value):
    return np.where(s>k,s-k,0)-call_value
    
def put_payoff(s,k,put_value):
    return np.where(s<k,k-s,0)-put_value

def strike_input_bull_call_spread(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2    
            
def bull_call_spread():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_bull_call_spread(symbol,s)
    k_long_call=k1
    price_long_call=p1
    k_short_call=k2
    price_short_call=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_short_call=call_payoff(s_range,k_short_call,price_short_call)*-1
    payoff=payoff_long_call+payoff_short_call
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Bull Call Spread Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_bear_put_spread(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2

def bear_put_spread():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_bear_put_spread(symbol,s)
    k_long_put=k1
    price_long_put=p1
    k_short_put=k2
    price_short_put=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff_short_put=put_payoff(s_range,k_short_put,price_short_put)*-1
    payoff=payoff_long_put+payoff_short_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Bear Put Spread Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_bull_call_spread_ratio(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2

def bull_call_spread_ratio():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_bull_call_spread_ratio(symbol,s)
    k_long_call=k1
    price_long_call=p1
    k_short_call1=k2
    price_short_call1=p2
    k_short_call2=k2
    price_short_call2=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_short_call1=call_payoff(s_range,k_short_call1,price_short_call1)*-1
    payoff_short_call2=call_payoff(s_range,k_short_call2,price_short_call2)*-1
    payoff=payoff_long_call+payoff_short_call1+payoff_short_call2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Bull Call Spread Ratio Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_bear_put_spread_ratio(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2
    
def bear_put_spread_ratio():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_bear_put_spread_ratio(symbol,s)
    k_long_put=k1
    price_long_put=p1
    k_short_put1=k2
    price_short_put1=p2
    k_short_put2=k2
    price_short_put2=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff_short_put1=put_payoff(s_range,k_short_put1,price_short_put1)*-1
    payoff_short_put2=put_payoff(s_range,k_short_put2,price_short_put2)*-1
    payoff=payoff_long_put+payoff_short_put1+payoff_short_put2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Bear Put Spread Ratio Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_straddle(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Option Strike"
        strike=option_strike_input(message_strike)
        strike=(int)(strike)
        message_price="Please enter the Option Strike Value"
        p=option_price_input(message_price)
        p=float(p)
        if(strike>s):
            break
        else:
            invalid()
    browser.close()
    return strike,p
    
def straddle():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k,p=strike_input_straddle(symbol,s)
    k_long_call=k
    price_long_call=p
    k_long_put=k
    price_long_put=p
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff=payoff_long_call+payoff_long_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Straddle Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def strike_input_strangle(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2
    
def strangle():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_straddle(symbol,s)
    k_long_call=k1
    price_long_call=p1
    k_long_put=k2
    price_long_put=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff=payoff_long_call+payoff_long_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Strangle Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def strike_input_straddle_strip(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Option Strike"
        strike=option_strike_input(message_strike)
        strike=(int)(strike)
        message_price="Please enter the Option Strike Value"
        p=option_price_input(message_price)
        p=float(p)
        if(strike>s):
            break
        else:
            invalid()
    browser.close()
    return strike,p
    
def straddle_strip():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k,p=strike_input_straddle_strip(symbol,s)
    k_long_call=k
    price_long_call=p
    k_long_put1=k
    price_long_put1=p
    k_long_put2=k
    price_long_put2=p
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_long_put1=put_payoff(s_range,k_long_put1,price_long_put1)
    payoff_long_put2=put_payoff(s_range,k_long_put2,price_long_put2)
    payoff=payoff_long_call+payoff_long_put1+payoff_long_put2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Straddle Strip Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def strike_input_straddle_strap(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Option Strike"
        strike=option_strike_input(message_strike)
        strike=(int)(strike)
        message_price="Please enter the Option Strike Value"
        p=option_price_input(message_price)
        p=float(p)
        if(strike>s):
            break
        else:
            invalid()
    browser.close()
    return strike,p
    
def straddle_strap():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k,p=strike_input_straddle_strap(symbol,s)
    k_long_call1=k
    price_long_call1=p
    k_long_call2=k
    price_long_call2=p
    k_long_put=k
    price_long_put=p
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call1=call_payoff(s_range,k_long_call1,price_long_call1)
    payoff_long_call2=call_payoff(s_range,k_long_call2,price_long_call2)
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff=payoff_long_call1+payoff_long_call2+payoff_long_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Straddle Strap Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_strangle_strip(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2
    
def strangle_strip():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_strangle_strip(symbol,s)
    k_long_call=k1
    price_long_call=p1
    k_long_put1=k2
    price_long_put1=p2
    k_long_put2=k2
    price_long_put2=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_long_put1=put_payoff(s_range,k_long_put1,price_long_put1)
    payoff_long_put2=put_payoff(s_range,k_long_put2,price_long_put2)
    payoff=payoff_long_call+payoff_long_put1+payoff_long_put2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Strangle Strip Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def strike_input_strangle_strap(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Higher Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Higher Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    while(True):
        message_strike="Please enter the Lower Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Lower Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike1>strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,p1,p2
    
def strangle_strap():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,p1,p2=strike_input_strangle_strap(symbol,s)
    k_long_call1=k1
    price_long_call1=p1
    k_long_call2=k1
    price_long_call2=p1
    k_long_put=k2
    price_long_put=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call1=call_payoff(s_range,k_long_call1,price_long_call1)
    payoff_long_call2=call_payoff(s_range,k_long_call2,price_long_call2)
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff=payoff_long_call1+payoff_long_call2+payoff_long_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Strangle Strap Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_butterfly_call(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Highest Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Highest Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    message_strike="Please enter the Lowest Option Strike"
    strike3=option_strike_input(message_strike)
    strike3=(int)(strike3)
    message_price="Please enter the Lowest Option Strike Value"
    p3=option_price_input(message_price)
    p3=float(p3)
    while(True):
        message_strike="Please enter the Middle Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Middle Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(((strike3+strike1)/2)==strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,strike3,p1,p2,p3
    
def butterfly_call():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,k3,p1,p2,p3=strike_input_butterfly_call(symbol,s)
    k_long_call1=k1
    price_long_call1=p1
    k_long_call2=k3
    price_long_call2=p3
    k_short_call1=k2
    price_short_call1=p2
    k_short_call2=k2
    price_short_call2=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call1=call_payoff(s_range,k_long_call1,price_long_call1)
    payoff_long_call2=call_payoff(s_range,k_long_call2,price_long_call2)
    payoff_short_call1=call_payoff(s_range,k_short_call1,price_short_call1)*-1
    payoff_short_call2=call_payoff(s_range,k_short_call2,price_short_call2)*-1
    payoff=payoff_long_call1+payoff_short_call1+payoff_long_call2+payoff_short_call2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Butterfly Call Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def strike_input_butterfly_put(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    message_strike="Please enter the Highest Option Strike"
    strike1=option_strike_input(message_strike)
    strike1=(int)(strike1)
    message_price="Please enter the Highest Option Strike Value"
    p1=option_price_input(message_price)
    p1=float(p1)
    message_strike="Please enter the Lowest Option Strike"
    strike3=option_strike_input(message_strike)
    strike3=(int)(strike3)
    message_price="Please enter the Lowest Option Strike Value"
    p3=option_price_input(message_price)
    p3=float(p3)
    while(True):
        message_strike="Please enter the Middle Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Middle Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(((strike3+strike1)/2)==strike2):
            break
        else:
            invalid()
    browser.close()
    return strike1,strike2,strike3,p1,p2,p3
    
def butterfly_put():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,k3,p1,p2,p3=strike_input_butterfly_put(symbol,s)
    k_long_put1=k1
    price_long_put1=p1
    k_long_put2=k3
    price_long_put2=p3
    k_short_put1=k2
    price_short_put1=p2
    k_short_put2=k2
    price_short_put2=p2
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_put1=put_payoff(s_range,k_long_put1,price_long_put1)
    payoff_long_put2=put_payoff(s_range,k_long_put2,price_long_put2)
    payoff_short_put1=put_payoff(s_range,k_short_put1,price_short_put1)*-1
    payoff_short_put2=put_payoff(s_range,k_short_put2,price_short_put2)*-1
    payoff=payoff_long_put1+payoff_short_put1+payoff_long_put2+payoff_short_put2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Butterfly Put Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_condor_call(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Highest Option Strike"
        strike1=option_strike_input(message_strike)
        strike1=(int)(strike1)
        message_price="Please enter the Highest Option Strike Value"
        p1=option_price_input(message_price)
        p1=float(p1)
        message_strike="Please enter the Second Highest Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Second Highest Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike2<strike1):
            message_strike="Please enter the Third Highest Option Strike"
            strike3=option_strike_input(message_strike)
            strike3=(int)(strike3)
            message_price="Please enter the Third Highest Option Strike Value"
            p3=option_price_input(message_price)
            p3=float(p3)
            if(strike3<strike2):
                message_strike="Please enter the Lowest Option Strike"
                strike4=option_strike_input(message_strike)
                strike4=(int)(strike4)
                message_price="Please enter the Lowest Option Strike Value"
                p4=option_price_input(message_price)
                p4=float(p4)
                if(strike4<strike3):
                    break
    browser.close()
    return strike1,strike2,strike3,strike4,p1,p2,p3,p4

def condor_call():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,k3,k4,p1,p2,p3,p4=strike_input_condor_call(symbol,s)
    k_long_call1=k1
    price_long_call1=p1
    k_short_call1=k2
    price_short_call1=p2
    k_long_call2=k4
    price_long_call2=p4
    k_short_call2=k3
    price_short_call2=p3
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call1=call_payoff(s_range,k_long_call1,price_long_call1)
    payoff_short_call1=call_payoff(s_range,k_short_call1,price_short_call1)*-1
    payoff_long_call2=call_payoff(s_range,k_long_call2,price_long_call2)
    payoff_short_call2=call_payoff(s_range,k_short_call2,price_short_call2)*-1
    payoff=payoff_long_call1+payoff_short_call1+payoff_long_call2+payoff_short_call2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Condor Call Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_condor_put(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Highest Option Strike"
        strike1=option_strike_input(message_strike)
        strike1=(int)(strike1)
        message_price="Please enter the Highest Option Strike Value"
        p1=option_price_input(message_price)
        p1=float(p1)
        message_strike="Please enter the Second Highest Option Strike"
        strike2=option_strike_input(message_strike)
        strike2=(int)(strike2)
        message_price="Please enter the Second Highest Option Strike Value"
        p2=option_price_input(message_price)
        p2=float(p2)
        if(strike2<strike1):
            message_strike="Please enter the Third Highest Option Strike"
            strike3=option_strike_input(message_strike)
            strike3=(int)(strike3)
            message_price="Please enter the Third Highest Option Strike Value"
            p3=option_price_input(message_price)
            p3=float(p3)
            if(strike3<strike2):
                message_strike="Please enter the Lowest Option Strike"
                strike4=option_strike_input(message_strike)
                strike4=(int)(strike4)
                message_price="Please enter the Lowest Option Strike Value"
                p4=option_price_input(message_price)
                p4=float(p4)
                if(strike4<strike3):
                    break
    browser.close()
    return strike1,strike2,strike3,strike4,p1,p2,p3,p4

def condor_put():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,k3,k4,p1,p2,p3,p4=strike_input_condor_put(symbol,s)
    k_long_put1=k1
    price_long_put1=p1
    k_short_put1=k2
    price_short_put1=p2
    k_long_put2=k4
    price_long_put2=p4
    k_short_put2=k3
    price_short_put2=p3
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_put1=put_payoff(s_range,k_long_put1,price_long_put1)
    payoff_short_put1=put_payoff(s_range,k_short_put1,price_short_put1)*-1
    payoff_long_put2=put_payoff(s_range,k_long_put2,price_long_put2)
    payoff_short_put2=put_payoff(s_range,k_short_put2,price_short_put2)*-1
    payoff=payoff_long_put1+payoff_short_put1+payoff_long_put2+payoff_short_put2
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Condor Put Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()

def strike_input_iron_condor(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Highest Option Strike"
        strike1=option_strike_input(message_strike)
        strike1=(int)(strike1)
        message_price="Please enter the Highest Option Strike Value"
        p1=option_price_input(message_price)
        p1=float(p1)
        if(strike1<s):
            message_strike="Please enter the Second Highest Option Strike"
            strike2=option_strike_input(message_strike)
            strike2=(int)(strike2)
            message_price="Please enter the Second Highest Option Strike Value"
            p2=option_price_input(message_price)
            p2=float(p2)
            if(strike2<strike1):
                break
            else:
                invalid()
    while(True):    
        message_strike="Please enter the Third Highest Option Strike"
        strike3=option_strike_input(message_strike)
        strike3=(int)(strike3)
        message_price="Please enter the Third Highest Option Strike Value"
        p3=option_price_input(message_price)
        p3=float(p3)
        if(strike2>strike3):
            message_strike="Please enter the Lowest Option Strike"
            strike4=option_strike_input(message_strike)
            strike4=(int)(strike4)
            message_price="Please enter the Lowest Option Strike Value"
            p4=option_price_input(message_price)
            p4=float(p4)
            if(strike4<strike3):
                break
            else:
                invalid()
    browser.close()
    return strike1,strike2,strike3,strike4,p1,p2,p3,p4

def iron_condor():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,k3,k4,p1,p2,p3,p4=strike_input_iron_condor(symbol,s)
    k_long_call=k1
    price_long_call=p1
    k_short_call=k2
    price_short_call=p2
    k_long_put=k4
    price_long_put=p4
    k_short_put=k3
    price_short_put=p3
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_short_call=call_payoff(s_range,k_short_call,price_short_call)*-1
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff_short_put=put_payoff(s_range,k_short_put,price_short_put)*-1
    payoff=payoff_long_call+payoff_short_call+payoff_long_put+payoff_short_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Iron Condor Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def strike_input_iron_butterfly(symbol,s):
    symbol=symbol+"\n"
    browser=webdriver.Chrome("chromedriver")
    browser.get("https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp")
    search=browser.find_element_by_id("underlyStock")
    search.send_keys(symbol)
    while(True):
        message_strike="Please enter the Highest Option Strike"
        strike1=option_strike_input(message_strike)
        strike1=(int)(strike1)
        message_price="Please enter the Highest Option Strike Value"
        p1=option_price_input(message_price)
        p1=float(p1)
        if(strike1<s):
            message_strike="Please enter the Second Highest Option Strike"
            strike2=option_strike_input(message_strike)
            strike2=(int)(strike2)
            message_price="Please enter the Second Highest Option Strike Value"
            p2=option_price_input(message_price)
            p2=float(p2)
            if(strike2<strike1):
                message_strike="Please enter the Lowest Option Strike"
                strike3=option_strike_input(message_strike)
                strike3=(int)(strike3)
                message_price="Please enter the Lowest Option Strike Value"
                p3=option_price_input(message_price)
                p3=float(p3)
                if(strike3<strike2):
                    break
                else:
                    invalid()
    browser.close()
    return strike1,strike2,strike3,p1,p2,p3

def iron_butterfly():
    symbol=symbol_input_fno()
    s=spot(symbol)
    close_price_message(s)
    k1,k2,k4,p1,p2,p4=strike_input_iron_butterfly(symbol,s)
    k3=k2
    p3=p2
    k_long_call=k1
    price_long_call=p1
    k_short_call=k2
    price_short_call=p2
    k_long_put=k4
    price_long_put=p4
    k_short_put=k3
    price_short_put=p3
    s_range=np.arange(0.5*s,2*s,1)
    payoff_long_call=call_payoff(s_range,k_long_call,price_long_call)
    payoff_short_call=call_payoff(s_range,k_short_call,price_short_call)*-1
    payoff_long_put=put_payoff(s_range,k_long_put,price_long_put)
    payoff_short_put=put_payoff(s_range,k_short_put,price_short_put)*-1
    payoff=payoff_long_call+payoff_short_call+payoff_long_put+payoff_short_put
    plt.plot(s_range,payoff,label='Payoff')
    plt.title("Iron Butterfly Payoff")
    plt.xlabel('Stock Prices')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.show()
    
def two_leg_option_strategies():
    while(True):
        print("\nWe have the following options in 2 Leg Option Trading Strategies:")
        print("1. Bull Call Spread")
        print("2. Bear Put Spread")
        print("3. Bull Call Spread Ratio")
        print("4. Bear Put Spread Ratio")
        print("5. Straddle")
        print("6. Strangle")
        print("7. Straddle Strip")
        print("8. Straddle Strap")
        print("9. Strangle Strip")
        print("10. Strangle Strap")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=10):
                break
            else:
                invalid()
        if(c==1):
            bull_call_spread()
        else:
            if(c==2):
                bear_put_spread()
            else:
                if(c==3):
                    bull_call_spread_ratio()
                else:
                    if(c==4):
                        bear_put_spread_ratio()
                    else:
                        if(c==5):
                            straddle()
                        else:
                            if(c==6):
                                strangle()
                            else:
                                if(c==7):
                                    straddle_strip()
                                else:
                                    if(c==8):
                                        straddle_strap()
                                    else:
                                        if(c==9):
                                            strangle_strip()
                                        else:
                                            if(c==10):
                                                strangle_strap()
                                                
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def three_leg_option_strategies():
    while(True):
        print("\nWe have the following options in 3 Leg Option Trading Strategies:")
        print("1. Butterfly Call")
        print("2. Butterfly Put")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=2):
                break
            else:
                invalid()
        if(c==1):
            butterfly_call()
        else:
            if(c==2):
                butterfly_put()
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break
    
def four_leg_option_strategies():
    while(True):
        print("\nWe have the following options in 4 Leg Option Trading Strategies:")
        print("1. Condor Call")
        print("2. Condor Put")
        print("3. Iron Condor")
        print("4. Iron Butterfly")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=4):
                break
            else:
                invalid()
        if(c==1):
            condor_call()
        else:
            if(c==2):
                condor_put()
            else:
                if(c==3):
                    iron_condor()
                else:
                    if(c==4):
                        iron_butterfly()
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def bhav():
    while(True):
        while(True):
            date_entry=date_entry_bhav()
            year,month,day=map(int,date_entry.split('-'))
            valid=valid_date(year,month,day)
            if(valid==1):
                date=datetime.date(year,month,day)
                if(date<=today_date):
                    break
                else:
                    invalid_date()
            else:
                invalid_date()
        bhav=bhavcopy(date)
        print(bhav)
        c=save()
        if(c==True):
            bhav.to_csv('BhavCopy.csv',index=False,header=True)
            message="Your file has been saved by the name: BhavCopy.csv"
            save_message(message)
            
        response=cont()
        if(response==False):
            continue_message_main()
            break    
    
def quote():
    while(True):
        symbol=symbol_input()
        quote=stock_quote(symbol)
        pprint(quote)
        
        response=cont()
        if(response==False):
            continue_message_main()
            break

def stocks():
    print("\nWe have the following options in Stocks:")
    while(True):
        print("1. Stock Historical Data")
        print("2. Stock Futures Historical Data")
        print("3. Stock Options Historical Data")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=3):
                break
            else:
                invalid()
        if(c==1):
            symbol=symbol_input()
            start,end=date_entry()
            historical=stock_historical(symbol,start,end)
            print(historical)
            c=save()
            if(c==True):
                historical.to_csv(symbol+'_Historical_Data.csv',index=False,header=True)
                message="Your file has been saved by the name: ",symbol,"_Historical_Data.csv"
                save_message(message)
        else:
            if(c==2):
                while(True):
                    symbol=symbol_input()
                    if(symbol in symbol_fno_list):
                        break;
                    else:
                        print("You have choosen the Company, which is not traded in F&O Segment")
                start,end,expdt=date_entry_fno()
                future=stock_future(symbol,start,end,expdt) 
                print(future)
                c=save()
                if(c==True):
                    future.to_csv(symbol+'_Futures_Data.csv',index=False,header=True)
                    message="Your file has been saved by the name: ",symbol,"_Futures_Data.csv"
                    save_message(message)
            else:
                if(c==3):
                    symbol=symbol_input_fno()
                    start,end,expdt=date_entry_fno()
                    close=spot(symbol)
                    close_price_message(close)
                    strike=browser(symbol)
                    option_type=option_type_input()
                    option=stock_option(symbol,start,end,option_type,strike,expdt) 
                    print(option)
                    c=save()
                    if(c==True):
                        option.to_csv(symbol+'_Options_Data.csv',index=False,header=True)
                        message="Your file has been saved by the name: ",symbol,"_Options_Data.csv"
                        save_message(message)
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break
            
def index():
    print("\nWe have the following options in Index:")
    while(True):
        print("1. Index Historical Data")
        print("2. Index Futures Historical Data")
        print("3. Index Options Historical Data")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=3):
                break
            else:
                invalid()
        if(c==1):
            while(True):
                symbol=(input("Please enter the Index Symbol (in UPPECASE): "))
                if(symbol=='NIFTY' or symbol=='BANKNIFTY'):
                    break
                else:
                    invalid()
            start,end=date_entry()
            historical=index_historical(symbol,start,end)
            print(historical)
            c==save()
            if(c==True):
                historical.to_csv(symbol+'_Historical_Data.csv',index=False,header=True)
                message="Your file has been saved by the name: ",symbol,"_Historical_Data.csv"
                save_message(message)
        else:
            if(c==2):
                while(True):
                    symbol=(input("Please enter the Index Symbol (in UPPECASE): "))
                    if(symbol=='NIFTY' or symbol=='BANKNIFTY'):
                        break
                    else:
                        invalid()
                start,end,expdt=date_entry_fno()
                future=index_future(symbol,start,end,expdt) 
                print(future)
                c=save()
                if(c==True):
                    future.to_csv(symbol+'_Futures_Data.csv',index=False,header=True)
                    message="Your file has been saved by the name: ",symbol,"_Futures_Data.csv"
                    save_message(message)
            else:
                if(c==3):
                    while(True):
                        symbol=(input("Please enter the Index Symbol (in UPPECASE): "))
                        if(symbol=='NIFTY' or symbol=='BANKNIFTY'):
                            break
                        else:
                            invalid()
                    start,end,expdt=date_entry_fno()
                    df=index_historical(symbol,start,end)
                    close=df.Close[-1:]
                    close_price_message(close)
                    strike=browser(symbol)
                    option_type=option_type_input()
                    option=index_option(symbol,start,end,option_type,strike,expdt) 
                    print(option)
                    c=save()
                    if(c==True):
                        option.to_csv(symbol+'_Options_Data.csv',index=False,header=True)
                        message="Your file has been saved by the name: ",symbol,"_Options_Data.csv"
                        save_message(message)
                   
        response=cont()
        if(response==False):
            continue_message_sub()
            break
        
def black_scholes():
    while(True):
        symbol=symbol_input_fno()
        s=spot(symbol)
        close_price_message(s)
        k=browser(symbol)  
        r=rate()
        month_current=today_date.month
        year=today_date.year
        month_next=month_current+1
        exp_dt_current=expiry_date(year,month_current)
        exp_dt_next=expiry_date(year,month_next)
        if(exp_dt_next>today_date and exp_dt_current<today_date):
            expdt=expiry_date(year,month_next)    
        else:
            expdt=expiry_date(year,month_current) 
        t=expdt-today_date
        t=t.days
        t=t/365
        expdt=(str)(expdt)
        datee=datetime.datetime.strptime(expdt,"%Y-%m-%d").date()
        exp_year=datee.year
        exp_month=datee.month
        exp_day=datee.day
        month_names={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
        month_name=month_names.get(exp_month)
        exp_date=(str)(exp_day)+month_name+(str)(exp_year)
        v=implied_vol(symbol,exp_date)
        v=v/100
        d1=(np.log(s/k))+((r+(v**2)/2)*t)
        d2=d1-v*np.sqrt(t)
        nd1=norm.cdf(d1,0.0,1.0)
        nd2=norm.cdf(d2,0.0,1.0)
        c=s*nd1-nd2*(k*np.exp(-r*t))
        p=c+(k*np.exp(-r*t))-s
        print("Call Value: ",c)
        print("Put Value: ",p)
    
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def delta():
    while(True):
        symbol=symbol_input_fno()
        s=spot(symbol)
        close_price_message(s)
        k=browser(symbol)  
        r=rate()
        month_current=today_date.month
        year=today_date.year
        month_next=month_current+1
        exp_dt_current=expiry_date(year,month_current)
        exp_dt_next=expiry_date(year,month_next)
        if(exp_dt_next>today_date and exp_dt_current<today_date):
            expdt=expiry_date(year,month_next)    
        else:
            expdt=expiry_date(year,month_current)  
        t=expdt-today_date
        t=t.days
        t=t/365
        expdt=(str)(expdt)
        datee=datetime.datetime.strptime(expdt,"%Y-%m-%d").date()
        exp_year=datee.year
        exp_month=datee.month
        exp_day=datee.day
        month_names={1:"JAN",2:"FEB",3:"MAR",4:"APR",5:"MAY",6:"JUN",7:"JUL",8:"AUG",9:"SEP",10:"OCT",11:"NOV",12:"DEC"}
        month_name=month_names.get(exp_month)
        exp_date=(str)(exp_day)+month_name+(str)(exp_year)
        v=implied_vol(symbol,exp_date)
        v=v/100
        call_delta,put_delta=delta_value(s,k,r,t,v)
        print(symbol," Call Delta: ",call_delta," Put Delta",put_delta)
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def option_trading_strategies():
    while(True):
        print("\nWe have the following Legs in Option Trading Strategies:")
        print("1. 2 Leg Option Trading Strategies")
        print("2. 3 Leg Option Trading Strategies")
        print("3. 4 Leg Option Trading Strategies")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=3):
                break
            else:
                invalid()
        if(c==1):
            two_leg_option_strategies()
        else:
            if(c==2):
                three_leg_option_strategies()
            else:
                if(c==3):
                    four_leg_option_strategies()
       
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def candlestick():
    while(True):
        print("\nWe have the following Asset Class in Candlestick Charts:")
        print("Asset Class: 1. Stocks")
        print("             2. Indices")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c==1 or c==2):
                break
            else:
                invalid()
        if(c==1):
            symbol=symbol_input()
            break
        else:
            if(c==2):
                while(True):
                    symbol=(input("Please enter the Index Symbol (in UPPECASE): "))
                    if(symbol=='NIFTY' or symbol=='BANKNIFTY'):
                        break
                    else:
                        invalid()
            else:
                invalid()
        end=today_date
        dd=datetime.timedelta(days=365)
        start=end-dd
        if(c==1):
            df=stock_historical(symbol,start,end)
        else:
            if(c==2):
                df=index_historical(symbol,start,end)
        df=df.drop(["Symbol","Series","Prev Close","Last","VWAP","Turnover","Trades","Deliverable Volume","%Deliverble"],axis=1)
        df.to_csv("data_candlestick.csv",index=False,header=True)
        my_headers=["Date","Open","High","Low","Close","Volume"]
        my_dtypes={"Date":"str","Open":"float","High":"float","Low":"float","Close":"float","Volume":"int"}
        my_parse_dates=["Date"]
        load_data=pd.read_csv("data_candlestick.csv",header=1,names=my_headers,dtype=my_dtypes,parse_dates=my_parse_dates)
        load_data["Date"]=[mdates.date2num(d) for d in load_data["Date"]]
        os.remove("data_candlestick.csv")
        quotes=[tuple(x) for x in load_data[["Date","Open","High","Low","Close"]].values]
        fig,ax=plt.subplots()
        candlestick_ohlc(ax,quotes,width=0.5,colorup='g',colordown='r');
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Candlestick")
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gcf().autofmt_xdate()
        plt.autoscale(tight=True)
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def technical():
    while(True):
        print("\nWe have the following Asset Class in Technical Indicators:")
        print("Asset Class: 1. Stocks")
        print("             2. Indices")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c==1 or c==2):
                break
            else:
                invalid()
        if(c==1):
            symbol=symbol_input()
            break
        else:
            if(c==2):
                while(True):
                    symbol=(input("Please enter the Index Symbol (in UPPECASE): "))
                    if(symbol=='NIFTY' or symbol=='BANKNIFTY'):
                        break
                    else:
                        invalid()
            else:
                invalid()
    start,end=date_entry()
    if(c==1):
        df=stock_historical(symbol,start,end)
    else:
        if(c==2):
            df=index_historical(symbol,start,end)
    while(True):
        print("\nWe have the following Indicators in Technical Analysis:")
        print("1. Momentum Indicator")
        print("2. Bollinger Bands")
        print("3. Pivot Points")
        print("4. MACD")
        print("5. RSI")
        print("6. Fibonacci Retrenchments")
        print("7. Single Crossover EMA")
        print("8. Double Crossover EMA")
        print("9. Triple Crossover EMA")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=9):
                break
            else:
                invalid()
        if(c==1):
            df1=momentum(df,symbol)
        else:
            if(c==2):
                df1=bollinger_bands(df,symbol)
            else:
                if(c==3):
                    df1=ppsr(df,symbol)
                else:
                    if(c==4):
                        df1=macd(df,symbol)
                    else:
                        if(c==5):
                            df1=relative_strength_index(df,symbol)
                        else:
                            if(c==6):
                                df1=fibonacci(df,symbol)
                            else:
                                if(c==7):
                                    p=(int)(input("Please enter the Period: "))
                                    df1=ema_single(df,p,symbol)
                                else:
                                    if(c==8):
                                        p1=(int)(input("Please enter the First Period: "))
                                        p2=0
                                        while(True):
                                            p2=(int)(input("Please enter the Second Period: "))
                                            if(p2>p1):
                                                break
                                            else:
                                                invalid()
                                            df1=ema_double(df,p1,p2,symbol)
                                    else:
                                        if(c==9):
                                            p1=(int)(input("Please enter the First Period: "))
                                            p2=0
                                            p3=0
                                            while(True):
                                                p2=(int)(input("Please enter the Second Period: "))
                                                if(p2>p1):
                                                    break
                                                else:
                                                    invalid()
                                            while(True):
                                                p3=(int)(input("Please enter the Third Period: "))
                                                if(p3>p2):
                                                    break
                                                else:
                                                    invalid()
                                            df1=ema_triple(df,p1,p2,p3,symbol)
                                        else:
                                            invalid()
            
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def technical_screener():
    while(True):
        print("\nWe have the following Indicators in Technical Screener:")
        print("1. MACD")
        print("2. RSI")
        print("3. EMA")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=3):
                break
            else:
                invalid()
        if(c==1):
            macd_screener()
        else:
            if(c==2):
                rsi_screener()
            else:
                if(c==3):
                    ema_screener()
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break
    
def stock_analysis():
    while(True):
        symbol=symbol_input()
        start,end=date_entry()
        df_stock=stock_historical(symbol,start,end)
        df_index=index_historical("NIFTY",start,end)
        df_stock['Returns']=returns(df_stock)
        df_index['Returns']=returns(df_index)
        stock_ret=df_stock['Returns']
        index_ret=df_index['Returns']
        avg_ret_stock=stock_ret.mean()
        avg_ret_index=index_ret.mean()
        std_stock=stock_ret.std()
        std_index=index_ret.std()
        print(symbol," Average Return: ",avg_ret_stock)
        print("NIFTY Average Return: ",avg_ret_index)
        print(symbol," Standard Deviation: ",std_stock)
        print("NIFTY Standard Deviation: ",std_index)
        alpha,beta,r_squared=aplha_beta_rsquared(symbol)
        print("\nAlpha: ",alpha)
        print("Beta: ",beta)
        print("R-Squared: ",r_squared)
        var=df_stock[['Close']]
        var=np.log(df_stock.Close)-np.log(df_stock.Close.shift(1))
        mean=var.mean()
        std=var.std()
        var_95_par=norm.ppf(0.05,mean,std)
        var_99_par=norm.ppf(0.01,mean,std)
        print("\nParametric VaR")
        print(tabulate([['95%',var_95_par],['99%',var_99_par]],headers=["Confidence Level","Value at Risk"]))
        var.sort_values(inplace=True,ascending=True)
        var_95_hist=var.quantile(0.05)
        var_99_hist=var.quantile(0.01)
        print("\nHistoric VaR")
        print(tabulate([['95%',var_95_hist],['99%',var_99_hist]],headers=["Confidence Level","Value at Risk"]))
        sim_returns=[]
        for i in range(10000):
            rand_rets=np.random.normal(mean,std,252)
            sim_returns.append(rand_rets)
        var_95_mont=np.percentile(sim_returns,5)
        var_99_mont=np.percentile(sim_returns,1)
        print("\nMonte-Carlo VaR")
        print(tabulate([['95%',var_95_mont],['99%',var_99_mont]],headers=["Confidence Level","Value at Risk"]))
        x=index_ret[1:]
        y=stock_ret[1:]
        plt.figure(figsize=(15,15))
        plt.plot(df_stock['Returns'],label="Stock Returns")
        plt.plot(df_index['Returns'],label="Index Returns")
        plt.title("Stock vs Index Returns",fontsize=18)
        plt.ylabel("Returns")
        plt.legend(loc="best",prop={'size':9})
        plt.grid(True)
        plt.show()
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break
            
def top_gainers_losers():
    while(True):
        print("\nWe have the following Indices in Top Daily Gainers/Losers:")
        print("1. NIFTY50")
        print("2. NIFTY100")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=2):
                break
            else:
                invalid()
        if(c==1):
            top_gainers_losers_nifty_50()
        else:
            if(c==2):
                top_gainers_losers_nifty_100()
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break
            
def high_low_52_week():
    while(True):
        print("\nWe have the following Indices in 52 Weeks High/Low:")
        print("1. NIFTY50")
        print("2. NIFTY100")
        while(True):
            c=(int)(input("Please enter your choice: "))
            if(c>=1 and c<=2):
                break
            else:
                invalid()
        if(c==1):
            high_low_52_week_nifty_50()
        else:
            if(c==2):
                high_low_52_week_nifty_100()
        
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def stock_returns():
    while(True):
        sym_list_cust=symbol_input_custom()
        if(len(sym_list_cust)==0):
            continue_message_sub()
            break
        start,end=date_entry()
        df=stock_historical_returns(sym_list_cust[0],start,end)
        df=pd.DataFrame(df)
        sym_list_cust=sym_list_cust[1:]
        for i in sym_list_cust:
            df1=stock_historical_returns(i,start,end)
            df=df.join(df1)
        print(df)
        df.to_csv('Stock_Returns.csv',index=False,header=True)
        message="Your file has been saved by the name: Stock_Returns.csv"
        save_message(message)
    
        response=cont()
        if(response==False):
            continue_message_sub()
            break    
    
def stock_returns_correlation():
    while(True):
        sym_list_cust=symbol_input_custom()
        if(len(sym_list_cust)==0):
            continue_message_sub()
            break
        start,end=date_entry()
        df=stock_historical_returns(sym_list_cust[0],start,end)
        df=pd.DataFrame(df)
        sym_list_cust=sym_list_cust[1:]
        for i in sym_list_cust:
            df1=stock_historical_returns(i,start,end)
            df=df.join(df1)
        print(df)
        df1=df.corr()
        df1.to_csv('Stock_Returns_Correlation_Matrix.csv',index=False,header=True)
        message="Your file has been saved by the name: Stock_Returns_Correlation_Matrix.csv"
        save_message(message)

        response=cont()
        if(response==False):
            continue_message_sub()
            break 

def futures_oi():
    while(True):
        sym_list_cust=symbol_input_custom_fno()
        if(len(sym_list_cust)==0):
            continue_message_sub()
            break
        start,end,expiry=date_entry_fno()
        df=stock_future_oi(sym_list_cust[0],start,end,expiry)
        df=pd.DataFrame(df)
        sym_list_cust=sym_list_cust[1:]
        for i in sym_list_cust:
            df1=stock_future_oi(i,start,end,expiry)
            df=df.join(df1)
        print(df)
        df.to_csv('Stock_Futures_OI.csv',index=False,header=True)
        message="Your file has been saved by the name: Stock_Futures_OI.csv"
        save_message(message)
    
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def options_oi():
    while(True):
        message="Please choose the File"
        choose_file_message(message)
        csv_file_path=askopenfilename()
        df=pd.read_csv(csv_file_path)
        df['Date']=pd.to_datetime(df['Date'])
        df=df[["Date","Open Int"]].groupby('Date').sum()
        print(df)
        df.to_csv('Sum_OI.csv',index=False,header=True)
        message="Your file has been saved by the name: Sum_OI.csv"
        save_message(message)
    
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def pcr_oi():
    while(True):
        message="Please choose the Call Options Files"
        choose_file_message(message)
        csv_file_path=askopenfilename()
        df1=pd.read_csv(csv_file_path)
        df1['Date']=pd.to_datetime(df1['Date'])
        count=1
        while(True):
            response=messagebox.askquestion("Add Files","Do you want to add more files")
            if(response=='no'):
                break        
            else:
                csv_file_path=askopenfilename()
                df=pd.read_csv(csv_file_path)
                df['Date']=pd.to_datetime(df['Date'])
                df1=df1.append(df)
                count+=1
        df1=df1[["Date","Open Int"]].groupby('Date').sum()
        message="Please choose the Put Options Files"
        choose_file_message(message)
        csv_file_path=askopenfilename()
        df2=pd.read_csv(csv_file_path)
        df2['Date']=pd.to_datetime(df2['Date'])
        if(count>1):
            for i in range(count-1):
                csv_file_path=askopenfilename()
                df=pd.read_csv(csv_file_path)
                df['Date']=pd.to_datetime(df['Date'])
                df2=df2.append(df)
        df2=df2[["Date","Open Int"]].groupby('Date').sum()
        df=df2/df1
        df=df.mask(np.isinf(df))
        df=df.dropna()
        print(df)
        df.to_csv('PCR_OI.csv',index=False,header=True)
        plt.figure(figsize=(15,15))
        plt.plot(df,label="PCR OI")
        plt.ylabel("Ratios")
        plt.legend(loc="best",prop={'size':15})
        plt.show()
        message="Your file has been saved by the name: PCR_OI.csv"
        save_message(message)
    
        response=cont()
        if(response==False):
            continue_message_sub()
            break

def main():
    trading_day_check=trading_day()
    if(trading_day_check==False):
        trading_day_message()
        main_exit_message()
    else:
        message_datasets()
        disclaimer()
        name=name_input()
        print("\nHi",name,", Welcome to Mini-Project on NSE.")
        print("\nWe have the following Sections:")
        while(True):
            print("\n1. Bhavcopy of Stocks")
            print("2. Stock Quote")
            print("3. Historical Data")
            print("4. Technicals")
            print("5. Stock Options")
            print("6. Stock Analysis")
            print("7. Additional Information")
            print("8. Custom Data")
            print("9. Exit")
            c=(int)(input("Please enter your choice: "))
            if(c==1):
                bhav()   
            else:
                if(c==2):
                    quote() 
                else:
                    if(c==3):
                        while(True):
                            print("\nWe have the following options in Historical Data:")
                            print("1. Stocks")
                            print("2. Indices")
                            print("3. Exit to the Main Section")
                            while(True):
                                c=(int)(input("Please enter your choice: "))
                                if(c>=1 and c<=3):
                                    break
                                else:
                                    invalid()
                            if(c==1):
                                stocks()  
                            else:
                                if(c==2):
                                    index()
                                else:
                                    if(c==3):
                                        response=main_exit()
                                        if(response==True):
                                            continue_message_main()
                                            break
                    else:
                        if(c==4):
                            while(True):
                                print("\nWe have the following options in Technicals:")
                                print("1. Candlestick Chart")
                                print("2. Technical Indicators")
                                print("3. Technical Screener")
                                print("4. Exit to the Main Section")
                                while(True):
                                    c=(int)(input("Please enter your choice: "))
                                    if(c>=1 and c<=4):
                                        break
                                    else:
                                        invalid()
                                if(c==1):
                                    candlestick()
                                else:
                                    if(c==2):
                                        technical()
                                    else:
                                        if(c==3):
                                            technical_screener()
                                        else:
                                            if(c==4):
                                                response=main_exit()
                                                if(response==True):
                                                    continue_message_main()
                                                    break
                        else:
                            if(c==5):
                                while(True):
                                    print("\nWe have the following options in Stock Options:")
                                    print("1. Stock Option Theoritical Price using Black-Scholes")
                                    print("2. Stock Option Delta Value")
                                    print("3. Stock Option Trading Strategies")
                                    print("4. Exit to the Main Section")
                                    while(True):
                                        c=(int)(input("Please enter your choice: "))
                                        if(c>=1 and c<=4):
                                            break
                                        else:
                                            invalid()
                                    if(c==1):
                                        black_scholes()
                                    else:
                                        if(c==2):
                                            delta()
                                        else:
                                            if(c==3):
                                                option_trading_strategies()
                                            else:
                                                if(c==4):
                                                    response=main_exit()
                                                    if(response==True):
                                                        continue_message_main()
                                                        break
                            else:
                                if(c==6):
                                    stock_analysis()                                         
                                else:
                                    if(c==7):
                                        while(True):
                                            print("\nWe have the following options in Additional Information:")
                                            print("1. Daily Top Gainers/Losers")
                                            print("2. 52 Week High/Low")
                                            print("3. Exit to the Main Section")
                                            while(True):
                                                c=(int)(input("Please enter your choice: "))
                                                if(c>=1 and c<=3):
                                                    break
                                                else:
                                                    invalid()
                                            if(c==1):
                                                top_gainers_losers()
                                            else:
                                                if(c==2):
                                                    high_low_52_week()
                                                else:
                                                    if(c==3):
                                                        response=main_exit()
                                                        if(response==True):
                                                            continue_message_main()
                                                            break
                                    else:
                                        if(c==8):
                                            while(True):
                                                print("We have the following options in Custom Data:")
                                                print("1. Stocks Returns")
                                                print("2. Stocks Returns Correlation Matrix")
                                                print("3. Stock Futures OI")
                                                print("4. Stock Options OI")
                                                print("5. Stock Options PCR OI")
                                                print("6. Exit to the Main Section")
                                                while(True):
                                                    c=(int)(input("Please enter your choice: "))
                                                    if(c>=1 and c<=6):
                                                        break
                                                    else:
                                                        invalid()
                                                if(c==1):
                                                    stock_returns()
                                                else:
                                                    if(c==2):
                                                        stock_returns_correlation()
                                                    else:
                                                        if(c==3):
                                                            futures_oi()
                                                        else:
                                                            if(c==4):
                                                                options_oi()
                                                            else:
                                                                if(c==5):
                                                                    pcr_oi()
                                                                else:
                                                                    if(c==6):
                                                                        response=main_exit()
                                                                        if(response==True):
                                                                            continue_message_main()
                                                                            break
                                        else:
                                            if(c==9):
                                                response=main_exit()
                                                if(response==True):
                                                    main_exit_message()
                                                    break
                                            else:
                                                invalid()
                                            
main()
