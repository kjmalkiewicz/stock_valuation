def ddm_valuation(data):
    try:
        dividend = data["dividend"] * 0.95  # konserwatywniejsze założenie co do dywidendy
        growth_rate = data["growth"] * 0.8
        discount_rate = 0.10  # lekko wyższa stopa dyskontowa

        if discount_rate <= growth_rate:
            return None
        return round(dividend * (1 + growth_rate) / (discount_rate - growth_rate), 2)
    except:
        return None
