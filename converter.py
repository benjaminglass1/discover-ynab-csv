#!/usr/bin/python3

import argparse

import pandas as pd


def main():
    # Setup the (basic) input and output arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile", metavar="IN", help="Input CSV file, in Discover Bank format."
    )
    parser.add_argument(
        "outfile", metavar="OUT", help="Output CSV file, in YNAB format."
    )
    args = parser.parse_args()

    # Read in the input CSV, and create an output dataframe with the four expected
    # columns.
    in_df = pd.read_csv(args.infile)
    out_dict = {
        "Date": in_df["Trans. Date"].to_list(),
        "Payee": in_df["Description"].to_list(),
        "Memo": ["" for _ in range(len(in_df))],
        "Amount": in_df["Amount"].to_list(),
    }
    out_df = pd.DataFrame(data=out_dict)

    # Output the dataframe as CSV without the index, to match the expected format.
    out_df.to_csv(args.outfile, index=False)


if __name__ == "__main__":
    main()
