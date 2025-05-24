from datetime import datetime, timedelta
import pandas as pd
import random

# ─────────────────────────────────────────────
# 📊 Calculate leverage (30% of credit limit)
def calculate_leverage(cc_limit):
    return 0.3 * cc_limit

# ─────────────────────────────────────────────
# 📆 Structural Summary: Track key timeline awareness
def structural_summary(start_date, statement_due_date, final_due_date, cc_limit, reserve_balance, fixed_expenses):
    weeks = max(1, (statement_due_date - start_date).days // 7)
    weekly_usage_target = round(sum(fixed_expenses) / weeks, 2)
    return pd.DataFrame([{
        "Start Date": start_date.strftime("%Y-%m-%d"),
        "Statement Due Date": statement_due_date.strftime("%Y-%m-%d"),
        "Final Due Date": final_due_date.strftime("%Y-%m-%d"),
        "Days Until Statement": (statement_due_date - start_date).days,
        "Weeks Until Statement": weeks,
        "Days Until Final Due": (final_due_date - start_date).days,
        "Weeks Until Final Due": (final_due_date - start_date).days // 7,
        "Leverage Cap (30%)": round(0.3 * cc_limit, 2),
        "Auto Weekly Target": weekly_usage_target,
        "Fixed Expenses Total": sum(fixed_expenses),
        "Reserve": reserve_balance,
        "Available Reserve (auto)": max(0, reserve_balance - sum(fixed_expenses))
    }])

# ─────────────────────────────────────────────
# 🔁 Simulated charge generator
def simulate_randomized_charge_history(start_date, statement_due_date, cc_limit, fixed_expenses_total):
    max_charge_per_week = 0.3 * cc_limit
    weeks = max(1, (statement_due_date - start_date).days // 7)
    remaining = fixed_expenses_total
    charges = []
    for i in range(weeks):
        if remaining <= 0:
            break
        min_charge = remaining * 0.2
        max_this_week = min(max_charge_per_week, remaining)
        amount = round(random.uniform(min_charge, max_this_week), 2)
        charges.append({"amount": amount, "date": start_date + timedelta(days=i * 7)})
        remaining -= amount
    return charges

# ─────────────────────────────────────────────
# 🧠 Forecast with reserve rules
def forecast_with_reserve_rules(charge_history, statement_due_date, start_date, reserve_balance, fixed_expenses):
    outcome_list = []
    current_date = min([c['date'] for c in charge_history])
    end_date = statement_due_date
    final_due_savings = sum(fixed_expenses)

    weeks = max(1, (statement_due_date - start_date).days // 7)
    weekly_usage_target = round(final_due_savings / weeks, 2)
    available_reserve = max(0, reserve_balance - final_due_savings)

    print("✅ Auto Weekly Target:", weekly_usage_target)
    print("✅ Reserve check (initial):", available_reserve)

    week = 1
    cumulative_spend = 0
    cumulative_paydown = 0
    cumulative_reserve_used = 0
    weekly_limit = available_reserve / weeks

    while current_date < end_date:
        week_charges = [c['amount'] for c in charge_history if current_date <= c['date'] < current_date + timedelta(days=7)]
        spend = sum(week_charges)
        cumulative_spend += spend
        expected_total = weekly_usage_target * week

        # 💡 Weekly logic
        if spend == 0:
            proposed = 0
            note = "No charges this week"
        elif spend <= weekly_usage_target:
            buffer_paydown = min(weekly_usage_target - spend, available_reserve * 0.1)
            proposed = round(buffer_paydown, 2)
            note = f"Under target – buffer paydown ${proposed}" if proposed > 0 else "On target – no paydown"
        else:
            over = spend - weekly_usage_target
            severity_ratio = min(over / weekly_usage_target, 1.0)
            ramp = 0.4 + (severity_ratio * 0.4)
            proposed = round(min(over * ramp, available_reserve), 2)
            note = f"Over target by ${round(over,2)} – {int(ramp * 100)}% paydown = ${proposed}"

        proposed = min(proposed, weekly_limit, available_reserve, cumulative_spend - cumulative_paydown)
        proposed = max(0, round(proposed, 2))

        cumulative_paydown += proposed
        available_reserve -= proposed
        cumulative_reserve_used += proposed
        adjusted_spend = cumulative_spend - cumulative_paydown

        credit_status = "On Pace" if adjusted_spend <= expected_total else "Off Pace"
        fixed_status = "Yes" if reserve_balance >= final_due_savings else "No"

        score = 0
        if adjusted_spend <= expected_total: score += 0.5
        if proposed > 0: score += 0.3
        if fixed_status == "Yes": score += 0.2

        outcome_list.append({
            "Week": week,
            "Start of Week": current_date.strftime("%Y-%m-%d"),
            "Spend This Week": f"${spend}",
            "Cumulative Spend": f"${round(cumulative_spend, 2)}",
            "Proposed Paydown": f"${proposed}",
            "Cumulative Paydown": f"${round(cumulative_paydown, 2)}",
            "Reserve Left (Available)": f"${round(available_reserve, 2)}",
            "Final Due Savings (Held)": f"${final_due_savings}",
            "Fixed Expenses Covered": fixed_status,
            "Credit Usage Status": credit_status,
            "Scenario Score": round(score, 1),
            "Notes": note
        })

        current_date += timedelta(days=7)
        week += 1

    outcome_list.append({
        "Week": "TOTAL",
        "Start of Week": "",
        "Spend This Week": "",
        "Cumulative Spend": "",
        "Proposed Paydown": "",
        "Cumulative Paydown": f"${round(cumulative_paydown, 2)}",
        "Reserve Left (Available)": "",
        "Final Due Savings (Held)": "",
        "Fixed Expenses Covered": "",
        "Credit Usage Status": "",
        "Scenario Score": "",
        "Notes": f"Paydown totaled ${round(cumulative_paydown, 2)}"
    })

    return outcome_list

# ─────────────────────────────────────────────
# ✅ Feasibility check
def evaluate_scenarios(scenarios, reserve_balance, fixed_expenses):
    return [
        {**s, "Feasible": "Yes" if float(s["Proposed Paydown"].strip('$')) + sum(fixed_expenses) <= reserve_balance else "No"}
        for s in scenarios
    ]

# ✅ Reserve check for final due date
def check_final_due_date_payment(final_due_date, reserve_balance, total_due):
    return "Can pay final due with reserves" if reserve_balance >= total_due else "Cannot cover due date"

# ─────────────────────────────────────────────
# # 🧪 Test the full simulation
if __name__ == "__main__":
    # 📌 Inputs
    cc_limit = 3000
    reserve_balance = 1000
    fixed_expenses = [275, 470]
    start_date = datetime(2024, 9, 1)
    statement_due_date = datetime(2024, 10, 11)
    final_due_date = datetime(2024, 10, 21)

    # 🔁 Simulate weekly charges
    test_charge_history = simulate_randomized_charge_history(
        start_date=start_date,
        statement_due_date=statement_due_date,
        cc_limit=cc_limit,
        fixed_expenses_total=sum(fixed_expenses)
    )

    # 📋 Structural Summary
    print("\n📋 STRUCTURAL SUMMARY:")
    summary_df = structural_summary(
        start_date=start_date,
        statement_due_date=statement_due_date,
        final_due_date=final_due_date,
        cc_limit=cc_limit,
        reserve_balance=reserve_balance,
        fixed_expenses=fixed_expenses
    )
    print(summary_df.to_string(index=False))

    # 📊 Run Forecast
    print("\n📊 CREDIT USAGE FORECAST:")
    forecast = forecast_with_reserve_rules(
        charge_history=test_charge_history,
        statement_due_date=statement_due_date,
        start_date=start_date,
        reserve_balance=reserve_balance,
        fixed_expenses=fixed_expenses
    )
    forecast_df = pd.DataFrame(forecast)
    print(forecast_df.to_string(index=False))