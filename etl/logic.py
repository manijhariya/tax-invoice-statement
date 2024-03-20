import os
import re

import pandas as pd
import tabula
from django.conf import settings

RE_NAME = re.compile(r"[A-Z]{2,}")


def get_something(row_data):
    borrower_name = " ".join(RE_NAME.findall(row_data[4]))
    if not borrower_name:
        borrower_name = " ".join(RE_NAME.findall(row_data[3]))
        if borrower_name:
            row_data[3] = re.sub(borrower_name, "", row_data[3]).strip()
    else:
        row_data[4] = re.sub(borrower_name, "", row_data[4]).strip()

    row_data = pd.concat(
        [row_data, pd.Series(borrower_name)], axis=0, ignore_index=True
    )
    return row_data


def extract_data_from_pdf(pdf_file_path):
    print(pdf_file_path)
    # Extract tables from PDF
    tables = tabula.read_pdf(
        os.path.join(settings.UPLOAD_FILES, pdf_file_path),
        pages="all",
        multiple_tables=True,
    )

    df = pd.DataFrame()
    for table in tables:
        table = table.dropna(axis=1, how="all")
        table = pd.concat([table.columns.to_frame().T, table], ignore_index=True)

        table.columns = range(len(table.columns))
        df = pd.concat([df, table], ignore_index=True, axis=0)

    df[[df.shape[1] + 1, df.shape[1] + 2]] = df[0].str.split(" ", expand=True)
    df.drop(columns=[0], axis=1, inplace=True)

    df = df.apply(get_something, axis=1)
    df.reset_index(drop=True, inplace=True)
    df.columns = [
        "Settlement Date",
        "Broker",
        "Sub Broker",
        "Description",
        "Total Loan Amount",
        "Comission Rate",
        "Upfront",
        "Upfront Incl GST",
        "App ID",
        "Xref",
        "Borrower Name",
    ]
    df["Total Loan Amount"] = df["Total Loan Amount"].apply(
        lambda x: float(str(x).replace(",", ""))
    )
    df["Comission Rate"] = df["Comission Rate"].apply(
        lambda x: float(str(x).replace(",", ""))
    )
    df["Upfront"] = df["Upfront"].apply(lambda x: float(str(x).replace(",", "")))
    df["Upfront Incl GST"] = df["Upfront Incl GST"].apply(
        lambda x: float(str(x).replace(",", ""))
    )

    df[["App ID", "Xref"]] = df[["App ID", "Xref"]].astype(int)
    df["Settlement Date"] = pd.to_datetime(df["Settlement Date"], format="%d/%m/%Y")
    df["Tier"] = df["Total Loan Amount"].apply(
        lambda x: "Tier 1" if x > 1_00_000 else "Tier 2" if x > 50_000 else "Tier 3"
    )
    return df
