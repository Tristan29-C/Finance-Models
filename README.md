# Finance Models

A collection of lightweight Python finance models built from scratch:

- DCF model with free cash flow projection, terminal value, enterprise/equity value, and implied share price.
- Monte Carlo DCF that randomizes growth, margins, and WACC to generate a valuation distribution.
- Easy LBO model with leverage, interest expense, cash sweeps, debt paydown, and IRR/MOIC outputs.

All models are written to be clean, reusable, and easy to run from IPython or a script.

To run the DCF model, open a terminal in the repository folder and run:
python dcf.py
This prints a full sample valuation including projected free cash flows, discounting, terminal value, enterprise value, and implied price per share.

To use the DCF functions interactively (for your own assumptions), open Python or IPython and import:
from dcf import project_fcf, dcf_calculation, monte_carlo_dcf, monte_carlo_neat

To use the LBO model, import:
from lbo import easy_lbo
Then call easy_lbo with your chosen inputs to get IRR, MOIC, EBITDA path, and debt paydown.

The only required dependency is numpy.
