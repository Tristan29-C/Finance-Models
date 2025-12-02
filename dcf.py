from typing import List, Literal, Optional

def project_fcf(
    start_revenue: float,
    years: int,
    revenue_growth: float,
    ebitda_margin: float,
    deprec_amor_pct_revenue: float,
    capex_pct_revenue: float,
    nwc_pct_revenue: float,
    tax_rate: float,
):
    """
    Projects free unlevered cash flow (fcf)

    All rates are given in decimals
    """
    revenues: List[float] =[]  #these lines create empty lists that hold values
    ebitdas: List[float] =[]
    ebits: List[float] =[]
    deprec_amor: List[float] =[]
    nwcs: List[float] =[]
    change_nwcs: List[float] =[]
    capexs: List[float] =[]
    fcfs: List[float] =[]

    # I assume base year net working capital (NWC) is tied to starting revenue
    nwc_prev = start_revenue * nwc_pct_revenue
    revenue = start_revenue

    for t in range(1, years + 1):
        revenue = revenue * (1 + revenue_growth)
        revenues.append(revenue)

        ebitda = revenue * ebitda_margin
        deprec_and_amor = revenue * deprec_amor_pct_revenue
        ebit = ebitda - deprec_and_amor

        taxable_income = max(ebit,0)
        income_tax = taxable_income * tax_rate
        nopat = ebit - income_tax

        nwc = revenue * nwc_pct_revenue
        change_nwc = nwc - nwc_prev

        capex = revenue * capex_pct_revenue

        fcf = nopat + deprec_and_amor - (change_nwc + capex)

        # Add to lists
        ebitdas.append(ebitda)
        deprec_amor.append(deprec_and_amor)
        ebits.append(ebit)
        nwcs.append(nwc)
        change_nwcs.append(change_nwc)
        capexs.append(capex)
        fcfs.append(fcf)

        nwc_prev = nwc

    return {
        "revenues": revenues,
        "ebitdas": ebitdas,
        "ebits": ebits,
        "deprec_amor": deprec_amor,
        "nwcs": nwcs,
        "change_nwcs": change_nwcs,
        "capexs": capexs,
        "fcfs": fcfs,
    }

def dcf_calculation(
    fcfs: List[float],
    wacc: float,
    terminal_method: Literal["perpetuity", "exit_multiple"],
    last_year_ebitda: float,
    terminal_growth: Optional[float] = None,
    exit_multiple: Optional[float] = None,
    net_debt: float = 0.0,
    shares_outstanding: Optional[float] = None,
):
    """
    Takes predicted FCFs and creates a DCF valuation.

    wacc, terminal_growth are in decimals
    """

    discount_factors: List[float] = []    # discount yearly FCF
    pv_fcfs: List[float] = []

    for t, fcf in enumerate(fcfs, start = 1):
        df = 1 / ((1 + wacc) ** t)
        discount_factors.append(df)
        pv_fcfs.append(fcf * df)

    if terminal_method == "perpetuity":
        if terminal_growth is None:
            raise ValueError("terminal_growth is required for perpetuity method")
        if terminal_growth >= wacc:
            raise ValueError("terminal_growth must be less than WACC")
        terminal_value = fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    elif terminal_method == "exit_multiple":
        if exit_multiple is None:
            raise ValueError("exit_multiple is required for exit_multiple method")
        terminal_value = last_year_ebitda * exit_multiple
    else:
        raise ValueError("terminal_method must be 'perpetuity' or 'exit_multiple'")

    df_terminal = discount_factors[-1]
    pv_terminal = terminal_value * df_terminal

    enterprise_value = sum(pv_fcfs) + pv_terminal
    equity_value = enterprise_value - net_debt

    price_per_share: Optional[float] = None
    if shares_outstanding and shares_outstanding > 0:
        price_per_share = equity_value / shares_outstanding
    
    return {
        "discount_factors": discount_factors,
        "pv_fcfs": pv_fcfs,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "price_per_share": price_per_share
    }

def main():
    """
    Inputs into model to test
    """
    # Inputs

    # Operating Inputs
    start_revenue = 1000.0 
    years = 5
    revenue_growth = 0.08
    ebitda_margin = 0.25
    deprec_amor_pct_revenue = 0.03
    capex_pct_revenue = 0.04
    nwc_pct_revenue = 0.10
    tax_rate = 0.25

    # Valuation Inputs
    wacc = 0.10
    terminal_method = "perpetuity"
    terminal_growth = 0.02
    exit_multiple = 10.0

    net_debt = 200.0
    shares_outstanding = 50.0

    projections = project_fcf(
        start_revenue=start_revenue,
        years=years,
        revenue_growth=revenue_growth,
        ebitda_margin=ebitda_margin,
        deprec_amor_pct_revenue=deprec_amor_pct_revenue,
        capex_pct_revenue=capex_pct_revenue,
        nwc_pct_revenue=nwc_pct_revenue,
        tax_rate=tax_rate,
    )

    fcfs = projections["fcfs"]
    last_year_ebitda = projections["ebitdas"][-1]

    dcf_result = dcf_calculation(
        fcfs=fcfs,
        wacc=wacc,
        terminal_method=terminal_method,
        last_year_ebitda=last_year_ebitda,
        terminal_growth=terminal_growth,
        exit_multiple=exit_multiple,
        net_debt=net_debt,
        shares_outstanding=shares_outstanding,
    )

    print("=== DCF SUMMARY ===")
    print(f"Projected FCFs: {[round(x, 2) for x in fcfs]}")
    print(f"PV of FCFs: {[round(x, 2) for x in dcf_result['pv_fcfs']]}")
    print(f"Terminal value (undiscounted): {dcf_result['terminal_value']:.2f}")
    print(f"PV of terminal value: {dcf_result['pv_terminal']:.2f}")
    print(f"Enterprise value: {dcf_result['enterprise_value']:.2f}")
    print(f"Equity value: {dcf_result['equity_value']:.2f}")
    if dcf_result["price_per_share"] is not None:
        print(f"Implied price per share: {dcf_result['price_per_share']:.2f}")


if __name__ == "__main__":
    main()