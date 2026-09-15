import streamlit as st
import pandas as pd

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🌡️ 서울의 100년 이상 연평균 기온 변화")
st.write(
    "서울의 일별 기온 데이터를 연도별로 평균하여 "
    "장기간의 기온 변화 추세를 살펴봅니다."
)

# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/"
    "modudata/main/data/seoul.csv"
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 평균기온을 숫자형으로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# 연평균 기온 계산
# --------------------------------------------------
yearly_temp = (
    df.dropna(subset=["평균기온"])
      .groupby("연도")["평균기온"]
      .mean()
      .reset_index()
)

yearly_temp.columns = ["연도", "연평균기온"]

# --------------------------------------------------
# 100년 이상 자료만 사용하는 것이 아니라
# 전체 자료를 보여주되, 분석 가능한 연도 수를 표시
# --------------------------------------------------
first_year = int(yearly_temp["연도"].min())
last_year = int(yearly_temp["연도"].max())
year_count = len(yearly_temp)

st.info(
    f"📊 분석 기간: {first_year}년 ~ {last_year}년  |  "
    f"연평균 기온이 계산된 연도: {year_count}년"
)


# --------------------------------------------------
# 그래프
# --------------------------------------------------
st.subheader("📈 연도별 연평균 기온")

chart_data = yearly_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="연평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)",
    height=500
)

st.caption(
    "※ 각 연도의 일평균 기온을 평균하여 연평균 기온을 계산했습니다."
)


# --------------------------------------------------
# 간단한 통계
# --------------------------------------------------
st.subheader("🔎 데이터로 확인하는 변화")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "가장 낮은 연평균 기온",
        f"{yearly_temp['연평균기온'].min():.1f} ℃"
    )

with col2:
    st.metric(
        "가장 높은 연평균 기온",
        f"{yearly_temp['연평균기온'].max():.1f} ℃"
    )

with col3:
    change = (
        yearly_temp.iloc[-1]["연평균기온"]
        - yearly_temp.iloc[0]["연평균기온"]
    )

    st.metric(
        "첫 기록 대비 최근 기록 변화",
        f"{change:+.1f} ℃"
    )


# --------------------------------------------------
# 원자료 확인
# --------------------------------------------------
with st.expander("📋 연도별 연평균 기온 데이터 보기"):
    display_df = yearly_temp.copy()
    display_df["연평균기온"] = display_df["연평균기온"].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
