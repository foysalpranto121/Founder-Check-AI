"""
Continuous Monitoring - Live updates, milestones, industry news, trend alerts
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


class MilestoneStatus(str, Enum):
    """Milestone status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"


class AlertType(str, Enum):
    """Alert types"""
    MARKET_TREND = "market_trend"
    COMPETITOR = "competitor"
    FUNDING = "funding"
    INDUSTRY_NEWS = "industry_news"
    MILESTONE = "milestone"
    PIVOT_DETECTION = "pivot_detection"


@dataclass
class Milestone:
    """Startup milestone"""
    milestone_id: str
    name: str
    description: str
    target_date: datetime
    status: MilestoneStatus
    progress: int  # 0-100
    category: str  # MVP, Funding, Team, Revenue, etc.
    completed_date: Optional[datetime] = None


@dataclass
class LiveAlert:
    """Live alert/notification"""
    alert_id: str
    type: AlertType
    title: str
    description: str
    data: Dict
    created_at: datetime
    read: bool = False
    priority: str = "medium"  # low, medium, high, critical


@dataclass
class IndustryNews:
    """Industry news item"""
    news_id: str
    title: str
    summary: str
    source: str
    category: str
    published_at: datetime
    relevance_score: float  # 0-1


@dataclass
class TrendAnalysis:
    """Trend analysis"""
    trend_id: str
    name: str
    category: str
    current_value: float
    previous_value: float
    direction: str  # up, down, stable
    momentum: str  # accelerating, stable, decelerating


class ContinuousMonitoringService:
    """Service for continuous monitoring and live updates"""

    def __init__(self):
        self.milestones: Dict[str, Milestone] = {}
        self.alerts: Dict[str, LiveAlert] = {}
        self.news_items: Dict[str, IndustryNews] = {}
        self.trends: Dict[str, TrendAnalysis] = {}
        self.milestone_count = 0
        self.alert_count = 0
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Initialize sample milestones and data"""
        # Add sample milestones
        sample_milestones = [
            ("MVP Launch", "Launch minimum viable product", "2024-04-15", "completed"),
            ("First 1000 Users", "Reach 1000 active users", "2024-06-30", "in_progress"),
            ("Series A Fundraising", "Raise $1M in Series A", "2024-09-30", "not_started"),
            ("Team Expansion", "Hire 5 core team members", "2024-05-31", "in_progress"),
            ("Market Expansion", "Enter Pakistan market", "2024-08-31", "not_started")
        ]

        for name, desc, date_str, status in sample_milestones:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            progress = 100 if status == "completed" else (60 if status == "in_progress" else 0)
            self.add_milestone(name, desc, target_date, status, progress)

    # ========== MILESTONE MANAGEMENT ==========

    def add_milestone(self, name: str, description: str, target_date: datetime,
                     status: str, progress: int = 0, category: str = "General") -> Milestone:
        """Add milestone"""
        self.milestone_count += 1
        milestone_id = f"milestone_{self.milestone_count}"

        milestone = Milestone(
            milestone_id=milestone_id,
            name=name,
            description=description,
            target_date=target_date,
            status=MilestoneStatus(status),
            progress=progress,
            category=category,
            completed_date=datetime.utcnow() if status == "completed" else None
        )

        self.milestones[milestone_id] = milestone
        return milestone

    def update_milestone_progress(self, milestone_id: str, progress: int) -> bool:
        """Update milestone progress"""
        if milestone_id in self.milestones:
            self.milestones[milestone_id].progress = min(100, progress)
            if progress >= 100:
                self.milestones[milestone_id].status = MilestoneStatus.COMPLETED
                self.milestones[milestone_id].completed_date = datetime.utcnow()
            return True
        return False

    def get_milestones(self, status: Optional[str] = None) -> List[Dict]:
        """Get milestones, optionally filtered by status"""
        milestones = list(self.milestones.values())
        if status:
            milestones = [m for m in milestones if m.status.value == status]

        milestones.sort(key=lambda x: x.target_date)

        return [{
            'id': m.milestone_id,
            'name': m.name,
            'description': m.description,
            'target_date': m.target_date.isoformat(),
            'status': m.status.value,
            'progress': m.progress,
            'category': m.category,
            'completed_date': m.completed_date.isoformat() if m.completed_date else None
        } for m in milestones]

    def get_milestone_summary(self) -> Dict:
        """Get milestone summary"""
        total = len(self.milestones)
        completed = len([m for m in self.milestones.values() if m.status == MilestoneStatus.COMPLETED])
        in_progress = len([m for m in self.milestones.values() if m.status == MilestoneStatus.IN_PROGRESS])
        delayed = len([m for m in self.milestones.values() if m.status == MilestoneStatus.DELAYED])

        avg_progress = sum(m.progress for m in self.milestones.values()) / total if total > 0 else 0

        return {
            'total_milestones': total,
            'completed': completed,
            'in_progress': in_progress,
            'delayed': delayed,
            'not_started': total - completed - in_progress - delayed,
            'overall_progress': round(avg_progress, 1),
            'completion_rate': round((completed / total * 100), 1) if total > 0 else 0
        }

    # ========== ALERT & NEWS MANAGEMENT ==========

    def create_alert(self, alert_type: str, title: str, description: str,
                    data: Dict, priority: str = "medium") -> LiveAlert:
        """Create live alert"""
        self.alert_count += 1
        alert_id = f"alert_{self.alert_count}"

        alert = LiveAlert(
            alert_id=alert_id,
            type=AlertType(alert_type),
            title=title,
            description=description,
            data=data,
            created_at=datetime.utcnow(),
            priority=priority
        )

        self.alerts[alert_id] = alert
        return alert

    def get_alerts(self, limit: int = 20, alert_type: Optional[str] = None) -> List[Dict]:
        """Get alerts"""
        alerts = list(self.alerts.values())
        if alert_type:
            alerts = [a for a in alerts if a.type.value == alert_type]

        # Sort by priority and recency
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        alerts.sort(key=lambda x: (priority_order.get(x.priority, 4), -x.created_at.timestamp()))

        return [{
            'id': a.alert_id,
            'type': a.type.value,
            'title': a.title,
            'description': a.description,
            'priority': a.priority,
            'created_at': a.created_at.isoformat(),
            'read': a.read
        } for a in alerts[:limit]]

    def mark_alert_read(self, alert_id: str) -> bool:
        """Mark alert as read"""
        if alert_id in self.alerts:
            self.alerts[alert_id].read = True
            return True
        return False

    def add_industry_news(self, title: str, summary: str, source: str,
                         category: str, relevance_score: float) -> IndustryNews:
        """Add industry news"""
        news_id = f"news_{len(self.news_items)}"

        news = IndustryNews(
            news_id=news_id,
            title=title,
            summary=summary,
            source=source,
            category=category,
            published_at=datetime.utcnow(),
            relevance_score=min(1.0, relevance_score)
        )

        self.news_items[news_id] = news
        return news

    def get_industry_news(self, limit: int = 15, category: Optional[str] = None) -> List[Dict]:
        """Get industry news"""
        news = list(self.news_items.values())
        if category:
            news = [n for n in news if n.category.lower() == category.lower()]

        # Sort by relevance and recency
        news.sort(key=lambda x: (-x.relevance_score, -x.published_at.timestamp()))

        return [{
            'id': n.news_id,
            'title': n.title,
            'summary': n.summary,
            'source': n.source,
            'category': n.category,
            'relevance': round(n.relevance_score * 100),
            'published_at': n.published_at.isoformat()
        } for n in news[:limit]]

    # ========== TREND ANALYSIS ==========

    def add_trend(self, name: str, category: str, current_value: float,
                 previous_value: float) -> TrendAnalysis:
        """Add trend analysis"""
        trend_id = f"trend_{len(self.trends)}"

        # Determine direction
        if current_value > previous_value:
            direction = "up"
        elif current_value < previous_value:
            direction = "down"
        else:
            direction = "stable"

        # Determine momentum
        change_rate = abs(current_value - previous_value) / (previous_value or 1)
        if change_rate > 0.15:
            momentum = "accelerating"
        elif change_rate < 0.05:
            momentum = "decelerating"
        else:
            momentum = "stable"

        trend = TrendAnalysis(
            trend_id=trend_id,
            name=name,
            category=category,
            current_value=current_value,
            previous_value=previous_value,
            direction=direction,
            momentum=momentum
        )

        self.trends[trend_id] = trend
        return trend

    def get_trends(self, category: Optional[str] = None) -> List[Dict]:
        """Get trends"""
        trends = list(self.trends.values())
        if category:
            trends = [t for t in trends if t.category.lower() == category.lower()]

        return [{
            'id': t.trend_id,
            'name': t.name,
            'category': t.category,
            'current': t.current_value,
            'previous': t.previous_value,
            'direction': t.direction,
            'momentum': t.momentum,
            'change_percent': round(((t.current_value - t.previous_value) / (t.previous_value or 1)) * 100, 1)
        } for t in trends]

    # ========== DAILY INSIGHTS & MONITORING ==========

    def generate_daily_insights(self) -> Dict:
        """Generate daily insights"""
        return {
            'date': datetime.utcnow().isoformat(),
            'market_insights': [
                {'title': 'EdTech market growing 35% YoY', 'impact': 'positive'},
                {'title': 'Regulatory uncertainty in FinTech', 'impact': 'negative'},
                {'title': 'Mobile adoption at 65% in Bangladesh', 'impact': 'positive'}
            ],
            'competitor_moves': [
                'Competitor A launched new AI feature',
                'Competitor B raised Series B funding',
                'Competitor C expanded to Pakistan'
            ],
            'funding_updates': [
                {'company': 'TechBD', 'amount': '$5M', 'round': 'Series A'},
                {'company': 'StartupX', 'amount': '$2M', 'round': 'Seed'}
            ],
            'trending_sectors': ['AI/ML', 'HealthTech', 'FinTech'],
            'opportunities': 3,
            'threats': 2
        }

    def detect_pivot_signals(self, startup_data: Dict) -> Dict:
        """Detect potential pivot signals"""
        signals = []
        confidence = 0.0

        # Analyze retention
        if startup_data.get('retention', 0) < 0.30:
            signals.append('Low user retention (< 30%)')
            confidence += 0.3

        # Analyze revenue growth
        if startup_data.get('revenue_growth', 0) < 0.05:
            signals.append('Slow revenue growth (< 5% monthly)')
            confidence += 0.3

        # Analyze market feedback
        if startup_data.get('nps', 0) < 20:
            signals.append('Poor NPS score (< 20)')
            confidence += 0.2

        # Analyze team satisfaction
        if startup_data.get('team_churn', 0) > 0.3:
            signals.append('High team turnover (> 30%)')
            confidence += 0.2

        return {
            'pivot_likely': confidence > 0.5,
            'confidence': round(confidence, 2),
            'signals': signals,
            'recommendation': 'Consider strategic pivot' if confidence > 0.5 else 'Continue current strategy',
            'areas_to_investigate': [
                'Customer feedback & NPS trends',
                'Retention metrics by cohort',
                'Competitive positioning',
                'Market fit indicators'
            ]
        }

    def get_monitoring_dashboard(self, startup_id: str) -> Dict:
        """Get continuous monitoring dashboard"""
        return {
            'startup_id': startup_id,
            'timestamp': datetime.utcnow().isoformat(),
            'milestones': {
                'summary': self.get_milestone_summary(),
                'upcoming': self.get_milestones(status='not_started')[:3],
                'in_progress': self.get_milestones(status='in_progress')
            },
            'alerts': {
                'recent': self.get_alerts(limit=10),
                'unread_count': len([a for a in self.alerts.values() if not a.read]),
                'critical_count': len([a for a in self.alerts.values() if a.priority == 'critical'])
            },
            'news': {
                'latest': self.get_industry_news(limit=8),
                'trending_categories': ['FinTech', 'EdTech', 'HealthTech']
            },
            'trends': self.get_trends(),
            'daily_insights': self.generate_daily_insights(),
            'health_check': {
                'system_status': 'operational',
                'last_update': datetime.utcnow().isoformat(),
                'data_freshness': 'current',
                'alerts_status': 'monitoring'
            }
        }


# Global monitoring service instance
continuous_monitoring_service = ContinuousMonitoringService()
