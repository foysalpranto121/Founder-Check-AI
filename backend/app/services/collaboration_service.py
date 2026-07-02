"""
Collaboration Service - Managing teams, sharing, comments, and networks
"""

from typing import List, Dict, Optional
from datetime import datetime
from uuid import uuid4
from app.models.collaboration import (
    User, Workspace, SharedAnalysis, Comment, AnalysisVersion,
    Advisor, ConsultationRequest, Investor, InvestorOutreach, TeamActivity,
    UserRole, AccessLevel
)


class CollaborationService:
    """Service for managing collaboration features"""

    def __init__(self):
        self.workspaces: Dict[str, Workspace] = {}
        self.users: Dict[str, User] = {}
        self.shared_analyses: Dict[str, SharedAnalysis] = {}
        self.comments: Dict[str, Comment] = {}
        self.versions: Dict[str, AnalysisVersion] = {}
        self.advisors: Dict[str, Advisor] = {}
        self.investors: Dict[str, Investor] = {}
        self.consultations: Dict[str, ConsultationRequest] = {}
        self.outreach: Dict[str, InvestorOutreach] = {}
        self.activities: List[TeamActivity] = []

    # ========== USER MANAGEMENT ==========

    def create_user(self, email: str, name: str, role: UserRole, profile_data: dict = None) -> User:
        """Create a new user"""
        user_id = str(uuid4())
        user = User(user_id, name, email, role, profile_data)
        self.users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)

    def search_users(self, query: str, role_filter: Optional[UserRole] = None) -> List[User]:
        """Search users by name or email"""
        results = []
        query_lower = query.lower()
        for user in self.users.values():
            if role_filter and user.role != role_filter:
                continue
            if query_lower in user.name.lower() or query_lower in user.email.lower():
                results.append(user)
        return results

    # ========== WORKSPACE MANAGEMENT ==========

    def create_workspace(self, name: str, creator_id: str) -> Workspace:
        """Create new workspace"""
        workspace_id = str(uuid4())
        workspace = Workspace(workspace_id, name, creator_id)
        self.workspaces[workspace_id] = workspace
        return workspace

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        """Get workspace"""
        return self.workspaces.get(workspace_id)

    def add_workspace_member(self, workspace_id: str, user_id: str, role: str = "member") -> bool:
        """Add member to workspace"""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False
        workspace.add_member(user_id, role)
        self._log_activity(workspace_id, user_id, "joined_workspace", f"Joined workspace")
        return True

    def remove_workspace_member(self, workspace_id: str, user_id: str, requester_id: str) -> bool:
        """Remove member (only admin can do this)"""
        workspace = self.get_workspace(workspace_id)
        if not workspace or not workspace.is_admin(requester_id):
            return False
        workspace.remove_member(user_id)
        self._log_activity(workspace_id, requester_id, "removed_member", f"Removed {user_id}")
        return True

    def get_workspace_members(self, workspace_id: str) -> Dict[str, Dict]:
        """Get all workspace members"""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return {}
        return workspace.members

    # ========== SHARING ANALYSIS ==========

    def share_analysis(self, analysis_id: int, owner_id: str, user_id: str,
                       access_level: AccessLevel = AccessLevel.VIEW) -> bool:
        """Share analysis with user"""
        share_id = f"share_{analysis_id}_{user_id}"
        if share_id not in self.shared_analyses:
            shared = SharedAnalysis(share_id, analysis_id, owner_id)
            self.shared_analyses[share_id] = shared

        shared = self.shared_analyses[share_id]
        shared.share_with_user(user_id, access_level)
        return True

    def share_with_workspace(self, analysis_id: int, workspace_id: str, owner_id: str,
                             access_level: AccessLevel = AccessLevel.VIEW) -> bool:
        """Share analysis with entire workspace"""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False

        for member_id in workspace.members.keys():
            if member_id != owner_id:
                self.share_analysis(analysis_id, owner_id, member_id, access_level)

        self._log_activity(workspace_id, owner_id, "shared_analysis",
                          f"Shared analysis {analysis_id} with workspace")
        return True

    def revoke_access(self, analysis_id: int, user_id: str, requester_id: str) -> bool:
        """Revoke user access"""
        share_id = f"share_{analysis_id}_{user_id}"
        if share_id not in self.shared_analyses:
            return False

        shared = self.shared_analyses[share_id]
        if shared.owner_id != requester_id:
            return False

        shared.revoke_access(user_id)
        return True

    def can_user_access(self, analysis_id: int, user_id: str, access_type: str = "view") -> bool:
        """Check user access level"""
        share_id = f"share_{analysis_id}_{user_id}"
        if share_id not in self.shared_analyses:
            return False

        shared = self.shared_analyses[share_id]
        if access_type == "view":
            return shared.can_view(user_id)
        elif access_type == "comment":
            return shared.can_comment(user_id)
        elif access_type == "edit":
            return shared.can_edit(user_id)
        return False

    # ========== COMMENTS & DISCUSSIONS ==========

    def add_comment(self, analysis_id: int, author_id: str, text: str) -> Optional[Comment]:
        """Add comment to analysis"""
        comment_id = str(uuid4())
        comment = Comment(comment_id, analysis_id, author_id, text)
        self.comments[comment_id] = comment
        return comment

    def reply_to_comment(self, parent_comment_id: str, author_id: str, text: str) -> Optional[Comment]:
        """Reply to a comment"""
        parent = self.comments.get(parent_comment_id)
        if not parent:
            return None

        reply = self.add_comment(parent.analysis_id, author_id, text)
        parent.add_reply(reply)
        return reply

    def get_comments(self, analysis_id: int) -> List[Comment]:
        """Get all comments for analysis"""
        return [c for c in self.comments.values() if c.analysis_id == analysis_id]

    def edit_comment(self, comment_id: str, new_text: str, requester_id: str) -> bool:
        """Edit comment (only author can)"""
        comment = self.comments.get(comment_id)
        if not comment or comment.author_id != requester_id:
            return False
        comment.edit(new_text)
        return True

    def delete_comment(self, comment_id: str, requester_id: str) -> bool:
        """Delete comment (author or admin)"""
        comment = self.comments.get(comment_id)
        if not comment or comment.author_id != requester_id:
            return False
        del self.comments[comment_id]
        return True

    # ========== VERSION HISTORY ==========

    def record_version(self, analysis_id: int, user_id: str, changes: dict) -> AnalysisVersion:
        """Record analysis version"""
        version_id = str(uuid4())
        version = AnalysisVersion(version_id, analysis_id, user_id, changes)
        self.versions[version_id] = version
        return version

    def get_version_history(self, analysis_id: int) -> List[AnalysisVersion]:
        """Get version history"""
        return [v for v in self.versions.values() if v.analysis_id == analysis_id]

    # ========== ADVISOR NETWORK ==========

    def register_advisor(self, user_id: str, expertise: List[str], hourly_rate: float = 0) -> Advisor:
        """Register as advisor"""
        advisor_id = str(uuid4())
        advisor = Advisor(advisor_id, user_id, expertise, hourly_rate)
        self.advisors[advisor_id] = advisor
        return advisor

    def get_advisor(self, advisor_id: str) -> Optional[Advisor]:
        """Get advisor profile"""
        return self.advisors.get(advisor_id)

    def search_advisors(self, expertise: List[str] = None, sector: str = None) -> List[Advisor]:
        """Search advisors by expertise"""
        results = []
        for advisor in self.advisors.values():
            if expertise:
                if any(e in advisor.expertise for e in expertise):
                    results.append(advisor)
            else:
                results.append(advisor)
        return results

    def request_consultation(self, founder_id: str, advisor_id: str, analysis_id: int,
                           message: str = "") -> ConsultationRequest:
        """Request consultation from advisor"""
        request_id = str(uuid4())
        request = ConsultationRequest(request_id, founder_id, advisor_id, analysis_id)
        request.message = message
        self.consultations[request_id] = request
        return request

    def respond_to_consultation(self, request_id: str, advisor_id: str, accepted: bool,
                               scheduled_time: Optional[datetime] = None) -> bool:
        """Respond to consultation request"""
        consultation = self.consultations.get(request_id)
        if not consultation or consultation.advisor_id != advisor_id:
            return False

        if accepted:
            consultation.status = "accepted"
            consultation.scheduled_time = scheduled_time
        else:
            consultation.status = "rejected"

        return True

    def submit_consultation_feedback(self, request_id: str, founder_id: str,
                                    feedback: str, rating: float) -> bool:
        """Submit feedback after consultation"""
        consultation = self.consultations.get(request_id)
        if not consultation or consultation.founder_id != founder_id:
            return False

        consultation.status = "completed"
        consultation.feedback = feedback

        # Update advisor rating
        advisor = self.advisors.get(consultation.advisor_id)
        if advisor:
            advisor.num_reviews += 1
            advisor.rating = ((advisor.rating * (advisor.num_reviews - 1)) + rating) / advisor.num_reviews

        return True

    # ========== INVESTOR NETWORK ==========

    def register_investor(self, user_id: str, investment_type: str) -> Investor:
        """Register as investor"""
        investor_id = str(uuid4())
        investor = Investor(investor_id, user_id, investment_type)
        self.investors[investor_id] = investor
        return investor

    def get_investor(self, investor_id: str) -> Optional[Investor]:
        """Get investor profile"""
        return self.investors.get(investor_id)

    def search_investors(self, sectors: List[str] = None, investment_type: str = None) -> List[Investor]:
        """Search investors by criteria"""
        results = []
        for investor in self.investors.values():
            if investment_type and investor.investment_type != investment_type:
                continue
            if sectors and not any(s in investor.sectors for s in sectors):
                continue
            results.append(investor)
        return results

    # ========== INVESTOR OUTREACH ==========

    def send_to_investor(self, analysis_id: int, founder_id: str, investor_id: str) -> InvestorOutreach:
        """Send analysis to investor"""
        outreach_id = str(uuid4())
        outreach = InvestorOutreach(outreach_id, analysis_id, founder_id, investor_id)
        self.outreach[outreach_id] = outreach
        return outreach

    def get_outreach_status(self, outreach_id: str) -> Optional[InvestorOutreach]:
        """Get outreach status"""
        return self.outreach.get(outreach_id)

    def get_founder_outreach(self, founder_id: str) -> List[InvestorOutreach]:
        """Get all outreach from a founder"""
        return [o for o in self.outreach.values() if o.founder_id == founder_id]

    def get_investor_inbound(self, investor_id: str) -> List[InvestorOutreach]:
        """Get inbound opportunities for investor"""
        return [o for o in self.outreach.values() if o.investor_id == investor_id]

    def mark_viewed(self, outreach_id: str) -> bool:
        """Mark analysis as viewed by investor"""
        outreach = self.outreach.get(outreach_id)
        if not outreach:
            return False
        outreach.viewed_at = datetime.utcnow()
        outreach.status = "viewed"
        return True

    def respond_to_outreach(self, outreach_id: str, response: str) -> bool:
        """Investor responds to outreach"""
        outreach = self.outreach.get(outreach_id)
        if not outreach:
            return False

        outreach.response = response
        if "interested" in response.lower():
            outreach.status = "interested"
        elif "no" in response.lower() or "reject" in response.lower():
            outreach.status = "rejected"
        elif "meeting" in response.lower():
            outreach.status = "meeting_scheduled"

        return True

    # ========== ACTIVITY LOGGING ==========

    def _log_activity(self, workspace_id: str, user_id: str, activity_type: str, description: str):
        """Log team activity"""
        activity_id = str(uuid4())
        activity = TeamActivity(activity_id, workspace_id, user_id, activity_type)
        activity.description = description
        self.activities.append(activity)

    def get_workspace_activity(self, workspace_id: str, limit: int = 50) -> List[TeamActivity]:
        """Get recent workspace activity"""
        activities = [a for a in self.activities if a.workspace_id == workspace_id]
        return sorted(activities, key=lambda x: x.created_at, reverse=True)[:limit]

    # ========== STATISTICS & INSIGHTS ==========

    def get_collaboration_stats(self, workspace_id: str) -> Dict:
        """Get collaboration statistics"""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return {}

        all_comments = sum(len(self.get_comments(aid)) for aid in workspace.analyses)
        recent_activity = self.get_workspace_activity(workspace_id, limit=10)

        return {
            "members_count": len(workspace.members),
            "analyses_count": len(workspace.analyses),
            "total_comments": all_comments,
            "recent_activity": len(recent_activity),
            "last_activity": recent_activity[0].created_at if recent_activity else None
        }

    def get_investor_insights(self, investor_id: str) -> Dict:
        """Get investor inbound insights"""
        inbound = self.get_investor_inbound(investor_id)
        return {
            "total_inbound": len(inbound),
            "viewed": len([o for o in inbound if o.status != "sent"]),
            "interested": len([o for o in inbound if o.status == "interested"]),
            "by_sector": self._group_by_sector(inbound)
        }

    def _group_by_sector(self, outreach_list: List[InvestorOutreach]) -> Dict:
        """Group outreach by sector"""
        sectors = {}
        for o in outreach_list:
            # Would need sector from analysis, placeholder for now
            sector = "Technology"
            sectors[sector] = sectors.get(sector, 0) + 1
        return sectors


# Global collaboration service instance
collaboration_service = CollaborationService()
