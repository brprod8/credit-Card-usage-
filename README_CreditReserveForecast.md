
# 💳 Reserve-Based Credit Forecasting Model

This simulation model helps visualize how to use your **available reserves** and spending behavior to stay within a **credit usage strategy** tied to your credit card's billing cycle.

---

## 📁 Functions Breakdown

### `simulate_randomized_charge_history()`
- Simulates **weekly charges** based on total fixed expenses.
- Charges are **randomized but capped** at 30% of your credit limit (to mimic real-world usage constraints).
- Spreads the total spend across the billing cycle.

---

### `forecast_with_reserve_rules()`
- Core logic to project how **reserves are used weekly**.
- Calculates:
  - Weekly spending vs. expected pacing
  - How much to pay down to stay on track
  - Remaining reserve and credit status

### `structural_summary()`
- Outputs a table showing:
  - Start and due dates
  - Days/weeks left in the cycle
  - Credit usage cap
  - Reserve and fixed expenses

---

## 🎯 Weight Factors & Decision Logic

| Factor | Role | Impact |
|--------|------|--------|
| **Weekly Usage Target** | Auto-calculated based on number of weeks and total fixed expenses | Controls "on pace" logic and defines what counts as over/under spending |
| **Available Reserve** | Calculated as `reserve_balance - final_due_savings` | Determines how much can be used for paydowns |
| **Spend This Week** | Amount charged this week | Used to compare against weekly target |
| **Severity Ramp** | Based on how much user overspent | Scales paydown % from 40–80% |

---

## 🤖 Paydown Strategy Logic

- **If spend == 0** → no paydown
- **If under target** → soft buffer paydown (to lower utilization)
- **If over target**:
  - Calculate "excess"
  - Scale paydown based on how far over you are
  - Cap using reserve availability and weekly limit

---

## 📈 Graph Explanation

This graph visualizes:
- **Weekly spending (🔵)** vs **Paydowns (🟢)**
- Remaining reserve (🟡) trend
- Progress of **Cumulative Spend (⚫)** and **Cumulative Paydown (🔴)**

The goal: Stay below your 30% utilization curve while smartly using reserve capital over time.

---

## 📊 Visual Output

![Reserve Forecast](reserve_forecast_visual.png)
