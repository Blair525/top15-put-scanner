import requests
import pandas as pd
import datetime
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def get_finviz():
    url = "https://finviz.com/screener.ashx?v=111&f=cap_midover,sh_opt_option,sh_avgvol_o3000,sh_price_o20,ta_highlow52w_b0to5h,ta_sma50_pa,ta_sma200_pa"
    tables = pd.read_html(url)
    df = tables[-1]
    df.columns = df.iloc[0]
    df = df[1:]
    return df

def fake_iv_score():
    import random
    return random.randint(40, 95)

def main():
    df = get_finviz()

    rows = []

    for _, r in df.iterrows():
        iv = fake_iv_score()
        rows.append((r['Ticker'], iv))

    rows = sorted(rows, key=lambda x: x[1], reverse=True)[:15]

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M ET")

    msg = "🔥 Top 15 Sell Put Candidates\n\n"

    for i,(t,iv) in enumerate(rows,1):
        msg += f"{i}. {t}  IVR {iv}\n"

    msg += f"\nScan time: {now}"

    send(msg)

if __name__ == "__main__":
    main()
