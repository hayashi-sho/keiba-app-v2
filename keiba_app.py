import streamlit as st
from keiba_index import fetch_race_data, score_horses

st.set_page_config(page_title="競馬指数アプリ", layout="wide")
st.title("🏇 競馬指数アプリ（JRA + 地方 対応）")

url = st.text_input("🔗 出馬表URLを入力してください")

track_bias = st.selectbox("馬場傾向", ["先行有利", "差し有利", "フラット"])
pace = st.selectbox("展開予想", ["スロー", "ミドル", "ハイ"])
user_scores = {}

if url:
    df = fetch_race_data(url)
    st.markdown("### 馬体手動評価")
    for _, row in df.iterrows():
        score = st.slider(f"{row['馬名']} の馬体評価", 0, 5, 0)
        user_scores[row["馬名"]] = score

    df_scored = score_horses(df, track_bias, pace, user_scores)
    st.success("指数計算完了！")
    st.dataframe(df_scored, use_container_width=True)

    top3 = df_scored.head(3)["馬番"].tolist()
    st.markdown(f"**3連複**：{top3}")
    st.markdown(f"**3連単**：{top3[0]} → {top3[1]} → {top3[2]}")
