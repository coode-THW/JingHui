<template>
  <div class="scroll-x-wrap">
    <div class="order-table-wrap scroll-x" tabindex="0" role="region" aria-label="订单表格，可左右滑动">
      <table class="order-table">
        <caption class="sr-only">定制订单列表</caption>
        <thead><tr><th scope="col">订单 / 用户</th><th scope="col">定制作品</th><th scope="col">金额</th><th scope="col">当前状态</th><th scope="col">操作</th></tr></thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id">
            <td><strong>{{ o.order_no }}</strong><span>用户 ID {{ o.user_id }}</span></td>
            <td class="table-product"><img :src="mediaUrl(o.media_asset?.url)" alt=""/><div><strong>{{ o.product?.name }}</strong><span>{{ o.artist?.pen_name||'待匹配画师' }}</span></div></td>
            <td class="table-price">{{ money(o.amount) }}</td>
            <td><span :class="['table-status','status-'+(o.status||'').toLowerCase()]">{{ statusLabel(o.status) }}</span></td>
            <td class="table-actions"><button @click="$emit('status',o)">流转状态</button><button @click="$emit('progress',o)">代录进度</button></td>
          </tr>
          <tr v-if="!orders.length"><td colspan="5" class="table-empty">暂无订单</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script setup lang="ts">
import { mediaUrl } from '@/services/api'
import { money, statusLabel } from '@/utils/format'
defineProps<{ orders: any[] }>()
defineEmits(['status','progress'])
</script>
<style scoped>
.order-table-wrap{overflow-x:auto}
.order-table{width:100%;border-collapse:collapse;font-size:var(--fs-body-s)}
th{text-align:left;color:var(--ink-2);font-weight:400;font-size:var(--fs-body-s);background:var(--paper);padding:10px}
td{padding:12px 10px;border-bottom:1px solid var(--line);vertical-align:middle}
td>strong{display:block;font-size:var(--fs-body-s);font-weight:500}
td>span{display:block;font-size:var(--fs-body-s);color:var(--ink-2);margin-top:4px}
.table-product{display:flex;align-items:center;gap:10px;min-width:190px}
.table-product img{width:40px;height:46px;object-fit:cover}
.table-product strong{display:block;font-size:var(--fs-body-s);font-weight:500}
.table-product span{display:block;font-size:var(--fs-body-s);color:var(--ink-2);margin-top:4px}
.table-price{color:var(--cinnabar);font-family:var(--serif);font-size:14px}
/* Neutral fallback only; per-status colours come from the consumer view via .status-* classes. */
.table-status{display:inline-block!important;background:rgba(58,60,52,.06);color:var(--ink-soft);padding:5px 8px;margin:0!important;white-space:nowrap}
.table-actions{white-space:nowrap}
.table-actions button{border:0;background:none;color:var(--azure);font-size:12px;padding:4px 9px;min-height:36px;position:relative}
.table-actions button::after{content:'';position:absolute;inset:-4px}
.table-actions button:hover{color:var(--cinnabar)}
.table-empty{text-align:center;color:var(--muted);padding:35px}
</style>
