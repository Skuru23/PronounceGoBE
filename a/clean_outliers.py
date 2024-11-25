import pandas as pd


def remove_rows_from_csv(csv_file_path, rows_to_remove):
    df = pd.read_csv(
        csv_file_path, encoding="utf-8", delimiter="+", on_bad_lines="skip"
    )
    print(f"before: {len(df)}")
    rows_to_remove_set = set(rows_to_remove)
    df = df.drop(index=rows_to_remove_set, errors="ignore")
    print(f"after: {len(df)}")
    df.to_csv(csv_file_path, index=False, encoding="utf-8", sep="+")


csv_file_path = "create_dictionary/cleaned_dict.csv"

rows_to_remove = [
    1885,
    2435,
    2904,
    2905,
    2923,
    2924,
    2944,
    2950,
    2951,
    2952,
    2953,
    2954,
    2955,
    2956,
    2957,
    2958,
    2959,
    3026,
    3123,
    3406,
    3686,
    3822,
    5811,
    6499,
    7186,
    7282,
    7344,
    7728,
    9706,
    9719,
    10074,
    10590,
    10799,
    11396,
    11609,
    12723,
    12920,
    13354,
    13508,
    15225,
    17781,
    18020,
    18025,
    18291,
    21787,
    24805,
    34811,
    35517,
    35545,
    36976,
    37975,
    39823,
    40532,
    41939,
    43478,
    43736,
    47100,
    48735,
    48953,
    49283,
    50218,
    50221,
    55317,
    56690,
    56695,
    56846,
    57252,
    58232,
    58812,
    59169,
    62406,
    62800,
    63097,
    63506,
    65674,
    67847,
    72954,
    73033,
    73357,
    74574,
    75320,
    75321,
    75497,
    82874,
    82875,
    82876,
]

remove_rows_from_csv(csv_file_path, rows_to_remove)