# Financial Planner: Version 1 Spec (Goal planner)

Based on the principles in *How to Build Wealth in India With ₹1 Lakh a Month* (Feroze Azeez on Finance With Sharan, https://youtu.be/r3teXG_UJxs).
Timestamps in [mm:ss] point to that video.

## Decisions so far

| Topic | Decision |
|---|---|
| Platform | Web app (works on phone and laptop) |
| Data | Stays on the device (browser storage). No accounts, no server. |
| People | Separate plans per person, plus a combined view |
| Version 1 scope | **Goal planner only** |
| Advice boundary | Recommends asset types and fund *categories*, never named schemes. Shows an "educational, not investment advice" notice. |

## What the goal planner does

The user answers a short form. The app then shows, for each goal: the future cost, the money already set aside for it, and the monthly SIP still needed. It compares the total SIP with what the person can save and suggests ways to close any gap.

## Screens

### 1. Profiles (home)
- List of plans on this device (e.g. "Ayush", "Partner"), plus a **Combined** card
- Add a profile, open a profile, delete a profile
- **Export / Import backup** (JSON file). This is how data moves between devices, so the two plans can be combined on one device.

### 2. Onboarding form (one profile, 4 steps, saves as you go)
1. **About you:** name, age, retirement age (default 60)
2. **Monthly money:** take-home pay, monthly expenses, loan EMIs, current SIPs
   - Monthly savings capacity = take-home − expenses − EMIs (user can override)
3. **Existing savings:** amounts in cash/FD, EPF/PPF, equity MFs and stocks, gold. Each has an "can use for goals" tick (EPF defaults to usable for short-term goals [10:20]).
4. **Goals:** add from templates or custom:
   - Templates: Marriage, Child education, Car, Holiday, House down payment, Retirement, Custom [11:59]
   - Fields: name, cost in today's money, target year, priority (Must / Should / Nice), inflation (pre-filled per type, editable)
   - Retirement is special: asks for monthly expenses in today's money; corpus = annual expenses at retirement × multiplier (default 25, editable)

### 3. Plan (the result)
- **Snapshot:** savings capacity per month, total existing savings, savings rate
- **Goal table:** goal · cost today · target year · future cost · funded from savings · SIP needed · where to invest (asset type)
- **Total SIP needed vs. savings capacity:** surplus or gap, shown prominently
- **If there is a gap:** concrete fixes, worked out by the app:
  - push the lowest-priority goal(s) back by N years
  - reduce a goal's cost to ₹X
  - step up the SIP by X% a year
- **Action list:** e.g. "Raise SIP to ₹30,000/month", "Keep ₹10L for marriage in debt + arbitrage funds", "Long-term SIPs: 65% equity MFs / 35% gold ETF"
- **Assumptions panel:** returns, inflation, step-up, all editable, and the plan recalculates live

### 4. Combined view
- Each person's plan side by side, plus totals: total SIP needed vs. combined capacity, combined existing savings, all goals on one timeline
- Read-only in version 1; shared goals (one goal split between two people) come later

## Calculation rules

Default rates come from published data (checked October 2026, sources at the end). All are editable.

### Inflation (future cost)
- `future cost = cost today × (1 + inflation) ^ years`

| Goal type | Default | Evidence |
|---|---|---|
| Child education | **10%** | Education costs commonly reported rising 10–12% a year; private college fee hikes 7–15% a year |
| Marriage | **8%** | Wedding spending up 8% in 2025; venue, catering and jewellery costs up roughly 9% a year since FY22 |
| Car | **5%** | Average car prices up about 50% in 5 years, but much of that is buyers moving to SUVs; the same model rises less |
| Retirement living costs, Holiday, Custom | **6%** | CPI averaged about 5.2% from FY15 to FY24 (RBI); 6% leaves a small buffer for lifestyle creep |

The video's "doubles every 7 years" rule (about 10.4%) [12:31] fits education, but is too high for general living costs.

### Expected returns (after tax)
| Asset | Pre-tax default | Evidence |
|---|---|---|
| Equity mutual funds | **12%** | Nifty 50 TRI: 15-year CAGR 11.4–12.9%, 20-year 12.1–12.8% (2026 readings). The video's 15–16% [18:25] is above what the index has delivered. |
| Gold ETF | **10%** | Gold in rupees: 10-year CAGR about 16.5%, 20-year about 14–15%, but inflated by the 2025–26 rally. A lower default avoids chasing recent returns, which the video itself warns against [42:09]. |
| Debt + arbitrage | **7%** | Arbitrage category average: 3-year 7.3%, 5-year 6.5% |
| EPF | **8.25%** (tax-free) | Rate ratified for FY 2025-26 |

- Long-term gains on equity, gold ETFs and debt + arbitrage funds (held over 2 years) are taxed at **12.5%**; the plan uses after-tax returns.

### Where each goal's money goes (by years to goal)
| Years to goal | Asset type | Return used (after tax) |
|---|---|---|
| Under 3 | Debt + arbitrage funds [29:12] | 6.2% |
| 3 to 7 | Half debt + arbitrage, half long-term mix | 8.2% |
| 7 and above | 65% equity mutual funds / 35% gold ETF [31:51] (11.3% pre-tax) | 10.7–10.8% |

### Existing savings
- Assigned to goals **nearest first** [09:16], up to the amount each goal needs today (its future cost discounted at that goal's return)
- Money assigned grows at that goal's return; the SIP covers the rest

### SIP needed
- Monthly SIP that grows to the remaining amount by the target year, at the goal's after-tax return
- **Annual SIP step-up**, default 10% (raise SIPs in line with salary); can be set to 0%

### Gap fixes
- Gap = total SIP needed − savings capacity
- Fixes are tried lowest priority first: delay by 1–5 years, or reduce cost, until the gap closes; also the step-up % that closes it

## Worked example (from the video's hypothetical person [07:39])
Age 30, ₹1 lakh/month take-home, can save ₹30,000/month, ₹10 lakh saved, no loans. Retirement at 60 on ₹60k/month in today's money, corpus = 25 × annual expenses.

| Goal | Today | Years | Inflation | Future cost | From savings | SIP (no step-up) | SIP (10% step-up) |
|---|---|---|---|---|---|---|---|
| Marriage | ₹10L | 2 | 8% | ₹11.7L | ₹10L | ₹1,550 | ₹1,478 |
| Car | ₹8L | 5 | 5% | ₹10.2L | – | ₹13,851 | ₹11,514 |
| Child education | ₹25L | 20 | 10% | ₹1.68 Cr | – | ₹21,499 | ₹10,245 |
| Retirement | ₹60k/month | 30 | 6% | ₹10.34 Cr | – | ₹42,305 | ₹15,322 |
| **Total** | | | | | | **₹79,204** | **₹38,559** |

Against ₹30,000 of savings capacity, the gap is ₹49,204 without a step-up and ₹8,559 with a 10% step-up. These numbers become test cases for the calculation code.

## Not in version 1
Tracker and monthly check-ins · rent-vs-buy · fund-category checklist · fund vs. benchmark review · claimed-return checker · CAMS/KFintech import · shared goals · reminders

## Tech
- Vite + React + TypeScript; static site (can be hosted free)
- All maths in one pure module with unit tests (the worked example above)
- Storage: `localStorage`, versioned schema, with JSON export/import

## Sources (rates checked October 2026)
- Nifty 50 TRI returns: [FundsIndia Wealth Conversations, Aug 2026](https://fundsindia.com/blog/wp-content/uploads/2026/08/202608-FundsIndia-Wealth-Conversations.pdf), [Sep 2026](https://fundsindia.com/blog/wp-content/uploads/2026/09/202609-FundsIndia-Wealth-Conversations.pdf)
- CPI history: [RBI](https://rbi.org.in/scripts/PublicationsView.aspx?id=24061)
- Education inflation: [Kotak MF](https://www.kotakmf.com/Information/blogs/education-inflation-india-rising-costs), [Down To Earth](https://www.downtoearth.org.in/amp/story/governance/rising-education-cost-is-a-quieter-and-more-consequential-form-of-inflation-that-india-is-overlooking)
- Gold returns: [Aditya Birla Capital](https://www.adityabirlacapital.com/abc-of-money/gold-returns-over-the-years)
- Arbitrage fund returns: [Sharpely](https://sharpely.in/mutual-funds/invesco-india-arbitrage-fund/16368/performance)
- EPF rate: [Outlook Money](https://www.outlookmoney.com/retirement/govt-ratifies-825-per-cent-epf-interest-rate-for-2025-26-interest-likely-to-be-credited-from-this-month)
- Car prices: [Money9](https://www.money9.com/news/automobiles/car-prices-rose-50-per-cent-in-last-five-years-report-127935.html)
- Wedding costs: [Free Press Journal](https://www.freepressjournal.in/business/2025-lavish-indian-weddings-thrive-with-8-higher-spending-despite-soaring-gold-prices)
