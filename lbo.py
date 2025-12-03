from typing import List, Dict 
import numpy as np

def easy_lbo(
    entry_ebitda: float,
    entry_multiple: float,
    leverage_multiple: float,
    ebitda_growth: float,
    years: int,
    interest_rate: float,
    exit_multiple: float,
    cash_sweep: float = 1.0,
):
    """
    Assuming:
    EBITDA grows at a constant rate
    Entry EV = entry_ebitda * entry_multiple
    debt at entry = leverage_multiple * entry_ebitda
    equity at entry = EV - debt
    cash available each year for paydown = EBITDA - interest
    same % of cash is used each year to pay down debt
    simple model so no taxes, capex or working capital included
    IRR is based on equity cash flows
    """

    ev_entry = entry_ebitda * entry_multiple
    debt_entry = entry_ebitda * leverage_multiple
    equity_entry = ev_entry - debt_entry

    ebitdas = [entry_ebitda]
    debts = [debt_entry]
    interests = []

    debt = debt_entry
    ebitda = entry_ebitda

    for t in range(1, years + 1):
        ebitda = ebitda * (1 + ebitda_growth)
        ebitdas.append(ebitda)

        interest = debt * interest_rate
        interests.append(interest)

        cash = ebitda - interest # this is cash available to pay debts
        
        paydown = max(0.0, cash * cash_sweep)

        paydown = min(debt, paydown)

        debt = debt - paydown
        debts.append(debt)
    
    ebitda_exit = ebitdas[-1]
    ev_exit = ebitda_exit * exit_multiple
    final_debt = debts[-1]
    equity_exit = ev_exit - final_debt

    equity_cash_flows = [-equity_entry] + [0.0] * (years - 1) + [equity_exit]
    irr = float(np.irr(equity_cash_flows))
    moic = equity_exit / equity_entry if equity_entry != 0 else float("nan")

    return {
        'ev_entry': ev_entry,
        'debt_entry': debt_entry,
        'equity_entry': equity_entry,
        'ev_exit': ev_exit,
        'final_debt': final_debt,
        'equity_exit': equity_exit,
        'moic': moic,
        'irr': irr,
        'ebitdas': ebitdas,
        'debts': debts,
        'interests': interests
    }


