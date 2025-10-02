import os
import json
import shutil
import requests

from datetime import datetime, timedelta, timezone
from summarize_data import summarize_stock_data

def main():
    screens = {
        "below_200sma_monthly_perf": "https://personality.mschoi.com/stock/below_200sma_monthly_perf",
        # "mid_cap_new_high_52w": "https://personality.mschoi.com/stock/mid_cap_new_high_52w",
        # "small_cap_new_high_52w": "https://personality.mschoi.com/stock/small_cap_new_high_52w"
        "new_high_52w": "https://personality.mschoi.com/stock/new_high_52w"
    }
    
    kst = timezone(timedelta(hours=9))
    dt = datetime.now(kst)
    dt_str = f"{dt.year}{dt.month:02d}{dt.day:02d}"
    path = dt_str
    
    # if a directory exists
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            
    os.mkdir(path)
    
    for k, url in screens.items():
        data = requests.get(url)
        with open(f"{path}/{k}.json", "w") as f:
            f.write(data.text)
    
        with open(f"{path}/{k}_summary.json", "w") as f:
            summary = summarize_stock_data(json.loads(data.text))
            f.write(json.dumps(summary))
        
    
    
if __name__ == '__main__':
    main()
