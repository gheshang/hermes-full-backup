---
name: productivity-integrations
description: Productivity API integrations — Airtable records CRUD, Notion pages/databases, Google Workspace (Gmail/Calendar/Drive/Sheets/Docs), and location intelligence (geocoding, routing, POI search).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Airtable, Notion, Google-Workspace, Maps, API, Productivity, Database, Email, Calendar, Location]
    related_skills: []
---

# Productivity Integrations — Unified Guide

This umbrella skill consolidates all productivity API integrations. Each tool connects to a different service:

- **airtable**: Airtable REST API for records CRUD
- **notion**: Notion API for pages, databases, blocks
- **google-workspace**: Gmail, Calendar, Drive, Sheets, Docs
- **maps**: Location intelligence (geocoding, routing, POI search)

**Choose your integration based on the service:**

| Service | Tool | Auth |
|---------|------|------|
| Airtable | airtable | Personal Access Token (PAT) |
| Notion | notion | API key (`ntn_` or `secret_`) |
| Google Workspace | google-workspace | OAuth2 |
| Maps/Location | maps | None (free, OpenStreetMap) |

---

## 1. Airtable

### Overview

Airtable REST API via curl. Records CRUD, filters, upserts. No MCP server, no OAuth flow, no Python SDK — just curl and a personal access token.

### Prerequisites

1. Create **Personal Access Token (PAT)** at https://airtable.com/create/tokens (tokens start with `pat...`)
2. Grant scopes:
   - `data.records:read` — read rows
   - `data.records:write` — create/update/delete rows
   - `schema.bases:read` — list bases and tables
3. Add each base to token's **Access** list (PATs are scoped per-base)
4. Store in `${HERMES_HOME:-~/.hermes}/.env`:
   ```
   AIRTABLE_API_KEY=pat_your_token_here
   ```

**Note:** Legacy `key...` API keys deprecated Feb 2024. Only PATs and OAuth tokens work.

### API Basics

- **Endpoint:** `https://api.airtable.com/v0`
- **Auth header:** `Authorization: Bearer $AIRTABLE_API_KEY`
- **All requests:** JSON (`Content-Type: application/json` for POST/PATCH/PUT)
- **Object IDs:** bases `app...`, tables `tbl...`, records `rec...`, fields `fld...`
- **Rate limit:** 5 requests/sec/base. `429` → back off.

```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=5" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

### Field Types (Write Shapes)

| Field type | Write shape |
|------------|-------------|
| Single line text | `"Name": "hello"` |
| Long text | `"Notes": "multi\nline"` |
| Number | `"Score": 42` |
| Checkbox | `"Done": true` |
| Single select | `"Status": "Todo"` (name must exist unless `typecast: true`) |
| Multi-select | `"Tags": ["urgent", "bug"]` |
| Date | `"Due": "2026-04-01"` |
| DateTime (UTC) | `"At": "2026-04-01T14:30:00.000Z"` |
| URL / Email / Phone | `"Link": "https://…"` |
| Attachment | `"Files": [{"url": "https://…"}]` |
| Linked record | `"Owner": ["recXXXXXXXXXXXXXX"]` |
| User | `"AssignedTo": {"id": "usrXXXXXXXXXXXXXX"}` |

Pass `"typecast": true` to let Airtable auto-coerce values.

### Common Queries

**List bases:**
```bash
curl -s "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**List tables + schema:**
```bash
curl -s "https://api.airtable.com/v0/meta/bases/$BASE_ID/tables" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**List records:**
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=10" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**Get single record:**
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**Filter records (filterByFormula):**
```bash
FORMULA="{Status}='Todo'"
ENC=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$FORMULA")
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?filterByFormula=$ENC&maxRecords=20" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**Formula patterns:**
- Exact match: `{Email}='user@example.com'`
- Contains: `FIND('bug', LOWER({Title}))`
- Multiple conditions: `AND({Status}='Todo', {Priority}='High')`
- Or: `OR({Owner}='alice', {Owner}='bob')`
- Not empty: `NOT({Assignee}='')`
- Date comparison: `IS_AFTER({Due}, TODAY())`

**Sort + select fields:**
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?sort%5B0%5D%5Bfield%5D=Priority&sort%5B0%5D%5Bdirection%5D=asc&fields%5B%5D=Name&fields%5B%5D=Status" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**Use named view:**
```bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?view=Grid%20view&maxRecords=50" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

### Common Mutations

**Create record:**
```bash
curl -s -X POST "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Name":"New task","Status":"Todo","Priority":"High"}}' | python3 -m json.tool
```

**Create up to 10 records (batch):**
```bash
curl -s -X POST "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "typecast": true,
    "records": [
      {"fields": {"Name": "Task A", "Status": "Todo"}},
      {"fields": {"Name": "Task B", "Status": "In progress"}}
    ]
  }' | python3 -m json.tool
```

**Update record (PATCH — merges):**
```bash
curl -s -X PATCH "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fields":{"Status":"Done"}}' | python3 -m json.tool
```

**Upsert by merge field:**
```bash
curl -s -X PATCH "https://api.airtable.com/v0/$BASE_ID/$TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "performUpsert": {"fieldsToMergeOn": ["Email"]},
    "records": [{"fields": {"Email": "user@example.com", "Status": "Active"}}]
  }' | python3 -m json.tool
```

**Delete record:**
```bash
curl -s -X DELETE "https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

**Delete up to 10 records:**
```bash
curl -s -X DELETE "https://api.airtable.com/v0/$BASE_ID/$TABLE?records%5B%5D=rec1&records%5B%5D=rec2" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -m json.tool
```

### Pagination

List endpoints return max 100 records per page. Loop with `offset`:

```bash
OFFSET=""
while :; do
  URL="https://api.airtable.com/v0/$BASE_ID/$TABLE?pageSize=100"
  [ -n "$OFFSET" ] && URL="$URL&offset=$OFFSET"
  RESP=$(curl -s "$URL" -H "Authorization: Bearer $AIRTABLE_API_KEY")
  echo "$RESP" | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(r["id"], r["fields"].get("Name","")) for r in d["records"]]'
  OFFSET=$(echo "$RESP" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("offset",""))')
  [ -z "$OFFSET" ] && break
done
```

### Hermes Workflow

1. **Confirm auth:** `curl -s -o /dev/null -w "%{http_code}\n" https://api.airtable.com/v0/meta/bases -H "Authorization: Bearer $AIRTABLE_API_KEY"` — expect `200`
2. **Find base:** List bases OR ask user for `app...` ID
3. **Inspect schema:** `GET /v0/meta/bases/$BASE_ID/tables` — cache field names
4. **Read before write:** For "update X where Y", `filterByFormula` first to resolve `rec...` ID
5. **Batch writes:** Combine creates into one 10-record POST
6. **Destructive ops:** Deletions can't be undone. Confirm before firing.

### Pitfalls

- **`filterByFormula` MUST be URL-encoded.** Use Python `urllib.parse.quote` — never hand-escape.
- **Empty fields omitted from responses.** Missing key doesn't mean field missing — check schema.
- **PATCH vs PUT.** `PATCH` merges. `PUT` replaces entirely. Default to `PATCH`.
- **Single-select options must exist.** Write `typecast: true` to auto-create.
- **Per-base token scoping.** `403` on one base means token's Access list doesn't include it.
- **Rate limits per base.** 5 req/sec on baseA and 5 on baseB is fine; 6 on baseA alone throttles.

---

## 2. Notion

### Overview

Notion API for creating and managing pages, databases, and blocks via curl. Search, create, update, and query workspaces.

### Prerequisites

1. Create integration at https://notion.so/my-integrations
2. Copy API key (starts with `ntn_` or `secret_`)
3. Store in `~/.hermes/.env`:
   ```
   NOTION_API_KEY=ntn_your_key_here
   ```
4. **Important:** Share target pages/databases with your integration in Notion (click "..." → "Connect to" → integration name)

### API Basics

```bash
curl -s -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

**Note:** API version `2025-09-03` is latest. Databases are called "data sources" in this version.

### Common Operations

**Search:**
```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

**Get page:**
```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**Get page content (blocks):**
```bash
curl -s "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**Create page in database:**
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

**Query database:**
```bash
curl -s -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

**Create database:**
```bash
curl -s -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

**Update page properties:**
```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

**Add content to page:**
```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello from Hermes!"}}]}}
    ]
  }'
```

### Property Types

| Type | Format |
|------|--------|
| Title | `{"title": [{"text": {"content": "..."}}]}` |
| Rich text | `{"rich_text": [{"text": {"content": "..."}}]}` |
| Select | `{"select": {"name": "Option"}}` |
| Multi-select | `{"multi_select": [{"name": "A"}, {"name": "B"}]}` |
| Date | `{"date": {"start": "2026-01-15", "end": "2026-01-16"}}` |
| Checkbox | `{"checkbox": true}` |
| Number | `{"number": 42}` |
| URL | `{"url": "https://..."}` |
| Email | `{"email": "user@example.com"}` |
| Relation | `{"relation": [{"id": "page_id"}]}` |

### API Version 2025-09-03 Key Differences

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries
- **Two IDs:** Each database has `database_id` and `data_source_id`
  - Use `database_id` when creating pages
  - Use `data_source_id` when querying
- **Search results:** Databases return as `"object": "data_source"` with `data_source_id`

### Notes

- Page/database IDs are UUIDs (with or without dashes)
- Rate limit: ~3 requests/second average
- API cannot set database view filters — UI-only
- Use `is_inline: true` when creating data sources to embed in pages
- Add `-s` flag to curl to suppress progress bars

---

## 3. Google Workspace

### Overview

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — through Hermes-managed OAuth2. Prefers Google Workspace CLI (`gws`) when available, falls back to Python client libraries.

### Prerequisites

1. **OAuth2 setup** — run `python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py`
2. Create Google Cloud OAuth client (Desktop app)
3. Enable APIs: Gmail, Calendar, Drive, Sheets, Docs, People

### Setup Questions

**Question 1: What services do you need?**
- **Email only** → Use `himalaya` skill instead (Gmail App Password, no Google Cloud project needed)
- **Email + Calendar** → `--services email,calendar`
- **Calendar/Drive/Sheets/Docs only** → `--services calendar,drive,sheets,docs`
- **Full Workspace** → `--services all`

**Question 2: Advanced Protection?**
- If yes, Workspace admin must allowlist OAuth client ID

### Setup Steps

**Step 2: Create OAuth credentials**
1. Create/select project: https://console.cloud.google.com/projectselector2/home/dashboard
2. Enable required APIs: https://console.cloud.google.com/apis/library
3. Create OAuth client: https://console.cloud.google.com/apis/credentials → OAuth 2.0 Client ID → Desktop app
4. Download JSON file

**Step 3: Get authorization URL**
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py \
  --auth-url --services email,calendar --format json
```

**Step 4: Exchange code**
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py \
  --auth-code "THE_URL_OR_CODE" --format json
```

**Step 5: Verify**
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py --check
# Should print AUTHENTICATED
```

### Usage

**Gmail:**
```bash
# Search
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail search "is:unread" --max 10
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail search "from:boss@company.com newer_than:1d"

# Read
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail get MESSAGE_ID

# Send
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail send --to user@example.com --subject "Hello" --body "Message text"

# Reply
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail reply MESSAGE_ID --body "Thanks, that works."

# Labels
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail labels
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py gmail modify MESSAGE_ID --add-labels LABEL_ID
```

**Calendar:**
```bash
# List events (next 7 days)
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py calendar list

# Create event (ISO 8601 with timezone)
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py calendar create \
  --summary "Team Standup" \
  --start "2026-03-01T10:00:00-06:00" \
  --end "2026-03-01T10:30:00-06:00"
```

**Drive:**
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py drive search "quarterly report" --max 10
```

**Contacts:**
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py contacts list --max 20
```

**Sheets:**
```bash
# Read
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py sheets get SHEET_ID "Sheet1!A1:D10"

# Write
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# Append rows
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

**Docs:**
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/google_api.py docs get DOC_ID
```

### Rules

1. **Never send email or create/delete events without confirming with user first.**
2. **Check auth before first use** — run `setup.py --check`
3. **Use Gmail search syntax reference** for complex queries
4. **Calendar times must include timezone** — always use ISO 8601 with offset
5. **Respect rate limits** — avoid rapid-fire sequential API calls

### Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 |
| `REFRESH_FAILED` | Token revoked/expired — redo Steps 3-5 |
| `HttpError 403: Insufficient Permission` | Missing scope — redo setup |
| `HttpError 403: Access Not Configured` | API not enabled — enable in Google Cloud Console |
| Advanced Protection blocks auth | Workspace admin must allowlist OAuth client |

### Revoking Access
```bash
python ${HERMES_HOME}/skills/productivity/google-workspace/scripts/setup.py --revoke
```

---

## 4. Maps (Location Intelligence)

### Overview

Geocode, reverse-geocode, find nearby places (46 POI categories), driving/walking/cycling distance + time, turn-by-turn directions, timezone lookup, bounding box + area, POI search within rectangle.

**Free, no API key.** Uses OpenStreetMap + Overpass + OSRM.

### Prerequisites

Python 3.8+ (stdlib only — no pip installs needed).

Script: `~/.hermes/skills/maps/scripts/maps_client.py`

```bash
MAPS=~/.hermes/skills/maps/scripts/maps_client.py
```

### Commands

**Search (geocode):**
```bash
python3 $MAPS search "Eiffel Tower"
python3 $MAPS search "1600 Pennsylvania Ave, Washington DC"
```
Returns: lat, lon, display name, type, bounding box, importance.

**Reverse (coordinates to address):**
```bash
python3 $MAPS reverse 48.8584 2.2945
```
Returns: full address breakdown (street, city, state, country, postcode).

**Nearby (find places):**
```bash
# By coordinates
python3 $MAPS nearby 48.8584 2.2945 restaurant --limit 10
python3 $MAPS nearby 40.7128 -74.0060 hospital --radius 2000

# By address (auto-geocodes)
python3 $MAPS nearby --near "Times Square, New York" --category cafe
python3 $MAPS nearby --near "90210" --category pharmacy

# Multiple categories
python3 $MAPS nearby --near "downtown austin" --category restaurant --category bar --limit 10
```

**46 categories:** restaurant, cafe, bar, hospital, pharmacy, hotel, camp_site, supermarket, atm, gas_station, parking, museum, park, school, university, bank, police, fire_station, library, airport, train_station, bus_stop, church, mosque, synagogue, dentist, doctor, cinema, theatre, gym, swimming_pool, post_office, convenience_store, bakery, bookshop, laundry, car_wash, car_rental, bicycle_rental, taxi, veterinary, zoo, playground, stadium, nightclub.

**Distance:**
```bash
python3 $MAPS distance "Paris" --to "Lyon"
python3 $MAPS distance "New York" --to "Boston" --mode driving
python3 $MAPS distance "Big Ben" --to "Tower Bridge" --mode walking
```
Modes: driving (default), walking, cycling.

**Directions:**
```bash
python3 $MAPS directions "Eiffel Tower" --to "Louvre Museum" --mode walking
python3 $MAPS directions "JFK Airport" --to "Times Square" --mode driving
```
Returns numbered steps with instruction, distance, duration, road name, maneuver type.

**Timezone:**
```bash
python3 $MAPS timezone 48.8584 2.2945
python3 $MAPS timezone 35.6762 139.6503
```
Returns: timezone name, UTC offset, current local time.

**Area (bounding box):**
```bash
python3 $MAPS area "Manhattan, New York"
python3 $MAPS area "London"
```
Returns: bounding box coordinates, width/height in km, approximate area.

**BBox (search within rectangle):**
```bash
python3 $MAPS bbox 40.75 -74.00 40.77 -73.98 restaurant --limit 20
```

### Working With Telegram Location Pins

Extract lat/lon from message and pass to `nearby`:

```bash
# User sent pin at 36.17, -115.14, asked "find cafes nearby"
python3 $MAPS nearby 36.17 -115.14 cafe --radius 1500
```

Present results with names, distances, and `maps_url` for tap-to-open.

For "open now?" questions, check `hours` field; if missing/unclear, verify with `web_search`.

### Workflow Examples

**"Find Italian restaurants near Colosseum":**
```bash
python3 $MAPS nearby --near "Colosseum Rome" --category restaurant --radius 500
```

**"What's near this location pin?":**
1. Extract lat/lon from message
2. `nearby LAT LON cafe --radius 1500`

**"How do I walk from hotel to conference center?":**
```bash
python3 $MAPS directions "Hotel Name" --to "Conference Center" --mode walking
```

**"What restaurants in downtown Seattle?":**
1. `python3 $MAPS area "Downtown Seattle"` → get bounding box
2. `python3 $MAPS bbox S W N E restaurant --limit 30`

### Pitfalls

- Nominatim ToS: max 1 req/s (handled automatically)
- `nearby` requires lat/lon OR `--near "<address>"` — one of two needed
- OSRM routing coverage best for Europe and North America
- Overpass API can be slow during peak hours (script falls back between mirrors)
- `distance` and `directions` use `--to` flag for destination (not positional)
- Zip code alone may give ambiguous results globally — include country/state

### Verification

```bash
python3 ~/.hermes/skills/maps/scripts/maps_client.py search "Statue of Liberty"
# Should return lat ~40.689, lon ~-74.044

python3 ~/.hermes/skills/maps/scripts/maps_client.py nearby --near "Times Square" --category restaurant --limit 3
# Should return restaurants within ~500m
```

---

## Quick Reference

| Service | Auth | Key Command |
|---------|------|-------------|
| Airtable | PAT (`pat...`) | `curl -H "Authorization: Bearer $AIRTABLE_API_KEY" https://api.airtable.com/v0/$BASE/$TABLE` |
| Notion | API key (`ntn_`) | `curl -H "Authorization: Bearer $NOTION_API_KEY" https://api.notion.com/v1/search` |
| Google Workspace | OAuth2 | `python scripts/google_api.py gmail search "is:unread"` |
| Maps | None | `python3 $MAPS nearby --near "Times Square" --category restaurant` |

---

## Pitfalls Summary

1. **Airtable:** `filterByFormula` MUST be URL-encoded. Per-base token scoping. Rate limits per base.
2. **Notion:** Share pages/databases with integration. Two IDs per database (`database_id` vs `data_source_id`).
3. **Google Workspace:** Email-only → use `himalaya` instead (simpler). Always confirm before sending.
4. **Maps:** `nearby` requires lat/lon OR `--near`. OSRM coverage best for Europe/North America.