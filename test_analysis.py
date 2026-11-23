import os
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
ORIGINAL_CWD = Path.cwd()
try:
    os.chdir(DATA_DIR)
    from analysis import 정제
finally:
    os.chdir(ORIGINAL_CWD)


SCORES_DF = pd.read_csv(DATA_DIR / "scores_2026.csv")
MINI_DF = pd.read_csv(DATA_DIR / "mini.csv")


def test_scores_csv_has_100_clean_rows() -> None:
    정제_df = 정제(SCORES_DF)
    assert len(정제_df) == 100


def test_cleaned_sections_are_1반_and_2반() -> None:
    정제_df = 정제(SCORES_DF)
    assert set(정제_df["반"].unique()) == {"1반", "2반"}


def test_section_score_sums_equal_total_score_sum() -> None:
    정제_df = 정제(SCORES_DF)
    반별_점수_합 = 정제_df.groupby("반")["점수"].sum()
    assert 반별_점수_합.sum() == 정제_df["점수"].sum()


def test_mini_first_section_average_is_80() -> None:
    정제_df = 정제(MINI_DF)
    반별_평균 = 정제_df.groupby("반")["점수"].mean()
    assert 반별_평균["1반"] == 80.0


if __name__ == "__main__":
    test_scores_csv_has_100_clean_rows()
    print("① 정제 결과 100행 확인: 통과")

    test_cleaned_sections_are_1반_and_2반()
    print("② 반 종류 확인: 통과")

    test_section_score_sums_equal_total_score_sum()
    print("③ 점수 합계 확인: 통과")

    test_mini_first_section_average_is_80()
    print("④ mini.csv 1반 평균 확인: 통과")

