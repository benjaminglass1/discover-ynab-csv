#!/usr/bin/python3

import argparse

import pandas as pd


# Constant sets of the necessary columns for Discover Bank or Credit CSV
# inputs. These are used both to identify which type of CSV was read in and to
# query the data for the transformation.
NEEDED_BANK_COLUMNS = {"Credit", "Debit", "Transaction Date", "Transaction Description"}
NEEDED_CREDIT_COLUMNS = {"Amount", "Description", "Trans. Date"}


def main():
    # Setup the (basic) input and output arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile",
        metavar="IN",
        help="Input CSV file, in Discover Bank or Credit format.",
    )
    parser.add_argument(
        "outfile", metavar="OUT", help="Output CSV file, in YNAB format."
    )
    args = parser.parse_args()

    # Read in the input CSV, and identify whether it's in Bank or Credit format.
    in_df = pd.read_csv(args.infile)
    if NEEDED_BANK_COLUMNS.issubset(in_df.columns):
        out_dict = {
            "Date": in_df["Transaction Date"],
            "Payee": in_df["Transaction Description"],
            "Memo": ["" for _ in range(len(in_df))],
            "Outflow": in_df["Debit"],
            "Inflow": in_df["Credit"],
        }
    elif NEEDED_CREDIT_COLUMNS.issubset(in_df.columns):
        out_dict = {
            "Date": in_df["Trans. Date"].to_list(),
            "Payee": in_df["Description"].to_list(),
            "Memo": ["" for _ in range(len(in_df))],
            "Amount": (in_df["Amount"] * -1).to_list(),
        }
    # If the file is in neither Bank or Credit format, nothing to do.
    else:
        return

    # Create the output dataframe.
    out_df = pd.DataFrame(data=out_dict)
    # Output the dataframe as CSV without the index, to match the expected format.
    out_df.to_csv(args.outfile, index=False)


if __name__ == "__main__":
    main()
