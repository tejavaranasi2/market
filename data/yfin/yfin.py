try:
    import yfinance as yf
    import numpy as np
except:
    print("Import error: [data]")
    exit()


def get_open_close_with_time(sym,t):
  #t is time in months
  s_data=yf.Ticker(sym)
  hist=s_data.history(period=f"{t}mo")
  op=hist["Open"]
  cl=hist["Close"]

  return {"open":np.array(op),"close":np.array(cl)}

def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def get_curr_cost(sym_lst):
   to_ret=[]
   for sym in sym_lst:
    #print(stock.info)
    price = get_current_price(sym)
    
    to_ret.append(price)
   return to_ret

