import os
import shutil
import requests

from datetime import date

def main():
    screens = {
        "below_200sma_monthly_perf": "https://personality.mschoi.com/stock/below_200sma_monthly_perf",
        "new_high_52w": "https://personality.mschoi.com/stock/new_high_52w"
    }
    
    dt = date.today()
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
    
if __name__ == '__main__':
    main()
