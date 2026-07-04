from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=API_KEY)

# ============================================================================
# LLM Functions
# ============================================================================

def extract_idea_fields(idea_text: str) -> dict:
    """Extract structured fields from raw idea text using Claude"""

    prompt = f"""
    Analyze this startup idea and extract structured information.

    Idea: {idea_text}

    Return ONLY valid JSON with these fields:
    - title: Short 1-line title
    - description: 1-2 sentence description
    - sector: e.g., "fintech", "food_delivery", "agritech", "healthtech"
    - target_customer: Who is the primary customer?
    - revenue_model: How will it make money?
    - location: Where will it operate? (e.g., Dhaka, Bangladesh-wide, Online)

    RETURN ONLY JSON, NO OTHER TEXT.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text
        result = json.loads(response_text)
        return result

    except json.JSONDecodeError:
        return {
            "title": "Idea",
            "description": idea_text[:100],
            "sector": "unknown",
            "target_customer": "unknown",
            "revenue_model": "unknown",
            "location": "Bangladesh"
        }
    except Exception as e:
        print(f"Error in extract_idea_fields: {e}")
        raise


def analyze_demand(idea_text: str, target_customer: str) -> dict:
    """Analyze market demand for the idea"""

    prompt = f"""
    Analyze market demand for this Bangladesh startup idea:

    Idea: {idea_text}
    Target Customer: {target_customer}

    Return JSON with:
    - score: 1-10 rating
    - market_size: Estimated TAM in Bangladesh
    - competition: Existing competitors
    - opportunities: 3 key market opportunities
    - threats: 2 key market threats

    RETURN ONLY JSON.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "score": 5,
            "market_size": "Estimate needed",
            "competition": "Research needed",
            "opportunities": ["Local demand", "Underserved market", "Digital adoption"],
            "threats": ["Global competitors", "Regulatory changes"]
        }
    except Exception as e:
        print(f"Error in analyze_demand: {e}")
        raise


def analyze_regulatory_risks(idea_text: str, sector: str) -> dict:
    """Analyze regulatory risks for the idea in Bangladesh context"""

    prompt = f"""
    Analyze regulatory risks for a {sector} startup in Bangladesh:

    Idea: {idea_text}

    Key regulators:
    - NBR (tax): Corporate tax, VAT registration
    - RJSC (registration): Company registration
    - BIDA (investment): FDI incentives if applicable
    - BTRC (telecom): For telecom/app-based services
    - BSTI (food): For food-related businesses
    - Bangladesh Bank: For fintech/payment services
    - City Corporation: Trade licenses

    Return JSON with:
    - risk_score: 1-10 (10 = high risk, 1 = low risk)
    - key_regulators: [list of relevant regulators]
    - critical_approvals: What permits/licenses needed first?
    - estimated_timeline: Months to get all approvals
    - cost_estimate: Estimated cost in BDT
    - warnings: Critical regulatory issues

    RETURN ONLY JSON.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "risk_score": 5,
            "key_regulators": ["RJSC", "NBR"],
            "critical_approvals": "Business registration",
            "estimated_timeline": 30,
            "cost_estimate": 50000,
            "warnings": "Consult regulatory expert"
        }
    except Exception as e:
        print(f"Error in analyze_regulatory_risks: {e}")
        raise


def generate_business_canvas(idea_text: str, sector: str) -> dict:
    """Generate Business Model Canvas in Bangladeshi Taka context"""

    prompt = f"""
    Create a Business Model Canvas for this Bangladesh startup:

    Idea: {idea_text}
    Sector: {sector}

    Return JSON with Business Model Canvas blocks:
    - key_partners: Who will you partner with?
    - key_activities: Main activities
    - key_resources: Resources needed (estimate costs in BDT)
    - value_proposition: Main value delivery
    - customer_segments: Customer types
    - channels: How to reach customers
    - customer_relationships: How to engage customers
    - revenue_streams: Revenue sources (BDT per unit/month)
    - cost_structure: Major cost categories (BDT estimates)

    RETURN ONLY JSON.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "key_partners": ["To be determined"],
            "key_activities": ["To be determined"],
            "key_resources": {"tech": 500000, "marketing": 200000},
            "value_proposition": "Better solution",
            "customer_segments": ["Early adopters"],
            "channels": ["Direct", "Online"],
            "customer_relationships": ["Support"],
            "revenue_streams": {"main": 50000},
            "cost_structure": {"tech": 500000, "operations": 300000}
        }
    except Exception as e:
        print(f"Error in generate_business_canvas: {e}")
        raise


def generate_investor_questions(idea_text: str, sector: str) -> list:
    """Generate 10 investor questions for Q&A interview"""

    prompt = f"""
    Generate 10 tough investor questions for this startup pitch:

    Idea: {idea_text}
    Sector: {sector}
    Context: Bangladesh market

    Questions should be:
    - Specific to Bangladesh market
    - Challenging but fair
    - About market, execution, team, financials
    - In order from foundational to advanced

    Return JSON list:
    [
      {{"question": "...", "category": "market/execution/financials/team"}},
      ...
    ]

    RETURN ONLY JSON.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    except json.JSONDecodeError:
        return [
            {"question": "What is your target market size in Bangladesh?", "category": "market"},
            {"question": "Who are your direct competitors?", "category": "market"},
            {"question": "What is your go-to-market strategy?", "category": "execution"},
            {"question": "What is your financial projection?", "category": "financials"},
            {"question": "Why are you the right team to execute?", "category": "team"},
        ]
    except Exception as e:
        print(f"Error in generate_investor_questions: {e}")
        raise


def verify_regulatory_claims(claims: list, regulations_context: str) -> dict:
    """Verify regulatory claims against actual regulations"""

    prompt = f"""
    Verify these regulatory claims about Bangladesh against known regulations:

    Claims to verify:
    {json.dumps(claims)}

    Known regulations context:
    {regulations_context}

    Return JSON:
    {
      "verified_claims": [{"claim": "...", "status": "verified", "source": "..."}],
      "unverified_claims": [{"claim": "...", "reason": "..."}],
      "corrections": "Any corrections needed"
    }

    RETURN ONLY JSON.
    """

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "verified_claims": [],
            "unverified_claims": claims,
            "corrections": "Manual review needed"
        }
    except Exception as e:
        print(f"Error in verify_regulatory_claims: {e}")
        raise


# ============================================================================
# Test Function
# ============================================================================

def test_api():
    """Test Claude API connection"""
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Say 'FounderCheck API is working!' in JSON format."}
            ]
        )
        print("Claude API is working!")
        print(message.content[0].text)
        return True
    except Exception as e:
        print(f"Claude API error: {e}")
        return False


if __name__ == "__main__":
    test_api()
