# Sentry + Supabase Integration Issues

Issues encountered while building this full-stack demo with Sentry observability and Supabase.

**Related:** [getsentry/sentry#85338 - Sentry <> Supabase](https://github.com/getsentry/sentry/issues/85338)

---

## Issue 1: Supabase Integration Only Available for Next.js

**Status:** 🎯 Feature Request (tracked in [#85338](https://github.com/getsentry/sentry/issues/85338))

The `supabaseIntegration()` is only implemented for JavaScript (Next.js focus). Not available for:
- ❌ Python SDK
- ❌ Deno SDK  
- ❌ Vue SDK (exists but not documented)
- ❌ Other frameworks

**Current workaround:** Manual instrumentation using `Sentry.startSpan()` to wrap Supabase operations.

**What works:**
```javascript
// Vue - Integration exists!
Sentry.init({
  integrations: [
    Sentry.supabaseIntegration(supabase, Sentry, { tracing: true, errors: true })
  ]
})
```

**What doesn't exist:**
```python
# Python - No integration available
# Must manually wrap all supabase operations
```

---

## Issue 2: Missing Deno Structured Logging Docs

**Status:** 📝 Documentation Gap

[Sentry Logs documentation](https://docs.sentry.io/platforms/javascript/guides/vue/logs/) shows examples for Vue, React, Angular, but **not Deno**.

**Unclear:**
- Does `enableLogs: true` work in Deno?
- Is `Sentry.logger.info()` supported?
- How to configure console logging integration?

**Current workaround:**
```typescript
// Defensive check since it's undocumented
if (Sentry.logger) {
  Sentry.logger.info('Message', { attributes })
}
```

**Needed:** Add Deno to the structured logs documentation with Edge Function examples.

---

## Issue 3: Distributed Tracing Broken in Deno Edge Functions

**Status:** 🐛 SDK Bug

**Problem:** When calling a Deno Edge Function from FastAPI with `sentry-trace` and `baggage` headers, the trace **does not continue** - it creates a separate, disconnected trace.

**Expected:**
```
Single Trace:
  └─ Vue Frontend
      └─ FastAPI POST /orders
          └─ Edge Function create-order (continued)
              └─ Database operations
```

**Actual:**
```
Trace 1: Vue → FastAPI
Trace 2: Edge Function (disconnected)
```

**Evidence:** Sentry Issue #6980613071 - Error in Edge Function appears as standalone trace with no parent context.

**Attempted solutions:**
- `Sentry.continueTrace(req.headers)` - doesn't work/doesn't exist
- Manually parsing `sentry-trace` header - no API to set parent trace
- `Sentry.getActiveSpan()` - always returns undefined

**Questions for Sentry team:**
1. How to continue a trace from HTTP headers in Deno?
2. Does the Deno SDK support trace continuation at all?
3. Need example of distributed tracing: HTTP server → Edge Function

**Reproduction:** This repository demonstrates the issue - see `api/main.py` and `supabase/functions/create-order/index.ts`

---

## Summary

| Issue | Type | Action |
|-------|------|--------|
| Supabase integration limited to JS | Feature Request | Tracked in [#85338](https://github.com/getsentry/sentry/issues/85338) |
| Deno logging docs missing | Documentation | Add Deno examples to logs docs |
| Deno distributed tracing broken | Bug | Fix or document trace continuation API |

---

**Repository:** This codebase can be used to test and reproduce the distributed tracing issue.
