def multiples_valuation(data):
    try:
        pe_ratio = data["pe_ratio"] * 0.9  # konserwatywna rewizja P/E
        eps = data["eps"]
        sector_pe = data["sector_pe"] * 0.9
        return round(eps * (pe_ratio + sector_pe) / 2, 2)
    except:
        return None
