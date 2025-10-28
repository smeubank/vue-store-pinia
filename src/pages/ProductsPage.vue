<template>
  <div class="products-page">
    <div class="product-grid">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import * as Sentry from '@sentry/vue'

const products = ref([])

onMounted(async () => {
  try {
    // Use environment variable or default to localhost for development
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    console.log('Fetching products from API', baseUrl)
    Sentry.logger.info('Fetching products from API', { baseUrl })
    
    const response = await fetch(`${baseUrl}/products`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.status} ${response.statusText}`)
    }
    
    // Check data source from response header
    const dataSource = response.headers.get('X-Data-Source') || 'unknown'
    
    const data = await response.json();
    // Backend now returns full Supabase Storage URLs, no need to prepend path
    products.value = data;
    
    // Log data source clearly
    if (dataSource === 'supabase-database') {
      console.log('✅ Products loaded from SUPABASE DATABASE:', products.value.length, 'products')
      console.log('📦 Data source: Supabase Postgres + Storage')
    } else if (dataSource === 'fallback-static') {
      console.warn('⚠️ Products loaded from FALLBACK (static data):', products.value.length, 'products')
      console.warn('💡 Supabase is not connected or returned an error')
    } else {
      console.log('Products loaded:', products.value.length, 'products', '(source:', dataSource, ')')
    }
    
    console.log('Sample product:', products.value[0])
    console.log('Sample image URL:', products.value[0]?.image)
    
    Sentry.logger.info('Products loaded successfully', { 
      productCount: products.value.length,
      dataSource: dataSource,
      sampleImageUrl: products.value[0]?.image,
      firstProductId: products.value[0]?.id
    })
  } catch (error) {
    console.error('Failed to load products:', error.message)
    Sentry.logger.error(
      Sentry.logger.fmt`Failed to load products: ${error.message}`,
      { error: error.message, stack: error.stack }
    )
    throw error
  }
});
</script>

<style scoped>
.products-page {
  padding: 1rem;
  padding-top: 5rem;
  position: relative;
  z-index: 1;
  background: radial-gradient(
    circle at center,
    rgba(88, 236, 13, 0.1) 0%,
    transparent 70%
  );
  min-height: calc(100vh - 6rem);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  position: relative;
  z-index: 2;
}
</style>
