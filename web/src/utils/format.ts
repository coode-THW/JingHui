export const statusMap: Record<string, { label: string; short: string; color: string; step: number }> = {
  PENDING_CONFIRM: { label: '待确认定稿', short: '已下单', color: '#b59461', step: 0 },
  DESIGN_CONFIRM: { label: '待确认定稿', short: '定稿确认', color: '#b59461', step: 1 },
  ASSIGNED: { label: '已交付画师', short: '交付画师', color: '#2e4858', step: 2 },
  IN_PRODUCTION: { label: '画师创作中', short: '画师创作', color: '#a94b3c', step: 3 },
  QUALITY_CHECK: { label: '质检装裱中', short: '质检装裱', color: '#a94b3c', step: 4 },
  SHIPPED: { label: '作品已发货', short: '已发货', color: '#2e4858', step: 5 },
  COMPLETED: { label: '已完成', short: '已完成', color: '#6e806b', step: 6 }
}

export const statusLabel = (status: string) => statusMap[status]?.label || status
export const money = (value: number | string) => `¥${Number(value).toLocaleString('zh-CN', { minimumFractionDigits: 0 })}`
export const date = (value?: string) => value ? new Date(value).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' }) : ''
export const dateTime = (value?: string) => value ? new Date(value).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : ''
