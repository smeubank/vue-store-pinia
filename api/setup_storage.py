"""
Setup script to create Supabase storage bucket and upload product images.
Run this once to initialize storage: python api/setup_storage.py
"""

import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('api/.env')

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("Connected to Supabase!")
print(f"Project URL: {SUPABASE_URL}")

# Create storage bucket
BUCKET_NAME = "product-images"

def create_bucket():
    """Create the product-images storage bucket"""
    try:
        # Check if bucket exists
        buckets = supabase.storage.list_buckets()
        bucket_names = [b['name'] for b in buckets]
        
        if BUCKET_NAME in bucket_names:
            print(f"✓ Bucket '{BUCKET_NAME}' already exists")
            return True
        
        # Create bucket with public access
        result = supabase.storage.create_bucket(
            BUCKET_NAME,
            options={
                "public": True,
                "fileSizeLimit": 5242880,  # 5MB limit
                "allowedMimeTypes": ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            }
        )
        print(f"✓ Created bucket '{BUCKET_NAME}'")
        return True
    except Exception as e:
        print(f"✗ Error creating bucket: {e}")
        return False

def upload_images():
    """Upload product images from static/images/products/"""
    images_dir = Path("static/images/products")
    
    if not images_dir.exists():
        print(f"✗ Images directory not found: {images_dir}")
        return
    
    print(f"\nUploading images from {images_dir}...")
    
    image_files = list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
    
    if not image_files:
        print("✗ No image files found")
        return
    
    for image_path in image_files:
        try:
            # Read image file
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Upload to Supabase Storage
            file_path = f"products/{image_path.name}"
            
            result = supabase.storage.from_(BUCKET_NAME).upload(
                file_path,
                image_data,
                {
                    "content-type": "image/jpeg",
                    "x-upsert": "true"  # Overwrite if exists
                }
            )
            
            # Get public URL
            public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
            
            print(f"✓ Uploaded {image_path.name}")
            print(f"  URL: {public_url}")
            
        except Exception as e:
            print(f"✗ Error uploading {image_path.name}: {e}")

def set_bucket_policies():
    """Set storage policies for public read access"""
    print("\nSetting storage policies...")
    try:
        # Note: RLS policies need to be set via SQL in Supabase dashboard
        print("⚠ Storage policies must be configured in Supabase Dashboard:")
        print("  1. Go to Storage > Policies")
        print("  2. Enable RLS on storage.objects")
        print("  3. Add policy for public SELECT access:")
        print("     Name: 'Public Access for product images'")
        print("     Policy: bucket_id = 'product-images'")
        print("     Operation: SELECT")
        print("     Check: true")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    print("=" * 60)
    print("Supabase Storage Setup")
    print("=" * 60)
    
    # Step 1: Create bucket
    print("\n1. Creating storage bucket...")
    if not create_bucket():
        print("Failed to create bucket. Exiting.")
        return
    
    # Step 2: Upload images
    print("\n2. Uploading product images...")
    upload_images()
    
    # Step 3: Set policies (manual step)
    print("\n3. Configuring storage policies...")
    set_bucket_policies()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Configure storage policies in Supabase Dashboard")
    print("2. Test image access in your application")
    print("3. Update backend to fetch images from Supabase")

if __name__ == "__main__":
    main()

