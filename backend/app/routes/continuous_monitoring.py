"""Continuous Monitoring API Routes"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from datetime import datetime
from app.services.continuous_monitoring import continuous_monitoring_service

router = APIRouter(prefix="/api/monitoring", tags=["Continuous Monitoring"])


@router.post("/milestones/add")
async def add_milestone(name: str, description: str, target_date: str,
                       status: str = "not_started", progress: int = 0, category: str = "General"):
    """Add milestone"""
    try:
        target = datetime.fromisoformat(target_date)
        milestone = continuous_monitoring_service.add_milestone(name, description, target, status, progress, category)
        return {'success': True, 'milestone': {
            'id': milestone.milestone_id,
            'name': milestone.name,
            'status': milestone.status.value
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/milestones")
async def get_milestones(status: Optional[str] = None):
    """Get milestones"""
    try:
        milestones = continuous_monitoring_service.get_milestones(status)
        return {'success': True, 'milestones': milestones, 'count': len(milestones)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/milestones/summary")
async def get_milestone_summary():
    """Get milestone summary"""
    try:
        summary = continuous_monitoring_service.get_milestone_summary()
        return {'success': True, 'summary': summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/milestones/{milestone_id}/progress")
async def update_milestone_progress(milestone_id: str, progress: int):
    """Update milestone progress"""
    try:
        success = continuous_monitoring_service.update_milestone_progress(milestone_id, progress)
        return {'success': success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/create")
async def create_alert(alert_type: str, title: str, description: str,
                      data: Dict, priority: str = "medium"):
    """Create alert"""
    try:
        alert = continuous_monitoring_service.create_alert(alert_type, title, description, data, priority)
        return {'success': True, 'alert': {
            'id': alert.alert_id,
            'type': alert.type.value,
            'priority': alert.priority
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_alerts(limit: int = 20, alert_type: Optional[str] = None):
    """Get alerts"""
    try:
        alerts = continuous_monitoring_service.get_alerts(limit, alert_type)
        return {'success': True, 'alerts': alerts, 'count': len(alerts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: str):
    """Mark alert as read"""
    try:
        success = continuous_monitoring_service.mark_alert_read(alert_id)
        return {'success': success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/news/add")
async def add_news(title: str, summary: str, source: str, category: str, relevance_score: float):
    """Add industry news"""
    try:
        news = continuous_monitoring_service.add_industry_news(title, summary, source, category, relevance_score)
        return {'success': True, 'news': {'id': news.news_id, 'title': news.title}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news")
async def get_industry_news(limit: int = 15, category: Optional[str] = None):
    """Get industry news"""
    try:
        news = continuous_monitoring_service.get_industry_news(limit, category)
        return {'success': True, 'news': news, 'count': len(news)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trends/add")
async def add_trend(name: str, category: str, current_value: float, previous_value: float):
    """Add trend"""
    try:
        trend = continuous_monitoring_service.add_trend(name, category, current_value, previous_value)
        return {'success': True, 'trend': {
            'id': trend.trend_id,
            'name': trend.name,
            'direction': trend.direction
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
async def get_trends(category: Optional[str] = None):
    """Get trends"""
    try:
        trends = continuous_monitoring_service.get_trends(category)
        return {'success': True, 'trends': trends, 'count': len(trends)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights/daily")
async def get_daily_insights():
    """Get daily insights"""
    try:
        insights = continuous_monitoring_service.generate_daily_insights()
        return {'success': True, 'insights': insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pivot-detection")
async def detect_pivot_signals(startup_data: Dict):
    """Detect pivot signals"""
    try:
        result = continuous_monitoring_service.detect_pivot_signals(startup_data)
        return {'success': True, 'analysis': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/{startup_id}")
async def get_monitoring_dashboard(startup_id: str):
    """Get monitoring dashboard"""
    try:
        dashboard = continuous_monitoring_service.get_monitoring_dashboard(startup_id)
        return {'success': True, 'dashboard': dashboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
