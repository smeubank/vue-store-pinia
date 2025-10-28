# Pineapple Paradise Store 🍍

A full-stack e-commerce demo application showcasing **Sentry observability** with **Supabase** backend services. This project demonstrates distributed tracing, structured logging, and error monitoring across a modern web application stack.

---

## 🎯 Purpose

This repository serves as a comprehensive example of:

1. **Distributed Tracing** across multiple services (Frontend → Backend → Edge Function → Database)
2. **Structured Logging** with Sentry's logging integration across all SDKs
3. **Error Monitoring** with Sentry capturing and tracking issues
4. **Supabase Integration** including Authentication, Storage, Database, and Edge Functions
5. **Full-Stack Observability** demonstrating how to monitor a modern web application

**Target Audience:**
- Developers learning Sentry observability features
- Engineers implementing distributed tracing
- Teams evaluating Supabase + Sentry integration
- Anyone building full-stack applications with observability

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- **Vue.js 3** - Progressive JavaScript framework
- **Pinia** - Vue state management
- **Vite** - Build tool and dev server
- **Sentry Vue SDK v10** - Error monitoring, tracing, and logs

**Backend:**
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Supabase Python SDK** - Database and storage client
- **Sentry Python SDK v2** - Backend observability

**Supabase Services:**
- **PostgreSQL Database** - Product catalog and order storage
- **Storage** - Product image hosting
- **Authentication** - Google OAuth integration
- **Edge Functions** - Serverless Deno runtime for order processing
  - **Sentry Deno SDK v10** - Edge function observability

**Deployment:**
- **Vercel** - Frontend hosting
- **Render** - FastAPI backend hosting
- **Supabase Cloud** - Managed Supabase services

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User's Browser                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Vue.js Frontend (Vite)                                       │  │
│  │  • Product catalog display                                    │  │
│  │  • Shopping cart (Pinia state)                                │  │
│  │  • Google OAuth login                                         │  │
│  │  • Sentry: Tracing, Logs, Error Capture                      │  │
│  └──────────────┬───────────────────────────────────────────────┘  │
└─────────────────┼───────────────────────────────────────────────────┘
                  │
                  │ HTTP Requests
                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FastAPI Backend (Python)                                           │
│  • GET /products - Fetch from Supabase DB                           │
│  • POST /orders - Forward to Edge Function                          │
│  • Sentry: Distributed tracing, logs, errors                        │
│  • Supabase Python SDK (service role)                               │
└──────────────┬──────────────────────────────────────────────────────┘
               │
               │ HTTP POST (with sentry-trace headers)
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Supabase Edge Function (Deno)                                      │
│  • create-order function                                            │
│  • Inserts order + order_items into DB                              │
│  • Sentry: Distributed tracing, logs, errors                        │
└──────────────┬──────────────────────────────────────────────────────┘
               │
               │ SQL INSERT via Supabase Client
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   Supabase Services                                  │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────┐  │
│  │  PostgreSQL    │  │    Storage      │  │   Authentication   │  │
│  │  • products    │  │  • product-     │  │   • Google OAuth   │  │
│  │  • orders      │  │    images       │  │   • User sessions  │  │
│  │  • order_items │  │    bucket       │  │                    │  │
│  └────────────────┘  └─────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Observability Features

### Distributed Tracing
**Complete trace across 4 layers:**
1. **Vue Frontend** - User clicks "Checkout"
2. **FastAPI Backend** - Receives order, calls Edge Function
3. **Edge Function** - Processes order logic
4. **Supabase DB** - Inserts order records

All connected in a single Sentry trace using `sentry-trace` and `baggage` headers.

### Structured Logging
**Logging at every step:**
- Vue: `Sentry.logger.info()`, `Sentry.logger.error()`
- FastAPI: Python `logging` module integrated with Sentry
- Edge Function: `Sentry.logger` with structured attributes

**Example logs:**
- Cart actions (add/remove items)
- Product fetching (Supabase vs fallback)
- Order validation
- Database operations
- Success/error states

### Error Monitoring
- Frontend errors captured with Session Replay
- Backend errors with stack traces
- Edge Function errors with execution context
- Automatic error grouping and alerts

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.9+
- **Supabase CLI** (for Edge Functions)
- **Supabase Project** with:
  - Google OAuth configured
  - Storage bucket: `product-images`
  - Database tables: `products`, `orders`, `order_items`
- **Sentry** 
  - Project per app: FE, BE, and Function

