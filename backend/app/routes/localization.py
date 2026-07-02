"""Localization & Expansion API Routes"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from app.services.localization import localization_service

router = APIRouter(prefix="/api/localization", tags=["Localization"])


@router.get("/languages")
async def get_supported_languages():
    """Get supported languages"""
    try:
        languages = localization_service.get_supported_languages()
        return {'success': True, 'languages': languages, 'count': len(languages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/regions")
async def get_supported_regions():
    """Get supported regions"""
    try:
        regions = localization_service.get_supported_regions()
        return {'success': True, 'regions': regions, 'count': len(regions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_localization_config(language: str = 'en', region: str = 'bd'):
    """Get localization configuration"""
    try:
        config = localization_service.get_localization_config(language, region)
        return {'success': True, 'config': config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/content/{content_type}")
async def get_localized_content(content_type: str, language: str = 'en', region: str = 'bd'):
    """Get localized content"""
    try:
        content = localization_service.get_localized_content(language, region, content_type)
        if not content:
            return {'success': False, 'message': 'Content not found'}
        return {'success': True, 'content': content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/regional-data/{region}")
async def get_regional_market_data(region: str):
    """Get regional market data"""
    try:
        data = localization_service.get_regional_market_data(region)
        if not data:
            return {'success': False, 'message': 'Region not found'}
        return {'success': True, 'data': data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/regional-data")
async def get_all_regional_data():
    """Get all regional market data"""
    try:
        data = localization_service.get_all_regional_data()
        return {'success': True, 'data': data, 'count': len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_localization_dashboard(language: str = 'en', region: str = 'bd'):
    """Get localization dashboard"""
    try:
        dashboard = localization_service.get_localization_dashboard(language, region)
        return {'success': True, 'dashboard': dashboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/variant/{region}")
async def get_market_variant(region: str):
    """Get market-specific variant"""
    try:
        variant = localization_service.get_market_variant(region)
        return {'success': True, 'variant': variant}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compliance/{region}")
async def get_localized_compliance(region: str):
    """Get localized compliance checklist"""
    try:
        compliance = localization_service.get_localized_compliance(region)
        return {'success': True, 'compliance': compliance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
