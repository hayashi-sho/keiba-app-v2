import streamlit as st
from keiba_index import fetch_race_data, score_horses

st.set_page_config(page_title="競馬指数アプリv7", layout="wide")
st.markdown("<h1 style='text-align:center;'>🏇 競馬指数アプリ v7</h1>", unsafe_allow_html=True)
st.info("出馬表URLを貼るだけで自動分析（JRA・地方両対応）")

url = st.text_input("🔗 出馬表URLを入力", placeholder="https://race.netkeiba.com/race/shutuba.html?race_id=...")

track_bias = st.selectbox("馬場傾向", ["先行有利", "差し有利", "フラット"])
pace = st.selectbox("展開予想", ["スロー", "ミドル", "ハイ"])
user_scores = {}

if url:
    df = fetch_race_data(url)
    if df.empty:
        st.error("出馬表の取得に失敗しました。URLを確認してください。")
    else:
        st.subheader("🔧 馬体の手動評価（0〜5で選択）")
        for _, row in df.iterrows():
            score = st.slider(f"{row['馬名']}", 0, 5, 0, key=row["馬名"])
            user_scores[row["馬名"]] = score

        df_scored = score_horses(df, track_bias, pace, user_scores)
        st.success("✅ 指数を算出しました！")
        st.dataframe(df_scored, use_container_width=True)

        top3 = df_scored.head(3)["馬番"].tolist()
        st.markdown(f"### 🎯 推奨3連複：**{top3}**")
        st.markdown(f"### 🥇 推奨3連単：**{top3[0]} → {top3[1]} → {top3[2]}**")
