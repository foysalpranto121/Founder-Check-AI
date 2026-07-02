"""
Collaboration Models - Team, Users, Comments, Sharing
"""

from datetime import datetime
from typing import List, Optional
from enum import Enum

class UserRole(str, Enum):
    """User roles in the platform"""
    FOUNDER = "founder"
    ADVISOR = "advisor"
    INVESTOR = "investor"
    MENTOR = "mentor"
    ANALYST = "analyst"
    ADMIN = "admin"


class AccessLevel(str, Enum):
    """Access levels for shared analysis"""
    VIEW = "view"
    COMMENT = "comment"
    EDIT = "edit"
    ADMIN = "admin"


class User:
    """User representation"""
    def __init__(self, user_id: str, name: str, email: str, role: UserRole, profile_data: dict = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.profile_data = profile_data or {}
        self.created_at = datetime.utcnow()
        self.expertise = profile_data.get("expertise", [])  # For advisors
        self.company = profile_data.get("company")  # For investors/advisors
        self.bio = profile_data.get("bio", "")
        self.avatar_url = profile_data.get("avatar_url")


class Workspace:
    """Team workspace for collaboration"""
    def __init__(self, workspace_id: str, name: str, creator_id: str):
        self.workspace_id = workspace_id
        self.name = name
        self.creator_id = creator_id
        self.members: dict = {creator_id: {"role": "admin", "joined_at": datetime.utcnow()}}
        self.analyses: List[int] = []  # Analysis IDs
        self.created_at = datetime.utcnow()
        self.description = ""

    def add_member(self, user_id: str, role: str = "member"):
        """Add member to workspace"""
        self.members[user_id] = {"role": role, "joined_at": datetime.utcnow()}

    def remove_member(self, user_id: str):
        """Remove member from workspace"""
        if user_id != self.creator_id:  # Can't remove creator
            del self.members[user_id]

    def get_member_role(self, user_id: str) -> Optional[str]:
        """Get member's role"""
        return self.members.get(user_id, {}).get("role")

    def is_admin(self, user_id: str) -> bool:
        """Check if user is admin"""
        return self.get_member_role(user_id) in ["admin", "creator"]


class SharedAnalysis:
    """Shared analysis with access control"""
    def __init__(self, share_id: str, analysis_id: int, owner_id: str):
        self.share_id = share_id
        self.analysis_id = analysis_id
        self.owner_id = owner_id
        self.shared_with: dict = {}  # {user_id: access_level}
        self.created_at = datetime.utcnow()
        self.shared_link: Optional[str] = None  # Public link
        self.expires_at: Optional[datetime] = None

    def share_with_user(self, user_id: str, access_level: AccessLevel = AccessLevel.VIEW):
        """Share analysis with a user"""
        self.shared_with[user_id] = {
            "access_level": access_level,
            "shared_at": datetime.utcnow()
        }

    def revoke_access(self, user_id: str):
        """Revoke access for a user"""
        if user_id in self.shared_with:
            del self.shared_with[user_id]

    def can_view(self, user_id: str) -> bool:
        """Check if user can view"""
        return user_id in self.shared_with or user_id == self.owner_id

    def can_comment(self, user_id: str) -> bool:
        """Check if user can comment"""
        if user_id == self.owner_id:
            return True
        access = self.shared_with.get(user_id, {}).get("access_level")
        return access in [AccessLevel.COMMENT, AccessLevel.EDIT, AccessLevel.ADMIN]

    def can_edit(self, user_id: str) -> bool:
        """Check if user can edit"""
        if user_id == self.owner_id:
            return True
        access = self.shared_with.get(user_id, {}).get("access_level")
        return access in [AccessLevel.EDIT, AccessLevel.ADMIN]


class Comment:
    """Comment on analysis"""
    def __init__(self, comment_id: str, analysis_id: int, author_id: str, text: str):
        self.comment_id = comment_id
        self.analysis_id = analysis_id
        self.author_id = author_id
        self.text = text
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.replies: List["Comment"] = []
        self.mentioned_users: List[str] = []

    def add_reply(self, reply: "Comment"):
        """Add reply to comment"""
        self.replies.append(reply)

    def edit(self, new_text: str):
        """Edit comment"""
        self.text = new_text
        self.updated_at = datetime.utcnow()


class AnalysisVersion:
    """Version history for analysis"""
    def __init__(self, version_id: str, analysis_id: int, user_id: str, changes: dict):
        self.version_id = version_id
        self.analysis_id = analysis_id
        self.user_id = user_id
        self.changes = changes  # What changed
        self.created_at = datetime.utcnow()
        self.description = ""  # Change description
        self.previous_version: Optional[str] = None


class Advisor:
    """Advisor profile in the network"""
    def __init__(self, advisor_id: str, user_id: str, expertise: List[str], hourly_rate: float = 0):
        self.advisor_id = advisor_id
        self.user_id = user_id
        self.expertise = expertise  # Sectors/skills
        self.bio = ""
        self.hourly_rate = hourly_rate  # For paid consultations
        self.availability = []  # Time slots
        self.rating = 5.0
        self.num_reviews = 0
        self.portfolio = []  # Startups they've helped
        self.created_at = datetime.utcnow()


class ConsultationRequest:
    """Request for advisor consultation"""
    def __init__(self, request_id: str, founder_id: str, advisor_id: str, analysis_id: int):
        self.request_id = request_id
        self.founder_id = founder_id
        self.advisor_id = advisor_id
        self.analysis_id = analysis_id
        self.status = "pending"  # pending, accepted, completed, rejected
        self.message = ""
        self.scheduled_time: Optional[datetime] = None
        self.created_at = datetime.utcnow()
        self.feedback = ""


class Investor:
    """Investor profile in network"""
    def __init__(self, investor_id: str, user_id: str, investment_type: str):
        self.investor_id = investor_id
        self.user_id = user_id
        self.investment_type = investment_type  # angel, vc, corporate, other
        self.sectors = []  # Interested sectors
        self.investment_range = {"min": 0, "max": 0}  # Min/max investment
        self.portfolio = []  # Portfolio companies
        self.location = ""
        self.bio = ""
        self.created_at = datetime.utcnow()


class InvestorOutreach:
    """Outreach to investors"""
    def __init__(self, outreach_id: str, analysis_id: int, founder_id: str, investor_id: str):
        self.outreach_id = outreach_id
        self.analysis_id = analysis_id
        self.founder_id = founder_id
        self.investor_id = investor_id
        self.status = "sent"  # sent, viewed, interested, rejected, meeting_scheduled
        self.sent_at = datetime.utcnow()
        self.viewed_at: Optional[datetime] = None
        self.response: Optional[str] = None
        self.notes = ""


class TeamActivity:
    """Activity log for team collaboration"""
    def __init__(self, activity_id: str, workspace_id: str, user_id: str, activity_type: str):
        self.activity_id = activity_id
        self.workspace_id = workspace_id
        self.user_id = user_id
        self.activity_type = activity_type  # shared, commented, edited, joined, etc.
        self.description = ""
        self.related_id: Optional[int] = None  # Analysis ID or comment ID
        self.created_at = datetime.utcnow()
