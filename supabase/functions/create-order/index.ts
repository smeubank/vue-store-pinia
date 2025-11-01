import * as Sentry from 'npm:@sentry/deno@^10.0.0'
import { createClient } from 'npm:@supabase/supabase-js@2'

// Initialize Sentry (v10 - updated from v9)
Sentry.init({
  dsn: 'https://2063cf707cf29518cc1016545dfc0b0a@o673219.ingest.us.sentry.io/4510269126279168',
  defaultIntegrations: false,
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  sendDefaultPii: true,
  // v10 change: enableLogs is now a top-level option (was _experiments.enableLogs in v9)
  enableLogs: true,
  debug: true,
})

// Set region and execution_id as custom tags
Sentry.setTag('service', 'edge-function-create-order')
Sentry.setTag('region', Deno.env.get('SB_REGION') || 'unknown')
Sentry.setTag('execution_id', Deno.env.get('SB_EXECUTION_ID') || 'unknown')

// Create Supabase client using built-in environment variables
// Supabase automatically provides SUPABASE_URL in edge runtime
const supabaseUrl = Deno.env.get('SUPABASE_URL')
const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')

// Check for required environment variables
if (!supabaseUrl || !supabaseServiceKey) {
  const errorMsg = 'Missing required environment variables'
  console.error('❌ Configuration error:', {
    hasSupabaseUrl: !!supabaseUrl,
    hasServiceKey: !!supabaseServiceKey
  })
  
  if (Sentry.logger) {
    Sentry.logger.error('Edge function configuration error', {
      error: errorMsg,
      hasSupabaseUrl: !!supabaseUrl,
      hasServiceKey: !!supabaseServiceKey
    })
  }
  
  // Even if config is wrong, we can still send this error to Sentry before failing
  Sentry.captureException(new Error(errorMsg))
  await Sentry.flush(2000)
  
  throw new Error(errorMsg)
}

const supabase = createClient(supabaseUrl, supabaseServiceKey)

interface OrderItem {
  product_id: string
  quantity: number
  price_at_purchase: number
}

interface CreateOrderRequest {
  user_id: string
  items: OrderItem[]
  total?: number
}

Deno.serve(async (req) => {
  // Extract distributed tracing headers
  const sentryTrace = req.headers.get('sentry-trace')
  const baggage = req.headers.get('baggage')

  console.log('📨 Received order creation request')
  console.log('🔗 Distributed tracing headers:', { sentryTrace: !!sentryTrace, baggage: !!baggage })
  
  // Sentry v10: Use structured logging
  if (Sentry.logger) {
    Sentry.logger.info('Edge Function: Order creation request received', {
      hasSentryTrace: !!sentryTrace,
      hasBaggage: !!baggage,
      method: req.method,
    })
  }

  // Continue the distributed trace from FastAPI using Sentry.continueTrace()
  // This properly extracts and continues the trace context from headers
  return Sentry.continueTrace(
    {
      sentryTrace,
      baggage,
    },
    () => {
      // Start a span for this Edge Function within the continued trace
      return Sentry.startSpan(
        {
          name: 'POST /create-order',
          op: 'function.edge',
          attributes: {
            'edge.function': 'create-order',
            'edge.region': Deno.env.get('SB_REGION') || 'unknown',
          },
        },
        async (span) => {
      try {
        // Log the incoming request
        Sentry.addBreadcrumb({
          category: 'request',
          message: 'Received order creation request',
          level: 'info',
        })

        // Parse request body
        const requestData: CreateOrderRequest = await req.json()
        const { user_id, items } = requestData
        const total = requestData.total || items.reduce((sum, item) => sum + (item.quantity * item.price_at_purchase), 0)

        console.log('📝 Order data:', { user_id, itemCount: items.length, total })

        // Validate input
        if (!user_id || !items || items.length === 0) {
          throw new Error('Missing required fields: user_id or items')
        }

        // Sentry v10: Structured logging
        if (Sentry.logger) {
          Sentry.logger.info('Order data validated successfully', {
            user_id,
            item_count: items.length,
            total,
          })
        }

        Sentry.addBreadcrumb({
          category: 'validation',
          message: 'Order data validated',
          level: 'info',
          data: {
            user_id,
            item_count: items.length,
            total,
          },
        })

        // Database operations in a nested span
        const orderResult = await Sentry.startSpan(
          {
            name: 'db.insert.orders',
            op: 'db.query',
          },
          async () => {
            console.log('💾 Inserting order into database...')
            
            // Insert order into database
            const { data: order, error: orderError } = await supabase
              .from('orders')
              .insert({
                user_id,
                total,
                status: 'pending',
              })
              .select()
              .single()

            if (orderError) {
              console.error('❌ Failed to create order:', orderError)
              throw new Error(`Failed to create order: ${orderError.message}`)
            }

            console.log('✅ Order created:', order.id)

            // Sentry v10: Structured logging
            if (Sentry.logger) {
              Sentry.logger.info('Database: Order record created', {
                order_id: order.id,
                user_id: order.user_id,
                total: order.total,
                status: order.status,
              })
            }

            Sentry.addBreadcrumb({
              category: 'database',
              message: 'Order created successfully',
              level: 'info',
              data: {
                order_id: order.id,
              },
            })

            return order
          }
        )

        // Insert order items in a separate span
        const insertedItems = await Sentry.startSpan(
          {
            name: 'db.insert.order_items',
            op: 'db.query',
          },
          async () => {
            console.log('💾 Inserting order items...')
            
            const orderItems = items.map((item) => ({
              order_id: orderResult.id,
              product_id: item.product_id,
              quantity: item.quantity,
              price_at_purchase: item.price_at_purchase,
            }))

            const { data: insertedItems, error: itemsError } = await supabase
              .from('order_items')
              .insert(orderItems)
              .select()

            if (itemsError) {
              console.error('❌ Failed to create order items:', itemsError)
              // Rollback order if items insertion fails
              await supabase.from('orders').delete().eq('id', orderResult.id)
              throw new Error(`Failed to create order items: ${itemsError.message}`)
            }

            console.log('✅ Order items created:', insertedItems.length)

            // Sentry v10: Structured logging
            if (Sentry.logger) {
              Sentry.logger.info('Database: Order items inserted', {
                items_count: insertedItems.length,
                order_id: orderResult.id,
              })
            }

            Sentry.addBreadcrumb({
              category: 'database',
              message: 'Order items created successfully',
              level: 'info',
              data: {
                items_count: insertedItems.length,
              },
            })

            return insertedItems
          }
        )

        // Log successful order creation
        console.log('🎉 Order created successfully:', {
          order_id: orderResult.id,
          user_id,
          total,
          items_count: insertedItems.length,
        })

        // Sentry v10: Final success log
        if (Sentry.logger) {
          Sentry.logger.info('✅ Order creation completed successfully', {
            order_id: orderResult.id,
            user_id,
            total,
            items_count: insertedItems.length,
          })
        }

        span.setStatus({ code: 1, message: 'ok' })

        // Flush Sentry before the running process closes
        await Sentry.flush(2000)

        return new Response(
          JSON.stringify({
            success: true,
            order: {
              id: orderResult.id,
              user_id: orderResult.user_id,
              total: orderResult.total,
              status: orderResult.status,
              created_at: orderResult.created_at,
              items: insertedItems,
            },
          }),
          {
            status: 201,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
            },
          }
        )
      } catch (error) {
        console.error('❌ Error creating order:', error)

        // Sentry v10: Error logging
        if (Sentry.logger) {
          Sentry.logger.error('❌ Order creation failed', {
            error: error instanceof Error ? error.message : String(error),
            error_type: error instanceof Error ? error.name : 'unknown',
          })
        }

        // Capture exception in Sentry
        Sentry.captureException(error)

        // Set error status on span
        span.setStatus({ code: 2, message: 'internal_error' })

        // Flush Sentry before the running process closes
        await Sentry.flush(2000)

        return new Response(
          JSON.stringify({
            success: false,
            error: error instanceof Error ? error.message : 'Unknown error',
          }),
          {
            status: 500,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
            },
          }
        )
      }
        }
      )
    }
  )
})

/* To invoke locally:

  1. Run `supabase start` (see: https://supabase.com/docs/reference/cli/supabase-start)
  2. Make an HTTP request:

  curl -i --location --request POST 'http://127.0.0.1:54321/functions/v1/create-order' \
    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' \
    --header 'Content-Type: application/json' \
    --data '{"user_id":"123","items":[{"product_id":"456","quantity":2,"price_at_purchase":19.99}],"total":39.98}'

*/
