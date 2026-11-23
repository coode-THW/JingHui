<template>
  <div class="studio-page">
    <div class="container-wide studio-heading"><div><span class="eyebrow">AI CREATION STUDIO</span><h1 class="serif">形象创作工坊</h1><p>不必会写提示词，选一种喜欢的东方意境，再换成你的故事。</p></div><div class="quota"><span class="quota-icon"><el-icon><MagicStick /></el-icon></span><div><small>我的创作次数</small><strong>{{ auth.loggedIn ? auth.quota : '登录后查看' }}<em v-if="auth.loggedIn"> 次</em></strong></div><RouterLink v-if="!auth.loggedIn" to="/login?redirect=/create">登录</RouterLink></div></div>
    <div class="container-wide studio-layout">
      <section class="creation-panel paper-card">
        <div class="panel-title"><span>01</span><h2 class="serif">选择东方风格</h2><small>STYLE</small></div>
        <div class="scroll-x-wrap"><div class="category-tabs scroll-x" tabindex="0" role="group" aria-label="风格分类，可左右滑动"><button v-for="c in categories" :key="c" :class="{active:category===c}" :aria-pressed="category===c" @click="category=c">{{ c }}</button></div></div>
        <div v-if="loadingTemplates" class="template-grid"><div v-for="i in 4" :key="i" class="template-skeleton skeleton"></div></div>
        <div v-else class="template-grid" id="template-grid">
          <button v-for="(tpl,i) in visibleTemplates" :key="tpl.id" class="template-card" :class="{selected:selectedTemplate?.id===tpl.id}" :aria-pressed="selectedTemplate?.id===tpl.id" :aria-label="`选择风格：${tpl.name}`" @click="selectTemplate(tpl)"><img :src="templateCover(tpl,i)" :alt="tpl.name"/><span class="template-shade"></span><div><strong class="serif">{{ tpl.name }}</strong><small>{{ tpl.category }}</small></div><span class="selected-check"><el-icon><Check /></el-icon></span></button>
        </div>
        <button v-if="filteredTemplates.length>4" class="more-templates" :aria-expanded="showAll" aria-controls="template-grid" @click="showAll=!showAll">{{ showAll?'收起风格':'展开更多风格' }}<el-icon><ArrowDown v-if="!showAll"/><ArrowUp v-else/></el-icon></button>

        <div class="panel-divider"></div>
        <div class="panel-title"><span>02</span><h2 class="serif">描绘你的想象</h2><small>PROMPT</small></div>
        <div class="prompt-box" :class="{focused:promptFocused}"><textarea v-model="prompt" id="prompt" aria-label="描述你的想象" aria-describedby="prompt-count" maxlength="500" placeholder="例如：一位穿青色宋制汉服的女孩，站在月下桂花树旁，神情温柔，工笔画风，细腻线条，留白背景……" @focus="promptFocused=true" @blur="promptFocused=false"></textarea><div class="prompt-bottom"><button @click="polishPrompt"><el-icon><MagicStick /></el-icon>帮我润色</button><span id="prompt-count" aria-live="off">{{ prompt.length }} / 500</span></div></div>
        <div class="keyword-row"><span>灵感词</span><button v-for="word in keywords" :key="word" @click="addKeyword(word)">+ {{ word }}</button></div>

        <div class="panel-divider"></div>
        <div class="panel-title"><span>03</span><h2 class="serif">调整画幅</h2><small>FORMAT</small></div>
        <div class="format-row"><div class="format-options"><button v-for="r in ratios" :key="r.value" :class="{active:ratio===r.value}" :aria-pressed="ratio===r.value" @click="ratio=r.value"><span :class="r.class"></span><small>{{ r.label }}</small></button></div><div class="count-select"><label>生成数量</label><el-select v-model="count" aria-label="生成数量" style="width:110px"><el-option :value="1" label="1 幅"/><el-option :value="2" label="2 幅"/><el-option :value="4" label="4 幅"/></el-select></div></div>
        <div class="generation-note"><el-icon><InfoFilled /></el-icon><span>本次将消耗 {{ count }} 次创作机会，约需 10–30 秒</span><span class="demo-badge">可扩展 AI 渠道</span></div>
        <button class="btn btn-primary btn-lg generate-btn" :disabled="generating || !prompt.trim()" @click="generate"><el-icon v-if="!generating"><MagicStick /></el-icon><span>{{ generating ? '正在描绘你的想象…' : '开始生成形象' }}</span><el-icon v-if="!generating"><ArrowRight /></el-icon></button>
      </section>

      <section class="preview-panel">
        <div class="preview-top"><div><span class="live-dot"></span><span>创作预览</span></div><span>{{ selectedTemplate?.name || '自由创作' }} · {{ ratioLabel }}</span></div>
        <div class="preview-canvas" :class="canvasClass">
          <template v-if="generating"><div class="ink-loader"><div class="ink-circle c1"></div><div class="ink-circle c2"></div><div class="brush-loader"><el-icon><Brush /></el-icon></div></div><h3 class="serif">{{ loadingPhrases[loadingPhrase] }}</h3><p>AI 正在理解线条、色彩与东方意境</p><div class="loading-progress"><span :style="{width:loadingProgress+'%'}"></span></div><small>已用时 {{ elapsed }} 秒，请稍作等待</small><div class="culture-card"><span>非遗小识</span><p>{{ cultureFacts[cultureIndex] }}</p></div></template>
          <template v-else-if="generatedAssets.length"><div class="result-grid" :class="{'multi':generatedAssets.length>1}"><button v-for="(asset,i) in generatedAssets" :key="asset.id || i" class="result-item" :class="{selected:selectedAssetIndex===i}" :aria-pressed="selectedAssetIndex===i" :aria-label="`选择第 ${i+1} 幅生成形象`" @click="selectedAssetIndex=i"><img :src="mediaUrl(asset.url)" :alt="`第 ${i+1} 幅生成形象`"/><span class="result-check"><el-icon><Check /></el-icon></span></button></div><div class="result-seal">定稿候选</div></template>
          <template v-else><img class="placeholder-art" :src="templateCover(selectedTemplate,0)" alt="风格预览"/><div class="preview-placeholder"><span class="placeholder-seal serif">镜</span><h3 class="serif">你的想象，将在这里成形</h3><p>选择风格并描述心中模样<br>点击「开始生成形象」</p></div></template>
        </div>
        <div v-if="generatedAssets.length && !generating" class="result-info"><div><span class="success-mark"><el-icon><CircleCheck /></el-icon></span><div><strong>已生成 {{ generatedAssets.length }} 幅形象</strong><small>点击图片选择最满意的一幅</small></div></div><button class="text-button" @click="generate"><el-icon><RefreshRight /></el-icon>换一批</button></div>
        <div v-else class="preview-tips"><span><el-icon><Lock /></el-icon>你的作品仅自己可见</span><span><el-icon><Picture /></el-icon>支持高清下载</span></div>
        <div class="result-actions"><button class="btn btn-outline" :disabled="!generatedAssets.length || generating" @click="downloadCurrent"><el-icon><Download /></el-icon>下载形象</button><button class="btn btn-primary" :disabled="!generatedAssets.length || generating" @click="goCheckout">定稿并去定制<el-icon><ArrowRight /></el-icon></button></div>
        <p class="result-disclaimer">AI 生成结果可能存在随机性。定稿后，画师会与你确认细节再开始创作。</p>
      </section>
    </div>
    <div class="container studio-help"><div><span class="serif">不知道如何描述？</span><p>试试「人物 + 服饰 + 场景 + 情绪 + 画风」，就能写出好提示词。</p></div><button class="text-button" @click="useExample">使用示例提示词<el-icon><ArrowRight /></el-icon></button></div>
  </div>
</template>
<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { aiApi, contentApi, mediaUrl } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import type { MediaAsset, Template } from '@/types'

const router=useRouter(); const auth=useAuthStore()
const templates=ref<Template[]>([]); const loadingTemplates=ref(true); const selectedTemplate=ref<Template|null>(null)
const category=ref('全部'); const showAll=ref(false); const prompt=ref(''); const promptFocused=ref(false)
const ratio=ref('3:4'); const count=ref(1); const generating=ref(false); const generatedAssets=ref<MediaAsset[]>([]); const selectedAssetIndex=ref(0)
const loadingProgress=ref(5); const elapsed=ref(0); const loadingPhrase=ref(0); const cultureIndex=ref(0)
let timers:number[]=[]; let pollTimer:number|undefined
const keywords=['月下桂花','宋制汉服','温柔回眸','山水留白','敦煌飞天','清冷高级感']
const ratios=[{value:'1:1',label:'方形 1:1',class:'square'},{value:'3:4',label:'肖像 3:4',class:'portrait'},{value:'9:16',label:'长卷 9:16',class:'scroll'}]
const loadingPhrases=['正在铺陈宣纸底色','正在勾勒人物轮廓','正在晕染东方色彩','即将完成最后一笔']
const cultureFacts=['工笔画讲究“三矾九染”，层层设色，才能呈现温润而细腻的色彩。','中国画讲究“留白”，无画处并非空白，而是意境与想象的延伸。','敦煌壁画中的青金石与朱砂，跨越千年仍保留着动人的色彩。','团扇又称“纨扇”，自汉代以来便是诗画与风雅生活的载体。']
const categories=computed(()=>['全部',...Array.from(new Set(templates.value.map(t=>t.category).filter(Boolean)))].slice(0,7))
const filteredTemplates=computed(()=>category.value==='全部'?templates.value:templates.value.filter(t=>t.category===category.value))
const visibleTemplates=computed(()=>showAll.value?filteredTemplates.value:filteredTemplates.value.slice(0,4))
const ratioLabel=computed(()=>ratios.find(r=>r.value===ratio.value)?.label)
const canvasClass=computed(()=>ratio.value==='1:1'?'square-canvas':ratio.value==='9:16'?'scroll-canvas':'portrait-canvas')
const templateCover=(tpl:Template|null|undefined,i:number)=>mediaUrl(tpl?.cover_url||tpl?.cover_media_url||tpl?.example_url||`/assets/art-${((tpl?.id||i+1)-1)%8+1}.svg`)

onMounted(async()=>{try{templates.value=await contentApi.templates();if(templates.value.length)selectTemplate(templates.value[0])}catch(e){ElMessage.warning('模板服务暂未连接，请检查后端服务');templates.value=localTemplates;selectTemplate(templates.value[0])}finally{loadingTemplates.value=false}})
onBeforeUnmount(()=>{timers.forEach(clearInterval);if(pollTimer)clearTimeout(pollTimer)})
function selectTemplate(tpl:Template){selectedTemplate.value=tpl;prompt.value=tpl.positive_prompt||tpl.description||prompt.value}
function addKeyword(word:string){if(!prompt.value.includes(word))prompt.value=prompt.value.replace(/[，。\s]*$/,'')+'，'+word}
function polishPrompt(){if(!prompt.value.trim()){ElMessage.info('先写下一点想象，再让我帮你润色');return}if(!prompt.value.includes('细节丰富'))prompt.value+='，人物神态自然，线条细腻，色彩温润，细节丰富，东方美学构图，高级感';ElMessage.success('已补充人物神态与画面质感描述')}
function useExample(){prompt.value='一位穿青色宋制汉服的女孩，站在月下桂花树旁，微风轻起，神情温柔，工笔人物画风，细腻线条，宣纸肌理，雅致留白';selectedAssetIndex.value=0}
function startLoading(){generating.value=true;generatedAssets.value=[];elapsed.value=0;loadingProgress.value=5;loadingPhrase.value=0;cultureIndex.value=0;timers.push(window.setInterval(()=>{elapsed.value++;loadingProgress.value=Math.min(92,loadingProgress.value+Math.random()*6);loadingPhrase.value=Math.min(3,Math.floor(elapsed.value/5))},1000));timers.push(window.setInterval(()=>cultureIndex.value=(cultureIndex.value+1)%cultureFacts.length,5000))}
function stopLoading(){generating.value=false;loadingProgress.value=100;timers.forEach(clearInterval);timers=[]}
async function generate(){
  if(!auth.loggedIn){ElMessage.info('登录后即可免费生成 10 次');router.push('/login?redirect=/create');return}
  startLoading()
  try{
    const task=await aiApi.generate({prompt:prompt.value,template_id:selectedTemplate.value?.id,ratio:ratio.value,count:count.value,params:{ratio:ratio.value,count:count.value}})
    const id=task.id||task.task_id
    if(task.status==='SUCCESS'){setTaskResult(task);stopLoading();return}
    await pollTask(id)
  }catch(e:any){stopLoading();ElMessage.error(e.message||'生成失败，请稍后重试')}
}
async function pollTask(id:number){const started=Date.now();const poll=async()=>{try{const task=await aiApi.task(id);if(task.status==='SUCCESS'){setTaskResult(task);stopLoading();ElMessage.success('你的专属形象已生成');return}if(task.status==='FAILED')throw new Error(task.error_msg||'生成失败');if(Date.now()-started>90000)throw new Error('生成时间较长，请稍后在“我的形象”中查看');pollTimer=window.setTimeout(poll,1800)}catch(e:any){stopLoading();ElMessage.error(e.message)}};await poll()}
function setTaskResult(task:any){const assets=task.assets||task.result_assets||task.media_assets||(task.asset?[task.asset]:[])||(task.result?.assets)||[];generatedAssets.value=assets;selectedAssetIndex.value=0;if(!assets.length)ElMessage.warning('任务已完成，请前往“我的形象”查看作品');else ElMessage.success('你的专属形象已生成');auth.fetchMe()}
async function downloadCurrent(){const asset=generatedAssets.value[selectedAssetIndex.value];if(!asset)return;const a=document.createElement('a');a.href=mediaUrl(asset.url);a.download=`镜绘-${selectedTemplate.value?.name||'AI形象'}.svg`;a.target='_blank';a.click()}
function goCheckout(){const asset=generatedAssets.value[selectedAssetIndex.value];if(!asset)return;localStorage.setItem('jinghui_draft',JSON.stringify({asset_id:asset.id,image:mediaUrl(asset.url),prompt:prompt.value,template:selectedTemplate.value?.name}));router.push('/checkout')}
const localTemplates:Template[]=[
  {id:1,category:'工笔人物',name:'月下仕女',positive_prompt:'东方女子，宋制汉服，月下桂花，工笔人物，细腻线条，宣纸肌理'},
  {id:2,category:'东方幻想',name:'朱砂旧梦',positive_prompt:'东方幻想人物，朱砂红与黛蓝，流线衣袂，国风插画'},
  {id:3,category:'水墨写意',name:'青山如故',positive_prompt:'青山远黛，云雾缭绕，水墨写意，大量留白，东方意境'},
  {id:4,category:'青花美学',name:'青花映照',positive_prompt:'青花瓷器拟人，黛蓝纹样，古典女子，新中式美学'},
  {id:5,category:'敦煌壁画',name:'敦煌遗韵',positive_prompt:'敦煌飞天，飘带，赭石与石绿，壁画斑驳质感'},
  {id:6,category:'水墨写意',name:'松间清影',positive_prompt:'松间文人，山水清影，淡墨，文人画，诗意留白'}
]
</script>
<style scoped>
.studio-page{padding:55px 0 45px;background:linear-gradient(180deg,#f6f2e9,#f1ecdf);min-height:100vh}
.studio-heading{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:30px}
.studio-heading h1{font-size:var(--fs-h1);font-weight:600;letter-spacing:.08em;margin:12px 0 8px}
.studio-heading p{margin:0;color:var(--ink-2);font-size:var(--fs-body-s)}
.quota{display:flex;align-items:center;gap:12px;padding:13px 17px;border:1px solid var(--line);background:rgba(252,250,245,.7);min-width:185px;flex-wrap:wrap}
.quota-icon{width:37px;height:37px;display:grid;place-items:center;border-radius:50%;background:rgba(169,75,60,.09);color:var(--cinnabar)}
.quota small{display:block;font-size:var(--fs-body-s);color:var(--ink-2)}
.quota strong{font-family:var(--serif);font-size:17px;font-weight:500}
.quota em{font-family:var(--sans);font-size:var(--fs-body-s);font-style:normal;color:var(--ink-2)}
.quota a{font-size:var(--fs-body-s);color:var(--cinnabar);margin-left:auto}
.studio-layout{display:grid;grid-template-columns:minmax(480px,.95fr) minmax(450px,1.05fr);gap:25px;align-items:start}
.creation-panel{padding:28px 30px}
.panel-title{display:flex;align-items:center;gap:10px;margin-bottom:18px}
.panel-title>span{font-family:var(--serif);color:var(--gilt-dark);font-size:var(--fs-caption)}
.panel-title h2{font-size:var(--fs-h3);margin:0;font-weight:600;letter-spacing:.06em}
.panel-title small{margin-left:auto;font-size:var(--fs-body-s);letter-spacing:.2em;color:var(--ink-2)}
.category-tabs{display:flex;gap:6px;border-bottom:1px solid var(--line);margin-bottom:17px;overflow-x:auto}
.category-tabs button{flex-shrink:0;border:0;background:none;padding:0 12px 11px;color:var(--ink-2);font-size:var(--fs-body-s);position:relative;min-height:44px;transition:background .2s,color .2s}
.category-tabs button:hover{color:var(--cinnabar);background:rgba(169,75,60,.05)}
.category-tabs button:active{background:rgba(169,75,60,.12);transform:translateY(1px)}
.category-tabs button.active{color:var(--cinnabar)}
.category-tabs button.active::after{content:'';position:absolute;bottom:-1px;left:20%;right:20%;height:2px;background:var(--cinnabar)}
.template-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.template-card{position:relative;padding:0;border:2px solid transparent;background:#e8e0d3;overflow:hidden;text-align:left;aspect-ratio:.8;min-height:44px;transition:background .2s,color .2s,border-color .2s}
.template-card:hover{color:var(--cinnabar);background:rgba(169,75,60,.05);border-color:rgba(169,75,60,.45)}
.template-card:active{background:rgba(169,75,60,.12)}
.template-card img{width:100%;height:100%;object-fit:cover;transition:.3s}
.template-card:hover img{transform:scale(1.05)}
.template-card.selected{border-color:var(--cinnabar)}
.template-shade{position:absolute;inset:35% 0 0;background:linear-gradient(transparent 0%,rgba(22,30,30,.55) 45%,rgba(22,30,30,.88) 100%)}
.template-card>div{position:absolute;left:9px;right:7px;bottom:8px;color:white;padding:8px 10px 10px}
.template-card strong{display:block;font-size:var(--fs-body-s);font-weight:500;letter-spacing:.05em;text-shadow:0 1px 2px rgba(0,0,0,.5)}
.template-card small{font-size:var(--fs-body-s);color:rgba(255,255,255,.92)}
.selected-check{display:none;position:absolute;right:6px;top:6px;width:19px;height:19px;background:var(--cinnabar);color:white;border-radius:50%;place-items:center;font-size:11px}
.selected .selected-check{display:grid}
.template-skeleton{aspect-ratio:.8}
.more-templates{width:100%;border:0;background:none;color:var(--ink-2);font-size:var(--fs-body-s);padding:12px 0 0;display:flex;align-items:center;justify-content:center;gap:5px;min-height:44px;transition:background .2s,color .2s}
.more-templates:hover{color:var(--cinnabar);background:rgba(169,75,60,.05)}
.more-templates:active{background:rgba(169,75,60,.12)}
.panel-divider{height:1px;background:var(--line);margin:24px 0}
.prompt-box{border:1px solid var(--line);background:rgba(255,255,255,.45);transition:.2s}
.prompt-box.focused{border-color:var(--cinnabar);box-shadow:0 0 0 3px rgba(169,75,60,.06);background:#fffdf8}
.prompt-box textarea{width:100%;height:115px;resize:none;border:0;background:transparent;padding:14px;font-size:var(--fs-body);line-height:1.9;color:var(--ink)}
.prompt-box textarea::placeholder{color:#aaa79d}
.prompt-bottom{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-top:1px solid var(--line);font-size:var(--fs-body-s);color:var(--ink-2)}
.prompt-bottom button{border:0;background:none;color:var(--cinnabar);display:flex;align-items:center;gap:4px;font-size:var(--fs-body-s);min-height:44px;transition:background .2s}
.prompt-bottom button:hover{background:rgba(169,75,60,.05)}
.prompt-bottom button:active{background:rgba(169,75,60,.12)}
.keyword-row{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-top:12px}
.keyword-row>span{font-size:var(--fs-body-s);color:var(--ink-2);margin-right:3px}
.keyword-row button{border:0;background:#eee8dc;color:var(--ink-soft);padding:5px 8px;font-size:var(--fs-body-s);border-radius:2px;min-height:44px;transition:background .2s,color .2s}
.keyword-row button:hover{color:var(--cinnabar);background:rgba(169,75,60,.05)}
.keyword-row button:active{background:rgba(169,75,60,.12)}
.format-row{display:flex;justify-content:space-between;align-items:center}
.format-options{display:flex;gap:10px}
.format-options button{width:67px;border:1px solid var(--line);background:transparent;padding:9px 4px;color:var(--ink-2);position:relative;min-height:44px;transition:background .2s,color .2s}
.format-options button:hover{color:var(--cinnabar);background:rgba(169,75,60,.05)}
.format-options button:active{background:rgba(169,75,60,.12)}
.format-options button.active{border-color:var(--cinnabar);color:var(--cinnabar);background:rgba(169,75,60,.04)}
.format-options button.active::after{content:'✓';position:absolute;right:-1px;top:-1px;width:18px;height:18px;background:var(--cinnabar);color:#fff;border-radius:50%;display:grid;place-items:center;font-size:10px;line-height:1}
.format-options button>span{display:block;border:1px solid currentColor;margin:0 auto 6px}
.format-options .square{width:18px;height:18px}
.format-options .portrait{width:15px;height:20px}
.format-options .scroll{width:11px;height:20px}
.format-options small{font-size:var(--fs-body-s)}
.count-select{display:flex;align-items:center;gap:9px}
.count-select label{font-size:var(--fs-body-s);color:var(--ink-2)}
.generation-note{display:flex;align-items:center;gap:6px;color:var(--ink-2);font-size:var(--fs-body-s);margin:20px 0 12px;flex-wrap:wrap}
.demo-badge{margin-left:auto;color:var(--gilt-dark);border:1px solid rgba(181,148,97,.35);padding:3px 6px;font-size:var(--fs-body-s)}
.generate-btn{width:100%;font-size:14px;justify-content:center}
.generate-btn>.el-icon:last-child{margin-left:auto}
.generate-btn>.el-icon:first-child{margin-right:auto}
.preview-panel{position:sticky;top:var(--sticky-offset);background:#eae3d6;border:1px solid var(--line);padding:18px 22px 20px;min-height:0;display:flex;flex-direction:column;gap:12px}
.preview-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;font-size:var(--fs-body-s);color:var(--ink-2);flex-shrink:0}
.preview-top>div{display:flex;align-items:center;gap:7px;color:var(--ink-soft);font-size:var(--fs-body-s)}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--cinnabar)}
.preview-canvas{position:relative;width:100%;flex:1 1 auto;min-height:320px;height:auto;aspect-ratio:3/4;background:#e4dccd;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:.3s}
.preview-canvas.square-canvas{aspect-ratio:1/1}
.preview-canvas.scroll-canvas{aspect-ratio:9/16;max-height:calc(100vh - var(--sticky-offset) - 210px)}
.placeholder-art{position:absolute;width:100%;height:100%;object-fit:cover;filter:blur(2px);opacity:.25}
.preview-placeholder{position:relative;text-align:center;padding:30px}
.placeholder-seal{display:grid;place-items:center;width:50px;height:50px;border:1px solid rgba(169,75,60,.5);color:var(--cinnabar);font-size:25px;margin:0 auto 22px;transform:rotate(-4deg)}
.preview-placeholder h3{font-size:var(--fs-h3);font-weight:500;letter-spacing:.08em;margin:0 0 12px}
.preview-placeholder p{font-size:var(--fs-body-s);line-height:1.9;color:var(--ink-2)}
.preview-tips{display:flex;justify-content:center;gap:25px;margin-top:14px;color:var(--ink-2);font-size:var(--fs-body-s);flex-shrink:0}
.preview-tips span{display:flex;align-items:center;gap:4px}
.ink-loader{position:relative;width:100px;height:100px;margin-bottom:20px}
.ink-circle{position:absolute;inset:0;border-radius:50%;border:1px solid var(--cinnabar);animation:inkPulse 2s infinite}
.ink-circle.c2{animation-delay:1s}
.brush-loader{position:absolute;inset:22px;border-radius:50%;background:rgba(169,75,60,.08);display:grid;place-items:center;color:var(--cinnabar);font-size:30px}
.preview-canvas>h3{font-size:var(--fs-h3);font-weight:500;margin:0 0 8px}
.preview-canvas>p{font-size:var(--fs-body-s);color:var(--ink-2)}
.loading-progress{height:2px;background:rgba(46,72,88,.1);width:200px;margin:15px 0 8px}
.loading-progress span{height:100%;display:block;background:var(--cinnabar);transition:1s}
.preview-canvas>small{font-size:var(--fs-body-s);color:var(--ink-2)}
.culture-card{position:absolute;bottom:20px;left:25px;right:25px;padding:12px 15px;background:rgba(250,247,239,.7);border-left:2px solid var(--gilt);display:flex;align-items:center;gap:12px}
.culture-card>span{font-size:var(--fs-body-s);color:var(--gilt-dark);white-space:nowrap}
.culture-card p{margin:0;font-size:var(--fs-body-s);line-height:1.7;color:var(--ink-2)}
.result-grid{width:100%;height:100%;display:grid;grid-template-columns:1fr;gap:4px}
.result-grid.multi{grid-template-columns:1fr 1fr}
.result-item{position:relative;padding:0;border:2px solid transparent;background:none;overflow:hidden;min-height:44px;transition:background .2s,border-color .2s}
.result-item:hover{color:var(--cinnabar);background:rgba(169,75,60,.05);border-color:rgba(169,75,60,.45)}
.result-item:active{background:rgba(169,75,60,.12)}
.result-item img{width:100%;height:100%;object-fit:cover}
.result-item.selected{border-color:var(--cinnabar)}
.result-check{display:none;position:absolute;right:6px;top:6px;width:19px;height:19px;border-radius:50%;background:var(--cinnabar);color:white;place-items:center;font-size:11px}
.selected .result-check{display:grid}
.result-seal{position:absolute;left:15px;top:15px;background:var(--cinnabar);color:#fff1dc;padding:7px 10px;font-family:var(--serif);font-size:var(--fs-body-s);letter-spacing:.15em}
.result-info{display:flex;justify-content:space-between;align-items:center;margin-top:13px;flex-shrink:0;flex-wrap:wrap;gap:8px}
.result-info>div{display:flex;gap:9px;align-items:center}
.success-mark{color:#657e65;font-size:20px}
.result-info strong{display:block;font-size:var(--fs-body-s);font-weight:500}
.result-info small{font-size:var(--fs-body-s);color:var(--ink-2)}
.text-button{border:0;background:none;color:var(--cinnabar);font-size:var(--fs-body-s);display:inline-flex;align-items:center;gap:5px;min-height:44px;transition:background .2s}
.text-button:hover{background:rgba(169,75,60,.05)}
.text-button:active{background:rgba(169,75,60,.12)}
.result-actions{display:grid;grid-template-columns:1fr 1.4fr;gap:12px;margin-top:auto;flex-shrink:0}
.result-disclaimer{text-align:center;color:var(--ink-2);font-size:var(--fs-body-s);line-height:1.6;margin:12px 0 0;flex-shrink:0}
.studio-help{display:flex;align-items:center;justify-content:space-between;margin-top:25px;padding:18px 25px;border:1px solid var(--line);background:rgba(252,250,245,.5)}
.studio-help>div{display:flex;align-items:center;gap:18px}
.studio-help span{font-size:13px}
.studio-help p{margin:0;font-size:var(--fs-body-s);color:var(--ink-2)}
@media(max-width:1080px){.studio-layout{grid-template-columns:1fr 1fr}.creation-panel{padding:22px}.template-grid{grid-template-columns:repeat(2,1fr)}.template-card{aspect-ratio:1.1}.format-row{align-items:flex-end}.count-select{flex-direction:column;align-items:flex-start}.studio-help>div{display:block}.studio-help p{margin-top:5px}.preview-panel{position:relative;top:0}}
@media(max-width:768px){.studio-page{padding:35px 0}.studio-heading{align-items:flex-start}.studio-heading p{max-width:240px;line-height:1.7}.quota{min-width:auto;padding:9px 11px}.quota-icon{display:none}.studio-layout{grid-template-columns:1fr}.creation-panel{padding:22px 18px}.template-card{aspect-ratio:.78}.template-card small{display:none}.preview-panel{position:relative;top:0;min-height:auto;padding:15px}.preview-canvas{aspect-ratio:3/4;height:auto;max-height:70vh}.studio-help{padding:16px}.studio-help>div p{display:none}.format-options button{width:61px}.generation-note .demo-badge{display:none}}
@media(max-width:480px){.template-card{aspect-ratio:1}.format-row{display:block}.count-select{flex-direction:row;margin-top:15px}.quota{flex-wrap:wrap;gap:8px}.studio-heading p{max-width:none}.preview-canvas{aspect-ratio:3/4;height:auto;max-height:70vh}}
</style>
