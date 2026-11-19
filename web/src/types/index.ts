export interface ApiResponse<T> { code: number; message: string; data: T }
export interface User { id: number; email: string; nickname: string; avatar?: string; role: 'USER' | 'ADMIN'; quota?: number; remaining_count?: number }
export interface Template { id: number; category: string; name: string; description?: string; positive_prompt: string; negative_prompt?: string; params_json?: Record<string, any>; cover_url?: string; cover_media_url?: string; example_url?: string }
export interface MediaAsset { id: number; url: string; thumbnail_url?: string; prompt?: string; template_name?: string; width?: number; height?: number; created_at?: string; kind?: string }
export interface GenerationTask { id: number; status: 'PENDING'|'RUNNING'|'SUCCESS'|'FAILED'; prompt: string; type?: string; error_msg?: string; assets?: MediaAsset[]; result_assets?: MediaAsset[]; media_assets?: MediaAsset[]; created_at?: string }
export interface Product { id: number; name: string; category: string; description?: string; craft_desc?: string; base_price: number | string; price?: number; lead_time_days: number; image_url?: string; cover_url?: string; spec_json?: Record<string, any> }
export interface Artist { id: number; pen_name: string; name?: string; specialties: string[] | string; intro: string; avatar?: string; avatar_url?: string; rating: number; works_count?: number; years?: number; representative_media_ids?: string }
export interface ProgressPost { id: number; step_name: string; content: string; media_urls?: string[]; images?: string[]; created_at: string }
export interface StatusHistory { id: number; from_status?: string; to_status: string; note?: string; created_at: string }
export interface Order { id: number; order_no: string; status: OrderStatus; product?: Product; product_id: number; media_asset?: MediaAsset; media_asset_id: number; artist?: Artist; artist_id?: number; amount: number | string; spec_json?: Record<string, any>; created_at: string; timeline?: StatusHistory[]; progress_posts?: ProgressPost[]; shipping_info_json?: Record<string, any> }
export type OrderStatus = 'PENDING_CONFIRM'|'DESIGN_CONFIRM'|'ASSIGNED'|'IN_PRODUCTION'|'QUALITY_CHECK'|'SHIPPED'|'COMPLETED'
export interface MessageItem { id: number; title: string; content: string; is_read: boolean; created_at: string; ref_order_id?: number }
