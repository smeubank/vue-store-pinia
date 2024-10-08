import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => {
    console.log('Cart state created')
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
      } else {
        this.items.push({ ...item, quantity: 1 })
        console.log(`Added ${item.name} to cart`)
      }
      console.log('Current cart state:', JSON.stringify(this.items, null, 2))
    },
    removeItem(itemId) {
      const index = this.items.findIndex(item => item.id === itemId)
      if (index !== -1) {
        console.log(`Removed ${this.items[index].name} from cart`)
        this.items.splice(index, 1)
      }
      console.log('Current cart state:', JSON.stringify(this.items, null, 2))
    }
  },
  getters: {
    totalItems: (state) => state.items.reduce((total, item) => total + item.quantity, 0)
  }
})
