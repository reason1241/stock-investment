import json
import math
import pandas as pd

def get_pos(x):
    return x[x>=0]

def get_neg(x):
    return x[x<0]

def mean_pos(x):
    return get_pos(x).mean()

def mean_neg(x):
    return get_neg(x).mean()

def count_pos(x):
    return get_pos(x).count()

def count_neg(x):
    return get_neg(x).count()

def str_pct_to_float_pct(x):
    return x.str.replace("%","").astype(float)
    
def parse_groupby_to_dict(x):
    x.columns = [' '.join(col).strip() for col in x.columns.values]
    return x.to_dict(orient="index")

def postprocess(d):
    if isinstance(d, float):
        if math.isnan(d):
            return None
        else:
            return round(d, 2)
    elif isinstance(d, dict):
        return {k: postprocess(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [postprocess(i) for i in d]
    return d

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
        stock_data['Perf Week Pct'] = str_pct_to_float_pct(stock_data['Perf Week'])
        stock_data['Perf Month Pct'] = str_pct_to_float_pct(stock_data['Perf Month'])
        
        # extract sector, industry
        summary['Sector Agg'] = parse_groupby_to_dict(stock_data.groupby('Sector').agg({'Change Pct': ['min', 'max', *statistics]}))
        summary['Industry Agg'] = parse_groupby_to_dict(stock_data.groupby('Industry').agg({'Change Pct': ['min', 'max', *statistics]}))        
        
        # extract min max change pct
        columns = ['Ticker', 'Company', 'Sector', 'Industry', 'Market Cap', 'Change Pct', 'Perf Week Pct', 'Perf Month Pct']
        
        # extract weekly and monthly mean
        summary['Change Pct Max Top3'] = stock_data.nlargest(3, 'Change Pct')[columns].to_dict(orient="records")
        summary['Change Pct Min Top3'] = stock_data.nsmallest(3, 'Change Pct')[columns].to_dict(orient="records")

        # extract weekly and monthly mean
        summary['Perf Week Pct mean'] = stock_data['Perf Week Pct'].mean()
        summary['Perf Month Pct mean'] = stock_data['Perf Month Pct'].mean()
        
        
        with open('./20251002/below_200sma_monthly_perf_summary.json', 'w') as f:
            f.write(json.dumps(postprocess(summary)))
