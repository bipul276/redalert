# RedAlert - Interview Preparation Guide

This document is designed to help you prepare for an interview regarding the **RedAlert** project. It outlines the core architecture, key technical decisions, potential interview questions **with provided answers**, and how to discuss your work effectively.

---

## 1. Project Overview & Elevator Pitch

**The Pitch:**
"RedAlert is a unified product safety and recall intelligence platform. It solves the problem of fragmented safety alerts from various government bodies and news sources by aggregating, standardizing, and scoring product recalls from both the US and India. It acts as an intelligent early-warning system to keep communities safe, leveraging a modern decoupled architecture with Next.js on the frontend and FastAPI on the backend."

**Core Value Proposition (USP):**
- **Centralizes fragmented product safety data** (FDA, CPSC, NHTSA, FSSAI, CDSCO, Google News).
- **Custom NLP-based heuristics for accurate regional scoring** (e.g., distinguishing an Indian ban on Swiss chocolate from a Swiss ban).

---

## 2. Technical Stack & Justifications

Be prepared to explain *why* you chose these technologies.

*   **Frontend**: Next.js (React), TypeScript, Tailwind CSS.
    *   *Why?* Next.js provides Server-Side Rendering (SSR) for robust SEO and initial load performance. TypeScript ensures strong typing, reducing runtime errors. Tailwind CSS allows for rapid, consistent styling.
*   **Backend**: FastAPI (Python), SQLModel, APScheduler.
    *   *Why?* FastAPI is highly performant (async capabilities built-in) and auto-generates API documentation (Swagger/ReDoc). Python is the industry standard for NLP and data ingestion scripts. SQLModel elegantly bridges Pydantic and SQLAlchemy.
*   **Database**: PostgreSQL
    *   *Why?* A robust open-source relational database ideal for structured data (recalls, users) and complex queries (filtering by region, status, dates).
*   **Authentication & Security**: JWT (JSON Web Tokens), TOTP (Time-based One-Time Password) via Authenticator App, Argon2 hashing.
    *   *Why?* Ensures secure, stateless authentication with an extra layer of 2FA for the administrative panel to protect sensitive actions.
*   **Infrastructure & Deployment**: Docker, Docker Compose, Nginx (Reverse Proxy), Ubuntu VPS.
    *   *Why?* Docker ensures environment consistency across development and production, preventing "it works on my machine" issues.

---

## 3. Architecture & Data Flow

You should be able to draw or describe the system architecture on a whiteboard.

1.  **Ingestion Phase**: Background jobs (`AsyncIOScheduler`) run every 12 hours to scrape data from US and Indian government sources and Google News (RSS).
2.  **Processing Phase (NLP Engine)**: Raw data is standardized. The **Heuristic Region Scoring Engine** kicks in to assign scores (e.g., +5 if explicit FDA keywords appear, resolving context-aware regional attribution). Deduplication occurs based on similar titles or official reference numbers.
3.  **Storage Phase**: Data is saved to PostgreSQL, categorized with a **Confidence Level** (`CONFIRMED`, `PROBABLE`, `WATCH`).
4.  **Delivery Phase**: FastAPI serves the processed data via REST endpoints.
5.  **Presentation Phase**: The Next.js frontend fetches and displays data on a public dashboard and a secure admin panel.

---

## 4. Detailed Interview Questions & Answers

### General & Architecture
**Q: Why did you choose FastAPI over Django or Flask?**
**A:** I chose FastAPI primarily for its exceptional performance—it’s built from the ground up to be asynchronous, which is ideal for our I/O-bound data ingestion tasks (calling multiple external APIs simultaneously). Furthermore, it leverages Pydantic for data validation and automatically generates interactive API documentation (Swagger/ReDoc). This drastically reduces the time spent manually checking request bodies compared to Flask or Django.

**Q: How do you handle background tasks? Why `APScheduler` instead of Celery and Redis?**
**A:** We use `AsyncIOScheduler` from `APScheduler`. While Celery and Redis are extremely powerful for high-throughput messaging, they come with substantial infrastructure overhead (managing a message broker and worker nodes). Given that our core requirement is a scheduled ingestion pipeline running every 12 hours rather than an intensive event queue, running `APScheduler` directly within the FastAPI application's lifespan is robust, simpler to deploy natively, and perfectly suited for our needs.

**Q: Can you explain your database schema for the Recall model? What fields did you index?**
**A:** The `Recall` table uses SQLModel (which marries SQLAlchemy and Pydantic). It stores structured data like `title`, `brand`, `region`, and `confidence_level`. I deliberately indexed frequently queried fields such as `region`, `confidence_level` status, and `published_date`. This ensures that when users use the frontend dashboard filters or search, PostgreSQL retrieves results in milliseconds, even as our historically scraped dataset grows exponentially.

### Frontend
**Q: How are you fetching data in Next.js? Are you using Server Components or Client Components?**
**A:** Next.js uses a hybrid approach. For the main dashboard view, we rely heavily on Server Components (SSR/SSG) to fetch initial recall data directly from the FastAPI backend on the server side. This ensures a fast First Contentful Paint (FCP) and strong SEO. However, for highly interactive elements—like dynamic search bars or complex region/status filters—we utilize Client Components that react to user inputs by calling our client `api.ts` module with updated URL parameters. 

**Q: How do you manage global state for complex filtering on the dashboard?**
**A:** Rather than relying exclusively on heavy global stores like Redux, the dashboard state (filters, search terms) is intentionally decoupled into the URL (`URLSearchParams`). This is a web best practice: it ensures that filtered views are easily sharable and bookmarkable by users. Client components simply react to URL query changes, fetch the new data, and update their local state.

### Backend & Data Pipeline
**Q: How does your NLP deduplication process work? How do you prevent identical alerts from showing up twice?**
**A:** A primary headache of scraping multiple news sources for the same recall (like a massive chocolate ban) is duplicate spam. First, the pipeline attempts to cross-reference official ID numbers if the source provides them (e.g., FDA Recall numbers). If no ID is available, the system conducts a title and hazard similarity check within recent timeframes. If an alert has a high degree of textual overlap with an already existing record published within the previous 48 hours, it's flagged as a duplicate and merged rather than ingested entirely fresh.

**Q: If a scraper changes its HTML structure, your ingestion pipeline breaks. How do you handle this?**
**A:** This is a classic ETL pipeline vulnerability. To mitigate this:
1. I heavily prioritize consuming structured APIs (FDA JSON) or standardized RSS feeds (Google News) over fragile raw HTML parsing.
2. For modules that *must* scrape HTML, the ingestion scripts are wrapped in sweeping `try/except` fallback blocks with extensive logging. 
3. If a specific ingestor crashes, it handles the exception gracefully, logs an error (which I can monitor), and moves on to the next data source to ensure partial ingestion success. 

### Security & DevOps
**Q: Explain the flow of your TOTP 2FA implementation. Where do you store the secret?**
**A:** When an admin is first created via CLI, a cryptographically secure random secret (TOTP Encryption Key) is generated. The backend provides a provisioning URI (QR code) which the admin scans using Authy or Google Authenticator. Upon login, the admin submits both their password (verified via a strong Argon2 hash) and the current 6-digit code. The backend verifies the code using HMAC-SHA-1 before issuing a short-lived JWT session token. This provides devastatingly strong protection against credential stuffing or brute-forcing the admin panel.

**Q: Walk me through your Docker setup. How do your containers communicate?**
**A:** The application uses `docker-compose` to orchestrate a multi-container environment containing the Frontend UI, the FastAPI backend, and the PostgreSQL database. The containers communicate exclusively over an isolated internal Docker bridged network securely using their service names as DNS hostnames (e.g., the backend connects to the database via `postgresql://db:5432...`). Only necessary ports (like 80 for an Nginx proxy) are exposed to the public host machine, ensuring our database is entirely walled off from the raw internet.

---

## 5. Real-World Challenges & Follow-up Questions (STAR Format)

Be prepared for the interviewer to dig deeper. Use the **STAR Method** (Situation, Task, Action, Result).

### Challenge 1: The "Swiss Chocolate" Problem (Contextual Misattribution)
*   **Situation:** The NLP engine systematically incorrectly assigned the "Switzerland" or "Global" tag to Indian recalls simply because an Indian news headline read *"India bans imported Swiss chocolates"*.
*   **Task:** Improve the region-scoring algorithm to understand the true localized context of an article rather than relying on blunt string matching.
*   **Action:** I implemented a **Heuristic Region Scoring Engine**. Instead of a binary word match, the engine dynamically ranks an `india_score` vs `foreign_score`. Strong localized keywords (like explicitly mentioning "FSSAI", "CDSCO", or specific Indian cities like Delhi) add a high, compounding weight (+5), effectively overriding the foreign substring.
*   **Result:** The algorithmic false positive attribution plummeted, ensuring Indian users only saw Indian recalls on their regional dashboards.
*   **Interviewer Follow-up:** *"What if an article mentions both the FDA and FSSAI equally prominently?"*
    *   **Your Answer:** In extreme edge cases of a massive global recall, the heuristic engine defaults to a `GLOBAL`/Multi-Region tag, or flags the recall with a `WATCH` confidence level, queuing it for a human admin to manually review and approve the mapping.

### Challenge 2: Handling Unstructured and Chaotic Disparate Data
*   **Situation:** The disparate sources were chaotic. The US FDA provides structured JSON, the CPSC provides XML, and Google News provides raw unstructured text.
*   **Task:** Create a unified, queryable database schema from chaotic inputs.
*   **Action:** I built a standardized, decoupled ETL (Extract, Transform, Load) pipeline in Python. I created modular specific `Ingestors` (e.g., `FDAIngestor`, `RSSIngestor`) that all implement a common abstract class. Their sole responsibility is to translate their specific chaotic JSON/XML/HTML into our unified, strictly-typed `Recall` SQLModel schema.
*   **Result:** The database remains extremely clean and strictly formatted, allowing the Next.js frontend to blindly map over the database rows without worrying about null reference errors or misnamed variables.
*   **Interviewer Follow-up:** *"How do you handle incomplete data (e.g., an RSS feed missing a 'brand' name)?"*
    *   **Your Answer:** The SQLModel schema is designed to allow standardizing missing fields gracefully to `null` or "Unknown" values, which the frontend handles UI-wise. Additionally, the NLP engine attempts a secondary sweep to extract the brand from the headline text if it explicitly detects branded capitalization formatting.

### Challenge 3: Securing the Administrative Action Endpoints
*   **Situation:** The ability to approve, edit, or delete a public-facing recall is destructive and critical.
*   **Task:** Secure the FastApi admin endpoints beyond basic authentication.
*   **Action:** I injected a strict dependency (`get_current_admin_user`) into every sensitive router endpoint. This dependency not only verifies the stateless JWT token but checks the database role of the user. For login to even acquire that JWT, I enforced Argon2 password hashing combined with TOTP 2FA.
*   **Result:** Admins cannot execute destructive actions without valid, recently-issued JWTs.
*   **Interviewer Follow-up:** *"Why Argon2 over bcrypt?"*
    *   **Your Answer:** Argon2 is the winner of the Password Hashing Competition. It is specifically designed to be highly memory-hard. If an attacker dumps our database, Argon2 drastically slows down the rate at which they can run GPU parallel cracking attacks compared to older algorithms like bcrypt or PBKDF2.

### Challenge 4: Managing Next.js and FastAPI CORS 
*   **Situation:** The architecture is decoupled. During frontend API fetching, the Next.js application constantly faced Cross-Origin Resource Sharing (CORS) blocks from the browser because it ran on port `3000` while the backend ran on port `8000`.
*   **Task:** Securely allow the frontend to communicate with the API without creating security holes.
*   **Action:** In `main.py`, I configured FastAPI's `CORSMiddleware`. Crucially, I injected the `FRONTEND_URL` from an environment variable explicitly into the `allow_origins` array. This allowed it to dynamically support `http://localhost:3000` locally, while locking it down strictly to `https://redalert.my-domain.com` in production, completely avoiding using permissive, dangerous `allow_origins=["*"]` wildcards.
*   **Result:** Seamless cross-origin requests for the frontend while maintaining an ironclad back-end security posture.

---

## 6. Closing Advice
- **Acknowledge Trade-offs**: Perfect engineering doesn't exist. If asked why you didn't use an expensive machine-learning LLM instead of a heuristic NLP engine, emphasize speed, simplicity, predictable outcomes, and extreme cost-efficiency.
- **You are the Expert**: You built this full-stack project from the ground up—from scraping web endpoints to deploying a Dockerized Ubuntu VPS. Own that end-to-end expertise!
