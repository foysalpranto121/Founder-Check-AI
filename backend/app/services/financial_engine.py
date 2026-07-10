"""
Financial Projections Engine for FounderCheck
Generates 3-year financial forecasts, unit economics, and break-even analysis
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import math

@dataclass
class FinancialAssumptions:
    """Financial assumptions for projections"""
    monthly_revenue_month_1: float  # Revenue in month 1
    monthly_growth_rate: float  # 1-5% = 0.01-0.05
    customer_acquisition_cost: float  # Initial CAC in BDT
    cac_reduction_rate: float  # How much CAC improves monthly (%)
    lifetime_value_months: int  # How many months customer stays
    fixed_costs_monthly: float  # Monthly overhead in BDT
    variable_cost_percentage: float  # % of revenue (0-1)
    initial_investment: float  # Startup capital in BDT
    team_size_month_1: int
    avg_salary: float  # Monthly salary in BDT

class FinancialProjections:
    def __init__(self, assumptions: Dict[str, Any]):
        self.assumptions = assumptions
        self.months = 36  # 3 years

    def generate_projections(self) -> Dict[str, Any]:
        """Generate complete financial projections.

        Verdict fields (safety margin, breakeven timeline, unit economics
        health) are computed from the projected numbers, never asserted.
        """
        revenue = self._project_revenue()
        unit_economics = self._calculate_unit_economics()
        cash_flow = self._generate_cash_flow()
        break_even = self._calculate_break_even()

        # Breakeven timeline from the actual cash curve, not a canned string
        breakeven_month = cash_flow.get('cash_breakeven_month')
        break_even['breakeven_timeline_months'] = (
            f'Month {breakeven_month}' if breakeven_month else 'Not reached within 36 months'
        )

        # Safety margin from month-12 revenue vs the computed breakeven revenue
        month_12_revenue = revenue['monthly'][11]['monthly_revenue']
        be_revenue = break_even['breakeven_monthly_revenue']
        ratio = (month_12_revenue / be_revenue) if be_revenue > 0 else 0
        if ratio >= 2:
            break_even['safety_margin'] = f'Strong: month 12 revenue is {ratio:.1f}x breakeven'
        elif ratio >= 1.2:
            break_even['safety_margin'] = f'Adequate: month 12 revenue is {ratio:.1f}x breakeven'
        elif ratio >= 1:
            break_even['safety_margin'] = f'Thin: month 12 revenue is {ratio:.1f}x breakeven'
        else:
            break_even['safety_margin'] = f'Below breakeven at month 12 ({ratio:.1f}x)'

        return {
            'revenue_projections': revenue,
            'unit_economics': unit_economics,
            'pnl_statement': self._generate_pnl(),
            'cash_flow': cash_flow,
            'break_even': break_even,
            'sensitivity': self._sensitivity_analysis(),
            'key_metrics': self._calculate_key_metrics(unit_economics)
        }

    def _project_revenue(self) -> Dict[str, Any]:
        """Project monthly revenue for 3 years"""
        monthly_revenue = self.assumptions.get('monthly_revenue_month_1', 100000)
        growth_rate = self.assumptions.get('monthly_growth_rate', 0.03)

        revenues = []
        cumulative = 0

        for month in range(1, self.months + 1):
            # Compound growth
            revenue = monthly_revenue * ((1 + growth_rate) ** (month - 1))
            cumulative += revenue

            revenues.append({
                'month': month,
                'year': math.ceil(month / 12),
                'monthly_revenue': round(revenue),
                'cumulative_revenue': round(cumulative),
                'yoy_growth': None if month == 1 else 'calculated'
            })

        # Calculate YoY growth
        year_1_total = sum(r['monthly_revenue'] for r in revenues[:12])
        year_2_total = sum(r['monthly_revenue'] for r in revenues[12:24])
        year_3_total = sum(r['monthly_revenue'] for r in revenues[24:36])

        for r in revenues:
            if r['month'] > 12 and r['month'] <= 24:
                r['yoy_growth'] = ((year_2_total - year_1_total) / year_1_total * 100) if year_1_total > 0 else 0
            elif r['month'] > 24:
                r['yoy_growth'] = ((year_3_total - year_2_total) / year_2_total * 100) if year_2_total > 0 else 0

        return {
            'monthly': revenues,
            'year_1_total': round(year_1_total),
            'year_2_total': round(year_2_total),
            'year_3_total': round(year_3_total),
            'total_3_year': round(year_1_total + year_2_total + year_3_total)
        }

    def _calculate_unit_economics(self) -> Dict[str, Any]:
        """Calculate unit economics metrics"""
        cac = self.assumptions.get('customer_acquisition_cost', 5000)
        cac_reduction = self.assumptions.get('cac_reduction_rate', 0.02)
        ltv_months = self.assumptions.get('lifetime_value_months', 12)
        monthly_revenue = self.assumptions.get('monthly_revenue_month_1', 100000)
        variable_cost_pct = self.assumptions.get('variable_cost_percentage', 0.3)

        # Assume 10 customers at month 1 (rough estimate)
        initial_customers = 10 if monthly_revenue > 0 else 1
        revenue_per_customer = monthly_revenue / initial_customers if initial_customers > 0 else monthly_revenue

        # Customer Lifetime Value = monthly profit * LTV months
        monthly_profit_per_customer = revenue_per_customer * (1 - variable_cost_pct)
        ltv = monthly_profit_per_customer * ltv_months

        # Payback period = CAC / monthly profit per customer
        payback_months = (cac / monthly_profit_per_customer) if monthly_profit_per_customer > 0 else 999

        # LTV:CAC ratio
        ltv_cac_ratio = ltv / cac if cac > 0 else 0

        return {
            'customer_acquisition_cost': round(cac),
            'cac_trend': self._cac_trend(cac, cac_reduction),
            'revenue_per_customer_monthly': round(revenue_per_customer),
            'gross_margin_per_customer': round(monthly_profit_per_customer),
            'lifetime_value': round(ltv),
            'payback_period_months': round(payback_months, 1),
            'ltv_cac_ratio': round(ltv_cac_ratio, 2),
            'churn_rate_assumed': self.assumptions.get('churn_rate_pct', 3.0),
            'notes': 'Based on projected revenue and cost assumptions'
        }

    def _cac_trend(self, initial_cac: float, reduction_rate: float) -> List[Dict]:
        """Project CAC reduction over time"""
        trend = []
        cac = initial_cac

        for month in [1, 6, 12, 18, 24, 30, 36]:
            trend.append({
                'month': month,
                'cac': round(cac),
                'reduction_vs_initial': round(((initial_cac - cac) / initial_cac * 100), 1)
            })
            cac *= (1 - reduction_rate) ** 5  # Compound for next period

        return trend

    def _generate_pnl(self) -> Dict[str, Any]:
        """Generate Profit & Loss statement"""
        revenue_proj = self._project_revenue()
        fixed_costs = self.assumptions.get('fixed_costs_monthly', 50000)
        variable_cost_pct = self.assumptions.get('variable_cost_percentage', 0.3)

        years_pnl = []

        for year in range(1, 4):
            start_month = (year - 1) * 12
            end_month = year * 12

            year_revenue = revenue_proj['monthly'][start_month:end_month]
            total_revenue = sum(m['monthly_revenue'] for m in year_revenue)
            total_cogs = total_revenue * variable_cost_pct
            gross_profit = total_revenue - total_cogs
            gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0

            operating_expenses = fixed_costs * 12
            ebitda = gross_profit - operating_expenses
            ebitda_margin = (ebitda / total_revenue * 100) if total_revenue > 0 else 0

            # Estimate tax (15% on positive profit)
            tax = max(0, ebitda * 0.15)
            net_income = ebitda - tax
            net_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0

            years_pnl.append({
                'year': year,
                'revenue': round(total_revenue),
                'cogs': round(total_cogs),
                'gross_profit': round(gross_profit),
                'gross_margin_pct': round(gross_margin, 1),
                'operating_expenses': round(operating_expenses),
                'ebitda': round(ebitda),
                'ebitda_margin_pct': round(ebitda_margin, 1),
                'tax': round(tax),
                'net_income': round(net_income),
                'net_margin_pct': round(net_margin, 1),
                'profitability_status': 'Profitable' if net_income > 0 else 'Pre-revenue'
            })

        return {
            'annual_summary': years_pnl,
            'status': 'Healthy' if years_pnl[-1]['net_income'] > 0 else 'Needs work'
        }

    def _generate_cash_flow(self) -> Dict[str, Any]:
        """Generate cash flow projections"""
        revenue_proj = self._project_revenue()
        fixed_costs = self.assumptions.get('fixed_costs_monthly', 50000)
        variable_cost_pct = self.assumptions.get('variable_cost_percentage', 0.3)
        initial_capital = self.assumptions.get('initial_investment', 1000000)

        cash_flow = []
        cumulative_cash = initial_capital
        cumulative_operating = 0.0

        for month_data in revenue_proj['monthly'][:36]:
            revenue = month_data['monthly_revenue']
            cogs = revenue * variable_cost_pct
            operating_costs = fixed_costs

            net_monthly_cash = revenue - cogs - operating_costs
            cumulative_cash += net_monthly_cash
            cumulative_operating += net_monthly_cash

            cash_flow.append({
                'month': month_data['month'],
                'revenue': round(revenue),
                'costs': round(cogs + operating_costs),
                'net_cash_flow': round(net_monthly_cash),
                'cumulative_cash': round(cumulative_cash),
                'cumulative_operating_cash': round(cumulative_operating),
                'runway_status': 'Positive' if cumulative_cash > 0 else 'Negative'
            })

        # Break-even: first month where cumulative OPERATING cash turns
        # positive. Measuring total cash would count the initial capital
        # and mislabel month 1 as break-even.
        breakeven_month = None
        for cf in cash_flow:
            if cf['cumulative_operating_cash'] > 0 and (breakeven_month is None):
                breakeven_month = cf['month']

        return {
            'monthly_cashflow': cash_flow,
            'initial_capital': round(initial_capital),
            'final_cash_position': round(cumulative_cash),
            'cash_breakeven_month': breakeven_month,
            'runway_months': 'Profitable' if cumulative_cash > 0 else 'Calculate runway'
        }

    def _calculate_break_even(self) -> Dict[str, Any]:
        """Calculate break-even analysis"""
        fixed_costs = self.assumptions.get('fixed_costs_monthly', 50000)
        variable_cost_pct = self.assumptions.get('variable_cost_percentage', 0.3)
        avg_order_value = self.assumptions.get('monthly_revenue_month_1', 100000) / 10  # Rough estimate

        contribution_margin_pct = 1 - variable_cost_pct

        # Break-even revenue
        breakeven_revenue = fixed_costs / contribution_margin_pct if contribution_margin_pct > 0 else fixed_costs

        # Break-even units (assuming AOV)
        breakeven_units = breakeven_revenue / avg_order_value if avg_order_value > 0 else 0

        return {
            'breakeven_monthly_revenue': round(breakeven_revenue),
            'breakeven_units_per_month': round(breakeven_units),
            'breakeven_timeline_months': 'Month 3-6 (estimated)',
            'fixed_costs_monthly': round(fixed_costs),
            'contribution_margin_pct': round(contribution_margin_pct * 100, 1),
            'safety_margin': 'Strong - Revenue > 2x breakeven'
        }

    def _sensitivity_analysis(self) -> Dict[str, Any]:
        """Sensitivity analysis around this idea's own base growth rate.

        Scenarios are multiples of the idea-specific base rate, and the
        base rate is restored afterward so later calculations are not
        polluted by the last scenario.
        """
        base_growth = self.assumptions.get('monthly_growth_rate', 0.03)
        base_revenue = self._project_revenue()['total_3_year']
        scenarios_spec = [
            (0.5, 'Conservative'),
            (0.75, 'Cautious'),
            (1.0, 'Base'),
            (1.5, 'Optimistic'),
            (2.0, 'Aggressive'),
        ]

        sensitivity = []
        try:
            for multiple, label in scenarios_spec:
                growth = base_growth * multiple
                self.assumptions['monthly_growth_rate'] = growth
                proj_revenue = self._project_revenue()['total_3_year']
                variance = ((proj_revenue - base_revenue) / base_revenue * 100) if base_revenue > 0 else 0
                sensitivity.append({
                    'growth_rate_pct': round(growth * 100, 1),
                    'total_3_year_revenue': round(proj_revenue),
                    'variance_from_base_pct': round(variance, 1),
                    'scenario': label
                })
        finally:
            self.assumptions['monthly_growth_rate'] = base_growth

        return {
            'scenarios': sensitivity,
            'best_case': sensitivity[-1],
            'base_case': sensitivity[2],
            'worst_case': sensitivity[0]
        }

    def _calculate_key_metrics(self, unit_economics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate key performance metrics.

        Unit economics health is derived from the actual LTV:CAC ratio,
        never asserted.
        """
        pnl = self._generate_pnl()
        cashflow = self._generate_cash_flow()

        year_3_revenue = pnl['annual_summary'][2]['revenue']
        year_1_revenue = pnl['annual_summary'][0]['revenue']

        cagr = (((year_3_revenue / year_1_revenue) ** (1/2)) - 1) * 100 if year_1_revenue > 0 else 0

        ltv_cac = unit_economics.get('ltv_cac_ratio', 0)
        if ltv_cac >= 3:
            health = 'Strong'
        elif ltv_cac >= 1.5:
            health = 'Moderate'
        else:
            health = 'Weak'

        first_profitable = next(
            (y['year'] for y in pnl['annual_summary'] if y['net_income'] > 0), None
        )
        profitability = (
            f'Profitable by Year {first_profitable}' if first_profitable
            else 'Not profitable within 3 years'
        )

        return {
            'revenue_cagr_pct': round(cagr, 1),
            'month_to_profitability': profitability,
            'gross_margin_year_3': pnl['annual_summary'][2]['gross_margin_pct'],
            'net_margin_year_3': pnl['annual_summary'][2]['net_margin_pct'],
            'cash_position_year_3': cashflow['final_cash_position'],
            'unit_economics_health': health,
            'recommendation': 'Track metrics quarterly and adjust accordingly'
        }


# Cost-structure archetypes with BD-plausible BDT figures. The extracted
# sector slug (for example "agritech" or "cleaning_service") is matched by
# keyword; the old table used capitalized keys that never matched and so
# served identical Technology numbers for every idea. Order matters: the
# most specific archetypes come first, and the generic tech keywords come
# last so "agritech" is not swallowed by the "tech" substring.
SECTOR_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    'agritech': {
        'keywords': ['agri', 'farm', 'crop', 'fishery', 'livestock'],
        'monthly_revenue_month_1': 200000, 'monthly_growth_rate': 0.04,
        'customer_acquisition_cost': 500, 'cac_reduction_rate': 0.02,
        'lifetime_value_months': 8, 'fixed_costs_monthly': 120000,
        'variable_cost_percentage': 0.55, 'initial_investment': 4000000,
        'team_size_month_1': 6, 'avg_salary': 30000,
    },
    'food': {
        'keywords': ['food', 'kitchen', 'restaurant', 'meal', 'catering'],
        'monthly_revenue_month_1': 300000, 'monthly_growth_rate': 0.04,
        'customer_acquisition_cost': 400, 'cac_reduction_rate': 0.02,
        'lifetime_value_months': 6, 'fixed_costs_monthly': 180000,
        'variable_cost_percentage': 0.60, 'initial_investment': 2500000,
        'team_size_month_1': 8, 'avg_salary': 25000,
    },
    'logistics': {
        'keywords': ['logistic', 'delivery', 'transport', 'courier', 'marketplace', 'supply'],
        'monthly_revenue_month_1': 250000, 'monthly_growth_rate': 0.05,
        'customer_acquisition_cost': 800, 'cac_reduction_rate': 0.02,
        'lifetime_value_months': 10, 'fixed_costs_monthly': 200000,
        'variable_cost_percentage': 0.45, 'initial_investment': 5000000,
        'team_size_month_1': 8, 'avg_salary': 35000,
    },
    'hardware': {
        'keywords': ['energy', 'solar', 'manufactur', 'hardware', 'device', 'electronics'],
        'monthly_revenue_month_1': 400000, 'monthly_growth_rate': 0.03,
        'customer_acquisition_cost': 3000, 'cac_reduction_rate': 0.02,
        'lifetime_value_months': 24, 'fixed_costs_monthly': 300000,
        'variable_cost_percentage': 0.60, 'initial_investment': 10000000,
        'team_size_month_1': 10, 'avg_salary': 40000,
    },
    'retail': {
        'keywords': ['retail', 'commerce', 'fashion', 'shop', 'store'],
        'monthly_revenue_month_1': 500000, 'monthly_growth_rate': 0.04,
        'customer_acquisition_cost': 800, 'cac_reduction_rate': 0.01,
        'lifetime_value_months': 6, 'fixed_costs_monthly': 250000,
        'variable_cost_percentage': 0.55, 'initial_investment': 6000000,
        'team_size_month_1': 12, 'avg_salary': 30000,
    },
    'services': {
        'keywords': ['service', 'cleaning', 'health', 'education', 'consult', 'care', 'repair'],
        'monthly_revenue_month_1': 200000, 'monthly_growth_rate': 0.04,
        'customer_acquisition_cost': 2000, 'cac_reduction_rate': 0.02,
        'lifetime_value_months': 12, 'fixed_costs_monthly': 130000,
        'variable_cost_percentage': 0.40, 'initial_investment': 1500000,
        'team_size_month_1': 6, 'avg_salary': 35000,
    },
    'tech': {
        'keywords': ['tech', 'software', 'saas', 'fintech', 'edtech', 'app', 'platform', 'ai'],
        'monthly_revenue_month_1': 150000, 'monthly_growth_rate': 0.06,
        'customer_acquisition_cost': 1500, 'cac_reduction_rate': 0.03,
        'lifetime_value_months': 18, 'fixed_costs_monthly': 180000,
        'variable_cost_percentage': 0.20, 'initial_investment': 3000000,
        'team_size_month_1': 4, 'avg_salary': 50000,
    },
}

GENERAL_ARCHETYPE: Dict[str, Any] = {
    'monthly_revenue_month_1': 250000, 'monthly_growth_rate': 0.04,
    'customer_acquisition_cost': 1500, 'cac_reduction_rate': 0.02,
    'lifetime_value_months': 12, 'fixed_costs_monthly': 170000,
    'variable_cost_percentage': 0.40, 'initial_investment': 3500000,
    'team_size_month_1': 6, 'avg_salary': 35000,
}


def _match_archetype(sector: str) -> tuple:
    """Match the extracted sector slug to an archetype by keyword.

    Returns (archetype_name, assumptions_copy). Falls back to a general
    profile when nothing matches, so an unknown sector still projects.
    """
    slug = str(sector or '').lower()
    for name, spec in SECTOR_ARCHETYPES.items():
        if any(kw in slug for kw in spec['keywords']):
            assumptions = {k: v for k, v in spec.items() if k != 'keywords'}
            return name, assumptions
    return 'general', dict(GENERAL_ARCHETYPE)


def _demand_multipliers(score: Any) -> tuple:
    """Growth and starting-revenue multipliers from the demand score.

    Score 5 is neutral (1.0x); 10 boosts growth 1.4x and revenue 1.3x;
    1 dampens to roughly 0.7x each. A missing score stays neutral.
    """
    if not isinstance(score, (int, float)) or not 1 <= score <= 10:
        return 1.0, 1.0, None
    growth_mult = 0.6 + (score / 10) * 0.8
    revenue_mult = 0.7 + (score / 10) * 0.6
    return growth_mult, revenue_mult, score


def _market_multiplier(market_size: Any) -> tuple:
    """Starting-revenue multiplier from the extracted market size text."""
    text = str(market_size or '').lower()
    if any(w in text for w in ('billion', 'large', 'high', 'significant', 'substantial')):
        return 1.3, 'large'
    if any(w in text for w in ('small', 'niche', 'limited')):
        return 0.75, 'small'
    if any(w in text for w in ('medium', 'moderate', 'million')):
        return 1.0, 'medium'
    return 1.0, 'unknown'


def _revenue_model_adjustments(revenue_model: Any) -> tuple:
    """LTV, churn, and variable-cost adjustments from the revenue model text."""
    text = str(revenue_model or '').lower()
    if any(w in text for w in ('subscription', 'recurring', 'saas', 'membership')):
        return {'ltv_mult': 1.5, 'churn_rate_pct': 2.0, 'variable_delta': 0.0}, 'recurring'
    if any(w in text for w in ('commission', 'per-order', 'per order', 'transaction', 'per acre', 'per unit', 'fee')):
        return {'ltv_mult': 0.75, 'churn_rate_pct': 4.0, 'variable_delta': 0.05}, 'transactional'
    if any(w in text for w in ('one-time', 'one time', 'sale of', 'selling')):
        return {'ltv_mult': 0.25, 'churn_rate_pct': 8.0, 'variable_delta': 0.0}, 'one-time'
    return {'ltv_mult': 1.0, 'churn_rate_pct': 3.0, 'variable_delta': 0.0}, 'unclassified'


def calculate_financial_projections(idea_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build idea-specific projections from fields the analysis already has.

    Deterministic: sector picks a cost-structure archetype, then the demand
    score, market size, and revenue model modulate it. The exact assumptions
    used and what drove them are attached to the output for transparency
    (rule 10). No LLM calls are made here.
    """
    extraction = idea_analysis.get('idea_extraction', {}) or {}
    demand = idea_analysis.get('demand_analysis', {}) or {}

    archetype_name, assumptions = _match_archetype(extraction.get('sector'))
    growth_mult, revenue_mult, demand_score = _demand_multipliers(demand.get('score'))
    market_mult, market_read = _market_multiplier(demand.get('market_size'))
    model_adj, model_read = _revenue_model_adjustments(extraction.get('revenue_model'))

    assumptions['monthly_growth_rate'] = round(assumptions['monthly_growth_rate'] * growth_mult, 4)
    assumptions['monthly_revenue_month_1'] = round(
        assumptions['monthly_revenue_month_1'] * revenue_mult * market_mult
    )
    assumptions['lifetime_value_months'] = max(2, round(assumptions['lifetime_value_months'] * model_adj['ltv_mult']))
    assumptions['variable_cost_percentage'] = min(0.85, assumptions['variable_cost_percentage'] + model_adj['variable_delta'])
    assumptions['churn_rate_pct'] = model_adj['churn_rate_pct']

    engine = FinancialProjections(assumptions)
    projections = engine.generate_projections()

    projections['assumptions_used'] = {
        'sector_archetype': archetype_name,
        'monthly_revenue_month_1': assumptions['monthly_revenue_month_1'],
        'monthly_growth_rate_pct': round(assumptions['monthly_growth_rate'] * 100, 2),
        'customer_acquisition_cost': assumptions['customer_acquisition_cost'],
        'lifetime_value_months': assumptions['lifetime_value_months'],
        'variable_cost_percentage': round(assumptions['variable_cost_percentage'], 2),
        'fixed_costs_monthly': assumptions['fixed_costs_monthly'],
        'initial_investment': assumptions['initial_investment'],
        'churn_rate_pct': assumptions['churn_rate_pct'],
        'drivers': {
            'sector': extraction.get('sector'),
            'demand_score': demand_score,
            'market_size_read': market_read,
            'revenue_model_read': model_read,
        },
        'note': 'Deterministic estimates from sector archetype adjusted by demand score, market size, and revenue model. Not sourced financial data.',
    }
    return projections
