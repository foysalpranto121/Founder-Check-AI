"""
Advanced Financial Planning Tools - Funding, Unit Economics, Business Model Projections
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class FundingRequirements:
    """Funding requirements calculation"""
    monthly_burn_rate: float  # Monthly cash burn
    initial_capital: float
    runway_months: float
    required_funding: float  # Additional funding needed
    valuation_estimate: float
    equity_to_raise: float  # % equity for funding


@dataclass
class UnitEconomics:
    """Detailed unit economics"""
    revenue_per_customer: float
    customer_acquisition_cost: float
    lifetime_value: float
    payback_period_months: float
    ltv_cac_ratio: float
    gross_margin_per_customer: float
    monthly_churn_rate: float
    customer_retention_rate: float
    arpu: float  # Average Revenue Per User
    mrr: float  # Monthly Recurring Revenue


@dataclass
class BusinessModelProjection:
    """Business model projections"""
    month: int
    revenue: float
    cogs: float
    gross_profit: float
    operating_expenses: float
    ebitda: float
    cumulative_cash: float
    breakeven_status: bool


class FinancialPlanningService:
    """Service for advanced financial planning"""

    def __init__(self):
        self.funding_scenarios: Dict[str, FundingRequirements] = {}
        self.unit_economics_history: Dict[int, List[UnitEconomics]] = {}
        self.projection_scenarios: Dict[str, List[BusinessModelProjection]] = {}

    # ========== FUNDING CALCULATOR ==========

    def calculate_funding_requirements(self, monthly_burn_rate: float, current_capital: float,
                                      target_runway_months: int = 24) -> FundingRequirements:
        """Calculate funding requirements"""
        current_runway = current_capital / monthly_burn_rate if monthly_burn_rate > 0 else float('inf')
        months_short = max(0, target_runway_months - current_runway)
        required_funding = months_short * monthly_burn_rate

        # Estimate valuation (simple method: annual burn * multiple)
        annual_burn = monthly_burn_rate * 12
        valuation_multiple = 4  # Post-money valuation multiple of annual burn
        valuation = annual_burn * valuation_multiple

        # Equity to raise for 24 months runway
        equity_percentage = (required_funding / valuation * 100) if valuation > 0 else 0

        return FundingRequirements(
            monthly_burn_rate=round(monthly_burn_rate, 2),
            initial_capital=round(current_capital, 2),
            runway_months=round(current_runway, 1),
            required_funding=round(required_funding, 2),
            valuation_estimate=round(valuation, 2),
            equity_to_raise=round(equity_percentage, 1)
        )

    def calculate_runway(self, current_capital: float, monthly_burn_rate: float) -> Dict:
        """Calculate runway months"""
        if monthly_burn_rate <= 0:
            return {
                'runway_months': float('inf'),
                'status': 'Profitable',
                'months_to_profitability': 0
            }

        runway_months = current_capital / monthly_burn_rate if monthly_burn_rate > 0 else float('inf')

        status = 'Critical' if runway_months < 3 else 'Tight' if runway_months < 6 else 'Comfortable'

        return {
            'runway_months': round(runway_months, 1),
            'runway_status': status,
            'critical_runway': runway_months < 3,
            'recommendation': self._get_runway_recommendation(runway_months)
        }

    def _get_runway_recommendation(self, runway_months: float) -> str:
        """Get runway recommendation"""
        if runway_months < 3:
            return 'Critical: Start fundraising immediately'
        elif runway_months < 6:
            return 'Tight: Begin fundraising process now'
        elif runway_months < 12:
            return 'Comfortable: Plan fundraising for next quarter'
        else:
            return 'Strong: Focus on growth and metrics'

    def calculate_burn_rate_scenarios(self, monthly_expenses: float, revenue: float) -> Dict:
        """Calculate different burn rate scenarios"""
        current_burn = max(0, monthly_expenses - revenue)

        # Scenarios: reduce expenses by 10%, 20%, 30%
        scenarios = []
        for reduction_pct in [10, 20, 30]:
            reduced_expenses = monthly_expenses * (1 - reduction_pct / 100)
            scenario_burn = max(0, reduced_expenses - revenue)
            scenarios.append({
                'expense_reduction_pct': reduction_pct,
                'new_monthly_expenses': round(reduced_expenses, 2),
                'new_burn_rate': round(scenario_burn, 2),
                'runway_extension_months': round((current_burn - scenario_burn) * 12 / max(1, current_burn), 1)
            })

        return {
            'current_burn_rate': round(current_burn, 2),
            'scenarios': scenarios
        }

    def estimate_valuation(self, revenue: float, growth_rate: float, sector: str = 'Technology',
                          stage: str = 'early') -> Dict:
        """Estimate company valuation"""
        # Revenue multiples by sector and stage
        multiples = {
            'Technology': {'early': 5, 'growth': 8, 'mature': 4},
            'Service': {'early': 2, 'growth': 4, 'mature': 2},
            'Retail': {'early': 0.5, 'growth': 1.5, 'mature': 1},
        }

        base_multiple = multiples.get(sector, {}).get(stage, 3)

        # Adjust multiple based on growth
        growth_adjustment = min(2.0, 1 + (growth_rate - 50) / 100) if growth_rate > 50 else 0.8

        adjusted_multiple = base_multiple * growth_adjustment
        valuation = revenue * adjusted_multiple

        return {
            'annual_revenue': round(revenue, 2),
            'growth_rate': round(growth_rate, 1),
            'valuation_multiple': round(adjusted_multiple, 1),
            'estimated_valuation': round(valuation, 2),
            'valuation_range': {
                'low': round(valuation * 0.7, 2),
                'mid': round(valuation, 2),
                'high': round(valuation * 1.3, 2)
            }
        }

    def simulate_cap_table(self, founder_equity: float, seed_amount: float,
                          seed_valuation: float) -> Dict:
        """Simulate cap table after seed round"""
        pre_money_valuation = seed_valuation
        post_money_valuation = pre_money_valuation + seed_amount

        investor_equity_pct = (seed_amount / post_money_valuation) * 100
        founder_new_equity_pct = 100 - investor_equity_pct

        return {
            'pre_money_valuation': round(pre_money_valuation, 2),
            'seed_amount': round(seed_amount, 2),
            'post_money_valuation': round(post_money_valuation, 2),
            'founders': {
                'equity_pct': round(founder_new_equity_pct, 1),
                'shares': round(founder_equity * (founder_new_equity_pct / 100), 2)
            },
            'investors': {
                'equity_pct': round(investor_equity_pct, 1),
                'shares': round((post_money_valuation / pre_money_valuation) * seed_amount, 2)
            }
        }

    # ========== UNIT ECONOMICS DASHBOARD ==========

    def calculate_unit_economics(self, monthly_revenue: float, monthly_cogs: float,
                                 cac: float, ltv: float, monthly_churn: float) -> UnitEconomics:
        """Calculate comprehensive unit economics"""
        # Assume 10 customers at start for revenue per customer
        estimated_customers = max(1, monthly_revenue / 5000)  # Rough estimate
        revenue_per_customer = monthly_revenue / estimated_customers if estimated_customers > 0 else monthly_revenue

        gross_profit = monthly_revenue - monthly_cogs
        gross_margin_per_customer = (revenue_per_customer - (monthly_cogs / estimated_customers)) if estimated_customers > 0 else 0

        payback_months = cac / gross_margin_per_customer if gross_margin_per_customer > 0 else 0
        ltv_cac_ratio = ltv / cac if cac > 0 else 0

        retention_rate = max(0, 100 - monthly_churn)

        return UnitEconomics(
            revenue_per_customer=round(revenue_per_customer, 2),
            customer_acquisition_cost=round(cac, 2),
            lifetime_value=round(ltv, 2),
            payback_period_months=round(payback_months, 1),
            ltv_cac_ratio=round(ltv_cac_ratio, 2),
            gross_margin_per_customer=round(gross_margin_per_customer, 2),
            monthly_churn_rate=round(monthly_churn, 1),
            customer_retention_rate=round(retention_rate, 1),
            arpu=round(revenue_per_customer, 2),
            mrr=round(monthly_revenue, 2)
        )

    def get_unit_economics_health(self, unit_economics: UnitEconomics) -> Dict:
        """Assess unit economics health"""
        health_score = 0
        issues = []

        # LTV:CAC ratio (should be > 3)
        if unit_economics.ltv_cac_ratio > 3:
            health_score += 30
        elif unit_economics.ltv_cac_ratio > 1:
            health_score += 15
            issues.append('LTV:CAC ratio below 3 - customer economics need improvement')
        else:
            issues.append('Critical: Losing money on each customer')

        # Payback period (should be < 12 months)
        if unit_economics.payback_period_months < 12:
            health_score += 30
        elif unit_economics.payback_period_months < 24:
            health_score += 15
            issues.append('Payback period long - consider reducing CAC')
        else:
            issues.append('Payback period too long - business model needs review')

        # Churn rate (should be < 5%)
        if unit_economics.monthly_churn_rate < 5:
            health_score += 20
        elif unit_economics.monthly_churn_rate < 10:
            health_score += 10
            issues.append('Churn rate elevated - focus on retention')
        else:
            issues.append('High churn - retention critical issue')

        # Gross margin (should be > 60%)
        margin_pct = (unit_economics.gross_margin_per_customer / unit_economics.revenue_per_customer * 100) if unit_economics.revenue_per_customer > 0 else 0
        if margin_pct > 60:
            health_score += 20
        elif margin_pct > 40:
            health_score += 10
        else:
            issues.append('Gross margin too low - review cost structure')

        return {
            'health_score': health_score,
            'health_status': 'Excellent' if health_score > 80 else 'Good' if health_score > 60 else 'Fair' if health_score > 40 else 'Poor',
            'issues': issues,
            'recommendations': self._get_unit_economics_recommendations(unit_economics)
        }

    def _get_unit_economics_recommendations(self, ue: UnitEconomics) -> List[str]:
        """Get recommendations for improving unit economics"""
        recommendations = []

        if ue.ltv_cac_ratio < 3:
            recommendations.append('Increase LTV by improving retention or pricing')
            recommendations.append('Reduce CAC through more efficient marketing')

        if ue.payback_period_months > 12:
            recommendations.append('Reduce customer acquisition costs')
            recommendations.append('Increase revenue per customer')

        if ue.monthly_churn_rate > 5:
            recommendations.append('Implement customer retention program')
            recommendations.append('Improve product/service quality')

        if ue.mrr < 100000:
            recommendations.append('Scale customer acquisition')
            recommendations.append('Focus on growing ARR')

        return recommendations if recommendations else ['Unit economics are strong - focus on growth']

    # ========== BUSINESS MODEL PROJECTIONS ==========

    def project_business_model(self, initial_revenue: float, monthly_growth: float,
                              cogs_percentage: float, opex_monthly: float,
                              months: int = 36) -> List[BusinessModelProjection]:
        """Project business model performance"""
        projections = []
        cumulative_cash = -opex_monthly * 3  # Assume 3 months initial investment

        for month in range(1, months + 1):
            revenue = initial_revenue * ((1 + monthly_growth) ** (month - 1))
            cogs = revenue * cogs_percentage
            gross_profit = revenue - cogs
            operating_expenses = opex_monthly
            ebitda = gross_profit - operating_expenses

            cumulative_cash += ebitda
            breakeven_status = cumulative_cash >= 0

            projections.append(BusinessModelProjection(
                month=month,
                revenue=round(revenue, 2),
                cogs=round(cogs, 2),
                gross_profit=round(gross_profit, 2),
                operating_expenses=round(operating_expenses, 2),
                ebitda=round(ebitda, 2),
                cumulative_cash=round(cumulative_cash, 2),
                breakeven_status=breakeven_status
            ))

        return projections

    def project_revenue_scenarios(self, base_revenue: float, conservative_growth: float,
                                 base_growth: float, optimistic_growth: float) -> Dict:
        """Project revenue across scenarios"""
        scenarios = {}

        for scenario_name, growth_rate in [
            ('Conservative', conservative_growth),
            ('Base Case', base_growth),
            ('Optimistic', optimistic_growth)
        ]:
            year_1 = base_revenue * 12 * ((1 + growth_rate) ** 12 - 1) / growth_rate if growth_rate > 0 else base_revenue * 12
            year_2 = year_1 * ((1 + growth_rate) ** 12)
            year_3 = year_2 * ((1 + growth_rate) ** 12)

            scenarios[scenario_name] = {
                'growth_rate': round(growth_rate * 100, 1),
                'year_1_revenue': round(year_1, 2),
                'year_2_revenue': round(year_2, 2),
                'year_3_revenue': round(year_3, 2),
                'total_3year': round(year_1 + year_2 + year_3, 2),
                'cagr': round(((year_3 / year_1) ** (1/2) - 1) * 100, 1) if year_1 > 0 else 0
            }

        return scenarios

    def project_profitability_timeline(self, initial_revenue: float, monthly_growth: float,
                                      opex_monthly: float, cogs_pct: float) -> Dict:
        """Project when company reaches profitability"""
        cumulative_cash = -opex_monthly * 3
        profitability_month = None
        break_even_month = None

        for month in range(1, 61):  # Look up to 5 years
            revenue = initial_revenue * ((1 + monthly_growth) ** (month - 1))
            gross_profit = revenue * (1 - cogs_pct)
            ebitda = gross_profit - opex_monthly
            cumulative_cash += ebitda

            if break_even_month is None and cumulative_cash >= 0:
                break_even_month = month

            if profitability_month is None and ebitda > 0:
                profitability_month = month

        return {
            'profitability_month': profitability_month,
            'cash_breakeven_month': break_even_month,
            'months_to_profitability': profitability_month if profitability_month else 'Beyond 5 years',
            'profitability_status': 'On track' if profitability_month and profitability_month < 36 else 'Extended timeline'
        }

    # ========== WHAT-IF SCENARIOS ==========

    def run_what_if_scenario(self, base_revenue: float, base_expenses: float,
                            changes: Dict) -> Dict:
        """Run what-if scenario with parameter changes"""
        new_revenue = base_revenue * (1 + changes.get('revenue_change_pct', 0) / 100)
        new_expenses = base_expenses * (1 + changes.get('expense_change_pct', 0) / 100)
        new_burn = max(0, new_expenses - new_revenue)

        base_burn = max(0, base_expenses - base_revenue)

        return {
            'scenario_name': changes.get('name', 'Custom Scenario'),
            'new_revenue': round(new_revenue, 2),
            'new_expenses': round(new_expenses, 2),
            'new_burn_rate': round(new_burn, 2),
            'burn_rate_improvement': round(base_burn - new_burn, 2),
            'runway_improvement_months': round((base_burn - new_burn) * 12 / max(1, base_burn), 1) if base_burn > 0 else 0,
            'impact_summary': self._summarize_scenario_impact(base_burn, new_burn)
        }

    def _summarize_scenario_impact(self, base_burn: float, new_burn: float) -> str:
        """Summarize scenario impact"""
        if new_burn < 0:  # Profitable
            return f'Achieves profitability with ৳{abs(new_burn):.0f} monthly surplus'
        elif new_burn < base_burn:
            improvement = ((base_burn - new_burn) / base_burn * 100)
            return f'Improves burn rate by {improvement:.0f}% - extends runway'
        else:
            return 'Increases burn rate - worsens financial position'


# Global financial planning service instance
financial_planning_service = FinancialPlanningService()
