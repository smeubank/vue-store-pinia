<template>
  <div class="auth-callback">
    <div class="loading-container">
      <div class="spinner"></div>
      <p>{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../main'
import * as Sentry from '@sentry/vue'

const router = useRouter()
const message = ref('Completing sign in...')

onMounted(async () => {
  try {
    console.log('Auth callback page mounted')
    Sentry.logger.info('Processing auth callback')
    
    // Supabase automatically handles the OAuth callback
    // The session will be set via the onAuthStateChange listener
    const { data: { session }, error } = await supabase.auth.getSession()
    
    if (error) {
      console.error('Auth callback error:', error)
      Sentry.logger.error(
        Sentry.logger.fmt`Auth callback failed: ${error.message}`,
        { error: error.message }
      )
      message.value = 'Sign in failed. Redirecting...'
      setTimeout(() => router.push('/'), 2000)
      return
    }
    
    if (session) {
      console.log('Auth successful, user:', session.user.email)
      Sentry.logger.info('User authenticated via OAuth callback', {
        userId: session.user.id,
        email: session.user.email,
        provider: 'google'
      })
      message.value = 'Sign in successful! Redirecting...'
    } else {
      console.log('No session found in callback')
      message.value = 'Redirecting...'
    }
    
    // Redirect to home page after a brief delay
    setTimeout(() => {
      router.push('/')
    }, 1500)
    
  } catch (error) {
    console.error('Unexpected error in auth callback:', error)
    Sentry.logger.error('Unexpected auth callback error', { 
      error: error.message 
    })
    message.value = 'An error occurred. Redirecting...'
    setTimeout(() => router.push('/'), 2000)
  }
})
</script>

<style scoped>
.auth-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #e0d8b4, #f2f1e1);
}

.loading-container {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4285f4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

p {
  font-size: 1.1rem;
  color: #333;
  margin: 0;
}
</style>

