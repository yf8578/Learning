// import { is } from 'core-js/core/object'
import { createStore } from 'vuex'

export default createStore({
  state: {
    cart:{
      items:[],
    },
    isAuthenticated: false,
    token: '',
    isLoading: false,
  },
  getters: {
  },
  mutations: {
    initializeStore(state){
      if(localStorage.getItem('cart')){
        state.cart = JSON.parse(localStorage.getItem('cart'))
      }else{
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
    },
    addToCart(state, item){
      // const：这是 ES6 引入的关键字，用于声明一个常量。常量的值一旦被赋值，就不能再更改。
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)
      if(exists.length){
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      }else{
        state.cart.items.push(item)
      }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    }
  },
  actions: {
  },
  modules: {
  }
})
