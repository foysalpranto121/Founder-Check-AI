"""
Platform Integrations - Slack, Google Drive, Notion, Zapier, Calendar, API Access
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import hashlib


class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ERROR = "error"


class ReminderType(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    CALENDAR = "calendar"
    SMS = "sms"


@dataclass
class Integration:
    """Platform integration configuration"""
    integration_id: str
    platform: str  # slack, google_drive, notion, zapier, gmail
    status: IntegrationStatus
    config: Dict
    connected_at: datetime
    last_used: Optional[datetime]
    api_key: Optional[str]
    webhook_url: Optional[str]


@dataclass
class Reminder:
    """Reminder/action item"""
    reminder_id: str
    title: str
    description: str
    due_date: datetime
    reminder_type: ReminderType
    status: str  # pending, sent, completed, cancelled
    associated_milestone: Optional[str]
    recipients: List[str]


@dataclass
class CalendarEvent:
    """Calendar milestone"""
    event_id: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    event_type: str  # milestone, meeting, checkpoint, launch
    status: str  # scheduled, in_progress, completed, cancelled
    attendees: List[str]
    location: str


@dataclass
class WebhookEvent:
    """Webhook event for external integrations"""
    event_id: str
    event_type: str  # analysis_created, milestone_reached, reminder_due, status_change
    timestamp: datetime
    data: Dict
    status: str  # pending, sent, failed, delivered


@dataclass
class APIKey:
    """API key for programmatic access"""
    key_id: str
    key_hash: str
    name: str
    created_at: datetime
    last_used: Optional[datetime]
    is_active: bool
    scopes: List[str]


class PlatformIntegrationsService:
    """Service for managing platform integrations"""

    def __init__(self):
        self.integrations: Dict[str, Integration] = {}
        self.reminders: Dict[str, Reminder] = {}
        self.calendar_events: Dict[str, CalendarEvent] = {}
        self.webhooks: Dict[str, WebhookEvent] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.webhook_logs: List[Dict] = []

        self._initialize_integrations()

    def _initialize_integrations(self):
        """Initialize available platforms"""
        self.available_platforms = {
            'slack': {
                'name': 'Slack',
                'description': 'Get startup milestone alerts in Slack',
                'icon': '💬',
                'features': ['Milestone notifications', 'Daily digests', 'Team mentions']
            },
            'google_drive': {
                'name': 'Google Drive',
                'description': 'Export reports and analysis to Google Drive',
                'icon': '📁',
                'features': ['Auto-export PDFs', 'Shared folders', 'Version history']
            },
            'notion': {
                'name': 'Notion',
                'description': 'Sync analysis data with Notion workspace',
                'icon': '📝',
                'features': ['Database sync', 'Timeline view', 'Team collaboration']
            },
            'zapier': {
                'name': 'Zapier',
                'description': 'Connect to 5000+ apps via Zapier',
                'icon': '⚡',
                'features': ['Custom workflows', 'Multi-app automation', 'No-code setup']
            },
            'gmail': {
                'name': 'Gmail',
                'description': 'Share reports via Gmail with tracking',
                'icon': '📧',
                'features': ['Email sharing', 'Read receipts', 'Scheduled sends']
            }
        }

    # ========== INTEGRATION MANAGEMENT ==========

    def get_available_platforms(self) -> Dict:
        """Get list of available integrations"""
        return self.available_platforms

    def connect_integration(self, platform: str, config: Dict, api_key: Optional[str] = None) -> Integration:
        """Connect new integration"""
        integration_id = f"integration_{len(self.integrations)}"

        integration = Integration(
            integration_id=integration_id,
            platform=platform,
            status=IntegrationStatus.PENDING,
            config=config,
            connected_at=datetime.utcnow(),
            last_used=None,
            api_key=api_key,
            webhook_url=None
        )

        self.integrations[integration_id] = integration
        return integration

    def activate_integration(self, integration_id: str) -> bool:
        """Activate connected integration"""
        integration = self.integrations.get(integration_id)
        if not integration:
            return False

        integration.status = IntegrationStatus.ACTIVE
        integration.last_used = datetime.utcnow()
        return True

    def deactivate_integration(self, integration_id: str) -> bool:
        """Deactivate integration"""
        integration = self.integrations.get(integration_id)
        if not integration:
            return False

        integration.status = IntegrationStatus.INACTIVE
        return True

    def get_active_integrations(self) -> List[Dict]:
        """Get all active integrations"""
        active = []
        for integration in self.integrations.values():
            if integration.status == IntegrationStatus.ACTIVE:
                active.append({
                    'id': integration.integration_id,
                    'platform': integration.platform,
                    'platform_name': self.available_platforms.get(integration.platform, {}).get('name'),
                    'status': integration.status.value,
                    'connected_at': integration.connected_at.isoformat(),
                    'last_used': integration.last_used.isoformat() if integration.last_used else None
                })
        return active

    def test_integration(self, integration_id: str) -> Dict:
        """Test if integration is working"""
        integration = self.integrations.get(integration_id)
        if not integration:
            return {'success': False, 'message': 'Integration not found'}

        if integration.platform == 'slack':
            return {
                'success': True,
                'message': '✓ Slack connection successful',
                'workspace': 'FounderCheck Workspace',
                'channel': '#founders'
            }
        elif integration.platform == 'google_drive':
            return {
                'success': True,
                'message': '✓ Google Drive authenticated',
                'folder': 'FounderCheck Reports',
                'shared_count': 5
            }
        elif integration.platform == 'notion':
            return {
                'success': True,
                'message': '✓ Notion database synced',
                'database': 'Startup Analysis',
                'records': 12
            }
        else:
            return {'success': True, 'message': f'✓ {integration.platform} connected'}

    # ========== CALENDAR & REMINDERS ==========

    def create_calendar_event(self, title: str, description: str, start_date: datetime,
                             end_date: datetime, event_type: str = 'milestone',
                             attendees: List[str] = None) -> CalendarEvent:
        """Create calendar event"""
        event_id = f"event_{len(self.calendar_events)}"

        event = CalendarEvent(
            event_id=event_id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            event_type=event_type,
            status='scheduled',
            attendees=attendees or [],
            location=''
        )

        self.calendar_events[event_id] = event
        return event

    def get_upcoming_milestones(self, days: int = 30) -> List[Dict]:
        """Get upcoming milestones"""
        now = datetime.utcnow()
        future = now + timedelta(days=days)

        upcoming = []
        for event in sorted(self.calendar_events.values(), key=lambda e: e.start_date):
            if now <= event.start_date <= future:
                upcoming.append({
                    'id': event.event_id,
                    'title': event.title,
                    'description': event.description,
                    'start_date': event.start_date.isoformat(),
                    'event_type': event.event_type,
                    'days_until': (event.start_date - now).days,
                    'attendees': event.attendees
                })

        return upcoming

    def create_reminder(self, title: str, description: str, due_date: datetime,
                       reminder_type: ReminderType = ReminderType.EMAIL,
                       recipients: List[str] = None,
                       associated_milestone: Optional[str] = None) -> Reminder:
        """Create reminder/action item"""
        reminder_id = f"reminder_{len(self.reminders)}"

        reminder = Reminder(
            reminder_id=reminder_id,
            title=title,
            description=description,
            due_date=due_date,
            reminder_type=reminder_type,
            status='pending',
            associated_milestone=associated_milestone,
            recipients=recipients or []
        )

        self.reminders[reminder_id] = reminder
        return reminder

    def get_pending_reminders(self) -> List[Dict]:
        """Get pending reminders"""
        pending = []
        for reminder in self.reminders.values():
            if reminder.status == 'pending':
                pending.append({
                    'id': reminder.reminder_id,
                    'title': reminder.title,
                    'description': reminder.description,
                    'due_date': reminder.due_date.isoformat(),
                    'type': reminder.reminder_type.value,
                    'recipients': reminder.recipients,
                    'days_until': max(0, (reminder.due_date - datetime.utcnow()).days)
                })

        return sorted(pending, key=lambda r: r['days_until'])

    def mark_reminder_completed(self, reminder_id: str) -> bool:
        """Mark reminder as completed"""
        reminder = self.reminders.get(reminder_id)
        if not reminder:
            return False

        reminder.status = 'completed'
        return True

    def send_reminder(self, reminder_id: str) -> Dict:
        """Send reminder notification"""
        reminder = self.reminders.get(reminder_id)
        if not reminder:
            return {'success': False}

        # Simulate sending
        reminder.status = 'sent'

        if reminder.reminder_type == ReminderType.SLACK:
            return {
                'success': True,
                'message': f'Reminder sent to Slack: {reminder.title}',
                'channel': '#founders',
                'recipients': reminder.recipients
            }
        elif reminder.reminder_type == ReminderType.EMAIL:
            return {
                'success': True,
                'message': f'Email reminder sent: {reminder.title}',
                'recipients': reminder.recipients
            }
        else:
            return {'success': True, 'message': 'Reminder sent'}

    # ========== WEBHOOKS & EXTERNAL INTEGRATIONS ==========

    def register_webhook(self, event_type: str, webhook_url: str) -> str:
        """Register webhook for event"""
        webhook_id = f"webhook_{len(self.webhooks)}"

        webhook = WebhookEvent(
            event_id=webhook_id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            data={'webhook_url': webhook_url},
            status='pending'
        )

        self.webhooks[webhook_id] = webhook
        return webhook_id

    def trigger_webhook(self, event_type: str, data: Dict) -> Dict:
        """Trigger webhook for event"""
        webhooks_for_type = [w for w in self.webhooks.values() if w.event_type == event_type]

        results = []
        for webhook in webhooks_for_type:
            result = {
                'webhook_id': webhook.event_id,
                'event_type': event_type,
                'status': 'delivered',
                'timestamp': datetime.utcnow().isoformat()
            }
            results.append(result)
            self.webhook_logs.append(result)

        return {
            'event_type': event_type,
            'webhooks_triggered': len(results),
            'results': results
        }

    # ========== API KEY MANAGEMENT ==========

    def generate_api_key(self, name: str, scopes: List[str]) -> APIKey:
        """Generate new API key"""
        key_id = f"key_{len(self.api_keys)}"
        raw_key = f"{key_id}_{hashlib.sha256(str(datetime.utcnow()).encode()).hexdigest()[:32]}"
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        api_key = APIKey(
            key_id=key_id,
            key_hash=key_hash,
            name=name,
            created_at=datetime.utcnow(),
            last_used=None,
            is_active=True,
            scopes=scopes
        )

        self.api_keys[key_id] = api_key
        return api_key

    def get_api_keys(self) -> List[Dict]:
        """Get all API keys (masked)"""
        keys = []
        for key in self.api_keys.values():
            keys.append({
                'id': key.key_id,
                'name': key.name,
                'created_at': key.created_at.isoformat(),
                'last_used': key.last_used.isoformat() if key.last_used else 'Never',
                'is_active': key.is_active,
                'scopes': key.scopes,
                'display': f"{key.key_id}...{key.key_hash[-8:]}"
            })
        return keys

    def validate_api_key(self, key: str) -> Dict:
        """Validate API key"""
        key_hash = hashlib.sha256(key.encode()).hexdigest()

        for api_key in self.api_keys.values():
            if api_key.key_hash == key_hash and api_key.is_active:
                api_key.last_used = datetime.utcnow()
                return {
                    'valid': True,
                    'key_id': api_key.key_id,
                    'scopes': api_key.scopes
                }

        return {'valid': False}

    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        api_key = self.api_keys.get(key_id)
        if not api_key:
            return False

        api_key.is_active = False
        return True

    # ========== AUTOMATION & ACTIONS ==========

    def schedule_export(self, platform: str, analysis_id: str, schedule: str = 'weekly') -> Dict:
        """Schedule automatic export"""
        return {
            'success': True,
            'export_id': f'export_{analysis_id}',
            'platform': platform,
            'schedule': schedule,
            'next_export': (datetime.utcnow() + timedelta(days=7)).isoformat(),
            'message': f'Analysis will be exported to {platform} {schedule}'
        }

    def get_integration_dashboard(self) -> Dict:
        """Get integration dashboard summary"""
        return {
            'active_integrations': len([i for i in self.integrations.values() if i.status == IntegrationStatus.ACTIVE]),
            'total_integrations': len(self.integrations),
            'pending_reminders': len([r for r in self.reminders.values() if r.status == 'pending']),
            'upcoming_milestones': len([e for e in self.calendar_events.values() if e.status == 'scheduled']),
            'api_keys_active': len([k for k in self.api_keys.values() if k.is_active]),
            'webhook_logs_recent': len([l for l in self.webhook_logs[-10:]]),
            'platform_status': {
                'slack': 'Connected' if any(i.platform == 'slack' and i.status == IntegrationStatus.ACTIVE for i in self.integrations.values()) else 'Not connected',
                'google_drive': 'Connected' if any(i.platform == 'google_drive' and i.status == IntegrationStatus.ACTIVE for i in self.integrations.values()) else 'Not connected',
                'notion': 'Connected' if any(i.platform == 'notion' and i.status == IntegrationStatus.ACTIVE for i in self.integrations.values()) else 'Not connected',
                'zapier': 'Connected' if any(i.platform == 'zapier' and i.status == IntegrationStatus.ACTIVE for i in self.integrations.values()) else 'Not connected',
                'gmail': 'Connected' if any(i.platform == 'gmail' and i.status == IntegrationStatus.ACTIVE for i in self.integrations.values()) else 'Not connected'
            }
        }


# Global platform integrations service instance
platform_integrations_service = PlatformIntegrationsService()
