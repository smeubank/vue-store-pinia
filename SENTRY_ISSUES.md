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

## Summary

| Issue | Type | Action |
|-------|------|--------|
| Supabase integration limited to JS | Feature Request | Tracked in [#85338](https://github.com/getsentry/sentry/issues/85338) |
| Deno logging docs missing | Documentation | Add Deno examples to logs docs |

---

**Repository:** This codebase demonstrates Sentry observability across Vue.js, FastAPI, and Supabase Edge Functions.
