import logging
import os
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from urllib.parse import urlparse
import aiohttp
import json
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to filter out certain transactions
def filter_transactions(event, hint):
    url_string = event.get("request", {}).get("url", "")
    parsed_url = urlparse(url_string)

    # Filter out transactions for .jpg and .ico files
    if parsed_url.path.endswith(('.jpg', '.ico')):
        return None

    # Filter out transactions for specific paths like /healthcheck
    if parsed_url.path == "/healthcheck":
        return None

    return event

# Initialize Sentry with integrations and logging
sentry_sdk.init(
    dsn="https://b8233ed9639fc2fa0e0e5b1727ea893a@o673219.ingest.us.sentry.io/4508087188455424",
    enable_logs=True,  # Enable Sentry structured logs
    integrations=[
        FastApiIntegration(),
        StarletteIntegration(),
        LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        ),
    ],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    before_send_transaction=filter_transactions,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    logger.warning("⚠️ Supabase credentials not found in environment variables. Supabase features will be unavailable.")
    logger.warning("   Products will use FALLBACK static data")
    supabase: Client = None
else:
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("✅ Supabase client initialized successfully", extra={
            "supabase_url": supabase_url
        })
        logger.info("   Products will be fetched from Supabase database")
    except Exception as e:
        logger.error("❌ Failed to initialize Supabase client", extra={
            "error": str(e),
            "error_type": type(e).__name__
        })
        logger.error("   Products will use FALLBACK static data")
        supabase = None

app = FastAPI()

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI application starting up", extra={
        "environment": os.getenv("ENVIRONMENT", "development"),
        "port": os.getenv("PORT", 8000)
    })
    if supabase:
        logger.info("✅ Supabase integration: ACTIVE")
    else:
        logger.warning("⚠️ Supabase integration: DISABLED (using fallback data)")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure CORS with regex
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https://vue-store-pinia.*\.vercel\.app$|https://vue-store-pinia\.onrender\.com|http://localhost(:8000|:5173)?|http://127\.0\.0\.1(:8000)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["sentry-trace", "baggage", "*"],  # Include sentry-trace and baggage
)

# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Skip logging for static files and health checks
    if request.url.path.startswith("/static") or request.url.path == "/healthcheck":
        return await call_next(request)
    
    logger.info(f"Incoming request: {request.method} {request.url.path}", extra={
        "method": request.method,
        "path": request.url.path,
        "client_ip": request.client.host if request.client else "unknown"
    })
    
    response = await call_next(request)
    
    logger.info(f"Request completed: {request.method} {request.url.path} - {response.status_code}", extra={
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code
    })
    
    return response

# Fallback products data (used if Supabase is unavailable)
FALLBACK_PRODUCTS = [
    {"id": "1", "name": "Whole Pineapple", "price": 19.99, "image": "pineapple.jpg"},
    {"id": "2", "name": "Canned Pineapple", "price": 29.99, "image": "canned-pineapple.jpg"},
    {"id": "3", "name": "Pineapple Juice", "price": 39.99, "image": "pineapple-juice.jpg"},
    {"id": "4", "name": "Pineapple Sauce", "price": 49.99, "image": "pineapple-sauce.jpg"},
    {"id": "5", "name": "Sliced Pineapple", "price": 59.99, "image": "sliced-pineapple.jpg"},
    {"id": "6", "name": "Pineapple Bar Soap", "price": 69.99, "image": "pineapple-bar-soap.jpg"},
    {"id": "7", "name": "Pineapple State Flag", "price": 79.99, "image": "pineapple-state-flag.jpg"},
    {"id": "8", "name": "Pineapple Hat", "price": 89.99, "image": "pineapple-hat.jpg"},
]

@app.get("/products")
async def get_products(request: Request):
    client_host = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # Try to fetch from Supabase
    if supabase:
        try:
            logger.info("Fetching products from Supabase database", extra={
                "endpoint": "/products",
                "client_ip": client_host
            })
            
            # Fetch products from Supabase
            response = supabase.table("products").select("*").execute()
            
            # Transform data to match frontend expectations
            products = []
            for product in response.data:
                # Get public URL for the image from Supabase Storage
                image_url = supabase.storage.from_("product-images").get_public_url(product["image_path"])
                
                products.append({
                    "id": str(product["id"]),  # UUID to string
                    "name": product["name"],
                    "price": float(product["price"]),
                    "image": image_url,  # Full Supabase Storage URL
                    "description": product.get("description", "")
                })
            
            logger.info("✅ Products fetched from Supabase database successfully", extra={
                "product_count": len(products),
                "source": "supabase_database",
                "client_ip": client_host,
                "first_product_id": products[0]["id"] if products else None
            })
            
            # Add breadcrumb for Sentry
            sentry_sdk.add_breadcrumb(
                category='api',
                message='Products fetched from Supabase database',
                level='info',
                data={'product_count': len(products), 'source': 'supabase'}
            )
            
            # Return with custom header indicating source
            return JSONResponse(
                content=products,
                headers={"X-Data-Source": "supabase-database"}
            )
            
        except Exception as e:
            logger.error("Failed to fetch products from Supabase, falling back to static data", extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "client_ip": client_host
            })
            sentry_sdk.capture_exception(e)
            # Fall through to fallback data
    
    # Fallback to static data if Supabase is unavailable
    logger.warning("⚠️ Using fallback product data (not from Supabase)", extra={
        "product_count": len(FALLBACK_PRODUCTS),
        "source": "fallback",
        "reason": "supabase_unavailable" if not supabase else "supabase_error"
    })
    
    sentry_sdk.add_breadcrumb(
        category='api',
        message='Using fallback product data',
        level='warning',
        data={'product_count': len(FALLBACK_PRODUCTS), 'source': 'fallback'}
    )
    
    # Return with custom header indicating source
    return JSONResponse(
        content=FALLBACK_PRODUCTS,
        headers={"X-Data-Source": "fallback-static"}
    )

# Pydantic models for order creation
class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price_at_purchase: float

class CreateOrderRequest(BaseModel):
    user_id: str
    items: List[OrderItem]

@app.post("/orders")
async def create_order(order_request: CreateOrderRequest, request: Request):
    """
    Create a new order by calling Supabase Edge Function.
    This demonstrates distributed tracing: FastAPI -> Edge Function -> Supabase DB
    """
    client_host = request.client.host if request.client else "unknown"
    
    # Calculate total
    total = sum(item.quantity * item.price_at_purchase for item in order_request.items)
    
    logger.info("📝 Creating order via Edge Function", extra={
        "user_id": order_request.user_id,
        "item_count": len(order_request.items),
        "total": total,
        "client_ip": client_host
    })
    
    # Add breadcrumb for Sentry
    sentry_sdk.add_breadcrumb(
        category='order',
        message='Creating order via Edge Function',
        level='info',
        data={
            'user_id': order_request.user_id,
            'item_count': len(order_request.items),
            'total': total
        }
    )
    
    try:
        # Get Supabase Edge Function URL
        edge_function_url = f"{supabase_url}/functions/v1/create-order"
        
        # Prepare payload for Edge Function
        payload = {
            "user_id": order_request.user_id,
            "items": [item.dict() for item in order_request.items],
            "total": total
        }
        
        # Get Sentry trace headers for distributed tracing
        sentry_trace = sentry_sdk.Hub.current.scope.transaction.to_traceparent() if sentry_sdk.Hub.current.scope.transaction else None
        baggage = sentry_sdk.Hub.current.scope.transaction.to_baggage() if sentry_sdk.Hub.current.scope.transaction else None
        
        # Call Edge Function with tracing headers
        headers = {
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        
        # Add Sentry tracing headers if available
        if sentry_trace:
            headers["sentry-trace"] = sentry_trace
        if baggage:
            headers["baggage"] = baggage
        
        logger.info("🚀 Calling Edge Function", extra={
            "url": edge_function_url,
            "has_sentry_trace": sentry_trace is not None
        })
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                edge_function_url,
                json=payload,
                headers=headers
            ) as resp:
                response_data = await resp.json()
                
                if resp.status != 201:
                    error_msg = response_data.get('error', 'Unknown error from Edge Function')
                    logger.error("❌ Edge Function returned error", extra={
                        "status": resp.status,
                        "error": error_msg
                    })
                    raise HTTPException(status_code=resp.status, detail=error_msg)
                
                order_id = response_data.get('order', {}).get('id')
                
                logger.info("✅ Order created successfully via Edge Function", extra={
                    "order_id": order_id,
                    "user_id": order_request.user_id,
                    "total": total
                })
                
                # Add success breadcrumb
                sentry_sdk.add_breadcrumb(
                    category='order',
                    message='Order created successfully',
                    level='info',
                    data={
                        'order_id': order_id,
                        'total': total
                    }
                )
                
                return JSONResponse(
                    content=response_data,
                    status_code=201,
                    headers={"X-Order-Source": "edge-function"}
                )
                
    except aiohttp.ClientError as e:
        logger.error("❌ Failed to call Edge Function", extra={
            "error": str(e),
            "error_type": type(e).__name__
        })
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=503, detail="Failed to communicate with Edge Function")
    except Exception as e:
        logger.error("❌ Unexpected error creating order", extra={
            "error": str(e),
            "error_type": type(e).__name__
        })
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Failed to create order")

@app.get("/sentry-debug")
async def trigger_error(request: Request):
    client_host = request.client.host if request.client else "unknown"
    
    logger.warning("Sentry debug endpoint triggered - intentional error coming", extra={
        "endpoint": "/sentry-debug",
        "client_ip": client_host,
        "test": True
    })
    
    # Add breadcrumb before error
    sentry_sdk.add_breadcrumb(
        category='test',
        message='About to trigger intentional error',
        level='warning'
    )
    
    # Capture custom context
    sentry_sdk.set_context("debug_info", {
        "intentional": True,
        "test_type": "division_by_zero",
        "client_ip": client_host
    })
    
    division_by_zero = 1 / 0


# Replace with your actual Sentry host and project IDs
SENTRY_HOST = "o673219.ingest.us.sentry.io"
SENTRY_PROJECT_IDS = ["4508059881242624"]

@app.post("/tunnel")
async def sentry_tunnel(request: Request):
    try:
        # Read the raw bytes from the request body
        envelope_bytes = await request.body()
        
        # Decode bytes to string and split into lines
        envelope = envelope_bytes.decode('utf-8')
        pieces = envelope.split('\n')
        header_str = pieces[0]
        
        # Parse the envelope header as JSON
        header = json.loads(header_str)
        dsn = header.get('dsn', '')
        
        # Log the received DSN
        logger.debug("Received Sentry tunnel request", extra={
            "dsn": dsn,
            "envelope_size": len(envelope_bytes)
        })
        
        # Parse the DSN to extract hostname and project ID
        dsn_parsed = urlparse(dsn)
        hostname = dsn_parsed.hostname
        project_id = dsn_parsed.path.strip('/')
        
        # Validate the hostname and project ID
        if hostname != SENTRY_HOST:
            logger.error("Invalid Sentry hostname", extra={
                "received_hostname": hostname,
                "expected_hostname": SENTRY_HOST
            })
            raise Exception(f"Invalid Sentry hostname: {hostname}")
        
        if not project_id or project_id not in SENTRY_PROJECT_IDS:
            logger.error("Invalid Sentry project ID", extra={
                "received_project_id": project_id,
                "allowed_project_ids": SENTRY_PROJECT_IDS
            })
            raise Exception(f"Invalid Sentry project ID: {project_id}")
        
        # Construct the upstream Sentry URL
        upstream_sentry_url = f"https://{SENTRY_HOST}/api/{project_id}/envelope/"
        
        logger.debug("Forwarding envelope to Sentry", extra={
            "upstream_url": upstream_sentry_url,
            "project_id": project_id
        })
        
        # Forward the envelope to Sentry
        async with aiohttp.ClientSession() as session:
            async with session.post(
                upstream_sentry_url,
                data=envelope_bytes,
                headers={'Content-Type': 'application/x-sentry-envelope'}
            ) as resp:
                if resp.status != 200:
                    logger.error("Upstream Sentry returned error", extra={
                        "status_code": resp.status,
                        "project_id": project_id
                    })
                    raise Exception(f"Upstream Sentry returned status {resp.status}")
        
        logger.debug("Successfully forwarded to Sentry", extra={"project_id": project_id})
        # Return success response
        return Response(status_code=200)
    except Exception as e:
        logger.error("Error tunneling to Sentry", extra={
            "error": str(e),
            "error_type": type(e).__name__
        })
        return JSONResponse(content={'error': 'Error tunneling to Sentry'}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
