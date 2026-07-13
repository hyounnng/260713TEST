import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상 분석", layout="wide")

st.title("🌆 서울과 양평의 도시 열섬현상 분석")

# ==========================
# 데이터 불러오기
# ==========================
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")

# 날짜형으로 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])

# 필요한 열만 선택하고 이름 변경
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울"})
yangpyeong = yangpyeong[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평"})

# 데이터 합치기
df = pd.merge(seoul, yangpyeong, on="일시")

# 기온차 계산
df["기온차"] = df["서울"] - df["양평"]

# ==========================
# ① 1년간 기온 변화
# ==========================
st.header("① 1년간 서울과 양평의 기온 변화")

line_df = df.set_index("일시")[["서울", "양평"]]
st.line_chart(line_df)

# ==========================
# ② 시간대별 평균 기온차
# ==========================
st.header("② 시각(0~23시)별 평균 기온차 (서울 - 양평)")

df["시"] = df["일시"].dt.hour

hour_diff = (
    df.groupby("시")["기온차"]
      .mean()
      .round(2)
)

st.bar_chart(hour_diff)

# ==========================
# ③ 월별 평균 기온차
# ==========================
st.header("③ 월(1~12월)별 평균 기온차 (서울 - 양평)")

df["월"] = df["일시"].dt.month

month_diff = (
    df.groupby("월")["기온차"]
      .mean()
      .round(2)
)

st.bar_chart(month_diff)

# ==========================
# 요약
# ==========================
st.header("📊 분석 결과 요약")

st.write(f"**연평균 기온차(서울-양평)** : {df['기온차'].mean():.2f} ℃")
st.write(f"**최대 기온차** : {df['기온차'].max():.2f} ℃")
st.write(f"**최소 기온차** : {df['기온차'].min():.2f} ℃")

st.info("기온차가 양수일수록 서울이 양평보다 더 따뜻하며, 이는 도시 열섬현상의 영향을 보여줄 수 있습니다.")
