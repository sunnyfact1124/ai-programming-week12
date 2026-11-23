import pandas as pd

df = pd.read_csv("scores_2026.csv")

def 정제(df: pd.DataFrame) -> pd.DataFrame:
    정제_df = df.copy()

    # 1단계: 점수가 비어 있는 행을 삭제한다.
    정제_df = 정제_df.dropna(subset=["점수"])
    정제_df["점수"] = 정제_df["점수"].astype(int)
    print(f"점수 결측 행 삭제 후: {len(정제_df)}행")

    # 2단계: 모든 열의 값이 같은 중복 행을 삭제한다.
    정제_df = 정제_df.drop_duplicates()
    print(f"중복 행 삭제 후: {len(정제_df)}행")

    # 3단계: 반과 과목의 앞뒤 공백을 제거한다.
    정제_df["반"] = 정제_df["반"].str.strip()
    정제_df["과목"] = 정제_df["과목"].str.strip()
    print(f"공백 제거 후: {len(정제_df)}행")

    # 4단계: 점수가 0~100 범위를 벗어난 행을 삭제한다.
    정제_df = 정제_df[정제_df["점수"].between(0, 100)]
    print(f"점수 범위 확인 후: {len(정제_df)}행")

    return 정제_df

def 반별평균(df: pd.DataFrame) -> pd.Series:
    통계표 = df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
    print(통계표)
    return 통계표["mean"]


정제된_df = 정제(df)
print("\n정제")
print(sorted(정제된_df["반"].unique()))
print(sorted(정제된_df["과목"].unique()))

print("\n 필터링")
수학_df = 정제된_df[정제된_df["과목"] == "수학"]
print(f"수학 행 수: {len(수학_df)}")

응용_df = 정제된_df[(정제된_df["반"] == "1반") & (정제된_df["점수"] >= 90)]
print(f"1반 90점 이상 행 수: {len(응용_df)}")

print("\n그룹화")
반별_평균 = 정제된_df.groupby("반")["점수"].mean()
print("반별 점수 평균:")
print(반별_평균)

과목_반별_평균 = 정제된_df.groupby(["과목", "반"])["점수"].mean()
print("\n과목과 반별 점수 평균:")
print(과목_반별_평균)

print("\n반별 통계")
반별_평균값 = 반별평균(정제된_df)
print("\n반 이름별 평균값:")
print(반별_평균값)

print("n검증")
print(정제된_df.groupby("반")["점수"].sum().sum())
print(정제된_df["점수"].sum())
print(정제된_df.groupby("반")["점수"].count().sum())
print(len(정제된_df))