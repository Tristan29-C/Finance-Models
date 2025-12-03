# Finance Models

A collection of lightweight Python finance models built from scratch:

- DCF model with free cash flow projection, terminal value, enterprise/equity value, and implied share price.
- Monte Carlo DCF that randomizes growth, margins, and WACC to generate a valuation distribution.
- Easy LBO model with leverage, interest expense, cash sweeps, debt paydown, and IRR/MOIC outputs.

All models are written to be clean, reusable, and easy to run from IPython or a script.

How to run

Install numpy

Run the DCF model: python dcf.py

Or import the functions in IPython: from dcf import project_fcf, dcf_calculation, monte_carlo_neat

For the LBO model: from lbo import easy_lbo
