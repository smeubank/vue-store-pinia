# Pineapple Paradise Store 🍍

A full-stack e-commerce demo application showcasing **Sentry observability** with **Supabase** backend services. This project demonstrates distributed tracing, structured logging, and error monitoring across a modern web application stack.

**Live Demo:** https://vue-store-pinia.vercel.app/

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

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/vue-store-pinia.git
   cd vue-store-pinia
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```

3. **Install backend dependencies:**
   ```bash
   pip3 install -r api/requirements.txt
   ```

4. **Set up environment variables:**

   Create `.env.local` in the project root:
   ```bash
   VITE_SUPABASE_URL=your_supabase_url
   VITE_SUPABASE_ANON_KEY=your_anon_key
   VITE_API_URL=http://localhost:8000
   PUBLIC_SENTRY_DSN=your_sentry_frontend_dsn
   ```

   Create `api/.env`:
   ```bash
   SUPABASE_URL=your_supabase_url
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   ```

5. **Deploy the Edge Function:**
   ```bash
   supabase login
   supabase link --project-ref your_project_ref
   supabase functions deploy create-order
   ```

6. **Run the application:**
   ```bash
   npm run dev
   ```
   This starts both the Vue frontend (port 5173) and FastAPI backend (port 8000).

---

## 📦 Database Schema

### `products`
```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  description TEXT,
  image TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### `orders`
```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  total NUMERIC(10,2) NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### `order_items`
```sql
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id),
  quantity INTEGER NOT NULL,
  price_at_purchase NUMERIC(10,2) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## 🧪 Testing the App

### 1. Product Catalog
- Visit http://localhost:5173
- Products load from Supabase database
- Images served from Supabase Storage
- Check console for data source logs

### 2. Shopping Cart
- Add items to cart (Pinia state)
- View cart at `/checkout`
- Sentry logs cart actions

### 3. Checkout Flow
- Click "Checkout" button
- Order sent to FastAPI → Edge Function → Database
- Check Sentry for distributed trace
- Verify order in Supabase dashboard

### 4. Authentication
- Click "Sign In with Google"
- OAuth flow via Supabase
- User session stored
- Avatar displayed in header

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `src/main.js` | Vue app initialization, Sentry/Supabase setup |
| `src/pages/ProductsPage.vue` | Product catalog with Supabase data |
| `src/pages/CheckoutPage.vue` | Shopping cart and checkout flow |
| `src/store/cart.js` | Pinia store for cart state |
| `api/main.py` | FastAPI backend with Sentry integration |
| `supabase/functions/create-order/` | Edge Function for order processing |
| `IMPLEMENTATION_PLAN.md` | Detailed project roadmap and progress |
| `SENTRY_V10_MIGRATION.md` | Sentry SDK v10 migration notes |

---

## 🐛 Known Issues & Limitations

See [SENTRY_ISSUES.md](./SENTRY_ISSUES.md) for documentation and SDK issues encountered during development.

---

## 🤝 Contributing

This is a demo/example repository. Feel free to:
- Open issues for questions
- Submit PRs for improvements
- Use as a template for your own projects

---

## 📄 License

MIT License - Feel free to use this for learning and demonstration purposes.

---

## 🙏 Acknowledgments

- **Sentry** for observability platform
- **Supabase** for backend services
- **Vercel** for frontend hosting
- **Vue.js** and **FastAPI** communities

---

## 📚 Additional Resources

- [Sentry Vue SDK Documentation](https://docs.sentry.io/platforms/javascript/guides/vue/)
- [Sentry Python SDK Documentation](https://docs.sentry.io/platforms/python/)
- [Sentry Deno SDK Documentation](https://docs.sentry.io/platforms/javascript/guides/deno/)
- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)

---

**Built with ❤️ for demonstrating modern observability practices**
