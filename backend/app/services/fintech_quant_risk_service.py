"""
FinTech Quantitative Analytics & Risk Engine Service
Implements Black-Scholes-Merton European option pricing, analytical Greeks,
Parametric Value-at-Risk (VaR 95% & 99%), and portfolio Sharpe ratio optimization.
Zero external library dependencies; uses standard library math.erf.
"""

import math
from typing import Dict, Any, List, Optional


class FintechQuantRiskService:
    """
    Quantitative finance and risk service for student quant clubs and financial engineering.
    """

    @classmethod
    def _std_norm_cdf(cls, x: float) -> float:
        """Cumulative distribution function for standard normal distribution."""
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @classmethod
    def _std_norm_pdf(cls, x: float) -> float:
        """Probability density function for standard normal distribution."""
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

    @classmethod
    def calculate_black_scholes(
        cls,
        spot_price: float,
        strike_price: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float
    ) -> Dict[str, Any]:
        """
        Calculate European Call & Put option prices and Greeks using Black-Scholes-Merton model.
        Guards against singularities (S <= 0, K <= 0, T <= 0, sigma <= 0).
        """
        s = max(0.0001, float(spot_price))
        k = max(0.0001, float(strike_price))
        t = max(0.0001, float(time_to_maturity))
        r = float(risk_free_rate)
        sigma = max(0.0001, float(volatility))

        sqrt_t = math.sqrt(t)
        d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * sqrt_t)
        d2 = d1 - sigma * sqrt_t

        nd1 = cls._std_norm_cdf(d1)
        nd2 = cls._std_norm_cdf(d2)
        n_neg_d1 = cls._std_norm_cdf(-d1)
        n_neg_d2 = cls._std_norm_cdf(-d2)
        pdf_d1 = cls._std_norm_pdf(d1)

        discount_factor = math.exp(-r * t)

        # Call & Put Option Prices
        call_price = s * nd1 - k * discount_factor * nd2
        put_price = k * discount_factor * n_neg_d2 - s * n_neg_d1

        # Non-negative guarantees
        call_price = max(0.0, call_price)
        put_price = max(0.0, put_price)

        # Greeks
        call_delta = nd1
        put_delta = nd1 - 1.0

        gamma = pdf_d1 / (s * sigma * sqrt_t)

        call_theta = (-(s * pdf_d1 * sigma) / (2.0 * sqrt_t) - r * k * discount_factor * nd2) / 365.0
        put_theta = (-(s * pdf_d1 * sigma) / (2.0 * sqrt_t) + r * k * discount_factor * n_neg_d2) / 365.0

        vega = (s * sqrt_t * pdf_d1) / 100.0  # Per 1% vol change

        call_rho = (k * t * discount_factor * nd2) / 100.0  # Per 1% rate change
        put_rho = (-k * t * discount_factor * n_neg_d2) / 100.0

        intrinsic_call = max(0.0, s - k)
        time_value_call = max(0.0, call_price - intrinsic_call)

        return {
            "spot_price": round(s, 2),
            "strike_price": round(k, 2),
            "time_to_maturity_years": round(t, 4),
            "risk_free_rate": round(r, 4),
            "volatility": round(sigma, 4),
            "call_price": round(call_price, 4),
            "put_price": round(put_price, 4),
            "intrinsic_value_call": round(intrinsic_call, 4),
            "time_value_call": round(time_value_call, 4),
            "greeks": {
                "call_delta": round(call_delta, 4),
                "put_delta": round(put_delta, 4),
                "gamma": round(gamma, 6),
                "call_theta_per_day": round(call_theta, 4),
                "put_theta_per_day": round(put_theta, 4),
                "vega_per_pct": round(vega, 4),
                "call_rho_per_pct": round(call_rho, 4),
                "put_rho_per_pct": round(put_rho, 4)
            }
        }

    @classmethod
    def calculate_portfolio_var(
        cls,
        portfolio_value: float,
        expected_annual_return: float,
        annual_volatility: float,
        holding_period_days: int = 1,
        risk_free_rate: float = 0.05
    ) -> Dict[str, Any]:
        """
        Calculate Parametric Value-at-Risk (VaR) at 95% and 99% confidence intervals
        and annualized Sharpe Ratio.
        """
        pval = max(0.0, float(portfolio_value))
        mu_ann = float(expected_annual_return)
        sigma_ann = max(0.0001, float(annual_volatility))
        days = max(1, int(holding_period_days))
        rf = float(risk_free_rate)

        # Scale to holding period (assuming 252 trading days per year)
        time_scale = math.sqrt(days / 252.0)
        period_vol = sigma_ann * time_scale
        period_mu = mu_ann * (days / 252.0)

        # Z-scores for standard normal distributions
        z_95 = 1.64485
        z_99 = 2.32635

        var_95_pct = max(0.0, z_95 * period_vol - period_mu)
        var_99_pct = max(0.0, z_99 * period_vol - period_mu)

        var_95_amount = pval * var_95_pct
        var_99_amount = pval * var_99_pct

        # Sharpe Ratio: (R_p - R_f) / sigma_p
        sharpe = (mu_ann - rf) / sigma_ann

        if sharpe >= 2.0:
            rating = "EXCELLENT"
        elif sharpe >= 1.0:
            rating = "GOOD"
        elif sharpe >= 0.0:
            rating = "ACCEPTABLE"
        else:
            rating = "SUBOPTIMAL_NEGATIVE"

        return {
            "portfolio_value": round(pval, 2),
            "holding_period_days": days,
            "period_expected_return_pct": round(period_mu * 100.0, 3),
            "period_volatility_pct": round(period_vol * 100.0, 3),
            "var_95_pct": round(var_95_pct * 100.0, 2),
            "var_95_amount": round(var_95_amount, 2),
            "var_99_pct": round(var_99_pct * 100.0, 2),
            "var_99_amount": round(var_99_amount, 2),
            "annualized_sharpe_ratio": round(sharpe, 3),
            "risk_adjusted_rating": rating
        }
