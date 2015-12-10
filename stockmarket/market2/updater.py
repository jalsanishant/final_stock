#!/usr/bin/env python
if __name__ == '__main__':
    import sys, os
    sys.path.append('')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'stockmarket.settings'

    from django.core.management import setup_environ
    from stocksite import settings
    setup_environ(settings)

from market2 import stocks
from market2.models import Stock2, StockStatus2, Portfolio2

def update(stk):
    if __name__ == '__main__': print ('* updating %s...' % stk.symbol),
    data = stocks.get_all(stk.symbol)
    
    for key in data.keys():
        if data[key] == 'N/A': data[key] = '0.0'
    
    s = StockStatus2(
        price = float(data['price']),
        change = float(data['change']),
        volume = int(data['volume']),
        average_daily_volume = int(data['average_daily_volume']),       
        market_cap = data['market_cap'],
        book_value = float(data['book_value']),
        ebitda = data['ebitda'],
        dividend_per_share = float(data['dividend_per_share']),
        dividend_yield = float(data['dividend_yield']),
        earnings_per_share = float(data['earnings_per_share']),
        i52_week_high = float(data['52_week_high']),
        i52_week_low = float(data['52_week_low']),
        i50_day_moving_average = float(data['50_day_moving_average']),
        i200_day_moving_average = float(data['200_day_moving_average']),
        price_to_earnings_ratio = float(data['price_to_earnings_ratio']),
        price_to_earnings_growth_ratio = float(data['price_to_earnings_growth_ratio']),
        price_to_sales_ratio = float(data['price_to_sales_ratio']),
        price_to_book_ratio = float(data['price_to_book_ratio']),
    )
    s.save()
    stk.history.add(s)
    stk.price = float(data['price'])
    stk.exchange = data['exchange']
    stk.save()
    if __name__ == '__main__': print 'done'

def update_portfolio(p):
    if __name__ == '__main__': 
        print '* updating %s...' % p.user.username
        print '\t-> value = %s' % p.value
    value = 0
    for pos in p.positions.all():
        subval = pos.amount * pos.stock.price
        pos.value = subval
        pos.save()
        value += subval
    p.value = value
    p.save()
    if __name__ == '__main__': 
        print '\t-> new value = %s' % p.value

if __name__ == '__main__':
    for stk in Stock2.objects.all(): update(stk)
    for p in Portfolio2.objects.all(): 
        update_portfolio(p)
