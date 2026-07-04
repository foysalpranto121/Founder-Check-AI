# Agent.md, FounderCheck AI

This file is the living spec for any Claude Code session working on this project. Read this before making changes. Follow the current phase in roadmap.md, do not jump ahead.

## 1. Project Context

FounderCheck AI is a full stack AI startup analysis platform built for a Data Science Summit project showcase. Backend is FastAPI plus SQLAlchemy, frontend is Vite plus React. The pipeline takes a startup idea as input, runs it through demand validation, regulatory risk analysis, business model scoring, and produces an overall readiness score, plus deeper extended analysis (financial projections, SWOT, GTM, BD Impact, Founder Fit) and an investor Q&A flow that adjusts the score.

This is a working project with real gaps, not a from scratch build. 168 routes already exist across multiple feature routers (analytics, compliance, education, integrations, localization, monitoring, school, market intel, collaboration, validation, mobile). Do not rebuild what already works.

## 2. Tech Stack Decisions (locked)

- Backend: FastAPI plus SQLAlchemy. No Django rewrite.
- Database: Neon (Postgres), pooled connection string.
- Vector store: Chroma, already wired separately at `./data/chroma_db`, used for regulation and competitor embeddings. Do not conflate this with the Postgres application data.
- Auth: email and password with JWT. No OAuth.
- Roles: founder and admin.
- LLM provider: OpenAI primary (key confirmed real). Anthropic key present but unconfirmed, wire as optional fallback only, never block a feature on it being valid.
- Security scope for this pass: password hashing, JWT, CORS lockdown. No rate limiting yet, that is out of scope for today.

## 3. Rules

1. Never build beyond the current step.
2. Always respond in the same language the user typed (Bangla to Bangla).
3. Every analysis result must include a disclaimer: "This is an AI-generated startup assessment for exploration and learning, not investment advice or a guarantee of outcome."
4. Do not commit and push code. I will do it manually after testing. Ask if pushing is mandatory.
5. Write clean, well-commented code. Every function and class must have a docstring.
6. Follow secure coding practices. Never expose secrets, always validate and sanitize user input before processing, and enforce CORS and CSRF protections appropriate to the endpoint.
7. Write scalable code. Keep business logic in services, keep routes thin, never hardcode values that belong in settings or .env.
8. Do not over-comment. Only comment where the code is not self-explanatory. Avoid stating the obvious.
9. Never let the scoring engine output a fabricated number when the underlying LLM call fails or returns incomplete data. Default to a clearly labeled Incomplete or Calculating state, never a guessed score. A judge seeing a fake-looking number is worse than seeing an honest pending state.
10. Always show the user which factors drove a score (demand, regulatory, business model, and so on), not just a bare number. No black-box scoring. Transparency is a differentiator in a summit demo.
11. Respect free-tier API limits. Cache LLM responses for identical or near-identical inputs in Postgres so repeated demo runs do not burn quota during judging.
12. Treat all user-submitted text as untrusted. Never pass raw, unsanitized input directly into an LLM prompt. Clean it first.
13. Keep idea extraction, scoring, and Q&A adjustment as separate, independently testable service functions. Never merge pipeline stages into one function, even for speed.
14. Log every analysis run (input, scores, timestamp) to the database for traceability. If a judge asks how a score was reached, the system should be able to reconstruct the answer.
15. Never let an LLM call fail silently. Catch the error, fall back to the next configured provider before surfacing any error to the user.
16. No emojis and no em dashes anywhere: code comments, markdown files, and all frontend copy. Use plain punctuation only.

## 4. Frontend Design Rules

1. Make important things stand out. The readiness score and key verdicts should be the visual focal point of their section, not competing with secondary content.
2. Use basic visual tricks (size, weight, spacing, color) to guide attention, rather than decoration.
3. Keep it clean. Favor whitespace and clear hierarchy over dense layouts.
4. Do not overdo it with flashiness. No unnecessary animation, gradients, or effects that do not serve understanding.
5. Use gentle reminders when necessary (for example, incomplete data states or missing setup steps), without being alarming or intrusive.

## 5. Known Issues to Fix (see roadmap.md Phase 1)

- Financial tab crashes the whole app because it expects a full data structure that quick analysis does not provide.
- Frontend never calls the extended analysis endpoint, so five tabs render empty.
- Production build fails on one unused variable in ProductValidationDashboard.tsx.
- Two overlapping model files (database.py and models.py) need to be consolidated into one clean schema before the Neon migration.
- Analyses are currently stored in an in-memory dict and are lost on backend restart.
- Login currently accepts any email and password, no real authentication exists yet.

## 6. Environment

- Backend runs on port 9001. Frontend hardcodes this in multiple places, so keep the backend on this port unless every reference is updated.
- Frontend runs on port 5173.
- `.env` holds OPENAI_API_KEY, ANTHROPIC_API_KEY, DATABASE_URL (Neon), CHROMA_DB_PATH, and related config. Never hardcode any of these values in source.

## 7. Working Style

- One person (Sajib with communicating with Pranto) is executing this solo with Claude Code. No task division needed in this file.
- Document first, then build. Confirm each phase in roadmap.md before moving to the next.
- Manual git control only, Claude does not commit or push.