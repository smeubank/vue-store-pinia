import logging
import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse  # Add this import
import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from urllib.parse import urlparse
import aiohttp
import json

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

# Initialize Sentry with the filter
sentry_sdk.init(
    dsn="https://b8233ed9639fc2fa0e0e5b1727ea893a@o673219.ingest.us.sentry.io/4508087188455424",
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
    # debug=True,
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    before_send_transaction=filter_transactions,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

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

products = [
    {"id": 1, "name": "Whole Pineapple", "price": 19.99, "image": "pineapple.jpg"},
    {"id": 2, "name": "Canned Pineapple", "price": 29.99, "image": "canned-pineapple.jpg"},
    {"id": 3, "name": "Pineapple Juice", "price": 39.99, "image": "pineapple-juice.jpg"},
    {"id": 4, "name": "Pineapple Sauce", "price": 49.99, "image": "pineapple-sauce.jpg"},
    {"id": 5, "name": "Sliced Pineapple", "price": 59.99, "image": "sliced-pineapple.jpg"},
    {"id": 6, "name": "Pineapple Bar Soap", "price": 69.99, "image": "pineapple-bar-soap.jpg"},
    {"id": 7, "name": "Pineapple State Flag", "price": 79.99, "image": "pineapple-state-flag.jpg"},
    {"id": 8, "name": "Pineapple Hat", "price": 89.99, "image": "pineapple-hat.jpg"},
]

@app.get("/products")
async def get_products():
    logger.info("GET /products called")
    return products

@app.get("/sentry-debug")
async def trigger_error():
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
        logger.info(f"Received DSN: {dsn}")
        
        # Parse the DSN to extract hostname and project ID
        dsn_parsed = urlparse(dsn)
        hostname = dsn_parsed.hostname
        project_id = dsn_parsed.path.strip('/')
        
        # Validate the hostname and project ID
        if hostname != SENTRY_HOST:
            raise Exception(f"Invalid Sentry hostname: {hostname}")
        
        if not project_id or project_id not in SENTRY_PROJECT_IDS:
            raise Exception(f"Invalid Sentry project ID: {project_id}")
        
        # Construct the upstream Sentry URL
        upstream_sentry_url = f"https://{SENTRY_HOST}/api/{project_id}/envelope/"
        
        # Log the upstream URL
        logger.info(f"Forwarding to Sentry URL: {upstream_sentry_url}")
        
        # Forward the envelope to Sentry
        async with aiohttp.ClientSession() as session:
            async with session.post(
                upstream_sentry_url,
                data=envelope_bytes,
                headers={'Content-Type': 'application/x-sentry-envelope'}
            ) as resp:
                if resp.status != 200:
                    raise Exception(f"Upstream Sentry returned status {resp.status}")
        
        # Return success response
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error tunneling to Sentry: {e}")
        return JSONResponse(content={'error': 'Error tunneling to Sentry'}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
