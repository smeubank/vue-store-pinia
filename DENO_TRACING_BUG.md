# [Deno SDK] Distributed Tracing Broken in Edge Functions

**Issue for:** https://github.com/getsentry/sentry-javascript

---

## Description

The Deno SDK does not continue distributed traces when an Edge Function receives `sentry-trace` and `baggage` headers from an upstream service. Instead, it creates a new, disconnected trace.

---

## Environment

- **Deno SDK:** `@sentry/deno@^10.0.0`
- **Runtime:** Supabase Edge Functions (Deno 2.1.4)
- **Upstream Service:** FastAPI with `sentry-sdk[fastapi]@2.19.2`

---

## Expected Behavior

Edge Function should **continue the existing trace** as a child span:

```
Single Distributed Trace:
  └─ FastAPI POST /orders
      └─ Edge Function POST /create-order (continued)
          └─ Database operations
```

---

## Actual Behavior

Edge Function creates a **separate, disconnected trace**:

```
Trace 1:
  └─ FastAPI POST /orders

Trace 2 (disconnected):
  └─ Edge Function POST /create-order
      └─ Database operations
```

---

## Evidence

**Sentry Issue:** https://steven-eubank.sentry.io/issues/6980613071/?project=4510269126279168

**Details:**
- **Issue ID:** 6980613071
- **Date:** Oct 28, 2025
- **Execution IDs:** 
  - `2ca70f97-4407-48bb-aa5d-36212f40e920`
  - `1fe8e91b-d4e2-4524-a9a1-7dc827fc1e97`
- **Runtime:** Supabase Edge Runtime 1.69.4 (Deno 2.1.4)
- **Region:** eu-central-1
- **Service Tag:** `edge-function-create-order`

**The Problem:**
Errors in the Edge Function appear as **standalone events** in Sentry with no connection to the upstream trace:
- No parent span from FastAPI visible
- No distributed trace showing user flow: Frontend → FastAPI → Edge Function
- Appears isolated despite being triggered by HTTP request with trace headers
- Makes debugging user journeys impossible

**Example Error:**
```
Failed to create order: insert or update on table "orders" violates 
foreign key constraint "orders_user_id_fkey"
```

This error should appear **nested under** the FastAPI `/orders` span, showing the full context of:
- User ID attempting the order
- Cart contents from frontend
- FastAPI validation steps
- Then the Edge Function failure

Instead, it appears **disconnected**, losing all upstream context.

---

## Reproduction

### 1. Upstream Service (FastAPI) sends trace headers:

```python
import sentry_sdk
import aiohttp

# Get current trace context
sentry_trace = sentry_sdk.Hub.current.scope.transaction.to_traceparent()
baggage = sentry_sdk.Hub.current.scope.transaction.to_baggage()

headers = {
    "sentry-trace": sentry_trace,
    "baggage": baggage,
    "Content-Type": "application/json"
}

async with aiohttp.ClientSession() as session:
    await session.post(
        "https://project.supabase.co/functions/v1/create-order",
        json=payload,
        headers=headers
    )
```

### 2. Edge Function receives but doesn't use trace headers:

```typescript
import * as Sentry from 'npm:@sentry/deno@^10.0.0'

Sentry.init({
  dsn: '...',
  tracesSampleRate: 1.0,
})

Deno.serve(async (req) => {
  const sentryTrace = req.headers.get('sentry-trace')
  const baggage = req.headers.get('baggage')
  
  // ✅ Headers are present
  console.log({ sentryTrace, baggage })
  
  // ❌ But trace doesn't continue - creates new trace instead
  return await Sentry.startSpan({
    name: 'POST /create-order',
    op: 'function.edge',
    // No API to continue trace from headers?
  }, async (span) => {
    // ... function logic
  })
})
```

**Result:** New trace created, not connected to parent.

---

## What Doesn't Work

Attempted solutions:

```typescript
// 1. continueTrace() - doesn't exist or doesn't work
Sentry.startSpan({
  ...Sentry.continueTrace(req.headers),  // ❌
}, callback)

// 2. Manual header parsing - no API to set parent
const [traceId, parentSpanId] = sentryTrace.split('-')
Sentry.startSpan({
  traceId,  // ❌ Not accepted
  parentSpanId,  // ❌ Not accepted  
}, callback)

// 3. getActiveSpan() - returns undefined
const parent = Sentry.getActiveSpan()  // ❌ Always undefined
```

---

## Expected Solution

The SDK should **automatically detect and use** `sentry-trace` and `baggage` headers from incoming requests, similar to how other SDKs work.

**Or** provide a clear API:

```typescript
Deno.serve(async (req) => {
  return await Sentry.startSpanFromRequest(req, {
    name: 'POST /create-order',
    op: 'function.edge',
  }, async (span) => {
    // Trace continues automatically
  })
})
```

---

## Impact

- ❌ Distributed tracing completely broken for Edge Functions
- ❌ Cannot see full request flow across services
- ❌ Errors appear disconnected from user actions
- ❌ Performance monitoring incomplete

**This should work out-of-the-box.** Manual instrumentation is not a viable workaround.

---

## Reproduction Repository

https://github.com/your-username/vue-store-pinia

Files to check:
- `api/main.py` - FastAPI sending trace headers
- `supabase/functions/create-order/index.ts` - Edge Function not continuing trace
- `SENTRY_ISSUES.md` - Detailed analysis

---


