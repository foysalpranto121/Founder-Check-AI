"""
Collaboration API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.services.collaboration_service import collaboration_service
from app.models.collaboration import UserRole, AccessLevel
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["collaboration"])

# ========== SCHEMAS ==========

class UserCreateRequest(BaseModel):
    email: str
    name: str
    role: str
    profile_data: Optional[dict] = None

class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str

class WorkspaceCreateRequest(BaseModel):
    name: str

class MemberResponse(BaseModel):
    user_id: str
    role: str
    joined_at: datetime

class ShareAnalysisRequest(BaseModel):
    user_id: str
    access_level: str = "view"

class CommentRequest(BaseModel):
    text: str
    parent_id: Optional[str] = None

class ConsultationRequest(BaseModel):
    advisor_id: str
    message: str = ""

class ConsultationResponse(BaseModel):
    request_id: str
    status: str
    scheduled_time: Optional[datetime] = None

class AdvisorRegisterRequest(BaseModel):
    expertise: List[str]
    hourly_rate: float = 0

class InvestorRegisterRequest(BaseModel):
    investment_type: str  # angel, vc, corporate
    sectors: List[str] = []
    investment_range: dict = None

# ========== USER ENDPOINTS ==========

@router.post("/users")
async def create_user(request: UserCreateRequest):
    """Create a new user"""
    role = UserRole(request.role)
    user = collaboration_service.create_user(
        request.email, request.name, role, request.profile_data
    )
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value
    }

@router.get("/users/search")
async def search_users(q: str = Query(...), role: Optional[str] = None):
    """Search users by name or email"""
    role_filter = UserRole(role) if role else None
    users = collaboration_service.search_users(q, role_filter)
    return [
        {
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role.value
        }
        for u in users
    ]

# ========== WORKSPACE ENDPOINTS ==========

@router.post("/workspaces")
async def create_workspace(creator_id: str, request: WorkspaceCreateRequest):
    """Create new workspace"""
    workspace = collaboration_service.create_workspace(request.name, creator_id)
    return {
        "workspace_id": workspace.workspace_id,
        "name": workspace.name,
        "created_at": workspace.created_at,
        "members_count": len(workspace.members)
    }

@router.get("/workspaces/{workspace_id}")
async def get_workspace(workspace_id: str):
    """Get workspace details"""
    workspace = collaboration_service.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    stats = collaboration_service.get_collaboration_stats(workspace_id)
    return {
        "workspace_id": workspace.workspace_id,
        "name": workspace.name,
        "members_count": len(workspace.members),
        "analyses_count": len(workspace.analyses),
        "created_at": workspace.created_at,
        "stats": stats
    }

@router.post("/workspaces/{workspace_id}/members")
async def add_workspace_member(workspace_id: str, user_id: str, role: str = "member"):
    """Add member to workspace"""
    success = collaboration_service.add_workspace_member(workspace_id, user_id, role)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add member")
    return {"status": "success"}

@router.get("/workspaces/{workspace_id}/members")
async def get_members(workspace_id: str):
    """Get workspace members"""
    members = collaboration_service.get_workspace_members(workspace_id)
    return [
        {
            "user_id": uid,
            "role": data["role"],
            "joined_at": data["joined_at"]
        }
        for uid, data in members.items()
    ]

# ========== SHARING ENDPOINTS ==========

@router.post("/analyses/{analysis_id}/share")
async def share_analysis(analysis_id: int, owner_id: str, request: ShareAnalysisRequest):
    """Share analysis with user"""
    access = AccessLevel(request.access_level)
    success = collaboration_service.share_analysis(
        analysis_id, owner_id, request.user_id, access
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to share")
    return {"status": "shared"}

@router.post("/analyses/{analysis_id}/share-workspace")
async def share_with_workspace(analysis_id: int, owner_id: str, workspace_id: str,
                               access_level: str = "view"):
    """Share analysis with workspace"""
    access = AccessLevel(access_level)
    success = collaboration_service.share_with_workspace(
        analysis_id, workspace_id, owner_id, access
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to share")
    return {"status": "shared_with_workspace"}

@router.post("/analyses/{analysis_id}/revoke")
async def revoke_access(analysis_id: int, user_id: str, requester_id: str):
    """Revoke access"""
    success = collaboration_service.revoke_access(analysis_id, user_id, requester_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to revoke")
    return {"status": "access_revoked"}

@router.get("/analyses/{analysis_id}/access/{user_id}")
async def check_access(analysis_id: int, user_id: str, access_type: str = "view"):
    """Check user access level"""
    has_access = collaboration_service.can_user_access(analysis_id, user_id, access_type)
    return {"has_access": has_access}

# ========== COMMENTS ENDPOINTS ==========

@router.post("/analyses/{analysis_id}/comments")
async def add_comment(analysis_id: int, author_id: str, request: CommentRequest):
    """Add comment to analysis"""
    if request.parent_id:
        comment = collaboration_service.reply_to_comment(
            request.parent_id, author_id, request.text
        )
    else:
        comment = collaboration_service.add_comment(analysis_id, author_id, request.text)

    if not comment:
        raise HTTPException(status_code=400, detail="Failed to add comment")

    return {
        "comment_id": comment.comment_id,
        "author_id": comment.author_id,
        "text": comment.text,
        "created_at": comment.created_at
    }

@router.get("/analyses/{analysis_id}/comments")
async def get_comments(analysis_id: int):
    """Get all comments"""
    comments = collaboration_service.get_comments(analysis_id)
    return [
        {
            "comment_id": c.comment_id,
            "author_id": c.author_id,
            "text": c.text,
            "created_at": c.created_at,
            "reply_count": len(c.replies)
        }
        for c in comments
    ]

@router.put("/comments/{comment_id}")
async def edit_comment(comment_id: str, requester_id: str, new_text: str):
    """Edit comment"""
    success = collaboration_service.edit_comment(comment_id, new_text, requester_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to edit comment")
    return {"status": "updated"}

# ========== ADVISOR NETWORK ENDPOINTS ==========

@router.post("/advisors/register")
async def register_advisor(user_id: str, request: AdvisorRegisterRequest):
    """Register as advisor"""
    advisor = collaboration_service.register_advisor(
        user_id, request.expertise, request.hourly_rate
    )
    return {
        "advisor_id": advisor.advisor_id,
        "user_id": advisor.user_id,
        "expertise": advisor.expertise,
        "hourly_rate": advisor.hourly_rate
    }

@router.get("/advisors/search")
async def search_advisors(expertise: Optional[List[str]] = Query(None)):
    """Search advisors"""
    advisors = collaboration_service.search_advisors(expertise)
    return [
        {
            "advisor_id": a.advisor_id,
            "user_id": a.user_id,
            "expertise": a.expertise,
            "hourly_rate": a.hourly_rate,
            "rating": a.rating,
            "num_reviews": a.num_reviews
        }
        for a in advisors
    ]

@router.get("/advisors/{advisor_id}")
async def get_advisor_profile(advisor_id: str):
    """Get advisor profile"""
    advisor = collaboration_service.get_advisor(advisor_id)
    if not advisor:
        raise HTTPException(status_code=404, detail="Advisor not found")
    return {
        "advisor_id": advisor.advisor_id,
        "expertise": advisor.expertise,
        "bio": advisor.bio,
        "hourly_rate": advisor.hourly_rate,
        "rating": advisor.rating,
        "num_reviews": advisor.num_reviews
    }

@router.post("/consultations/request")
async def request_consultation(founder_id: str, request: ConsultationRequest):
    """Request consultation"""
    consultation = collaboration_service.request_consultation(
        founder_id, request.advisor_id, 0, request.message  # analysis_id hardcoded for now
    )
    return {
        "request_id": consultation.request_id,
        "status": consultation.status
    }

@router.post("/consultations/{request_id}/respond")
async def respond_consultation(request_id: str, advisor_id: str, accepted: bool,
                               scheduled_time: Optional[datetime] = None):
    """Respond to consultation request"""
    success = collaboration_service.respond_to_consultation(
        request_id, advisor_id, accepted, scheduled_time
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to respond")
    return {"status": "updated"}

# ========== INVESTOR NETWORK ENDPOINTS ==========

@router.post("/investors/register")
async def register_investor(user_id: str, request: InvestorRegisterRequest):
    """Register as investor"""
    investor = collaboration_service.register_investor(user_id, request.investment_type)
    investor.sectors = request.sectors
    if request.investment_range:
        investor.investment_range = request.investment_range
    return {
        "investor_id": investor.investor_id,
        "investment_type": investor.investment_type,
        "sectors": investor.sectors
    }

@router.get("/investors/search")
async def search_investors(sectors: Optional[List[str]] = Query(None),
                           investment_type: Optional[str] = None):
    """Search investors"""
    investors = collaboration_service.search_investors(sectors, investment_type)
    return [
        {
            "investor_id": inv.investor_id,
            "investment_type": inv.investment_type,
            "sectors": inv.sectors
        }
        for inv in investors
    ]

# ========== INVESTOR OUTREACH ENDPOINTS ==========

@router.post("/outreach/send")
async def send_to_investor(analysis_id: int, founder_id: str, investor_id: str):
    """Send analysis to investor"""
    outreach = collaboration_service.send_to_investor(analysis_id, founder_id, investor_id)
    return {
        "outreach_id": outreach.outreach_id,
        "status": outreach.status,
        "sent_at": outreach.sent_at
    }

@router.get("/outreach/{founder_id}")
async def get_founder_outreach(founder_id: str):
    """Get outreach status"""
    outreach_list = collaboration_service.get_founder_outreach(founder_id)
    return [
        {
            "outreach_id": o.outreach_id,
            "analysis_id": o.analysis_id,
            "investor_id": o.investor_id,
            "status": o.status,
            "sent_at": o.sent_at,
            "viewed_at": o.viewed_at
        }
        for o in outreach_list
    ]

@router.get("/inbound/{investor_id}")
async def get_inbound_opportunities(investor_id: str):
    """Get inbound opportunities"""
    inbound = collaboration_service.get_investor_inbound(investor_id)
    return [
        {
            "outreach_id": o.outreach_id,
            "analysis_id": o.analysis_id,
            "founder_id": o.founder_id,
            "status": o.status,
            "sent_at": o.sent_at
        }
        for o in inbound
    ]

@router.post("/outreach/{outreach_id}/view")
async def mark_viewed(outreach_id: str):
    """Mark as viewed"""
    success = collaboration_service.mark_viewed(outreach_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to mark viewed")
    return {"status": "marked_viewed"}

# ========== ANALYTICS ENDPOINTS ==========

@router.get("/workspaces/{workspace_id}/activity")
async def get_activity(workspace_id: str, limit: int = 50):
    """Get workspace activity"""
    activities = collaboration_service.get_workspace_activity(workspace_id, limit)
    return [
        {
            "activity_id": a.activity_id,
            "user_id": a.user_id,
            "activity_type": a.activity_type,
            "description": a.description,
            "created_at": a.created_at
        }
        for a in activities
    ]

@router.get("/investors/{investor_id}/insights")
async def get_investor_insights(investor_id: str):
    """Get investor insights"""
    insights = collaboration_service.get_investor_insights(investor_id)
    return insights
