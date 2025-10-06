import os
import json
import shutil
import logging
import requests

from datetime import datetime, timedelta, timezone
from summarize_data import summarize_stock_data

logger = logging.getLogger()


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
    
    data = None
    
    try:
        for k, url in screens.items():
            data = requests.get(url)
            with open(f"{path}/{k}.json", "w") as f:
                f.write(data.text)
        
            (sector, industry, best3, worst3, total) = summarize_stock_data(json.loads(data.text))
        
            with open(f"{path}/{k}_sector_summary.json", "w") as f:           
                f.write(json.dumps(sector))
                
            with open(f"{path}/{k}_industry_summary.json", "w") as f:           
                f.write(json.dumps(industry))
                
            with open(f"{path}/{k}_best3_summary.json", "w") as f:           
                f.write(json.dumps(best3))
                
            with open(f"{path}/{k}_worst3_summary.json", "w") as f:           
                f.write(json.dumps(worst3))
                
            with open(f"{path}/{k}_total_summary.json", "w") as f:           
                f.write(json.dumps(total))
    except Exception as e:
        logger.error(e)
        if data:
            logger.error(data.text)       
    
    
if __name__ == '__main__':
    main()
