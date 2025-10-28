# Implementation Plan: Supabase + Sentry Integration

## 📊 Progress Overview

### Completed ✅
- **Phase 1**: Sentry SDK updates and logging (Frontend + Backend)
- **Phase 2**: Supabase setup and Google OAuth configuration
- **Phase 3**: Frontend authentication UI and composables
- **Phase 3**: Products fetched from Supabase Database
- **Phase 3**: Images loaded from Supabase Storage
- **Phase 4**: Backend Supabase Python SDK integration
- **Phase 4**: `/products` endpoint fetches from Supabase DB
- **Phase 4**: `POST /orders` endpoint calls Edge Function
- **Phase 4**: Product images served via Supabase Storage public URLs
- **Phase 5**: Database schema and tables created (RLS intentionally skipped for advisor testing)
- **Phase 6**: Storage bucket created, images uploaded, public access enabled
- **Phase 7**: Edge Function for order creation with distributed tracing
- **Phase 8**: Comprehensive documentation

### In Progress ⏳
- **Phase 3**: Add protected routes (require auth for checkout)
- **Phase 5**: Apply RLS policies (after advisor testing)

### Deferred ⏸️
- **Phase 4**: JWT verification middleware (no protected endpoints yet)

### Newly Added ✨
- **Phase 7**: Edge Function for order creation with distributed tracing demo

### Next Steps 🎯
1. **Test Supabase Advisor**: Check if it detects missing RLS policies on products table
2. **Phase 5**: Apply RLS policies after confirming advisor warnings
3. **Phase 3**: Add protected routes (require auth for checkout)
4. **Phase 4**: Implement JWT verification when needed for protected endpoints
5. **Optional**: Add order creation endpoint
6. **Optional**: Add user profile endpoint

---

## Project Overview
This document outlines the plan to transform this demo repository from a Sentry-focused Vue + FastAPI application into a comprehensive demonstration of **Supabase features with Sentry observability** (tracing, errors, and logs).

---

## Current State Analysis

### Frontend (Vue 3 + Vite)
- **Framework**: Vue 3 with Pinia for state management
- **Sentry SDK**: `@sentry/vue` v8.37.0 (needs update)
- **Current Features**:
  - Product catalog display
  - Shopping cart (Pinia store)
  - Basic routing (Landing, Products, Checkout)
  - Sentry error tracking & replay

### Backend (FastAPI)
- **Framework**: FastAPI with uvicorn
- **Sentry SDK**: `sentry-sdk` (Python)
- **Current Features**:
  - Products API endpoint (in-memory data)
  - Static file serving for product images
  - Sentry tunnel endpoint for error forwarding
  - Error debug endpoint

---

## Proposed Architecture

### New Tech Stack
```
Frontend: Vue 3 + Pinia + Supabase JS SDK + Sentry Vue SDK (latest)
Backend: FastAPI + Supabase Python SDK + Sentry Python SDK (latest)
Services: Supabase (Auth, Storage, Database, Edge Functions) + Sentry (Errors, Tracing, Logs)
```

### Data Flow
```
User → Vue App → Supabase Auth (login/signup)
                ↓
         Authenticated requests to FastAPI
                ↓
         FastAPI → Supabase Storage (fetch product images)
                → Supabase Database (fetch product data)
                ↓
         Sentry captures: Errors, Traces, Logs
```

---

## Implementation Plan

### Phase 1: Update Sentry SDKs & Enable Logging ✅ COMPLETE

#### Frontend Updates
- [✅] Update `@sentry/vue` to v10.22.0
- [✅] Enable Sentry Logs with `enableLogs: true`
- [✅] Add `Sentry.logger` calls for key user actions (cart, products)
- [✅] Configure `consoleLoggingIntegration` for console logs
- [✅] Update trace propagation for Supabase requests
- [✅] Add Supabase integration to Sentry

**Questions for You:**
1. Do you want to keep the Sentry tunnel endpoint or use direct DSN?
- keep tunnel
2. What's your preferred log level strategy? (debug/info in dev, warn/error in prod?)
- none strictly, just want a good amount of logs, so i can test and demo loggind products across sentry, vercel, supabase, betterstack, and render
3. Should we implement `beforeSendLog` filtering?
- for now no, but i am curious about this feature for later

#### Backend Updates
- [✅] Update `sentry-sdk` to v2.19.2 with FastAPI integrations
- [✅] Enable logging integration for Python
- [✅] Add structured logging for API operations
- [✅] Add request middleware for comprehensive logging
- [✅] Remove deprecated `enable_tracing` option
- [⏳] Configure tracing for Supabase SDK calls (pending Phase 4)

**Questions for You:**
1. Should we keep the current tracing sample rates (100%)?
- yes
2. Any specific API endpoints that should NOT be traced?
- no

---

### Phase 2: Supabase Setup & Configuration ✅ COMPLETE

#### Prerequisites Needed from You:
- [✅] **Supabase Project Details**:
  - Project URL: `https://your-project.supabase.co`
  - Anon/Public Key (for frontend): `<your-supabase-anon-key>`
  - Service Role Key (for backend - secret!): `<your-service-role-key>`
  
- [✅] **Supabase Features to Configure**:
  - Auth providers to enable (email/password, OAuth providers?)
  - only google
  - Storage bucket name for product images
  - don't have one yet, never used this feature before
  - Database schema preferences
  - none, just logical and like what you;d see in the real world

#### Questions:
1. **Authentication**: Which auth methods do you want to demo?
   - [X] OAuth (Google, GitHub, etc.) - which providers? - i only want to do a simply google sign in really - https://supabase.com/docs/guides/auth/social-login/auth-google?queryGroups=platform&platform=web
   - keep it simple, so i can just test
   

2. **Storage**: How should we organize product images?
   - Suggested structure: `products/[product-id]/image.jpg`
   - i want to store the images in supabase
   - https://supabase.com/docs/guides/storage/quickstart?queryGroups=language&language=python
   - the pyhton app should fetch them
   - https://supabase.com/docs/reference/python/storage-createbucket 
   - Do you want to demo image transformations? not now

3. **Database**: Do you want to:
   - [yes] Store product catalog in Supabase Postgres
   - [no] Store user cart data (persisted carts) use pinia
   - [not now] Store order history
   - [yes] Demo Row Level Security (RLS) policies?

4. **Edge Functions**: Any specific backend logic to move to Edge Functions?
   - Suggested candidates:
     - [not yet i don't have this feature in the site] Product recommendations
     - [there is no real order processing is there?] Order processing
     - [ ] Webhook handlers
     - [yes] Image processing/validation

---

### Phase 3: Frontend Implementation ✅ COMPLETE (except protected routes)

#### User Authentication Flow
- [✅] Create auth UI components (Header with Sign In/Out, AuthCallbackPage)
- [✅] Implement Supabase Auth SDK integration (useAuth composable)
- [⏳] Add protected routes (require auth for checkout) - **DEFERRED**
- [✅] Display user info in header (avatar, name)
- [✅] Handle auth state changes (onAuthStateChange listener)
- [✅] Link Sentry user context with Supabase user

#### Supabase Integration
- [✅] Configure Supabase client with project credentials
- [✅] Fetch product data from Supabase Database (via backend API)
- [✅] Load product images from Supabase Storage (public URLs)
- [N/A] Persist cart to Supabase (skipped - using Pinia only)

#### Sentry Logging
- [✅] Log authentication events (login, logout, OAuth callback)
- [✅] Log cart operations (add/remove items with structured attributes)
- [✅] Log product fetching operations with data source indicator
- [✅] Log API errors with context
- [✅] Log data source (Supabase vs fallback) in frontend console

**Questions:**
1. Should cart data be stored only in Pinia (local) or synced to Supabase? local
2. Do you want a user profile page? no
3. Should we implement password reset flow? no

---

### Phase 4: Backend Implementation ✅ COMPLETE (except JWT verification)

#### Supabase Python SDK Integration
- [✅] Install `supabase-py` package (in requirements.txt)
- [✅] Configure Supabase client with service role key
- [✅] Create API endpoints that use Supabase:
  - ✅ `GET /products` - fetches from Supabase DB with fallback
  - ✅ Images served via Supabase Storage public URLs (no proxy needed)
  - ⏸️ `POST /orders` - save order to DB (deferred)
  - ⏸️ `GET /user/profile` - fetch user data (deferred)

#### Authentication Middleware
- [⏸️] Verify Supabase JWT tokens - **DEFERRED** (no protected endpoints yet)
- [⏸️] Extract user info from JWT - **DEFERRED**
- [⏸️] Protect endpoints that require auth - **DEFERRED**

#### Sentry Integration
- [✅] Add Sentry logging to all endpoints (request middleware)
- [✅] Capture Supabase client errors with fallback handling
- [✅] Add custom breadcrumbs for Supabase operations
- [✅] Link traces between frontend and backend (CORS configured)
- [✅] Log data source (Supabase vs fallback) with clear indicators
- [✅] Added X-Data-Source response header for verification

**Questions:**
1. Should FastAPI validate Supabase JWTs or trust the frontend?
2. Do you want FastAPI to query Supabase DB directly or use Edge Functions?
3. Any specific business logic to demonstrate?

---

### Phase 5: Database Schema & Migration ✅ TABLES CREATED | ⏳ RLS PENDING

#### Proposed Schema
```sql
-- Products table
CREATE TABLE products (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name text NOT NULL,
  description text,
  price numeric(10,2) NOT NULL,
  image_path text,
  created_at timestamp with time zone DEFAULT now()
);

-- Orders table
CREATE TABLE orders (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  total numeric(10,2) NOT NULL,
  status text DEFAULT 'pending',
  created_at timestamp with time zone DEFAULT now()
);

-- Order items table
CREATE TABLE order_items (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id uuid REFERENCES orders(id) ON DELETE CASCADE,
  product_id uuid REFERENCES products(id),
  quantity integer NOT NULL,
  price_at_purchase numeric(10,2) NOT NULL
);

-- Cart items (optional - for persistent carts)
CREATE TABLE cart_items (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  product_id uuid REFERENCES products(id),
  quantity integer NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  UNIQUE(user_id, product_id)
);
```

**Status:**
- [✅] Schema approved
- [✅] Tables created in Supabase
- [✅] 8 products seeded with UUIDs
- [❌] RLS policies NOT applied yet (intentionally - testing advisor detection)

#### Row Level Security (RLS) Policies
```sql
-- Example: Users can only see their own orders
CREATE POLICY "Users can view own orders" ON orders
  FOR SELECT USING (auth.uid() = user_id);

-- Example: Products are publicly readable
CREATE POLICY "Products are viewable by everyone" ON products
  FOR SELECT USING (true);
```

**Status:**
- [❌] RLS policies NOT applied yet
- **Testing Strategy**: Intentionally leaving RLS disabled to test Supabase advisor detection
- **TODO**: Apply RLS policies after testing advisor warnings

---

### Phase 6: Storage Setup ✅ COMPLETE

#### Bucket Configuration
- [✅] Created `api/setup_storage.py` script to automate setup
- [✅] Created `product-images` bucket in Supabase
- [✅] Uploaded all product images to bucket
- [✅] Enabled public access on bucket (not via RLS policy, just bucket setting)
- [N/A] Set up image transformation rules (not needed yet)

**Note on Public Access:**
- Bucket is marked as public in Supabase (bucket-level setting)
- No RLS policies configured on storage yet (storage.objects table)
- Images are accessible via public URLs
- Future: Can add storage RLS policies for more granular control

**Questions:**
1. Should I migrate all images from `/public` to Supabase Storage?
2. Do you want to demo:
   - [ ] Image uploads (user-generated content)?
   - [ ] Image transformations (resize, crop, optimize)?
   - [ ] Signed URLs (temporary access)?

---

### Phase 7: Edge Functions ✅ IMPLEMENTED - Order Creation

**Status:** Implemented for order creation with distributed tracing

**Use Case:** Order processing with distributed tracing demonstration

**Implementation:**
- [✅] Created `create-order` Edge Function (Deno/TypeScript)
- [✅] FastAPI calls Edge Function (service-to-service)
- [✅] Full Sentry integration in Edge Function (separate Sentry project)
- [✅] Distributed tracing: FastAPI → Edge Function → Supabase DB
- [✅] Comprehensive logging and breadcrumbs
- [✅] Database operations: INSERT orders + order_items
- [✅] Error handling with transaction rollback

**Key Features:**
- **Separate Sentry Project**: Edge Function has its own Sentry project for monitoring
- **Distributed Tracing**: Sentry trace headers propagated from FastAPI to Edge Function
- **Transaction Boundaries**: Clear transaction boundaries across services
- **Performance Monitoring**: Track Edge Function execution time and DB operations
- **Custom Tags**: Region and execution_id tagged in Sentry

**Technology:**
- Deno runtime (TypeScript first)
- Sentry Deno SDK v9.0.0
- Supabase JS SDK v2
- Deployed to Supabase Edge Runtime

**Files Created:**
- `supabase/functions/create-order/index.ts` - Edge Function code
- `supabase/functions/create-order/deno.json` - Deno configuration
- `EDGE_FUNCTION_SETUP.md` - Complete setup and deployment guide

**API Endpoints:**
- FastAPI: `POST /orders` - Accepts order request, calls Edge Function
- Edge Function: `POST /create-order` - Saves to database

**Other Potential Use Cases (Future):**
- Product Recommendations (personalized)
- Webhook handlers (Stripe, GitHub)
- Image processing/validation
- Real-time inventory updates

---

### Phase 8: Documentation Updates ✅ COMPLETE

#### README Updates
- [✅] Created IMPLEMENTATION_PLAN.md with comprehensive plan
- [✅] Created PHASE_1_2_SUMMARY.md with completion status
- [✅] Created QUICKSTART.md with setup instructions
- [✅] Created AUTH_TESTING_GUIDE.md for auth flow testing
- [✅] Created SUPABASE_SETUP.md with credentials and configuration
- [⏳] Update main README.md (pending final implementation)
- [⏳] Architecture diagram (pending final architecture)
- [⏳] Screenshots/GIFs (pending after Phase 3-4 completion)

**Questions:**
1. Do you want me to create an architecture diagram (Mermaid/ASCII)?
2. Should we include troubleshooting section?
3. Any specific callouts for Supabase employees viewing this?

---

## Environment Variables Needed

### Frontend (`.env`)
```bash
# Supabase
VITE_SUPABASE_URL=https://[PROJECT_REF].supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...

# Sentry
VITE_SENTRY_DSN=https://...@sentry.io/...
VITE_SENTRY_AUTH_TOKEN=... # for sourcemaps upload
VITE_SENTRY_ORG=...
VITE_SENTRY_PROJECT=...

# API
VITE_API_URL=http://localhost:8000
```

### Backend (`.env`)
```bash
# Supabase
SUPABASE_URL=https://[PROJECT_REF].supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ... # KEEP SECRET!

# Sentry
SENTRY_DSN=https://...@sentry.io/...

# App
PORT=8000
```

**Questions:**
1. Should I create `.env.example` files?
2. Do you want separate configs for dev/staging/prod?

---

## Testing Strategy

### Frontend Tests
- [ ] Auth flow tests (login, signup, logout)
- [ ] Cart operations with Pinia
- [ ] Protected route access
- [ ] Supabase integration tests

### Backend Tests
- [ ] API endpoint tests
- [ ] Supabase client integration tests
- [ ] JWT validation tests
- [ ] Error handling tests

**Questions:**
1. How comprehensive should testing be?
2. Should we add E2E tests (Playwright/Cypress)?

---

## Deployment Considerations

### Current Deployment
- Frontend: Vercel (vue-store-pinia.vercel.app)
- Backend: Render (vue-store-pinia.onrender.com)

### Updated Deployment Needs
- [ ] Add Supabase environment variables to Vercel
- [ ] Add Supabase environment variables to Render
- [ ] Configure Sentry releases/sourcemaps
- [ ] Update CORS settings for Supabase

**Questions:**
1. Keep current deployment platforms?
2. Should we use Supabase Edge Functions instead of FastAPI for some endpoints?

---

## Timeline Estimate

| Phase | Estimated Time |
|-------|---------------|
| Phase 1: Sentry SDK updates | 2-3 hours |
| Phase 2: Supabase setup | 1-2 hours |
| Phase 3: Frontend implementation | 6-8 hours |
| Phase 4: Backend implementation | 4-6 hours |
| Phase 5: Database schema | 2-3 hours |
| Phase 6: Storage setup | 2-3 hours |
| Phase 7: Edge Functions (optional) | 3-5 hours |
| Phase 8: Documentation | 3-4 hours |
| **Total** | **23-34 hours** |

---

## Priority Questions to Answer

### Critical (Need to start):
1. ✅ **Supabase Project Credentials**: URL, anon key, service role key
2. ✅ **Auth Methods**: Which providers to enable?
3. ✅ **Database Schema**: Approve or modify proposed schema?
4. ✅ **Storage Strategy**: Public or private? Migrate all images?

### Important (Need for full implementation):
5. ✅ **Cart Persistence**: Local only or sync to Supabase?
6. ✅ **Edge Functions**: Which use case to demo?
7. ✅ **RLS Policies**: Which security features to showcase?
8. ✅ **Sentry Configuration**: Log levels, sampling rates, filtering?

### Nice-to-have (Can decide later):
9. ⚪ Image transformations demo?
10. ⚪ User profile page?
11. ⚪ Order history?
12. ⚪ E2E testing?

---

## Next Steps

Once you provide answers to the priority questions above, I will:
1. Create a detailed task list and todos
2. Begin implementation phase by phase
3. Update you after each major milestone
4. Ensure all code is well-documented and follows best practices

**Please review this plan and provide:**
- Supabase credentials (via environment variables or .env file structure)
- Answers to the priority questions
- Any modifications to the proposed architecture
- Any additional features you'd like to demonstrate

---

## Notes
- All existing Sentry functionality will be preserved and enhanced
- Current product catalog and images will be migrated to Supabase
- The demo will showcase real-world integration patterns
- Code will be production-ready with proper error handling
- Documentation will be clear for both Supabase and non-Supabase developers

