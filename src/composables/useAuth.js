import { ref, onMounted } from 'vue'
import { supabase } from '../main'
import * as Sentry from '@sentry/vue'

// Global auth state
const user = ref(null)
const session = ref(null)
const loading = ref(true)

export function useAuth() {
  const signInWithGoogle = async () => {
    try {
      console.log('Signing in with Google...')
      Sentry.logger.info('User initiated Google sign-in')
      
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin + '/auth/callback',
          queryParams: {
            access_type: 'offline',
            prompt: 'consent',
          },
        },
      })
      
      if (error) {
        console.error('Google sign-in error:', error)
        Sentry.logger.error(
          Sentry.logger.fmt`Google sign-in failed: ${error.message}`,
          { error: error.message }
        )
        throw error
      }
      
      console.log('Google sign-in initiated successfully')
      return data
    } catch (error) {
      console.error('Sign in error:', error)
      throw error
    }
  }

  const signOut = async () => {
    try {
      console.log('Signing out...')
      Sentry.logger.info('User signing out', { userId: user.value?.id })
      
      const { error } = await supabase.auth.signOut()
      
      if (error) {
        console.error('Sign out error:', error)
        Sentry.logger.error(
          Sentry.logger.fmt`Sign out failed: ${error.message}`,
          { error: error.message }
        )
        throw error
      }
      
      user.value = null
      session.value = null
      console.log('Signed out successfully')
      Sentry.logger.info('User signed out successfully')
    } catch (error) {
      console.error('Sign out error:', error)
      throw error
    }
  }

  const initializeAuth = async () => {
    try {
      loading.value = true
      
      // Get initial session
      const { data: { session: currentSession }, error } = await supabase.auth.getSession()
      
      if (error) {
        console.error('Error getting session:', error)
        Sentry.logger.error('Failed to get session', { error: error.message })
      }
      
      session.value = currentSession
      user.value = currentSession?.user ?? null
      
      if (user.value) {
        console.log('User is authenticated:', user.value.email)
        Sentry.setUser({
          id: user.value.id,
          email: user.value.email,
          username: user.value.user_metadata?.full_name || user.value.email,
        })
        Sentry.logger.info('User session restored', { 
          userId: user.value.id,
          email: user.value.email 
        })
      } else {
        console.log('No active session')
        Sentry.setUser(null)
      }
      
      // Listen for auth changes
      supabase.auth.onAuthStateChange((event, newSession) => {
        console.log('Auth state changed:', event)
        
        session.value = newSession
        user.value = newSession?.user ?? null
        
        if (user.value) {
          console.log('User logged in:', user.value.email)
          Sentry.setUser({
            id: user.value.id,
            email: user.value.email,
            username: user.value.user_metadata?.full_name || user.value.email,
          })
          Sentry.logger.info('User authenticated', { 
            event,
            userId: user.value.id,
            email: user.value.email 
          })
        } else {
          console.log('User logged out')
          Sentry.setUser(null)
          Sentry.logger.info('User session ended', { event })
        }
      })
      
    } catch (error) {
      console.error('Auth initialization error:', error)
      Sentry.logger.error('Auth initialization failed', { error: error.message })
    } finally {
      loading.value = false
    }
  }

  // Initialize on mount
  onMounted(() => {
    initializeAuth()
  })

  return {
    user,
    session,
    loading,
    signInWithGoogle,
    signOut,
    initializeAuth,
  }
}

