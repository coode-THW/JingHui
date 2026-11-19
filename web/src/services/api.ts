import axios, { type AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: 30000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('jinghui_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(undefined, error => {
  const detail = error.response?.data?.detail || error.response?.data?.message
  const message = typeof detail === 'string' ? detail : error.code === 'ERR_NETWORK' ? '服务暂未连接，请先启动后端服务' : '操作未完成，请稍后重试'
  if (error.response?.status === 401) {
    localStorage.removeItem('jinghui_token')
  }
  return Promise.reject(new Error(message))
})

export async function request<T>(call: Promise<AxiosResponse<ApiResponse<T>>>): Promise<T> {
  const response = await call
  if (response.data.code !== 0 && response.data.code !== 200) throw new Error(response.data.message || '请求失败')
  return response.data.data
}

export function mediaUrl(url?: string) {
  if (!url) return '/assets/art-1.svg'
  if (url.startsWith('http') || url.startsWith('data:') || url.startsWith('/assets/')) return url
  const base = import.meta.env.VITE_STATIC_BASE_URL || 'http://127.0.0.1:8000'
  return `${base}${url.startsWith('/') ? url : '/' + url}`
}

export const authApi = {
  login: (data: { email: string; password: string }) => request<{ access_token: string; user: any }>(api.post('/auth/login', data)),
  register: (data: { email: string; password: string; nickname: string }) => request<{ access_token: string; user: any }>(api.post('/auth/register', data)),
  me: () => request<any>(api.get('/auth/me'))
}

export const contentApi = {
  templates: () => request<any[]>(api.get('/ai/templates')),
  products: () => request<any[]>(api.get('/products')),
  artists: () => request<any[]>(api.get('/artists'))
}

export const aiApi = {
  generate: (data: any) => request<any>(api.post('/ai/generate', data)),
  task: (id: number) => request<any>(api.get(`/ai/tasks/${id}`)),
  assets: () => request<any[]>(api.get('/ai/assets'))
}

export const orderApi = {
  create: (data: any) => request<any>(api.post('/orders', data)),
  list: () => request<any[]>(api.get('/orders')),
  detail: (id: number) => request<any>(api.get(`/orders/${id}`)),
  timeline: (id: number) => request<any>(api.get(`/orders/${id}/timeline`)),
  confirm: (id: number) => request<any>(api.post(`/orders/${id}/confirm-design`))
}

export const adminApi = {
  stats: () => request<any>(api.get('/admin/stats')),
  orders: () => request<any[]>(api.get('/admin/orders')),
  artists: () => request<any[]>(api.get('/admin/artists')),
  saveArtist: (data: any, id?: number) => request<any>(id ? api.put(`/admin/artists/${id}`, data) : api.post('/admin/artists', data)),
  updateStatus: (id: number, status: string, note: string) => request<any>(api.post(`/admin/orders/${id}/status`, { status, to_status: status, note })),
  addProgress: (id: number, data: any) => request<any>(api.post(`/admin/orders/${id}/progress`, data))
}
