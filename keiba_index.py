import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

def fetch_race_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    horse_data = []
    rows = soup.select("div.RaceTable01 > table > tbody > tr")
    for row in rows:
        num = row.select_one("td.Number")
        name = row.select_one("td.Horse_Name a")
        jockey = row.select_one("td.Jockey")
        odds = row.select_one("td.Odds")

        if num and name and jockey:
            try:
                odds_val = float(odds.text.strip()) if odds else None
            except:
                odds_val = None
            horse_data.append({
                "馬番": num.text.strip(),
                "馬名": name.text.strip(),
                "騎手": jockey.text.strip(),
                "単勝オッズ": odds_val
            })
    return pd.DataFrame(horse_data)

def score_horses(df, track_bias, pace, user_scores=None):
    scored = []
    for _, row in df.iterrows():
        ch = random.randint(1, 5)
        te = 2 if pace == "スロー" else 1
        ba = 2 if track_bias == "先行有利" else 1
        body = user_scores.get(row["馬名"], 0) if user_scores else 0
        odds_bonus = 1 if row["単勝オッズ"] and row["単勝オッズ"] >= 10 else 0
        total = ch * 4 + te * 3 + ba * 2 + body + odds_bonus
        scored.append([ch, te, ba, body, total])
    df[["調教点", "展開点", "馬場点", "馬体点", "総合指数"]] = scored
    df = df.sort_values("総合指数", ascending=False).reset_index(drop=True)
    return df
