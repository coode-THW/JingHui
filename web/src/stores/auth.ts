import { defineStore } from 'pinia'
import { authApi } from '@/services/api'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('jinghui_token') || '',
    user: null as User | null,
    loading: false
  }),
  getters: {
    loggedIn: state => Boolean(state.token),
    isAdmin: state => state.user?.role === 'ADMIN',
    quota: state => state.user?.remaining_count ?? state.user?.quota ?? 0
  },
  actions: {
    async login(email: string, password: string) {
      this.loading = true
      try {
        const data = await authApi.login({ email, password })
        this.token = data.access_token
        this.user = data.user
        localStorage.setItem('jinghui_token', data.access_token)
        return data.user
      } finally { this.loading = false }
    },
    async register(email: string, password: string, nickname: string) {
      const data = await authApi.register({ email, password, nickname })
      this.token = data.access_token
      this.user = data.user
      localStorage.setItem('jinghui_token', data.access_token)
    },
    async fetchMe() {
      if (!this.token) return
      try { this.user = await authApi.me() } catch { this.logout(false) }
    },
    logout(redirect = true) {
      this.token = ''; this.user = null
      localStorage.removeItem('jinghui_token')
      if (redirect) window.location.href = '/'
    }
  }
})
