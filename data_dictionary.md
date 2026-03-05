\# GARI Project: Data Dictionary



| Dataset Name | Source / URL | Date Acquired | Primary Use / Key Variables | Data Type / Format | Notes \& Constraints |

| :--- | :--- | :--- | :--- | :--- | :--- |

| \*\*GARI Core Cost Index\*\* | Numbeo (Scraped) | Feb 19, 2026 | Rent, Groceries, Utilities, Health Care Index | CSV | Heavy-tailed distribution; requires Robust Scaling (IQR). 85 city-country pairs. |

| \*\*Legal Feasibility Matrix\*\* | IRS (Pub 54) / Manual | Feb 12, 2026 | Tax Treaty Status (Yes/No), Digital Nomad Visa | CSV | Used as a hard binary filter prior to clustering. |

| \*\*Digital Infrastructure\*\* | SpeedTest Global Index | Feb 26, 2026 | Mobile and Broadband Speeds | CSV | Replaced Ookla AWS Parquet/Shapefiles due to extraction overhead. |

| \*\*Physical Infrastructure\*\* | World Bank LPI | Feb 19, 2026 | Road Quality, Supply Chain Reliability | CSV | Acts as a minimum threshold penalty (Shannon Entropy logic). |

| \*\*Safety \& Stability\*\* | Global Peace Index | Feb 19, 2026 | Institutional Safety Score, Geopolitical Risk | CSV | Anchors Numbeo's crowdsourced safety sentiment to dampen noise. |

| \*\*Validation Benchmark\*\* | OECD Better Life Index | Feb 19, 2026 | External validation for rankings | CSV | Currently facing naming formatting mismatches requiring resolution. |

| \*\*California Baseline (Control)\*\* | Numbeo / GPI / WB LPI (Manual Extract) | Mar 5, 2026 | Rent, US Safety (2.448), US LPI (3.8) | Hardcoded | Acts as the control anchor to calculate the "Net-Income Stretch" (Arbitrage Gap). |

