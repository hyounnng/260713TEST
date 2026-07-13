import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상과 전력수요 분석", layout="wide")

st.title("🌆 도시 열섬현상과 전력수요 분석")

# =========================
# 데이터 불러오기
# =========================
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜 형식 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 필요한 열만 선택
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울기온"})
yangpyeong = yangpyeong[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평기온"})
power = power[["일시", "전력수요(MWh)"]]

# =========================
# 탭 생성
# =========================
tab1, tab2 = st.tabs(["🌆 열섬 분석", "⚡ 전력 연결"])

# ======================================================
# 탭1 : 열섬 분석
# ======================================================
with tab1:

    st.header("서울과 양평의 도시 열섬현상")

    # 데이터 합치기
    df = pd.merge(seoul, yangpyeong, on="일시")
    df["기온차"] = df["서울기온"] - df["양평기온"]

    # -----------------
    # ① 선그래프
    # -----------------
    st.subheader("① 1년간 두 지역 기온 변화")

    line = df.set_index("일시")[["서울기온", "양평기온"]]
    st.line_chart(line)

    # -----------------
    # ② 시간별 평균 기온차
    # -----------------
    st.subheader("② 시각별 평균 기온차 (서울-양평)")

    df["시"] = df["일시"].dt.hour
    hour = df.groupby("시")["기온차"].mean()

    st.bar_chart(hour)

    # -----------------
    # ③ 월별 평균 기온차
    # -----------------
    st.subheader("③ 월별 평균 기온차 (서울-양평)")

    df["월"] = df["일시"].dt.month
    month = df.groupby("월")["기온차"].mean()

    st.bar_chart(month)

# ======================================================
# 탭2 : 전력 연결
# ======================================================
with tab2:

    st.header("서울 기온과 전력수요")

    # 데이터 합치기
    power_df = pd.merge(seoul, power, on="일시")

    # -----------------
    # ① 산점도
    # -----------------
    st.subheader("① 기온과 전력수요의 관계")

    scatter = power_df.rename(
        columns={
            "서울기온": "x",
            "전력수요(MWh)": "y"
        }
    )

    st.scatter_chart(scatter, x="x", y="y")

    # -----------------
    # ② 기온 구간별 평균 전력수요
    # -----------------
    st.subheader("② 기온 구간별 평균 전력수요")

    bins = [-20, -10, 0, 10, 20, 30, 40]
    labels = [
        "-20~-10",
        "-10~0",
        "0~10",
        "10~20",
        "20~30",
        "30~40"
    ]

    power_df["기온구간"] = pd.cut(
        power_df["서울기온"],
        bins=bins,
        labels=labels
    )

    temp_power = power_df.groupby("기온구간")["전력수요(MWh)"].mean()

    st.bar_chart(temp_power)

    # -----------------
    # ③ 월별 평균 전력수요
    # -----------------
    st.subheader("③ 월별 평균 전력수요")

    power_df["월"] = power_df["일시"].dt.month

    month_power = power_df.groupby("월")["전력수요(MWh)"].mean()

    st.bar_chart(month_power)

# =========================
# 하단 설명
# =========================
st.markdown("---")
st.write("**도시 열섬현상**은 도시 지역의 기온이 주변 지역보다 높아지는 현상입니다.")
st.write("서울과 양평의 기온 차이를 통해 열섬현상을 확인하고, 서울의 기온과 전력수요의 관계를 함께 분석할 수 있습니다.")
