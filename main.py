import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import numpy as np


def load_metric(filename):
    df = pd.read_csv(filename)
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
    df = df.set_index(df.columns[0]).sort_index()
    df.columns = [filename.replace("Pendle - ", "").replace(".csv", "")]
    return df


tvl              = load_metric("Pendle - Total Value Locked.csv")
revenue          = load_metric("Pendle - Revenue.csv")
fees             = load_metric("Pendle - Fees.csv")
earnings         = load_metric("Pendle - Earnings.csv")
token_incentives = load_metric("Pendle - Token Incentives.csv")

price        = load_metric("Pendle - Price.csv")
mcap         = load_metric("Pendle - Market Cap.csv")
fdv          = load_metric("Pendle - Fully Diluted Market Cap.csv")
daily_vol    = load_metric("Pendle - Daily Token Trading Volume.csv")
holder_count = load_metric("Pendle - Token Holder Count.csv")

circ_supply        = load_metric("Pendle - Circulating Supply.csv")
total_supply       = load_metric("Pendle - Total Supply Native.csv")
outstanding_supply = load_metric("Pendle - Outstanding Supply Native.csv")
locked_supply      = load_metric("Pendle - Locked Supply (Native).csv")

treasury_usd    = load_metric("Pendle - Treasury Value.csv")
treasury_tokens = load_metric("Pendle - Own Token Treasury Value (Native).csv")
spot_dau        = load_metric("Pendle - Spot DEX Daily Active Users.csv")
spot_txs        = load_metric("Pendle - Spot DEX Transactions.csv")
txs             = load_metric("Pendle - Transactions.csv")
core_devs       = load_metric("Pendle - Weekly Core Active Developers.csv")
core_commits    = load_metric("Pendle - Weekly Core Commits.csv")


start_date = max(df.index.min() for df in [
    tvl, revenue, earnings, token_incentives, price, mcap, fdv
])
end_date = min(df.index.max() for df in [
    tvl, revenue, earnings, token_incentives, price, mcap, fdv
])
window = slice(start_date, end_date)

tvl_w              = tvl.loc[window]
revenue_w          = revenue.loc[window]
earnings_w         = earnings.loc[window]
fees_w             = fees.loc[window]
token_incentives_w = token_incentives.loc[window]

price_w        = price.loc[window]
mcap_w         = mcap.loc[window]
fdv_w          = fdv.loc[window]
daily_vol_w    = daily_vol.loc[window]
holder_count_w = holder_count.loc[window]

circ_supply_w        = circ_supply.loc[window]
total_supply_w       = total_supply.loc[window]
outstanding_supply_w = outstanding_supply.loc[window]
locked_supply_w      = locked_supply.loc[window]

treasury_usd_w    = treasury_usd.loc[window]
treasury_tokens_w = treasury_tokens.loc[window]


def trailing_sum(series, days):
    end = series.index.max()
    start = end - timedelta(days=days - 1)
    clipped = series.loc[series.index >= start]
    return clipped.sum(), clipped.index.min(), clipped.index.max()


tvl_latest  = float(tvl_w.iloc[-1, 0])
tvl_30d_avg = float(tvl_w.iloc[-30:, 0].mean())

rev_365, rev_365_start, rev_365_end = trailing_sum(revenue_w.iloc[:, 0], 365)
earn_365, _, _                      = trailing_sum(earnings_w.iloc[:, 0], 365)
fees_365, _, _                      = trailing_sum(fees_w.iloc[:, 0], 365)
incentives_365, _, _                = trailing_sum(token_incentives_w.iloc[:, 0], 365)

avg_tvl_365 = float(tvl_w.loc[rev_365_start:rev_365_end].iloc[:, 0].mean())
monetization_bps = float((rev_365 / avg_tvl_365) * 10000) if avg_tvl_365 > 0 else float("nan")
earnings_margin  = float((earn_365 / rev_365) * 100)       if rev_365 != 0       else float("nan")


price_latest   = float(price_w.iloc[-1, 0])
mcap_latest    = float(mcap_w.iloc[-1, 0])
fdv_latest     = float(fdv_w.iloc[-1, 0])
holders_latest = float(holder_count_w.iloc[-1, 0])

vol_30_sum, vol_30_start, vol_30_end = trailing_sum(daily_vol_w.iloc[:, 0], 30)
avg_daily_vol_30 = float(vol_30_sum / 30.0)
vol_mcap_ratio   = float((avg_daily_vol_30 / mcap_latest) * 100) if mcap_latest > 0 else float("nan")


circ_latest        = float(circ_supply_w.iloc[-1, 0])
total_latest       = float(total_supply_w.iloc[-1, 0])
outstanding_latest = float(outstanding_supply_w.iloc[-1, 0])
locked_latest      = float(locked_supply_w.iloc[-1, 0])

one_year_ago = circ_supply_w.index.max() - timedelta(days=365)
idx_circ  = np.abs(circ_supply_w.index  - one_year_ago).argmin()
idx_total = np.abs(total_supply_w.index - one_year_ago).argmin()

circ_one_year_ago  = float(circ_supply_w.iloc[idx_circ, 0])
total_one_year_ago = float(total_supply_w.iloc[idx_total, 0])

net_new_circ_yr  = float(circ_latest  - circ_one_year_ago)
net_new_total_yr = float(total_latest - total_one_year_ago)

treasury_tokens_latest = float(treasury_tokens_w.iloc[-1, 0])
treasury_share_total   = float((treasury_tokens_latest / total_latest) * 100) if total_latest > 0 else float("nan")
treasury_share_circ    = float((treasury_tokens_latest / circ_latest) * 100)  if circ_latest  > 0 else float("nan")

treasury_usd_latest = float(treasury_usd_w.iloc[-1, 0])
treasury_to_mcap    = float((treasury_usd_latest / mcap_latest) * 100) if mcap_latest > 0 else float("nan")


dau_recent      = spot_dau.iloc[-365:]
spot_txs_recent = spot_txs.iloc[-365:]
txs_recent      = txs.iloc[-365:]

dau_avg_recent      = float(dau_recent.iloc[:, 0].mean())
dau_max_recent      = float(dau_recent.iloc[:, 0].max())
spot_txs_avg_recent = float(spot_txs_recent.iloc[:, 0].mean())
spot_txs_max_recent = float(spot_txs_recent.iloc[:, 0].max())
txs_avg_recent      = float(txs_recent.iloc[:, 0].mean())
txs_max_recent      = float(txs_recent.iloc[:, 0].max())


dev_recent     = core_devs.iloc[-52:]
commits_recent = core_commits.iloc[-52:]

dev_avg_recent     = float(dev_recent.iloc[:, 0].mean())
dev_max_recent     = float(dev_recent.iloc[:, 0].max())
commits_avg_recent = float(commits_recent.iloc[:, 0].mean())
commits_max_recent = float(commits_recent.iloc[:, 0].max())


summary = {
    "latest_date":                     str(tvl_w.index.max().date()),
    "tvl_latest_usd":                  tvl_latest,
    "tvl_30d_avg_usd":                 tvl_30d_avg,
    "rev_365_usd":                     float(rev_365),
    "earn_365_usd":                    float(earn_365),
    "fees_365_usd":                    float(fees_365),
    "token_incentives_365_usd":        float(incentives_365),
    "avg_tvl_365_usd":                 avg_tvl_365,
    "monetization_bps":                monetization_bps,
    "earnings_margin_pct":             earnings_margin,
    "price_latest_usd":                price_latest,
    "mcap_latest_usd":                 mcap_latest,
    "fdv_latest_usd":                  fdv_latest,
    "holders_latest":                  holders_latest,
    "avg_daily_vol_30_usd":            avg_daily_vol_30,
    "vol_mcap_ratio_pct":              vol_mcap_ratio,
    "circ_latest_tokens":              circ_latest,
    "total_latest_tokens":             total_latest,
    "outstanding_latest_tokens":       outstanding_latest,
    "locked_latest_tokens":            locked_latest,
    "circ_one_year_ago_tokens":        circ_one_year_ago,
    "total_one_year_ago_tokens":       total_one_year_ago,
    "net_new_circ_yr_tokens":          net_new_circ_yr,
    "net_new_total_yr_tokens":         net_new_total_yr,
    "treasury_pendle_latest_tokens":   treasury_tokens_latest,
    "treasury_usd_latest":             treasury_usd_latest,
    "treasury_share_total_pct":        treasury_share_total,
    "treasury_share_circ_pct":         treasury_share_circ,
    "treasury_to_mcap_pct":            treasury_to_mcap,
    "dau_avg_recent":                  dau_avg_recent,
    "dau_max_recent":                  dau_max_recent,
    "spot_txs_avg_recent":             spot_txs_avg_recent,
    "spot_txs_max_recent":             spot_txs_max_recent,
    "txs_avg_recent":                  txs_avg_recent,
    "txs_max_recent":                  txs_max_recent,
    "dev_avg_recent":                  dev_avg_recent,
    "dev_max_recent":                  dev_max_recent,
    "commits_avg_recent":              commits_avg_recent,
    "commits_max_recent":              commits_max_recent,
}

for k, v in summary.items():
    print(f"{k}: {v}")


plt.figure()
tvl_w.iloc[-730:].plot()
plt.title("Pendle Total Value Locked (TVL)")
plt.ylabel("TVL (USD)")
plt.xlabel("Date")
plt.tight_layout()
plt.savefig("pendle_tvl.png")
plt.close()

plt.figure()
revenue_w.iloc[-730:].plot()
earnings_w.iloc[-730:].plot()
token_incentives_w.iloc[-730:].plot()
plt.title("Pendle Protocol Economics: Revenue, Earnings, Incentives")
plt.ylabel("USD per Day")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.savefig("pendle_econ.png")
plt.close()

plt.figure()
mcap_w.iloc[-730:].plot()
fdv_w.iloc[-730:].plot()
plt.title("Pendle Market Cap vs Fully Diluted Market Cap")
plt.ylabel("USD")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.savefig("pendle_mcap_fdv.png")
plt.close()

plt.figure()
total_supply_w.iloc[-730:].plot()
circ_supply_w.iloc[-730:].plot()
locked_supply_w.iloc[-730:].plot()
plt.title("Pendle Token Supply: Total, Circulating, Locked")
plt.ylabel("PENDLE Tokens")
plt.xlabel("Date")
plt.legend()
plt.tight_layout()
plt.savefig("pendle_supply.png")
plt.close()
