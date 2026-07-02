"""Advanced Analytics API Routes"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from app.services.advanced_analytics import advanced_analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Advanced Analytics"])


@router.post("/health-score")
async def calculate_health_score(startup_id: str, metrics: Dict):
    """Calculate startup health score"""
    try:
        score = advanced_analytics_service.calculate_health_score(startup_id, metrics)
        return {'success': True, 'score': {
            'id': score.score_id,
            'overall': score.overall_score,
            'financial': score.financial_health,
            'market': score.market_health,
            'team': score.team_health,
            'product': score.product_health,
            'trend': score.trend
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health-score/{startup_id}")
async def get_health_score(startup_id: str):
    """Get current health score"""
    try:
        score = advanced_analytics_service.get_health_score(startup_id)
        if not score:
            return {'success': False, 'message': 'No scores calculated'}
        return {'success': True, 'score': score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health-trend/{startup_id}")
async def get_health_trend(startup_id: str, days: int = 90):
    """Get health score trend"""
    try:
        trend = advanced_analytics_service.get_health_trend(startup_id, days)
        return {'success': True, 'trend': trend}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reports/create")
async def create_report(name: str, metrics: List[str], frequency: str,
                       recipients: List[str], format: str = 'pdf'):
    """Create custom report"""
    try:
        report = advanced_analytics_service.create_report(name, metrics, frequency, recipients, format)
        return {'success': True, 'report': {'id': report.report_id, 'name': report.name}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports")
async def get_reports():
    """Get all reports"""
    try:
        reports = advanced_analytics_service.get_reports()
        return {'success': True, 'reports': reports, 'count': len(reports)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heatmap/strength-weakness")
async def get_strength_weakness_heatmap(startup_id: str):
    """Get strength/weakness heatmap"""
    try:
        heatmap = advanced_analytics_service.get_strength_weakness_heatmap(startup_id)
        return {'success': True, 'heatmap': heatmap}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heatmap/market-opportunity")
async def get_market_opportunity():
    """Get market opportunity map"""
    try:
        opp_map = advanced_analytics_service.get_market_opportunity_map()
        return {'success': True, 'map': opp_map}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_analytics_dashboard():
    """Get analytics dashboard"""
    try:
        dashboard = advanced_analytics_service.get_analytics_dashboard()
        return {'success': True, 'dashboard': dashboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
