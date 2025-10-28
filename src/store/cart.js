import { defineStore } from 'pinia'
import * as Sentry from '@sentry/vue'

export const useCartStore = defineStore('cart', {
  state: () => {
    console.log('Cart state created')
    Sentry.logger.info('Cart state created')
    return {
      items: []
    }
  },
  actions: {
    addItem(item) {
      const existingItem = this.items.find(i => i.id === item.id)
      if (existingItem) {
        existingItem.quantity += 1
        console.log(`Increased quantity of ${item.name} to ${existingItem.quantity}`)
        Sentry.logger.info(
          Sentry.logger.fmt`Increased quantity of ${item.name} to ${existingItem.quantity}`,
          { productId: item.id, quantity: existingItem.quantity, action: 'increase' }
        )
      } else {
        this.items.push({ ...item, quantity: 1 })
        console.log(`Added ${item.name} to cart`)
        Sentry.logger.info(
          Sentry.logger.fmt`Added ${item.name} to cart`,
          { productId: item.id, productName: item.name, action: 'add' }
        )
      }
      Sentry.logger.debug('Current cart state', { 
        itemCount: this.items.length,
        totalItems: this.totalItems,
        cartValue: this.items.reduce((sum, i) => sum + (i.price * i.quantity), 0)
      })
    },
    removeItem(itemId) {
      const index = this.items.findIndex(item => item.id === itemId)
      if (index !== -1) {
        const itemName = this.items[index].name
        console.log(`Removed ${itemName} from cart`)
        Sentry.logger.info(
          Sentry.logger.fmt`Removed ${itemName} from cart`,
          { productId: itemId, productName: itemName, action: 'remove' }
        )
        this.items.splice(index, 1)
      }
      console.log('Current cart state:', this.items)
      Sentry.logger.debug('Current cart state', { 
        itemCount: this.items.length,
        totalItems: this.totalItems 
      })
    },
    setItems(items) {
      this.items = items
      Sentry.logger.info('Cart items set', { 
        itemCount: items.length,
        totalItems: this.totalItems 
      })
    }
  },
  getters: {
    totalItems: (state) => state.items.reduce((total, item) => total + item.quantity, 0)
  }
})
