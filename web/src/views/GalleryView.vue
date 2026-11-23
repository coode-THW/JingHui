<template>
  <div class="gallery-page">
    <div class="container page-head">
      <div><span class="eyebrow">MY CREATIONS</span><h1 class="serif">我的形象</h1><p>每一次描绘，都是想象留下的独特痕迹。</p></div>
      <RouterLink to="/create" class="btn btn-primary"><el-icon aria-hidden="true"><Plus /></el-icon>创作新形象</RouterLink>
    </div>
    <div class="container gallery-toolbar" role="group" aria-label="作品筛选，可左右滑动" tabindex="0">
      <div class="filter-tabs" role="group" aria-label="作品筛选">
        <button v-for="t in ['全部作品','已定稿','未分类']" :key="t" :class="{active:filter===t}" @click="filter=t" :aria-pressed="filter===t">{{ t }}</button>
      </div>
      <span>共 {{ assets.length }} 幅作品</span>
    </div>
    <div class="container">
      <div v-if="loading" class="works-grid"><div v-for="i in 4" :key="i" class="work-skeleton skeleton"></div></div>
      <div v-else-if="assets.length" class="works-grid">
        <article v-for="(asset,i) in assets" :key="asset.id" class="work-card">
          <div class="work-image">
            <img :src="mediaUrl(asset.url)" :alt="asset.prompt||'我的 AI 形象'" loading="lazy"/>
            <button class="card-hit" type="button" aria-hidden="true" tabindex="-1" @click="openAsset(asset)"></button>
            <div class="work-overlay"><button @click="openAsset(asset)"><el-icon aria-hidden="true"><FullScreen /></el-icon>查看大图</button></div>
            <span class="work-tag">AI 创作</span>
          </div>
          <div class="work-info">
            <div><h3 class="serif">{{ asset.template_name || `东方意象 · ${String(i+1).padStart(2,'0')}` }}</h3><p>{{ date(asset.created_at) }}</p></div>
            <el-dropdown><button class="more-btn" :aria-label="`更多操作：${asset.template_name||'AI 形象'}`" aria-haspopup="menu"><el-icon aria-hidden="true"><MoreFilled /></el-icon></button><template #dropdown><el-dropdown-menu><el-dropdown-item @click="openAsset(asset)">查看详情</el-dropdown-item><el-dropdown-item @click="useAsset(asset)">去定制</el-dropdown-item><el-dropdown-item @click="download(asset)">下载作品</el-dropdown-item></el-dropdown-menu></template></el-dropdown>
          </div>
        </article>
      </div>
      <div v-else class="empty-state">
        <div class="empty-art"><img src="/assets/product-scroll.svg" alt=""/></div>
        <span class="seal">镜</span>
        <h2 class="serif">一纸空白，待你落笔</h2>
        <p>从一句描述开始，生成你的第一幅专属形象。</p>
        <RouterLink to="/create" class="btn btn-primary">开始 AI 创作<el-icon aria-hidden="true"><ArrowRight /></el-icon></RouterLink>
      </div>
    </div>
    <el-dialog v-model="dialogOpen" width="min(850px, 94vw)" class="art-dialog" :show-close="false">
      <div v-if="current" class="asset-detail">
        <div class="detail-image"><img :src="mediaUrl(current.url)" alt="AI 形象大图"/></div>
        <div class="detail-copy">
          <span class="eyebrow">CREATION DETAIL</span>
          <h2 class="serif">{{ current.template_name || '我的东方形象' }}</h2>
          <p class="detail-date">{{ date(current.created_at) }} · AI 辅助生成</p>
          <h4>创作描述</h4>
          <p class="prompt-text">{{ current.prompt || '由镜绘东方风格模板生成，保留这一刻独特的想象。' }}</p>
          <div class="detail-actions">
            <button class="btn btn-outline" @click="download(current)"><el-icon aria-hidden="true"><Download /></el-icon>下载</button>
            <button class="btn btn-primary" @click="useAsset(current)">定稿并去定制<el-icon aria-hidden="true"><ArrowRight /></el-icon></button>
          </div>
          <button class="dialog-close icon-btn" aria-label="关闭详情" @click="dialogOpen=false"><el-icon aria-hidden="true"><Close /></el-icon></button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';import { useRouter } from 'vue-router';import { ElMessage } from 'element-plus';import { aiApi, mediaUrl } from '@/services/api';import { date } from '@/utils/format';import type { MediaAsset } from '@/types'
const router=useRouter(),assets=ref<MediaAsset[]>([]),loading=ref(true),filter=ref('全部作品'),dialogOpen=ref(false),current=ref<MediaAsset|null>(null)
onMounted(async()=>{try{assets.value=await aiApi.assets()}catch(e:any){ElMessage.error(e.message)}finally{loading.value=false}})
function openAsset(a:MediaAsset){current.value=a;dialogOpen.value=true}
function useAsset(a:MediaAsset){localStorage.setItem('jinghui_draft',JSON.stringify({asset_id:a.id,image:mediaUrl(a.url),prompt:a.prompt,template:a.template_name}));router.push('/checkout')}
function download(a:MediaAsset){const link=document.createElement('a');link.href=mediaUrl(a.url);link.target='_blank';link.download=`镜绘作品-${a.id}.svg`;link.click()}
</script>
<style scoped>
/* ===== 基础 ===== */
.gallery-page{padding:55px 0 90px;min-height:75vh}
.page-head{display:flex;justify-content:space-between;align-items:flex-end}
.page-head h1{font-size:var(--fs-h1,clamp(28px,3vw,36px));letter-spacing:.08em;margin:13px 0 8px}
.page-head p{color:var(--muted);font-size:var(--fs-body-s,12px);margin:0}
.gallery-toolbar{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);margin-top:35px;margin-bottom:28px;overflow-x:auto}
.filter-tabs{display:flex;gap:25px;flex-shrink:0;white-space:nowrap}
.filter-tabs button{border:0;background:none;padding:0 0 13px;min-height:44px;display:inline-flex;align-items:flex-end;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);position:relative;border-radius:3px;transition:color .2s,background .2s}
.filter-tabs button.active{color:var(--cinnabar)}
.filter-tabs button.active::after{content:'';position:absolute;left:25%;right:25%;bottom:-1px;height:2px;background:var(--cinnabar)}
.gallery-toolbar>span{font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);padding-bottom:13px;min-height:44px;display:inline-flex;align-items:flex-end;flex-shrink:0;white-space:nowrap}
.works-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:25px 18px}
.work-skeleton{aspect-ratio:.73}
.work-image{position:relative;aspect-ratio:.78;overflow:hidden;background:#e8e1d4}
.work-image img{width:100%;height:100%;object-fit:cover;transition:.5s}
.work-card:hover img{transform:scale(1.04)}
/* 键盘 Tab 到隐藏按钮时也要可见：focus-within 显示 */
.work-overlay{position:absolute;inset:0;background:rgba(27,38,40,.28);display:grid;place-items:center;opacity:0;visibility:hidden;transition:.3s;z-index:2;pointer-events:none}
.work-card:hover .work-overlay,.work-card:focus-within .work-overlay{opacity:1;visibility:visible}
.work-overlay button{border:1px solid rgba(255,255,255,.7);background:rgba(250,247,239,.9);padding:10px 16px;min-height:46px;min-width:44px;display:inline-flex;align-items:center;justify-content:center;gap:6px;color:var(--azure);font-size:var(--fs-body-s,12px);pointer-events:auto;transition:background .2s,transform .2s}
.work-overlay button:hover{background:#fffaf0}
.work-overlay button:active{transform:scale(.97)}
.work-tag{position:absolute;left:10px;top:10px;z-index:2;pointer-events:none;background:rgba(250,247,239,.88);color:var(--cinnabar);padding:4px 7px;font-size:var(--fs-body-s,12px)}
.work-info{display:flex;justify-content:space-between;align-items:center;padding:13px 2px}
.work-info h3{font-size:var(--fs-h3,18px);font-weight:500;margin:0 0 5px}
.work-info p{font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);margin:0}
.more-btn{border:0;background:none;color:var(--muted);padding:6px;min-width:44px;min-height:44px;display:inline-flex;align-items:center;justify-content:center;border-radius:3px;transition:color .2s,background .2s}
.more-btn:hover{color:var(--cinnabar);background:rgba(169,75,60,.06)}
.more-btn:active{background:rgba(169,75,60,.13)}
/* 整卡可点：z-index 低于 overlay，不拦截“查看大图”按钮 */
.card-hit{position:absolute;inset:0;z-index:1;border:0;background:transparent}
.empty-state{text-align:center;padding:45px 0}
.empty-art{height:200px;width:190px;margin:0 auto -30px;opacity:.55}
.empty-art img{height:100%;object-fit:cover}
.empty-state .seal{margin:0 auto 20px}
.empty-state h2{font-size:27px;margin:0 0 12px}
.empty-state p{font-size:var(--fs-body-s,12px);color:var(--muted);margin-bottom:25px}
.asset-detail{display:grid;grid-template-columns:1.1fr .9fr;min-height:500px}
.detail-image{background:#e8e0d3}
.detail-image img{width:100%;height:100%;object-fit:cover}
.detail-copy{position:relative;padding:45px 32px;display:flex;flex-direction:column}
.detail-copy h2{font-size:27px;margin:15px 0 7px}
.detail-date{font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63)}
.detail-copy h4{font-size:var(--fs-h4,14px);margin:30px 0 10px}
.prompt-text{font-size:var(--fs-body,14px);line-height:1.9;color:var(--ink-2,#6e6d63);background:var(--paper);padding:14px}
.detail-actions{display:grid;grid-template-columns:1fr 1.4fr;gap:9px;margin-top:auto}
.detail-actions .btn{min-height:46px}
.dialog-close{position:absolute;right:0;top:-30px;min-width:44px;min-height:44px}

/* ===== 交互反馈 / 焦点环 ===== */
.filter-tabs button:hover{color:var(--cinnabar);background:rgba(169,75,60,.05)}
.filter-tabs button:active{background:rgba(169,75,60,.12)}
/* 焦点环由全局 main.css 的 :where(...):focus-visible 提供，此处不重复定义 */

/* ===== 断点：>1080 → 1080 → 768 → 480，列数单调不增（4→3→2→2） ===== */
@media(max-width:1080px){.works-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:768px){
  .gallery-page{padding:35px 0 60px}
  .page-head .btn{padding:0 14px;font-size:var(--fs-body-s,12px)}
  .works-grid{grid-template-columns:1fr 1fr;gap:20px 11px}
  /* P0：主操作不再 display:none，常驻图片底部条 */
  .work-overlay{position:absolute;inset:auto 0 0;display:flex;justify-content:center;align-items:center;opacity:1;visibility:visible;background:linear-gradient(transparent,rgba(22,30,30,.72));padding:12px}
  .work-overlay button{min-height:46px;min-width:44px;font-size:var(--fs-body-s,12px)}
  .asset-detail{grid-template-columns:1fr;min-height:auto}
  .detail-image{height:380px}
  .detail-copy{padding:25px}
  .detail-copy h4{margin-top:15px}
  .dialog-close{top:0}
  .detail-actions{margin-top:20px}
}
@media(max-width:480px){
  .page-head{flex-wrap:wrap;gap:16px}
  .filter-tabs{gap:16px}
}
</style>
