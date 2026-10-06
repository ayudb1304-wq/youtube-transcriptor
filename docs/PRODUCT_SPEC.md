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

### Inflation (future cost)
- `future cost = cost today × (1 + inflation) ^ years`
- Default per goal type:
  - Child education, Marriage: **10.4%** (the video's "doubles every 7 years" rule [12:31])
  - Retirement living costs, Holiday, Car, Custom: **6%** (general inflation)
- Why not 10.4% everywhere: applied to retirement it gives a ₹35 crore corpus and an SIP of more than ₹1 lakh/month for someone on ₹1 lakh/month, which no-one can act on (see the worked example below).

### Where each goal's money goes (by years to goal)
| Years to goal | Asset type | Default expected return |
|---|---|---|
| Under 3 | Debt + arbitrage funds (taxed as long-term after 2 years [29:12]) | 7% |
| 3 to 7 | Mix: half debt + arbitrage, half equity MFs | 9.5% |
| 7 and above | 65% equity mutual funds / 35% gold ETF [31:51] | 12% |

The video claims 15–16% for equity [18:25]. The default is a more cautious 12%, editable from 8% to 16%.

### Existing savings
- Assigned to goals **nearest first** [09:16], up to the amount each goal needs today (its future cost discounted at that goal's return)
- Money assigned grows at that goal's return; the SIP covers the rest

### SIP needed
- Monthly SIP that grows to the remaining amount by the target year, at the goal's return
- Optional **annual SIP step-up** (default 0%, suggested 10% as a fix when there is a gap)

### Gap fixes
- Gap = total SIP needed − savings capacity
- Fixes are tried lowest priority first: delay by 1–5 years, or reduce cost, until the gap closes; also the step-up % that closes it

## Worked example (from the video's hypothetical person [07:39])
Age 30, ₹1 lakh/month take-home, can save ₹30,000/month, ₹10 lakh saved, no loans.

| Goal | Today | Years | Future cost | From savings | SIP / month |
|---|---|---|---|---|---|
| Marriage | ₹10L | 2 | ₹12.2L | ₹10L | ₹2,892 |
| Car | ₹8L | 5 | ₹10.7L (6%) | – | ₹14,153 |
| Child education | ₹25L | 20 | ₹181L | – | ₹19,880 |
| Retirement (₹60k/month expenses today) | – | 30 | ₹10.3 Cr (6%, ×25) | – | ₹33,555 · or ₹12,946 with a 10%/yr step-up |

What this shows: without a yearly step-up the plan doesn't fit in ₹30,000/month; with a 10% step-up it comes close. That trade-off is the main thing the planner should make visible. These numbers become test cases for the calculation code.

## Not in version 1
Tracker and monthly check-ins · rent-vs-buy · fund-category checklist · fund vs. benchmark review · claimed-return checker · CAMS/KFintech import · shared goals · reminders

## Tech
- Vite + React + TypeScript; static site (can be hosted free)
- All maths in one pure module with unit tests (the worked example above)
- Storage: `localStorage`, versioned schema, with JSON export/import
