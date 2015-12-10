
import urllib

class StockFormat(object):
    def __init__(self, name, code): 
        self.name = [name] if isinstance(name, str) else name
        self.code = code
    def __and__(self, other): return StockFormat(self.name + other.name,
                                                 self.code + other.code)
    def __repr__(self): return self.code

price                          = StockFormat('price', 'l1')
change                         = StockFormat('change', 'c1')
volume                         = StockFormat('volume', 'v')
average_daily_volume           = StockFormat('average_daily_volume', 'a2')
exchange                       = StockFormat('exchange', 'x')
market_cap                     = StockFormat('market_cap', 'j1')
book_value                     = StockFormat('book_value', 'b4')
ebitda                         = StockFormat('ebitda', 'j4')
dividend_per_share             = StockFormat('dividend_per_share', 'd')
dividend_yield                 = StockFormat('dividend_yield', 'y')
earnings_per_share             = StockFormat('earnings_per_share', 'e')
i52_week_high                  = StockFormat('52_week_high', 'k')
i52_week_low                   = StockFormat('52_week_low', 'j')
i50_day_moving_average         = StockFormat('50_day_moving_average', 'm3')
i200_day_moving_average        = StockFormat('200_day_moving_average', 'm4')
price_to_earnings_ratio        = StockFormat('price_to_earnings_ratio', 'r')
price_to_earnings_growth_ratio = StockFormat('price_to_earnings_growth_ratio', 'r5')
price_to_sales_ratio           = StockFormat('price_to_sales_ratio', 'p5')
price_to_book_ratio            = StockFormat('price_to_book_ratio', 'p6')
short_ratio                    = StockFormat('short_ratio', 's7')

def get(symbol, format):
    if isinstance(format, StockFormat):
        url = 'http://finance.yahoo.com/d/quotes?s=%s&f=%s' % (symbol, format.code)
        data = [x.strip('"') for x in urllib.urlopen(url).read().strip().split(',')]
        return dict((format.name[i], data[i]) for i in range(len(format.name)))
    else:
        url = 'http://finance.yahoo.com/d/quotes?s=%s&f=%s' % (symbol, format)
        return [x.strip('"') for x in urllib.urlopen(url).read().strip().split(',')]

def get_price(symbol):                          return get(symbol, 'l1')[0]
def get_change(symbol):                         return get(symbol, 'c1')[0]
def get_volume(symbol):                         return get(symbol, 'v')[0]
def get_average_daily_volume(symbol):           return get(symbol, 'a2')[0]
def get_exchange(symbol):                       return get(symbol, 'x')[0]
def get_market_cap(symbol):                     return get(symbol, 'j1')[0]
def get_book_value(symbol):                     return get(symbol, 'b4')[0]
def get_ebitda(symbol):                         return get(symbol, 'j4')[0]
def get_dividend_per_share(symbol):             return get(symbol, 'd')[0]
def get_dividend_yield(symbol):                 return get(symbol, 'y')[0]
def get_earnings_per_share(symbol):             return get(symbol, 'e')[0]
def get_52_week_high(symbol):                   return get(symbol, 'k')[0]
def get_52_week_low(symbol):                    return get(symbol, 'j')[0]
def get_50_day_moving_average(symbol):          return get(symbol, 'm3')[0]
def get_200_day_moving_average(symbol):         return get(symbol, 'm4')[0]
def get_price_to_earnings_ratio(symbol):        return get(symbol, 'r')[0]
def get_price_to_earnings_growth_ratio(symbol): return get(symbol, 'r5')[0]
def get_price_to_sales_ratio(symbol):           return get(symbol, 'p5')[0]
def get_price_to_book_ratio(symbol):            return get(symbol, 'p6')[0]
def get_short_ratio(symbol):                    return get(symbol, 's7')[0]
def get_all(symbol):
    return get(symbol, price & change & volume & average_daily_volume &
                       exchange & market_cap & book_value & ebitda &
                       dividend_per_share & dividend_yield & earnings_per_share &
                       i52_week_high & i52_week_low & i50_day_moving_average &
                       i200_day_moving_average & price_to_earnings_ratio &
                       price_to_earnings_growth_ratio & price_to_sales_ratio &
                       price_to_book_ratio & short_ratio)
