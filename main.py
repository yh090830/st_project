import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr

# -----------------------------------
# 1. 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="청소년 건강행태 상관관계 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 청소년 아침식사 결식률과 신체활동 실천율")
st.markdown("""
### 두 변수 사이에는 정말 유의미한 관계가 있을까?
질병관리청 청소년건강행태조사 통계를 활용한 데이터 분석
""")

st.divider()

# -----------------------------------
# 2. 공식 공개 통계 데이터
# 단위: %
# -----------------------------------
data = [
    [2016, "남학생", 27.3, 18.8],
    [2017, "남학생", 30.1, 19.5],
    [2018, "남학생", 32.2, 20.3],
    [2019, "남학생", 34.6, 21.5],
    [2020, "남학생", 35.5, 19.9],
    [2021, "남학생", 37.0, 20.7],
    [2022, "남학생", 37.4, 23.4],
    [2023, "남학생", 39.7, 24.6],
    [2024, "남학생", 40.2, 25.1],
    [2025, "남학생", 41.9, 24.5],

    [2016, "여학생", 29.3, 7.0],
    [2017, "여학생", 33.0, 7.5],
    [2018, "여학생", 35.1, 7.1],
    [2019, "여학생", 36.9, 7.3],
    [2020, "여학생", 39.2, 7.7],
    [2021, "여학생", 39.1, 8.1],
    [2022, "여학생", 40.7, 8.8],
    [2023, "여학생", 42.6, 9.2],
    [2024, "여학생", 44.7, 8.9],
    [2025, "여학생", 45.3, 8.5],
]

df = pd.DataFrame(
    data,
    columns=[
        "연도",
        "성별",
        "아침식사 결식률",
        "신체활동 실천율"
    ]
)

# -----------------------------------
# 3. 사이드바
# -----------------------------------
st.sidebar.header("📌 분석 설정")

gender = st.sidebar.selectbox(
    "분석할 성별",
    ["전체", "남학생", "여학생"]
)

if gender == "전체":
    selected_df = df.copy()
else:
    selected_df = df[df["성별"] == gender].copy()

# -----------------------------------
# 4. 핵심 통계
# -----------------------------------
st.subheader("1. 주요 통계 현황")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "2025년 남학생 아침식사 결식률",
        "41.9%"
    )

with col2:
    st.metric(
        "2025년 여학생 아침식사 결식률",
        "45.3%"
    )

st.caption(
    "출처: 질병관리청 청소년건강행태조사, 2025년"
)

# -----------------------------------
# 5. 연도별 추이 그래프
# -----------------------------------
st.subheader("2. 연도별 건강행태 변화")

fig1 = px.line(
    selected_df,
    x="연도",
    y=["아침식사 결식률", "신체활동 실천율"],
    color="성별",
    markers=True,
    title="아침식사 결식률과 신체활동 실천율 추이",
    labels={
        "value": "비율 (%)",
        "variable": "건강 지표",
        "연도": "연도"
    }
)

fig1.update_layout(
    hovermode="x unified",
    yaxis_title="비율 (%)",
    legend_title="성별"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------
# 6. 막대그래프
# -----------------------------------
st.subheader("3. 성별 건강행태 비교")

fig2 = px.bar(
    selected_df,
    x="연도",
    y=["아침식사 결식률", "신체활동 실천율"],
    barmode="group",
    color_discrete_sequence=["#EF553B", "#636EFA"],
    title="연도별 아침식사 결식률과 신체활동 실천율"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# 7. 상관관계 분석
# -----------------------------------
st.subheader("4. 두 변수 사이의 상관관계")

st.info(
    "주의: 아래 기본 분석은 연도별 집계 비율을 이용한 "
    "탐색적 분석입니다. 개인별 생활습관 사이의 관계를 "
    "직접 증명하는 분석은 아닙니다."
)

fig3 = px.scatter(
    selected_df,
    x="아침식사 결식률",
    y="신체활동 실천율",
    color="성별",
    text="연도",
    trendline="ols",
    title="아침식사 결식률과 신체활동 실천율의 관계",
    labels={
        "아침식사 결식률": "아침식사 결식률 (%)",
        "신체활동 실천율": "신체활동 실천율 (%)"
    }
)

st.plotly_chart(fig3, use_container_width=True)

if len(selected_df) >= 3:
    r, p = pearsonr(
        selected_df["아침식사 결식률"],
        selected_df["신체활동 실천율"]
    )

    st.metric("집계자료 피어슨 상관계수", f"{r:.3f}")
    st.metric("집계자료 p-value", f"{p:.4f}")

    st.caption(
        "이 p-value는 연도별 집계자료의 선형 상관에 대한 "
        "탐색적 결과이며, 개인 수준의 관계에 대한 "
        "통계적 유의성으로 해석하면 안 됩니다."
    )

# -----------------------------------
# 8. 실제 개인별 자료 업로드
# -----------------------------------
st.divider()
st.subheader("5. 실제 개인별 자료로 통계적 유의성 검정")

st.markdown("""
개인별 조사자료 CSV를 업로드하면 두 변수의 관계를 직접 분석합니다.

CSV에는 다음 열이 있어야 합니다.

- `breakfast_skipped`: 아침식사 결식 여부 (1=결식, 0=결식하지 않음)
- `activity_practice`: 신체활동 실천 여부 (1=실천, 0=실천하지 않음)

두 변수 모두 개인별 응답을 사용해야 합니다.
""")

uploaded_file = st.file_uploader(
    "개인별 조사 CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        individual_df = pd.read_csv(uploaded_file)

        required = [
            "breakfast_skipped",
            "activity_practice"
        ]

        if not all(col in individual_df.columns for col in required):
            st.error("필수 열 이름을 확인해주세요.")
        else:
            analysis_df = individual_df[required].apply(
                pd.to_numeric,
                errors="coerce"
            ).dropna()

            valid = analysis_df[
                analysis_df["breakfast_skipped"].isin([0, 1])
                & analysis_df["activity_practice"].isin([0, 1])
            ]

            if len(valid) < 3:
                st.warning("분석에 사용할 수 있는 응답이 부족합니다.")

            elif valid["breakfast_skipped"].nunique() < 2 or \
                    valid["activity_practice"].nunique() < 2:
                st.warning("두 변수 모두 0과 1의 응답이 있어야 합니다.")

            else:
                r, p = pearsonr(
                    valid["breakfast_skipped"],
                    valid["activity_practice"]
                )

                st.success("개인별 자료 분석 완료!")

                c1, c2, c3 = st.columns(3)

                c1.metric("분석 인원", f"{len(valid):,}명")
                c2.metric("상관계수", f"{r:.3f}")
                c3.metric("p-value", f"{p:.4f}")

                if p < 0.05:
                    st.write(
                        "📌 통계적으로 유의한 상관관계가 "
                        "관찰되었습니다. (p < 0.05)"
                    )
                else:
                    st.write(
                        "📌 통계적으로 유의한 상관관계가 "
                        "확인되지 않았습니다. (p ≥ 0.05)"
                    )

                st.write("### 응답 조합별 비율")

                table = pd.crosstab(
                    valid["breakfast_skipped"],
                    valid["activity_practice"],
                    normalize="index"
                ) * 100

                st.dataframe(table.round(2))

    except Exception as e:
        st.error(f"파일 분석 중 오류가 발생했습니다: {e}")

# -----------------------------------
# 9. 원본 데이터 확인
# -----------------------------------
with st.expander("📋 사용된 연도별 통계 데이터 확인"):
    st.dataframe(selected_df, use_container_width=True)

# -----------------------------------
# 10. 결론 및 출처
# -----------------------------------
st.divider()

st.subheader("6. 탐구 결과 및 해석")

st.markdown("""
- 청소년의 아침식사 결식률은 장기적으로 증가하는 추세를 보입니다.
- 신체활동 실천율은 성별에 따라 차이가 나타납니다.
- 두 지표의 연도별 변화만으로 개인의 아침식사 습관과
  신체활동 사이의 직접적인 관계를 확정할 수는 없습니다.
- 개인별 조사자료를 활용하면 두 변수 사이의 관계를
  더욱 정확하게 검증할 수 있습니다.
""")

st.markdown("""
**자료 출처**

질병관리청 청소년건강행태조사

https://www.kdca.go.kr/yhs/yhshmpg/main.do
""")

st.caption(
    "본 분석은 교육 및 탐구 발표 목적으로 제작되었습니다."
)
