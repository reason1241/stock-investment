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
    x.columns = ['_'.join(col).strip() for col in x.columns.values]
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

def summarize_stock_data(data):
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
        
        # rename columns
        stock_data.columns = [c.lower().replace(' ', '_') for c in stock_data.columns]
                
        stock_data['change_pct'] = str_pct_to_float_pct(stock_data['change'])
        stock_data['perf_week_pct'] = str_pct_to_float_pct(stock_data['perf_week'])
        stock_data['perf_month_pct'] = str_pct_to_float_pct(stock_data['perf_month'])
        
        # extract sector, industry
        summary['aggregates'] = {}
        summary['aggregates']['by_sector'] = parse_groupby_to_dict(stock_data.groupby('sector').agg({'change_pct': ['min', 'max', *statistics]}))
        summary['aggregates']['by_industry'] = parse_groupby_to_dict(stock_data.groupby('industry').agg({'change_pct': ['min', 'max', *statistics]}))        
        
        # extract min max change pct
        columns = ['ticker', 'company', 'sector', 'industry', 'market_cap', 'change_pct', 'perf_week_pct', 'perf_month_pct']
        
        # extract weekly and monthly mean
        summary['change_pct'] = {}
        summary['change_pct']['best3'] = stock_data.nlargest(3, 'change_pct')[columns].to_dict(orient="records")
        summary['change_pct']['worst3'] = stock_data.nsmallest(3, 'change_pct')[columns].to_dict(orient="records")

        # extract summary
        summary['summary'] = {}
        summary['summary']['perf_week_pct_mean'] = stock_data['perf_week_pct'].mean()
        summary['summary']['perf_month_pct_mean'] = stock_data['perf_month_pct'].mean()
        summary['summary']['n_total'] = len(stock_data)
        summary['summary']['n_change_pct_pos'] = len(stock_data[stock_data['change_pct'] >= 0])
        summary['summary']['n_change_pct_neg'] = len(stock_data[stock_data['change_pct'] < 0])

    return postprocess(summary)

if __name__ == '__main__':
    with open('./20251002/below_200sma_monthly_perf.json') as f:
        data = json.loads(f.read())
        
        summary = summarize_stock_data(data)
        
        with open('./20251002/below_200sma_monthly_perf_summary.json', 'w') as f:
            f.write(json.dumps(postprocess(summary)))
