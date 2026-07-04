"""
Advanced Analytics - Health Score, Heatmaps, Custom Reports
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import random


@dataclass
class HealthScore:
    """Startup health score"""
    score_id: str
    overall_score: float  # 0-100
    financial_health: float
    market_health: float
    team_health: float
    product_health: float
    calculated_at: datetime
    trend: str  # up, down, stable


@dataclass
class AnalyticsReport:
    """Custom analytics report"""
    report_id: str
    name: str
    metrics: List[str]
    frequency: str  # once, daily, weekly, monthly
    recipients: List[str]
    format: str  # pdf, csv, json
    last_sent: Optional[datetime]


class AdvancedAnalyticsService:
    """Service for advanced analytics and reporting"""

    def __init__(self):
        self.health_scores: Dict[str, HealthScore] = {}
        self.reports: Dict[str, AnalyticsReport] = {}
        self.health_history: Dict[str, List[Dict]] = {}

    # ========== STARTUP HEALTH SCORE ==========

    def calculate_health_score(self, startup_id: str, metrics: Dict) -> HealthScore:
        """Calculate comprehensive startup health score"""
        score_id = f"score_{len(self.health_scores)}"

        # Calculate component scores from metrics
        financial_health = self._score_financial(metrics.get('financial', {}))
        market_health = self._score_market(metrics.get('market', {}))
        team_health = self._score_team(metrics.get('team', {}))
        product_health = self._score_product(metrics.get('product', {}))

        # Weighted overall score
        overall_score = (
            financial_health * 0.35 +
            market_health * 0.25 +
            team_health * 0.20 +
            product_health * 0.20
        )

        score = HealthScore(
            score_id=score_id,
            overall_score=round(overall_score, 1),
            financial_health=round(financial_health, 1),
            market_health=round(market_health, 1),
            team_health=round(team_health, 1),
            product_health=round(product_health, 1),
            calculated_at=datetime.utcnow(),
            trend=self._determine_trend(startup_id, overall_score)
        )

        self.health_scores[score_id] = score

        # Track history
        if startup_id not in self.health_history:
            self.health_history[startup_id] = []

        self.health_history[startup_id].append({
            'timestamp': score.calculated_at.isoformat(),
            'score': score.overall_score
        })

        return score

    def _score_financial(self, metrics: Dict) -> float:
        """Score financial health (0-100)"""
        score = 50  # baseline

        if metrics.get('runway_months', 0) > 18:
            score += 25
        elif metrics.get('runway_months', 0) > 12:
            score += 15
        elif metrics.get('runway_months', 0) > 6:
            score += 5

        if metrics.get('revenue_growth', 0) > 0.30:  # 30%+ monthly growth
            score += 15
        elif metrics.get('revenue_growth', 0) > 0.10:
            score += 10

        ltv_cac_ratio = metrics.get('ltv_cac_ratio', 0)
        if ltv_cac_ratio > 3:
            score += 10
        elif ltv_cac_ratio > 2:
            score += 5

        return min(100, score)

    def _score_market(self, metrics: Dict) -> float:
        """Score market health (0-100)"""
        score = 50

        market_size = metrics.get('market_size_billions', 0)
        if market_size > 5:
            score += 20
        elif market_size > 1:
            score += 10
        elif market_size > 0.1:
            score += 5

        growth_rate = metrics.get('market_growth_rate', 0)
        if growth_rate > 0.25:  # 25%+ growth
            score += 15
        elif growth_rate > 0.10:
            score += 10

        if metrics.get('market_position') == 'leader':
            score += 15
        elif metrics.get('market_position') == 'strong':
            score += 10

        return min(100, score)

    def _score_team(self, metrics: Dict) -> float:
        """Score team health (0-100)"""
        score = 50

        team_size = metrics.get('team_size', 0)
        if team_size > 10:
            score += 15
        elif team_size > 5:
            score += 10

        if metrics.get('has_experienced_founder'):
            score += 15

        if metrics.get('has_technical_lead'):
            score += 10

        if metrics.get('advisor_count', 0) > 3:
            score += 10

        return min(100, score)

    def _score_product(self, metrics: Dict) -> float:
        """Score product health (0-100)"""
        score = 50

        if metrics.get('product_market_fit'):
            score += 25

        user_retention = metrics.get('user_retention_rate', 0)
        if user_retention > 0.50:
            score += 15
        elif user_retention > 0.30:
            score += 10

        nps = metrics.get('nps_score', 0)
        if nps > 50:
            score += 10
        elif nps > 30:
            score += 5

        return min(100, score)

    def _determine_trend(self, startup_id: str, current_score: float) -> str:
        """Determine score trend"""
        if startup_id not in self.health_history or len(self.health_history[startup_id]) < 2:
            return 'stable'

        recent = self.health_history[startup_id][-1]['score']
        if current_score > recent + 5:
            return 'up'
        elif current_score < recent - 5:
            return 'down'
        return 'stable'

    def get_health_score(self, startup_id: str) -> Optional[Dict]:
        """Get current health score"""
        for score in self.health_scores.values():
            if score.calculated_at:
                return {
                    'id': score.score_id,
                    'overall': score.overall_score,
                    'financial': score.financial_health,
                    'market': score.market_health,
                    'team': score.team_health,
                    'product': score.product_health,
                    'trend': score.trend,
                    'warning_indicators': self._get_warnings(score),
                    'improvements': self._get_improvements(score)
                }
        return None

    def _get_warnings(self, score: HealthScore) -> List[str]:
        """Get warning indicators"""
        warnings = []

        if score.financial_health < 40:
            warnings.append('Low financial health - Runway may be tight')
        if score.market_health < 40:
            warnings.append('Market challenges - Competition or growth slowdown')
        if score.team_health < 40:
            warnings.append('Team concerns - Key hires or experience gaps')
        if score.product_health < 40:
            warnings.append('Product issues - Retention or PMF concerns')

        return warnings

    def _get_improvements(self, score: HealthScore) -> List[str]:
        """Get improvement opportunities"""
        improvements = []

        if score.financial_health < 70:
            improvements.append('Improve runway & burn rate management')
        if score.market_health < 70:
            improvements.append('Expand market share & competitive positioning')
        if score.team_health < 70:
            improvements.append('Strengthen team with key hires or advisors')
        if score.product_health < 70:
            improvements.append('Enhance product-market fit & user retention')

        return improvements

    def get_health_trend(self, startup_id: str, days: int = 90) -> List[Dict]:
        """Get health score trend over time"""
        if startup_id not in self.health_history:
            return []

        history = self.health_history[startup_id]
        cutoff = datetime.utcnow() - timedelta(days=days)

        return [
            {
                'date': item['timestamp'],
                'score': item['score']
            }
            for item in history
        ]

    # ========== CUSTOM REPORTS ==========

    def create_report(self, name: str, metrics: List[str], frequency: str,
                     recipients: List[str], format: str = 'pdf') -> AnalyticsReport:
        """Create custom report"""
        report_id = f"report_{len(self.reports)}"

        report = AnalyticsReport(
            report_id=report_id,
            name=name,
            metrics=metrics,
            frequency=frequency,
            recipients=recipients,
            format=format,
            last_sent=None
        )

        self.reports[report_id] = report
        return report

    def get_reports(self) -> List[Dict]:
        """Get all reports"""
        return [{
            'id': r.report_id,
            'name': r.name,
            'metrics': r.metrics,
            'frequency': r.frequency,
            'recipients': r.recipients,
            'format': r.format,
            'last_sent': r.last_sent.isoformat() if r.last_sent else None
        } for r in self.reports.values()]

    # ========== HEATMAPS & VISUALIZATIONS ==========

    def get_strength_weakness_heatmap(self, startup_id: str) -> Dict:
        """Get strength/weakness heatmap data"""
        return {
            'strengths': [
                {'area': 'Financial Planning', 'score': 85},
                {'area': 'Team Quality', 'score': 78},
                {'area': 'Product-Market Fit', 'score': 72}
            ],
            'weaknesses': [
                {'area': 'Market Reach', 'score': 45},
                {'area': 'Brand Awareness', 'score': 38},
                {'area': 'Competitive Differentiation', 'score': 52}
            ]
        }

    def get_market_opportunity_map(self) -> Dict:
        """Get market opportunity visualization"""
        return {
            'segments': [
                {'name': 'High Growth, High Competition', 'size': 35, 'growth': 0.35},
                {'name': 'High Growth, Low Competition', 'size': 25, 'growth': 0.45},
                {'name': 'Low Growth, High Competition', 'size': 30, 'growth': 0.05},
                {'name': 'Low Growth, Low Competition', 'size': 10, 'growth': 0.02}
            ]
        }

    # ========== DASHBOARD SUMMARY ==========

    def get_analytics_dashboard(self) -> Dict:
        """Get analytics dashboard summary"""
        return {
            'total_reports': len(self.reports),
            'total_scores_calculated': len(self.health_scores),
            'avg_startup_health': 65.5,
            'top_opportunities': [
                'Expand market reach',
                'Strengthen team',
                'Improve product retention'
            ]
        }


# Global analytics service instance
advanced_analytics_service = AdvancedAnalyticsService()
