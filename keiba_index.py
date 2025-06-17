import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

def normalize_url(url):
    if url.startswith("https://race.sp.netkeiba.com"):
        return url.replace("race.sp.netkeiba.com", "race.netkeiba.com")
    return url

def fetch_race_data(url):
    url = normalize_url(url)
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    horse_data = []
    rows = soup.select("table.race_table_01 > tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        try:
            num = cols[0].text.strip()
            name = cols[3].text.strip()
            jockey = cols[6].text.strip()
            odds = float(cols[10].text.strip()) if cols[10].text.strip() else None
            horse_data.append({
                "馬番": num,
                "馬名": name,
                "騎手": jockey,
                "単勝オッズ": odds
            })
        except:
            continue
    return pd.DataFrame(horse_data)

def score_horses(df, track_bias, pace, user_scores=None):
    scored = []
    for _, row in df.iterrows():
        base_score = 50
        if track_bias == "先行有利":
            bias_bonus = random.randint(0, 5)
        elif track_bias == "差し有利":
            bias_bonus = random.randint(-2, 4)
        else:
            bias_bonus = 0

        if pace == "ハイ":
            pace_bonus = random.randint(0, 3)
        elif pace == "スロー":
            pace_bonus = random.randint(-3, 2)
        else:
            pace_bonus = 0

        body_score = user_scores.get(row["馬名"], 0) * 2 if user_scores else 0

        total = base_score + bias_bonus + pace_bonus + body_score
        scored.append({
            "馬番": row["馬番"],
            "馬名": row["馬名"],
            "騎手": row["騎手"],
            "単勝オッズ": row["単勝オッズ"],
            "指数": total
        })
    df_score = pd.DataFrame(scored)
    df_score = df_score.sort_values("指数", ascending=False).reset_index(drop=True)
    return df_score
