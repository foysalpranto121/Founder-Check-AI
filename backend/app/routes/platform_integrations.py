"""
Platform Integrations API Routes
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
from datetime import datetime, timedelta
from app.services.platform_integrations import (
    platform_integrations_service,
    ReminderType,
    IntegrationStatus
)

router = APIRouter(prefix="/api/integrations", tags=["Platform Integrations"])


# ========== INTEGRATION MARKETPLACE ==========

@router.get("/platforms")
async def get_available_platforms():
    """Get available integration platforms"""
    try:
        platforms = platform_integrations_service.get_available_platforms()
        return {
            'success': True,
            'platforms': platforms,
            'count': len(platforms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/connect")
async def connect_integration(platform: str, config: Dict = None, api_key: str = None):
    """Connect new integration"""
    try:
        if platform not in platform_integrations_service.get_available_platforms():
            raise HTTPException(status_code=400, detail="Platform not supported")

        integration = platform_integrations_service.connect_integration(
            platform=platform,
            config=config or {},
            api_key=api_key
        )

        return {
            'success': True,
            'integration': {
                'id': integration.integration_id,
                'platform': platform,
                'status': integration.status.value,
                'message': f'Pending authorization for {platform}. Check your {platform} account.'
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/activate/{integration_id}")
async def activate_integration(integration_id: str):
    """Activate integration"""
    try:
        success = platform_integrations_service.activate_integration(integration_id)
        if not success:
            raise HTTPException(status_code=404, detail="Integration not found")

        return {
            'success': True,
            'message': 'Integration activated successfully',
            'integration_id': integration_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deactivate/{integration_id}")
async def deactivate_integration(integration_id: str):
    """Deactivate integration"""
    try:
        success = platform_integrations_service.deactivate_integration(integration_id)
        if not success:
            raise HTTPException(status_code=404, detail="Integration not found")

        return {
            'success': True,
            'message': 'Integration deactivated',
            'integration_id': integration_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active")
async def get_active_integrations():
    """Get all active integrations"""
    try:
        integrations = platform_integrations_service.get_active_integrations()
        return {
            'success': True,
            'integrations': integrations,
            'count': len(integrations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/{integration_id}")
async def test_integration(integration_id: str):
    """Test integration connection"""
    try:
        result = platform_integrations_service.test_integration(integration_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== CALENDAR & MILESTONES ==========

@router.post("/calendar/event")
async def create_calendar_event(
    title: str,
    description: str,
    start_date: str,
    end_date: str,
    event_type: str = 'milestone',
    attendees: List[str] = None
):
    """Create calendar event/milestone"""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)

        event = platform_integrations_service.create_calendar_event(
            title=title,
            description=description,
            start_date=start,
            end_date=end,
            event_type=event_type,
            attendees=attendees or []
        )

        return {
            'success': True,
            'event': {
                'id': event.event_id,
                'title': event.title,
                'start_date': event.start_date.isoformat(),
                'end_date': event.end_date.isoformat(),
                'type': event.event_type
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/milestones")
async def get_upcoming_milestones(days: int = 30):
    """Get upcoming milestones"""
    try:
        milestones = platform_integrations_service.get_upcoming_milestones(days)
        return {
            'success': True,
            'milestones': milestones,
            'count': len(milestones),
            'timeframe_days': days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== REMINDERS & ACTION ITEMS ==========

@router.post("/reminders/create")
async def create_reminder(
    title: str,
    description: str,
    due_date: str,
    reminder_type: str = 'email',
    recipients: List[str] = None
):
    """Create reminder/action item"""
    try:
        due = datetime.fromisoformat(due_date)
        reminder_enum = ReminderType(reminder_type)

        reminder = platform_integrations_service.create_reminder(
            title=title,
            description=description,
            due_date=due,
            reminder_type=reminder_enum,
            recipients=recipients or []
        )

        return {
            'success': True,
            'reminder': {
                'id': reminder.reminder_id,
                'title': reminder.title,
                'due_date': reminder.due_date.isoformat(),
                'type': reminder.reminder_type.value,
                'status': reminder.status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reminders/pending")
async def get_pending_reminders():
    """Get all pending reminders"""
    try:
        reminders = platform_integrations_service.get_pending_reminders()
        return {
            'success': True,
            'reminders': reminders,
            'count': len(reminders)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reminders/{reminder_id}/send")
async def send_reminder(reminder_id: str):
    """Send reminder notification"""
    try:
        result = platform_integrations_service.send_reminder(reminder_id)
        if not result.get('success'):
            raise HTTPException(status_code=404, detail="Reminder not found")

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reminders/{reminder_id}/complete")
async def complete_reminder(reminder_id: str):
    """Mark reminder as completed"""
    try:
        success = platform_integrations_service.mark_reminder_completed(reminder_id)
        if not success:
            raise HTTPException(status_code=404, detail="Reminder not found")

        return {
            'success': True,
            'message': 'Reminder marked as completed',
            'reminder_id': reminder_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== WEBHOOKS & AUTOMATION ==========

@router.post("/webhooks/register")
async def register_webhook(event_type: str, webhook_url: str):
    """Register webhook for events"""
    try:
        webhook_id = platform_integrations_service.register_webhook(
            event_type=event_type,
            webhook_url=webhook_url
        )

        return {
            'success': True,
            'webhook_id': webhook_id,
            'event_type': event_type,
            'webhook_url': webhook_url,
            'message': 'Webhook registered successfully'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhooks/trigger")
async def trigger_webhook(event_type: str, data: Dict = None):
    """Trigger webhook event (admin only)"""
    try:
        result = platform_integrations_service.trigger_webhook(
            event_type=event_type,
            data=data or {}
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== API KEY MANAGEMENT ==========

@router.post("/api-keys/generate")
async def generate_api_key(name: str, scopes: List[str] = None):
    """Generate new API key"""
    try:
        scopes = scopes or ['read:analyses', 'read:market', 'read:financial']

        api_key = platform_integrations_service.generate_api_key(
            name=name,
            scopes=scopes
        )

        return {
            'success': True,
            'key': f"{api_key.key_id}_{api_key.key_hash[:16]}...",
            'key_id': api_key.key_id,
            'name': api_key.name,
            'scopes': api_key.scopes,
            'message': 'Save your API key - you won\'t see it again!'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api-keys")
async def get_api_keys():
    """Get all API keys (masked)"""
    try:
        keys = platform_integrations_service.get_api_keys()
        return {
            'success': True,
            'keys': keys,
            'count': len(keys)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api-keys/{key_id}/revoke")
async def revoke_api_key(key_id: str):
    """Revoke API key"""
    try:
        success = platform_integrations_service.revoke_api_key(key_id)
        if not success:
            raise HTTPException(status_code=404, detail="API key not found")

        return {
            'success': True,
            'message': 'API key revoked',
            'key_id': key_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api-keys/validate")
async def validate_api_key(key: str):
    """Validate API key (for external services)"""
    try:
        result = platform_integrations_service.validate_api_key(key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== AUTOMATION & EXPORTS ==========

@router.post("/exports/schedule")
async def schedule_export(
    platform: str,
    analysis_id: str,
    schedule: str = 'weekly'
):
    """Schedule automatic export"""
    try:
        result = platform_integrations_service.schedule_export(
            platform=platform,
            analysis_id=analysis_id,
            schedule=schedule
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== DASHBOARD & SUMMARY ==========

@router.get("/dashboard")
async def get_integration_dashboard():
    """Get integration dashboard summary"""
    try:
        dashboard = platform_integrations_service.get_integration_dashboard()
        return {
            'success': True,
            'dashboard': dashboard
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
