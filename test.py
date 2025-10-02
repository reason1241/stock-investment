import json
import pandas as pd

def get_pos(x):
    return x[x>=0]

def get_neg(x):
    return x[x<0]

def mean_pos(x):
    return get_pos(x).mean()

def mean_neg(x):
    return get_neg(x).mean()

def min_pos(x):
    return get_pos(x).min()

def min_neg(x):
    return get_neg(x).min()

def max_pos(x):
    return get_pos(x).max()

def max_neg(x):
    return get_neg(x).max()

def count_pos(x):
    return get_pos(x).count()

def count_neg(x):
    return get_neg(x).count()

def str_pct_to_float_pct(x):
    return x.str.replace("%","").astype(float)
    
def parse_groupby_to_dict(x):
    x.columns = [' '.join(col).strip() for col in x.columns.values]
    return x.to_dict(orient="index")

statistics = [mean_pos, mean_neg, count_pos, count_neg]

if __name__ == '__main__':
    with open('./20251002/below_200sma_monthly_perf.json') as f:
        data = json.loads(f.read())
        
    summary = {}
    summary['status'] = data['status']
    summary['message'] = data['message']
        
    if data['status'] == 'success':
        stock_data = pd.DataFrame(data['data'])
        """
        Columns:
            ['No.', 'Ticker', 'Company', 'Sector', 'Industry', 'Country', 'Exchange',
        'Market Cap', 'P/E', 'Perf Week', 'Perf Month', 'Perf Quart',
        'Perf Half', 'Perf Year', 'Volume', 'Price', 'Change']
        """
        stock_data['Change Pct'] = str_pct_to_float_pct(stock_data['Change'])
        
        summary['Sector Agg'] = parse_groupby_to_dict(stock_data.groupby('Sector').agg({'Change Pct': ['min', 'max', *statistics]}))
        
        # print(stock_data.groupby('Industry').agg({'Change Pct': ['min', 'max', *statistics]}))
        
        
        # print(stock_data[stock_data['Change Pct'] == stock_data['Change Pct'].max()])
        # print(stock_data[stock_data['Change Pct'] == stock_data['Change Pct'].min()])
        
        # stock_data['Perf Week Pct'] = str_pct_to_float_pct(stock_data['Perf Week'])
        # stock_data['Perf Month Pct'] = str_pct_to_float_pct(stock_data['Perf Month'])
        
        # print(stock_data['Perf Week Pct'].mean())
        # print(stock_data['Perf Month Pct'].mean())
        
        # print(stock_data.nlargest(3, 'Change Pct'))
        # print(stock_data.nsmallest(3, 'Change Pct'))
        
