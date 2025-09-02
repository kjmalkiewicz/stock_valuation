def dcf_valuation(data):
    try:
        eps = data["eps"]
        if eps is None or eps <= 0:
            return None

        base_cash_flow = eps * 1.1  # Conservative proxy for Free Cash Flow
        discount_rate = 0.11  # Higher discount rate to account for risk
        growth_rate = data["growth"] * 0.75  # Reduced long-term growth projection

        years = 5
        future_cash_flows = [
            base_cash_flow * ((1 + growth_rate) ** year) for year in range(1, years + 1)
        ]

        discounted_cash_flows = [
            fcf / ((1 + discount_rate) ** year) for year, fcf in enumerate(future_cash_flows, 1)
        ]

        # Terminal value using Gordon Growth Model
        terminal_growth_rate = 0.03  # conservative long-term GDP-level growth
        terminal_value = future_cash_flows[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
        discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)

        total_value = sum(discounted_cash_flows) + discounted_terminal_value
        return round(total_value, 2)

    except Exception as e:
        print("❌ Błąd w DCF:", e)
        return None
