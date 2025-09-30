import os
import shutil
import requests
import pandas as pd

from datetime import datetime, timedelta, timezone

def main():
    screens = {
        "below_200sma_monthly_perf": "https://personality.mschoi.com/stock/below_200sma_monthly_perf",
        "mid_cap_new_high_52w": "https://personality.mschoi.com/stock/mid_cap_new_high_52w",
        "small_cap_new_high_52w": "https://personality.mschoi.com/stock/small_cap_new_high_52w"
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
        response = requests.get(url)
        data = response.json().get('data', [])
        df = pd.DataFrame(data)
        df.to_csv(f"{path}/{k}.csv")
    
if __name__ == '__main__':
    main()
