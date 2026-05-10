import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup

class CurrencyScraper:
    _rates_df = None

    @classmethod
    def load_rates(cls):
        url = "https://www.x-rates.com/table/?from=USD&amount=1"
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')

        rows = soup.find_all('tr')
        data = []
        for row in rows:
            row_td = row.find_all('td')
            if row_td:
                str_cells = str(row_td)
                cleantext = BeautifulSoup(str_cells, "lxml").get_text()
                data.append(cleantext)

        #text extraction
        df = pd.DataFrame(data)
        df1 = df[0].str.split(',', expand=True)
        df1[0] = df1[0].str.strip('[')
        
        #drop third column
        df = df1.drop(columns=[2], errors='ignore')
        
        #assign columns
        df.columns = ["Currency", "Rate"]
        
        #clean whitespace and convert
        df["Currency"] = df["Currency"].str.strip()
        df["Rate"] = pd.to_numeric(df["Rate"].str.strip(), errors='coerce')
        
        cls._rates_df = df.dropna()

    @classmethod
    def get_exchange_rate(cls, from_curr, to_curr):
        """Called by system.py to convert currencies using the full name"""
        #check usd
        if to_curr.lower() in ["usd", "us dollar", "1.00 usd"]:
            return 1.0
            
        if cls._rates_df is None:
            cls.load_rates()
            
        #match currency name
        match = cls._rates_df[cls._rates_df["Currency"].str.lower() == to_curr.lower()]
        
        if not match.empty:
            return float(match.iloc[0]["Rate"])
        else:
            print(f"\n[!] Error: Could not find exchange rate for '{to_curr}'.")
            #show examples
            examples = ", ".join(cls._rates_df["Currency"].head(5).tolist())
            print(f"Available examples: {examples} ...")
            return None
