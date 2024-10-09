import logging
import os
from fastapi import FastAPI
import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Initialize Sentry
sentry_sdk.init(
    dsn="https://b8233ed9639fc2fa0e0e5b1727ea893a@o673219.ingest.us.sentry.io/4508087188455424",
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for tracing.
    # debug=True,
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific frontend domain
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
