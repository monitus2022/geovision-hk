# Monitus GeoVision HK

An intelligent, production-grade **Multimodal Spatial-RAG (Retrieval-Augmented Generation) Engine** that maps street-level photographs to physical architectural footprints in Hong Kong's hyper-dense urban environments.

---

## Context
This is an **SLC (Simple, Lovable, Complete)** project. Do not propose bloated enterprise microservices. Focus on clean data contracts, strict error boundaries, and defensive spatial query logic. Prioritize localized scope (Quarry Bay / Eastern District) before city-wide data scalability.
---

## 🛠️ Tech Stack & Boundary System

| Layer | Technology | Key Engineering Guardrails |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) + Tailwind CSS | Must request Secure Context (`https://`) location sensors with `enableHighAccuracy: true`. Must capture `position.coords.accuracy`. |
| **Backend** | Python (FastAPI) | Async execution pools. Handles tight CORS whitelist constraints blocking unauthorized domain origins. |
| **Database** | PostgreSQL + PostGIS | Use geometric index-aware routing functions. Coordinates map explicitly to `(Longitude, Latitude)` axis order ($X, Y$). |
| **AI Orchestration** | Gemini Flash (Free Tier) or other compatible models to be tested, routed through OpenRouter | Ingests native unstructured visual assets + text candidate arrays. Enforces a zero-hallucination structured JSON output contract. |

---

## 📦 Repository Layout

```text
├── .github/workflows/
│   ├── etl-pipeline.yml   # Conditional scheduled cron tracking data modifications
│   ├── backend-ci.yml     # Fast API code linting and testing execution
│   └── frontend-cd.yml    # Continuous deployment flow to edge hosting platforms
├── data-etl/              # Python processing script manipulating massive GeoJSON streams
├── backend/               # Core FastAPI app handling routing logic and API client pools
├── frontend/              # Single-page interface tracking browser geo-sensor payloads
└── README.md              # Global project blueprint configuration
```

🛰️ Component Specifications & Implementations

1. Data ETL Pipeline (/data-etl)
- Upstream Source: HK Lands Department Building Footprints (CSDI Portal / data.gov.hk)
- Format: Geometry polygons populated with localized attribute labels (BuildingNameEN, BuildingNameTC, TopHeight, BaseHeight).
- Update Strategy: Semi-annual data frequency. Pipeline runs an idempotent HTTP check verifying ETag / Last-Modified headers to completely bypass data operations unless upstream records modify.
- Database Swapping: To prevent deployment race conditions or system crashes, data updates write to isolated staging tables (hk_buildings_staging) before firing an atomic, zero-downtime blue-green rename sequence inside a single SQL transaction block.

3. Backend Engine & Spatial Query Contract (/backend)
- The API accepts a multi-part payload consisting of user coordinate values, an image file, and accuracy values. It must execute the following operations sequentially:
  - Step A: Calculate Dynamic Search FootprintPrevent bad GPS signals from overwhelming system contexts by setting strict calculation constraints:$$\text{Search Radius} = \text{Clamp}(\text{Accuracy Meters}, \text{Min}=20.0, \text{Max}=150.0)$$
  - Step B: Execute PostGIS Spatial MatchQuery the closest physical boundaries without relying on arbitrary point centers:
```SQL
SELECT "BuildingNameEN", "BuildingNameTC", "TopHeight", "BaseHeight", "BuildingBlockType"
FROM hk_buildings
WHERE ST_DWithin(
    geom, 
    ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography, 
    :radius
)
ORDER BY ST_Distance(geom, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)::geography) ASC
LIMIT 5;
```
  - Step C: Inject Multimodal LLM Grounding ContextBundle matching rows into text strings and append them to system instructions alongside the image file. Force Gemini to output a strict JSON payload:JSON{
  "matched_building": "String or UNKNOWN",
  "confidence_score": 0.00,
  "visual_reasoning": "Detailed visual analysis cues tracking materials or shapes."
}

5. Frontend Application Layer (/frontend)
- Domain Anchor: Deployed to https://*.monitus.org subdomains.
- Sensor Tracking: Intercepts native browser hardware parameters through navigator.geolocation.
- Edge Case Handling: If accuracy_meters > 200, the UI must display a user prompt warning of urban signal degradation and provide localized fallback override mechanics.
