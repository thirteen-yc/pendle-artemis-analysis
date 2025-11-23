# Pendle (PENDLE) – Artemis Data Script

This repo contains a single script, `main.py`, used to analyze Pendle (PENDLE) data exported from Artemis for a research paper.

## What `main.py` does

- Loads Pendle time series from Artemis CSV files.
- Calculates summary metrics (TVL, revenue, earnings, supply, treasury, usage, dev activity).
- Prints all metrics as `key: value` to the terminal.
- Saves four charts:
  - `pendle_tvl.png`
  - `pendle_econ.png`
  - `pendle_mcap_fdv.png`
  - `pendle_supply.png`

## Required CSV files

Place the following Artemis exports in the same folder as `main.py`:

- `Pendle - Total Value Locked.csv`
- `Pendle - Revenue.csv`
- `Pendle - Fees.csv`
- `Pendle - Earnings.csv`
- `Pendle - Token Incentives.csv`
- `Pendle - Price.csv`
- `Pendle - Market Cap.csv`
- `Pendle - Fully Diluted Market Cap.csv`
- `Pendle - Daily Token Trading Volume.csv`
- `Pendle - Token Holder Count.csv`
- `Pendle - Circulating Supply.csv`
- `Pendle - Total Supply Native.csv`
- `Pendle - Outstanding Supply Native.csv`
- `Pendle - Locked Supply (Native).csv`
- `Pendle - Treasury Value.csv`
- `Pendle - Own Token Treasury Value (Native).csv`
- `Pendle - Spot DEX Daily Active Users.csv`
- `Pendle - Spot DEX Transactions.csv`
- `Pendle - Transactions.csv`
- `Pendle - Weekly Core Active Developers.csv`
- `Pendle - Weekly Core Commits.csv`

These CSVs are exported directly from Artemis and are **not** included in this repo.

## Requirements

```bash
pip install pandas matplotlib numpy
