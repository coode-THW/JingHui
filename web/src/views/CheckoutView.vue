<template>
  <div class="checkout-page">
    <div class="container checkout-head">
      <RouterLink to="/gallery" class="back-link"><el-icon aria-hidden="true"><ArrowLeft /></el-icon>返回我的形象</RouterLink>
      <div class="checkout-steps" role="group" aria-label="下单流程：AI 定稿、确认定制、画师创作、作品交付">
        <span class="done"><i>1</i>AI 定稿</span><b></b>
        <span class="active" aria-current="step"><i>2</i>确认定制</span><b></b>
        <span><i>3</i>画师创作</span><b></b>
        <span><i>4</i>作品交付</span>
      </div>
      <span class="secure"><el-icon aria-hidden="true"><Lock /></el-icon>安心定制</span>
    </div>
    <div class="container">
      <div class="checkout-title">
        <span class="eyebrow">CONFIRM YOUR CREATION</span>
        <h1 class="serif">让想象，成为作品</h1>
        <p>确认定稿与定制细节。提交后进入模拟支付，不会真实扣款。</p>
      </div>
      <div v-if="draft" class="checkout-layout">
        <div class="checkout-main">
          <section class="checkout-section paper-card">
            <div class="section-title"><span>01</span><h2 class="serif">你的定稿形象</h2><button @click="router.push('/gallery')">更换形象</button></div>
            <div class="draft-info">
              <img :src="draft.image" alt="AI 定稿形象"/>
              <div>
                <span class="tag">AI 定稿</span>
                <h3 class="serif">{{ draft.template||'我的东方形象' }}</h3>
                <p>{{ draft.prompt||'由镜绘 AI 创作工坊生成的专属形象。' }}</p>
                <small><el-icon aria-hidden="true"><CircleCheck /></el-icon>定稿后，画师将以此图为创作依据</small>
              </div>
            </div>
          </section>
          <section class="checkout-section paper-card">
            <div class="section-title"><span>02</span><h2 class="serif">选择作品载体</h2></div>
            <div v-if="products.length" class="product-options" role="group" aria-label="作品载体">
              <button v-for="(p,i) in products" :key="p.id" :class="{selected:selectedProduct?.id===p.id}" @click="selectedProduct=p" :aria-pressed="selectedProduct?.id===p.id" :aria-label="`选择载体：${p.name}`">
                <img :src="p.image_url||p.cover_url||`/assets/product-${['scroll','fan','porcelain','canvas','screen','gift'][i%6]}.svg`" :alt="p.name"/>
                <div><strong class="serif">{{ p.name }}</strong><small>约 {{ p.lead_time_days }} 天 · {{ money(p.base_price) }} 起</small></div>
                <span class="radio"><i></i></span>
              </button>
            </div>
            <div v-else class="product-loading skeleton"></div>
          </section>
          <section class="checkout-section paper-card">
            <div class="section-title"><span>03</span><h2 class="serif">完善定制细节</h2></div>
            <div class="spec-group">
              <label>作品尺寸</label>
              <div class="spec-options" role="group" aria-label="作品尺寸">
                <button v-for="size in sizes" :key="size.name" :class="{selected:selectedSize.name===size.name}" @click="selectedSize=size" :aria-pressed="selectedSize.name===size.name"><strong>{{ size.name }}</strong><small>{{ size.desc }}</small><span v-if="size.extra">+{{ money(size.extra) }}</span></button>
              </div>
            </div>
            <div class="spec-group">
              <label>装裱方式</label>
              <div class="inline-options" role="group" aria-label="装裱方式">
                <button v-for="f in ['经典原木','胡桃木框','简约无框']" :key="f" :class="{selected:frame===f}" @click="frame=f" :aria-pressed="frame===f">{{ f }}</button>
              </div>
            </div>
            <div class="spec-group">
              <label for="inscription">题字 / 落款 <small>选填，画师将以书法题写</small></label>
              <input v-model="inscription" id="inscription" class="form-control" maxlength="30" placeholder="例如：岁岁常欢愉 · 赠吾爱" aria-label="题字 / 落款"/>
            </div>
            <div class="spec-group">
              <label>画师偏好 <small>选填，由平台根据画种匹配</small></label>
              <el-select v-model="artistId" clearable placeholder="由平台推荐合适画师" style="width:100%" aria-label="画师偏好"><el-option v-for="a in artists" :key="a.id" :value="a.id" :label="`${a.pen_name||a.name} · ${formatSpecialties(a.specialties)}`"/></el-select>
            </div>
          </section>
          <section class="checkout-section paper-card">
            <div class="section-title"><span>04</span><h2 class="serif">收货与联系信息</h2></div>
            <div class="address-grid">
              <label for="addr-name">收货人<input v-model="address.name" id="addr-name" class="form-control" placeholder="请输入姓名" aria-required="true" :aria-invalid="addressInvalid && !address.name" aria-describedby="addr-name-err"/></label>
              <span id="addr-name-err" class="sr-only" role="alert">{{ addressInvalid && !address.name ? '请填写收货人' : '' }}</span>
              <label for="addr-phone">联系电话<input v-model="address.phone" id="addr-phone" class="form-control" placeholder="请输入手机号" aria-required="true" :aria-invalid="addressInvalid && !address.phone" aria-describedby="addr-phone-err"/></label>
              <span id="addr-phone-err" class="sr-only" role="alert">{{ addressInvalid && !address.phone ? '请填写联系电话' : '' }}</span>
              <label class="full" for="addr-region">所在地区<input v-model="address.region" id="addr-region" class="form-control" placeholder="省 / 市 / 区" :aria-invalid="false" aria-describedby="addr-region-hint"/></label>
              <span id="addr-region-hint" class="sr-only">选填，省 / 市 / 区</span>
              <label class="full" for="addr-detail">详细地址<textarea v-model="address.detail" id="addr-detail" class="form-control" placeholder="街道、小区、楼栋与门牌号" aria-required="true" :aria-invalid="addressInvalid && !address.detail" aria-describedby="addr-detail-err"></textarea></label>
              <span id="addr-detail-err" class="sr-only" role="alert">{{ addressInvalid && !address.detail ? '请填写详细地址' : '' }}</span>
            </div>
          </section>
        </div>
        <aside class="order-summary">
          <div class="summary-sticky paper-card">
            <h2 class="serif">定制清单</h2>
            <div class="summary-art">
              <img :src="draft.image" alt="定稿缩略图"/>
              <div>
                <strong>{{ selectedProduct?.name||'请选择载体' }}</strong>
                <span>{{ selectedSize.name }} · {{ frame }}</span>
                <span v-if="inscription">题字：{{ inscription }}</span>
              </div>
            </div>
            <div class="summary-lines">
              <div><span>载体定制</span><strong>{{ money(selectedProduct?.base_price||0) }}</strong></div>
              <div><span>尺寸升级</span><strong>{{ selectedSize.extra?'+ '+money(selectedSize.extra):'已包含' }}</strong></div>
              <div><span>基础装裱</span><strong>已包含</strong></div>
              <div><span>作品运费</span><strong>免运费</strong></div>
            </div>
            <div class="summary-total"><span>定制合计<small>模拟支付</small></span><strong>{{ money(total) }}</strong></div>
            <div class="promise">
              <span><el-icon aria-hidden="true"><CircleCheck /></el-icon>定稿确认后再开始创作</span>
              <span><el-icon aria-hidden="true"><CircleCheck /></el-icon>关键节点实拍同步</span>
              <span><el-icon aria-hidden="true"><CircleCheck /></el-icon>作品问题专属售后</span>
            </div>
            <button class="btn btn-primary btn-lg submit-order" :disabled="!selectedProduct||submitting" @click="submitOrder">{{ submitting?'正在提交…':'提交定制并模拟支付' }}<el-icon aria-hidden="true"><ArrowRight /></el-icon></button>
            <p>提交即表示同意《定制服务说明》<br>定制作品确认定稿后不支持无理由退换</p>
          </div>
        </aside>
      </div>
      <div v-else class="no-draft">
        <span class="seal">镜</span>
        <h2 class="serif">先选择一幅满意的形象</h2>
        <p>你可以从 AI 创作工坊生成，或在我的形象中挑选。</p>
        <RouterLink to="/create" class="btn btn-primary">去创作形象</RouterLink>
      </div>
    </div>
    <el-dialog v-model="successOpen" width="min(450px,90vw)" :show-close="false" class="success-dialog">
      <div class="payment-success">
        <div class="success-icon"><el-icon aria-hidden="true"><Check /></el-icon></div>
        <span class="eyebrow">ORDER CONFIRMED</span>
        <h2 class="serif">定制已提交</h2>
        <p>模拟支付已完成。接下来请确认定稿，<br>画师便会开始亲笔创作。</p>
        <div class="success-order"><span>订单编号</span><strong>{{ createdOrder?.order_no }}</strong></div>
        <button class="btn btn-primary" @click="router.push(`/orders/${createdOrder?.id}`)">查看创作进度<el-icon aria-hidden="true"><ArrowRight /></el-icon></button>
        <button class="text-btn" @click="router.push('/')">返回首页</button>
      </div>
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';import { useRouter } from 'vue-router';import { ElMessage } from 'element-plus';import { contentApi, orderApi } from '@/services/api';import { money } from '@/utils/format';import type { Artist, Product } from '@/types'
const router=useRouter(),draft=ref<any>(null),products=ref<Product[]>([]),artists=ref<Artist[]>([]),selectedProduct=ref<Product|null>(null),artistId=ref<number>(),frame=ref('经典原木'),inscription=ref(''),submitting=ref(false),successOpen=ref(false),createdOrder=ref<any>(null),addressInvalid=ref(false)
const sizes=[{name:'小品珍藏',desc:'30 × 40 cm',extra:0},{name:'雅致中堂',desc:'50 × 70 cm',extra:300},{name:'典藏大幅',desc:'70 × 100 cm',extra:800}];const selectedSize=ref(sizes[0]);const address=ref({name:'',phone:'',region:'',detail:''})
const total=computed(()=>Number(selectedProduct.value?.base_price||0)+selectedSize.value.extra)
onMounted(async()=>{const saved=localStorage.getItem('jinghui_draft');if(saved)draft.value=JSON.parse(saved);try{const [p,a]=await Promise.all([contentApi.products(),contentApi.artists()]);products.value=p;artists.value=a;selectedProduct.value=p[0]||null}catch(e:any){ElMessage.error(e.message)}})
function formatSpecialties(s:any){return Array.isArray(s)?s.join(' / '):s||'传统画师'}
async function submitOrder(){if(!address.value.name||!address.value.phone||!address.value.detail){addressInvalid.value=true;ElMessage.warning('请完整填写收货人、电话和详细地址');return}submitting.value=true;try{const spec={size:selectedSize.value.name,dimensions:selectedSize.value.desc,frame:frame.value,inscription:inscription.value,address:address.value};createdOrder.value=await orderApi.create({product_id:selectedProduct.value!.id,media_asset_id:draft.value.asset_id,artist_id:artistId.value,spec:{size:`${selectedSize.value.name}（${selectedSize.value.desc}）`,framing:frame.value,inscription:inscription.value,note:selectedSize.value.extra?`尺寸升级费用 ${selectedSize.value.extra} 元`:''},shipping_info:{name:address.value.name,phone:address.value.phone,address:`${address.value.region} ${address.value.detail}`}});successOpen.value=true;localStorage.removeItem('jinghui_draft')}catch(e:any){ElMessage.error(e.message)}finally{submitting.value=false}}
</script>
<style scoped>
/* ===== 基础 ===== */
.checkout-page{padding:25px 0 85px}
.checkout-head{display:flex;justify-content:space-between;align-items:center;padding-bottom:25px;border-bottom:1px solid var(--line)}
.back-link,.secure{display:flex;align-items:center;gap:6px;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63)}
.back-link{min-height:44px}
.checkout-steps{display:flex;align-items:center;gap:10px}
.checkout-steps span{display:flex;align-items:center;gap:6px;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63)}
.checkout-steps i{font-style:normal;width:19px;height:19px;border:1px solid var(--line);border-radius:50%;display:grid;place-items:center;font-size:11px}
.checkout-steps b{width:30px;height:1px;background:var(--line)}
.checkout-steps .active{color:var(--cinnabar)}
.checkout-steps .active i{border-color:var(--cinnabar);background:var(--cinnabar);color:white}
.checkout-steps .done{color:var(--azure)}
.checkout-steps .done i{background:var(--azure);color:white}
.checkout-title{padding:38px 0 28px}
.checkout-title h1{font-size:var(--fs-h1,clamp(28px,3vw,36px));letter-spacing:.08em;margin:12px 0 8px}
.checkout-title p{font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);margin:0}
.checkout-layout{display:grid;grid-template-columns:1fr 340px;gap:25px;align-items:start}
.checkout-main{display:grid;gap:18px}
.checkout-section{padding:25px}
.section-title{display:flex;align-items:center;gap:10px;margin-bottom:22px}
.section-title>span{font-family:var(--serif);font-size:var(--fs-body-s,12px);color:var(--gilt)}
.section-title h2{font-size:var(--fs-h3,18px);font-weight:600;letter-spacing:.06em;margin:0}
.section-title>button{margin-left:auto;border:0;background:none;color:var(--cinnabar);font-size:var(--fs-body-s,12px);min-height:44px;display:inline-flex;align-items:center;padding:0 10px;border-radius:3px;transition:.2s}
.draft-info{display:grid;grid-template-columns:130px 1fr;gap:22px;background:var(--paper);padding:14px}
.draft-info>img{width:130px;height:145px;object-fit:cover}
.draft-info h3{font-size:var(--fs-h3,18px);margin:10px 0 8px}
.draft-info p{font-size:var(--fs-body-s,12px);line-height:1.7;color:var(--ink-2,#6e6d63);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.draft-info small{display:flex;align-items:center;gap:5px;color:#6f806b;font-size:var(--fs-body-s,12px);margin-top:12px}
.product-options{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.product-options>button{position:relative;border:1px solid var(--line);background:transparent;padding:8px;text-align:left;display:grid;grid-template-columns:65px 1fr;align-items:center;gap:10px;min-height:44px;min-width:0;transition:background .2s,border-color .2s}
.product-options>button.selected{border-color:var(--cinnabar);background:rgba(169,75,60,.035)}
.product-options img{width:65px;height:70px;object-fit:cover}
.product-options strong{display:block;font-size:var(--fs-body-s,12px);font-weight:500}
.product-options small{display:block;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);margin-top:5px}
.radio{position:absolute;right:7px;top:7px;width:12px;height:12px;border:1px solid #c6bfb2;border-radius:50%}
.selected .radio{border-color:var(--cinnabar)}
.selected .radio i{display:block;width:6px;height:6px;border-radius:50%;background:var(--cinnabar);margin:2px}
.product-loading{height:120px}
.spec-group{margin-top:22px}
.spec-group>label{display:block;font-size:var(--fs-body-s,12px);font-weight:500;margin-bottom:11px}
.spec-group>label small{font-weight:400;color:var(--ink-2,#6e6d63);font-size:var(--fs-body-s,12px);margin-left:7px}
.spec-options{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.spec-options button{position:relative;border:1px solid var(--line);background:transparent;text-align:left;padding:13px;display:flex;flex-direction:column;min-height:64px;min-width:0;transition:background .2s,border-color .2s}
.spec-options button.selected{border-color:var(--cinnabar);background:rgba(169,75,60,.035)}
.spec-options strong{display:block;font-size:var(--fs-body,14px);font-weight:500}
.spec-options small{display:block;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);margin-top:4px}
.spec-options span{position:static;display:block;margin-top:6px;color:var(--gilt-dark,#8a6d40);font-size:var(--fs-body-s,12px)}
.inline-options{display:flex;gap:9px}
.inline-options button{border:1px solid var(--line);background:transparent;padding:9px 18px;min-height:44px;font-size:var(--fs-body-s,12px);color:var(--muted);transition:background .2s,border-color .2s,color .2s}
.inline-options button.selected{border-color:var(--cinnabar);color:var(--cinnabar);background:rgba(169,75,60,.035)}
.address-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;position:relative}
.address-grid label{font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63)}
.address-grid .form-control{margin-top:8px;font-size:var(--fs-body,14px)}
.address-grid textarea{height:75px;resize:none}
.address-grid .full{grid-column:1/-1}
.summary-sticky{position:sticky;top:var(--sticky-offset,125px);padding:24px}
.summary-sticky>h2{font-size:var(--fs-h3,18px);margin:0 0 20px}
.summary-art{display:grid;grid-template-columns:65px 1fr;gap:12px;padding-bottom:18px;border-bottom:1px solid var(--line)}
.summary-art img{width:65px;height:78px;object-fit:cover}
.summary-art strong{display:block;font-size:var(--fs-body-s,12px);margin:4px 0 8px}
.summary-art span{display:block;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);line-height:1.8}
.summary-lines{padding:17px 0;border-bottom:1px solid var(--line);display:grid;gap:11px}
.summary-lines>div{display:flex;justify-content:space-between;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63)}
.summary-lines strong{font-weight:400;color:var(--ink-soft)}
.summary-total{display:flex;justify-content:space-between;align-items:center;padding:18px 0}
.summary-total>span{font-size:var(--fs-body-s,12px)}
.summary-total small{display:block;font-size:var(--fs-body-s,12px);color:var(--gilt);margin-top:3px}
.summary-total strong{font-family:var(--serif);font-size:26px;color:var(--cinnabar);font-weight:500}
.promise{display:grid;gap:8px;background:var(--paper);padding:13px;margin-bottom:16px}
.promise span{display:flex;align-items:center;gap:6px;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63)}
.promise .el-icon{color:#72836c}
.submit-order{width:100%;font-size:var(--fs-body-s,12px)}
.summary-sticky>p{text-align:center;font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);line-height:1.8}
.no-draft{text-align:center;padding:80px 0}
.no-draft .seal{margin:0 auto 20px}
.no-draft h2{font-size:28px}
.no-draft p{color:var(--muted);font-size:var(--fs-body-s,12px);margin-bottom:25px}
.payment-success{text-align:center;padding:25px 10px}
.success-icon{width:65px;height:65px;border-radius:50%;background:rgba(105,132,100,.1);color:#698464;display:grid;place-items:center;font-size:30px;margin:0 auto 22px}
.payment-success h2{font-size:29px;margin:15px 0 10px}
.payment-success>p{font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);line-height:1.9}
.success-order{display:flex;justify-content:space-between;padding:13px;background:var(--paper);font-size:var(--fs-body-s,12px);color:var(--ink-2,#6e6d63);margin:22px 0}
.success-order strong{color:var(--ink-soft);font-weight:500}
.payment-success>.btn{width:100%;min-height:46px}
.text-btn{border:0;background:none;color:var(--muted);font-size:var(--fs-body-s,12px);margin-top:15px;min-height:44px;min-width:44px;display:inline-flex;align-items:center;justify-content:center;padding:0 12px;border-radius:3px;transition:.2s}

/* ===== 交互反馈 / 选中态 / 焦点环 ===== */
.product-options>button:hover,.spec-options button:hover,.inline-options button:hover{border-color:var(--cinnabar);background:rgba(169,75,60,.06)}
.product-options>button:active,.spec-options button:active,.inline-options button:active{background:rgba(169,75,60,.13)}
.section-title>button:hover,.text-btn:hover{color:var(--cinnabar-dark,#8d3d31);background:rgba(169,75,60,.06)}
.section-title>button:active,.text-btn:active{background:rgba(169,75,60,.13)}
/* 选中态不只靠边框：右上角 19px 朱砂圆底白勾（装饰字符，真实状态由 aria-pressed 承担） */
.product-options>button.selected::after,.spec-options button.selected::after{content:'✓';position:absolute;right:6px;top:6px;width:19px;height:19px;border-radius:50%;background:var(--cinnabar);color:#fff;display:grid;place-items:center;font-size:12px;line-height:1;font-weight:700}
.product-options>button.selected .radio{display:none}
/* 焦点环(:where)、.form-control:focus-visible、[aria-invalid]、.sr-only、.field-error 均由全局 main.css 提供；
   此处不重复定义，仅确认本组件未写任何 outline:none 抹除焦点环。 */

/* ===== 断点：>1080 → 1080 → 768 → 480，列数单调不增 ===== */
@media(max-width:1080px){.checkout-layout{grid-template-columns:1fr 300px}.product-options{grid-template-columns:1fr}.checkout-section{padding:20px}.checkout-steps b{width:15px}}
@media(max-width:768px){
  .checkout-page{padding-top:15px}
  /* P0 返回入口常驻首屏 */
  .checkout-head{flex-wrap:wrap;justify-content:flex-start;gap:12px}
  .back-link{display:inline-flex;order:-1;width:100%;min-height:44px;font-size:var(--fs-body-s,12px)}
  .secure{display:none}
  .checkout-steps{flex:1;justify-content:center;gap:6px}
  .checkout-steps b{width:12px}
  .checkout-title{padding:28px 0 22px}
  .checkout-layout{grid-template-columns:1fr}
  /* P0 恢复 DOM 自然顺序：原 .order-summary{order:-1} 已删除；撤销 5 条 display:none 改紧凑排版 */
  .summary-sticky{padding:16px 24px;position:relative;top:0}
  .summary-sticky>h2{display:block;font-size:var(--fs-h3,18px);margin-bottom:12px}
  .summary-art{display:grid;grid-template-columns:56px 1fr;gap:10px;padding-bottom:12px}
  .summary-art img{width:56px;height:68px}
  .summary-lines{display:grid;gap:8px;padding:12px 0}
  .promise{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:10px;margin-bottom:12px}
  .promise span:nth-child(3){grid-column:1/-1}
  .summary-total{padding:0 0 14px}
  .summary-sticky>p{display:block;font-size:var(--fs-body-s,12px)}
  .submit-order{width:100%;min-height:46px}
  .checkout-section{padding:18px 14px}
  .draft-info{grid-template-columns:90px 1fr;gap:13px}
  .draft-info>img{width:90px;height:115px}
  .draft-info p{-webkit-line-clamp:1}
  .product-options{grid-template-columns:1fr}
  .spec-options{gap:7px}
  .spec-options button{padding:10px}
  .inline-options button{padding:9px 12px}
  .address-grid{grid-template-columns:1fr}
  .address-grid .full{grid-column:auto}
}
@media(max-width:480px){
  .checkout-steps{gap:4px}
  .checkout-steps b{width:8px}
  .spec-options{grid-template-columns:1fr}
  .inline-options{flex-wrap:wrap}
  .summary-art{grid-template-columns:48px 1fr}
  .summary-art img{width:48px;height:60px}
  .promise{grid-template-columns:1fr}
  .promise span:nth-child(3){grid-column:auto}
}
</style>
