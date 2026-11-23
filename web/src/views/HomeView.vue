<template>
  <div>
    <section class="hero">
      <div class="hero-orb orb-one" aria-hidden="true"></div><div class="hero-orb orb-two" aria-hidden="true"></div>
      <div class="container hero-grid">
        <div class="hero-copy fade-up">
          <div class="hero-kicker"><span></span>AI × 传统手作<span class="vertical">东方形象定制平台</span></div>
          <h1 class="display-title">先见心中模样<br>再落<span class="accent">人间一笔</span><span class="title-dot">。</span></h1>
          <p class="hero-sub">用 AI 反复描绘，直到遇见满意的自己。<br>再由签约画师亲笔创作，让数字想象成为可珍藏的手作。</p>
          <div class="hero-actions"><RouterLink to="/create" class="btn btn-primary btn-lg">免费生成我的形象<el-icon><ArrowRight /></el-icon></RouterLink><a href="#process" class="text-link hit-44">了解如何创作<span class="circle"><el-icon aria-hidden="true"><ArrowDown /></el-icon></span></a></div>
          <div class="hero-proof"><div><strong>20<sup>+</sup></strong><span>东方美学风格</span></div><i></i><div><strong>3–7<sup>天</sup></strong><span>画师匠心创作</span></div><i></i><div><strong>100<sup>%</sup></strong><span>过程透明可溯</span></div></div>
        </div>
        <div class="hero-art fade-up-delay">
          <div class="art-shadow"></div>
          <div class="main-frame"><img src="/assets/art-1.svg" alt="镜绘东方风格 AI 形象作品" /><div class="frame-label"><span>AI 定稿 · 工笔人物</span><span>JINGHUI NO. 001</span></div></div>
          <div class="small-frame"><img src="/assets/compare-hand.svg" alt="画师手绘作品" /><span>画师亲绘</span></div>
          <div class="seal hero-seal">镜绘</div>
          <div class="floating-note"><span class="note-dot"></span><div><strong>从灵感到作品</strong><small>每一笔，都有迹可循</small></div><el-icon aria-hidden="true"><Right /></el-icon></div>
          <span class="brush-word serif" aria-hidden="true">绘</span>
        </div>
      </div>
      <div class="container hero-bottom"><span>TRADITION MEETS IMAGINATION</span><div class="cloud-line" aria-hidden="true"></div><span>EST. 2026</span></div>
    </section>

    <section class="section" id="process">
      <div class="container">
        <SectionHeader eyebrow="HOW IT WORKS" title="四步，让想象落笔成真" description="你负责想象与选择，我们负责让每一步都简单、透明、值得期待。" center />
        <div class="process-grid">
          <div v-for="(step,i) in steps" :key="step.title" class="process-item">
            <div class="step-top"><span class="step-no">0{{ i+1 }}</span><div class="step-icon"><el-icon aria-hidden="true"><component :is="step.icon" /></el-icon></div><span v-if="i<3" class="step-line"></span></div>
            <h3 class="serif">{{ step.title }}</h3><p>{{ step.desc }}</p><span class="step-caption">{{ step.caption }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-light inspiration">
      <div class="container">
        <div class="split-head"><SectionHeader eyebrow="INSPIRATION GALLERY" title="千面东方，总有一面是你" description="从工笔的细腻，到水墨的留白。选择一种风格，也可以写下只属于你的意境。" /><RouterLink to="/create" class="btn btn-outline">探索全部风格<el-icon><ArrowRight /></el-icon></RouterLink></div>
        <div class="scroll-x-wrap"><div class="filter-row scroll-x" tabindex="0" role="group" aria-label="风格筛选，可左右滑动"><button v-for="c in categories" :key="c" class="chip hit-44" :class="{active: category===c}" :aria-pressed="category===c" @click="category=c">{{ c }}</button></div></div>
        <div class="art-grid"><ArtworkCard v-for="(art,i) in filteredArts" :key="art.title" :image="art.image" :title="art.title" :subtitle="art.style" :badge="i===0?'本周热门':''" @view="router.push('/create')" /></div>
        <div class="gallery-note"><span class="seal-mini">AI</span><p>以上作品均由镜绘风格模板生成，仅作灵感展示。<br>你的下一幅作品，可以从一个词语开始。</p><RouterLink to="/create">开始我的第一幅<el-icon><ArrowRight /></el-icon></RouterLink></div>
      </div>
    </section>

    <section class="section compare-section">
      <div class="container compare-grid">
        <div class="compare-copy"><span class="eyebrow">FROM PIXELS TO PAPER</span><h2 class="serif">AI 看见想象<br>画师赋予<span>灵魂</span></h2><p>AI 让创意没有门槛，画师让作品不可复制。定稿之后，签约画师会重新理解线条、神态与意境，用传统技法完成真正的艺术创作。</p><ul><li><span>01</span>定稿前不限思路，满意后再下单</li><li><span>02</span>画师范本复核，尊重你的每一处期待</li><li><span>03</span>起稿、勾线、分染，关键节点实拍同步</li></ul><RouterLink to="/artists" class="text-arrow">认识我们的画师<el-icon><ArrowRight /></el-icon></RouterLink></div>
        <div class="compare-visual">
          <div class="compare-canvas"><img src="/assets/compare-hand.svg" alt="画师手绘定稿" class="hand-img"/><div class="ai-layer" :style="{'--compare': compare + '%'}"><img src="/assets/compare-ai.svg" alt="AI 形象定稿" /></div><div class="compare-line" :style="{left: compare + '%'}"><span><el-icon aria-hidden="true"><DCaret /></el-icon></span></div><span class="compare-label left">AI 定稿</span><span class="compare-label right">画师亲绘</span></div>
          <input v-model="compare" type="range" min="10" max="90" aria-label="拖动比较 AI 定稿与画师亲绘" :aria-valuetext="`AI 定稿占 ${compare}%，画师亲绘占 ${100-compare}%`" />
          <p><el-icon aria-hidden="true"><DCaret /></el-icon>左右滑动，看见从数字到纸面的温度</p>
        </div>
      </div>
    </section>

    <section class="artist-banner">
      <div class="container artist-grid"><div class="artist-art"><img src="/assets/art-6.svg" alt="镜绘签约画师创作意象"/><div class="artist-quote serif">“一笔有来处，<br>一画有归途。”</div></div><div class="artist-copy"><span class="eyebrow">MEET THE ARTISTS</span><h2 class="serif">让手艺被看见<br>让创作者有名字</h2><p>镜绘连接传统画师与当代生活。每一幅定制作品都会署名创作者，你不仅收到一幅画，也读到一门技艺、一段坚守的故事。</p><div class="artist-stats"><div><strong>10<sup>+</sup></strong><span>年均创作经验</span></div><div><strong>6</strong><span>传统创作画种</span></div><div><strong>1 : 1</strong><span>专属作品沟通</span></div></div><RouterLink to="/artists" class="btn btn-light">走进画师的故事<el-icon><ArrowRight /></el-icon></RouterLink></div></div>
    </section>

    <section class="section final-cta"><div class="container final-inner"><span class="mini-ornament">◇</span><span class="eyebrow">YOUR STORY, YOUR PORTRAIT</span><h2 class="serif">下一件值得珍藏的作品<br>从此刻的想象开始</h2><p>新用户免费获得 10 次 AI 创作机会，满意后再决定是否定制。</p><RouterLink to="/create" class="btn btn-primary btn-lg">免费创作我的形象<el-icon><ArrowRight /></el-icon></RouterLink><span class="no-risk">无需付费 · 反复试稿 · 满意再定制</span></div></section>
  </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import SectionHeader from '@/components/SectionHeader.vue'
import ArtworkCard from '@/components/ArtworkCard.vue'
const router = useRouter(); const compare = ref(50); const category = ref('全部风格')
const steps = [
  {icon:'EditPen',title:'写下心中所想',desc:'一句描述，或从东方美学模板中找到灵感。',caption:'自由提示词 · 预设模板'},
  {icon:'MagicStick',title:'AI 反复试稿',desc:'生成不同构图与风格，直到遇见满意的形象。',caption:'先看效果 · 满意再定'},
  {icon:'Brush',title:'画师亲笔创作',desc:'选定载体，签约画师从起稿到上色亲手完成。',caption:'真人创作 · 画者署名'},
  {icon:'Box',title:'见证与珍藏',desc:'关键节点实拍同步，成品装裱后送抵你的手中。',caption:'全程可溯 · 专属珍藏'}
]
const categories = ['全部风格','工笔人物','水墨写意','东方幻想']
const arts = [
  {title:'月下仕女',style:'工笔人物 · 雅致东方',image:'/assets/art-1.svg',category:'工笔人物'},
  {title:'朱砂旧梦',style:'东方幻想 · 新中式',image:'/assets/art-2.svg',category:'东方幻想'},
  {title:'青山如故',style:'青绿山水 · 东方幻想',image:'/assets/art-3.svg',category:'东方幻想'},
  {title:'青花映照',style:'工笔人物 · 青花美学',image:'/assets/art-4.svg',category:'工笔人物'},
  {title:'敦煌遗韵',style:'东方幻想 · 壁画质感',image:'/assets/art-5.svg',category:'东方幻想'},
  {title:'松间清影',style:'水墨写意 · 留白',image:'/assets/art-6.svg',category:'水墨写意'}
]
const filteredArts = computed(() => category.value==='全部风格' ? arts : arts.filter(a=>a.category===category.value))
</script>
<style scoped>
.hero { position: relative; overflow: hidden; padding: 80px 0 28px; min-height: 720px; }
.hero::before { content: ''; position: absolute; width: 48%; height: 80%; right: 0; top: 0; background: radial-gradient(ellipse, rgba(181,148,97,.15), transparent 68%); }
.hero-orb { position: absolute; border-radius: 50%; filter: blur(1px); pointer-events: none; }.orb-one { width: 300px; height: 300px; left: -180px; top: 200px; border: 1px solid rgba(181,148,97,.18); }.orb-two { width: 80px; height: 80px; left: 45%; bottom: 50px; background: rgba(169,75,60,.035); }
.hero-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; align-items: center; position: relative; }
#process { scroll-margin-top: var(--sticky-offset); }
.hero-kicker { display: flex; align-items: center; gap: 10px; color: var(--cinnabar); font-size: var(--fs-body-s); font-weight: 600; letter-spacing: .2em; margin-bottom: 25px; }.hero-kicker>span:first-child { width: 24px; height: 1px; background: var(--cinnabar); }.hero-kicker .vertical { color: var(--ink-2); font-weight: 400; letter-spacing: .12em; border-left: 1px solid var(--line); padding-left: 14px; margin-left: 4px; }
.accent { color: var(--cinnabar); position: relative; }.accent::after { content: ''; position: absolute; left: 2%; right: 0; bottom: -6px; height: 8px; background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='8'%3E%3Cpath d='M0 5 Q50 0 100 4 T200 2' fill='none' stroke='%23a94b3c' stroke-width='1.2' opacity='.55'/%3E%3C/svg%3E") center/100% 100% no-repeat; }.title-dot { color: var(--gilt-dark); }
.hero-sub { font-size: 15px; line-height: 2.05; color: var(--ink-soft); margin: 30px 0; font-weight: 300; letter-spacing: .04em; }
.hero-actions { display: flex; align-items: center; gap: 28px; }.text-link { display: inline-flex; align-items: center; gap: 12px; font-size: 12px; color: var(--azure); }.circle { width: 32px; height: 32px; display: grid; place-items: center; border: 1px solid var(--line); border-radius: 50%; transition: .2s; }.text-link:hover .circle { border-color: var(--cinnabar); color: var(--cinnabar); transform: translateY(3px); }
.hero-proof { display: flex; align-items: center; gap: 26px; margin-top: 45px; }.hero-proof>div { display: flex; flex-direction: column; gap: 5px; }.hero-proof strong { font-family: var(--serif); font-size: 23px; font-weight: 500; color: var(--azure); }.hero-proof sup { font-family: var(--sans); font-size: var(--fs-caption); margin-left: 2px; color: var(--gilt-dark); }.hero-proof span { font-size: var(--fs-body-s); color: var(--ink-2); letter-spacing: .06em; }.hero-proof i { height: 28px; width: 1px; background: var(--line); }
.hero-art { height: 570px; position: relative; max-width: 540px; width: 100%; justify-self: end; }.art-shadow { position: absolute; width: 350px; height: 480px; background: #e8dfcf; transform: rotate(5deg); left: 110px; top: 26px; }
.main-frame { position: absolute; width: 365px; left: 68px; top: 0; padding: 11px 11px 0; background: #faf7f0; box-shadow: 0 25px 70px rgba(45,42,34,.16); transform: rotate(1.5deg); }.main-frame img { height: 465px; width: 100%; object-fit: cover; }.frame-label { display: flex; justify-content: space-between; align-items: center; height: 44px; font-size: var(--fs-body-s); letter-spacing: .06em; color: var(--ink-2); }.frame-label span:last-child { font-size: var(--fs-body-s); letter-spacing: .14em; }
.small-frame { position: absolute; right: -4px; bottom: 10px; width: 176px; padding: 8px 8px 28px; background: #faf7f0; box-shadow: 0 15px 40px rgba(45,42,34,.15); transform: rotate(-5deg); animation: breathe 6s ease-in-out infinite; }.small-frame img { height: 212px; object-fit: cover; object-position: center; }.small-frame span { position: absolute; bottom: 8px; left: 10px; font-size: var(--fs-body-s); letter-spacing: .2em; color: var(--ink-2); }
.hero-seal { position: absolute; left: 30px; bottom: 56px; transform: rotate(-8deg); }
.floating-note { position: absolute; right: 0; top: 60px; padding: 13px 15px; background: rgba(252,250,245,.92); backdrop-filter: blur(8px); box-shadow: 0 10px 30px rgba(45,42,34,.09); display: flex; align-items: center; gap: 10px; font-size: var(--fs-body-s); }.floating-note strong { display: block; font-size: var(--fs-body); font-weight: 500; }.floating-note small { color: var(--ink-2); font-size: var(--fs-body-s); }.note-dot { width: 7px; height: 7px; border-radius: 50%; background: #718c70; box-shadow: 0 0 0 4px rgba(113,140,112,.12); }.floating-note>.el-icon { margin-left: 8px; color: var(--gilt-dark); }
.brush-word { position: absolute; left: -25px; top: 45px; font-size: 100px; color: rgba(46,72,88,.035); font-weight: 900; }
.hero-bottom { display: flex; align-items: center; gap: 25px; margin-top: 40px; font-size: var(--fs-body-s); letter-spacing: .25em; color: var(--ink-2); }.hero-bottom .cloud-line { flex: 1; }
.process-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 32px; }.step-top { display: flex; align-items: center; position: relative; margin-bottom: 22px; }.step-no { font-family: var(--serif); font-size: 13px; color: var(--gilt-dark); margin-right: 16px; }.step-icon { width: 58px; height: 58px; border-radius: 50%; border: 1px solid rgba(181,148,97,.45); display: grid; place-items: center; color: var(--cinnabar); font-size: 24px; background: var(--paper-light); position: relative; z-index: 2; transition: .3s; }.process-item:hover .step-icon { background: var(--cinnabar); color: #fff7e8; transform: translateY(-4px); }.step-line { position: absolute; height: 1px; background: var(--line); left: 98px; width: calc(100% + 10px); top: 50%; }.process-item h3 { margin: 0 0 12px; font-size: 20px; font-weight: 600; letter-spacing: .05em; }.process-item p { color: var(--muted); font-size: 12px; line-height: 1.85; margin: 0 0 13px; max-width: 220px; }.step-caption { font-size: var(--fs-body-s); letter-spacing: .08em; color: var(--gilt-dark); }
.split-head { display: flex; justify-content: space-between; align-items: flex-end; }.split-head .section-head { margin-bottom: 25px; }.split-head>.btn { margin-bottom: 28px; }.filter-row { display: flex; gap: 10px; margin-bottom: 30px; }.filter-row .chip { flex-shrink: 0; }.art-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 34px 25px; }
.gallery-note { margin-top: 45px; padding-top: 25px; border-top: 1px solid var(--line); display: flex; align-items: center; flex-wrap: wrap; gap: 14px; }.seal-mini { width: 35px; height: 35px; border: 1px solid var(--cinnabar); color: var(--cinnabar); display: grid; place-items: center; font-family: var(--serif); font-size: var(--fs-caption); transform: rotate(-3deg); }.gallery-note p { font-size: var(--fs-body-s); line-height: 1.8; color: var(--ink-2); margin: 0; }.gallery-note a { margin-left: auto; display: flex; align-items: center; gap: 8px; color: var(--cinnabar); font-size: 12px; }
.compare-grid { display: grid; grid-template-columns: .85fr 1.15fr; gap: 100px; align-items: center; }.compare-copy h2 { font-size: clamp(32px,3.5vw,46px); font-weight: 600; line-height: 1.5; letter-spacing: .06em; margin: 18px 0 22px; }.compare-copy h2 span { color: var(--cinnabar); }.compare-copy>p { color: var(--muted); font-size: 13px; line-height: 2; }.compare-copy ul { list-style: none; padding: 0; margin: 28px 0; }.compare-copy li { display: flex; align-items: center; gap: 14px; padding: 11px 0; border-bottom: 1px solid var(--line); font-size: 12px; }.compare-copy li span { color: var(--gilt-dark); font-family: var(--serif); font-size: var(--fs-caption); }.text-arrow { color: var(--cinnabar); display: inline-flex; gap: 8px; align-items: center; font-size: 12px; }
.compare-visual { text-align: center; }.compare-canvas { height: 480px; position: relative; overflow: hidden; box-shadow: 0 18px 50px rgba(44,42,34,.12); background: #e8dfcf; }.compare-canvas>img,.ai-layer img { width: 100%; height: 100%; object-fit: cover; object-position: center 35%; }.ai-layer { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; overflow: hidden; border-right: 1px solid #fff; clip-path: inset(0 calc(100% - var(--compare,50%)) 0 0); }.compare-line { position: absolute; top: 0; bottom: 0; width: 1px; background: #fff; }.compare-line span { position: absolute; left: -18px; top: 50%; width: 36px; height: 36px; background: #faf7ef; color: var(--cinnabar); border-radius: 50%; display: grid; place-items: center; box-shadow: 0 4px 15px rgba(0,0,0,.15); }.compare-label { position: absolute; top: 18px; background: rgba(250,247,239,.88); padding: 7px 12px; font-size: var(--fs-body-s); letter-spacing: .1em; pointer-events: none; }.compare-label.left { left: 18px; }.compare-label.right { right: 18px; }.compare-visual input { width: 80%; margin-top: 25px; accent-color: var(--cinnabar); }.compare-visual>p { font-size: var(--fs-body-s); color: var(--ink-2); display: flex; justify-content: center; align-items: center; gap: 7px; }
.artist-banner { background: var(--azure); color: #f5f0e6; padding: 85px 0; }.artist-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 100px; align-items: center; }.artist-art { height: 420px; position: relative; }.artist-art img { width: 76%; height: 100%; object-fit: cover; opacity: .9; }.artist-quote { position: absolute; right: 0; bottom: 35px; background: var(--paper); color: var(--azure); padding: 25px 28px; font-size: 20px; line-height: 1.8; box-shadow: 0 15px 40px rgba(0,0,0,.18); }.artist-copy h2 { font-size: clamp(32px,3.5vw,45px); line-height: 1.5; font-weight: 500; letter-spacing: .06em; margin: 18px 0; }.artist-copy>p { color: var(--on-dark-muted); font-size: 13px; line-height: 2; max-width: 450px; }.artist-copy .eyebrow { color: #d0b482; }.artist-stats { display: flex; gap: 38px; margin: 30px 0; }.artist-stats>div { display: flex; flex-direction: column; }.artist-stats strong { font-family: var(--serif); font-size: 25px; font-weight: 400; }.artist-stats sup { font-size: var(--fs-caption); color: #d0b482; }.artist-stats span { color: var(--on-dark-muted); font-size: var(--fs-body-s); margin-top: 5px; }
.final-cta { text-align: center; position: relative; overflow: hidden; }.final-cta::before,.final-cta::after { content: ''; position: absolute; border: 1px solid rgba(181,148,97,.15); border-radius: 50%; width: 350px; height: 350px; top: 20%; }.final-cta::before { left: -220px; }.final-cta::after { right: -220px; }.final-inner { position: relative; }.mini-ornament { display: block; color: var(--gilt-dark); font-size: 35px; margin-bottom: 15px; }.final-inner h2 { font-size: clamp(31px,4vw,45px); line-height: 1.6; font-weight: 500; letter-spacing: .06em; margin: 20px 0 15px; }.final-inner p { color: var(--muted); font-size: 13px; margin-bottom: 30px; }.no-risk { display: block; margin-top: 16px; color: var(--ink-2); font-size: var(--fs-body-s); letter-spacing: .08em; }
@media(max-width:1080px){.hero-grid{gap:20px}.hero-art{transform:scale(.88);transform-origin:right center}.compare-grid{gap:50px}.artist-grid{gap:50px}}
@media(max-width:768px){.hero{padding:48px 0 20px;min-height:auto}.hero-grid{grid-template-columns:1fr}.hero-copy{text-align:center}.hero-kicker{justify-content:center;font-size:var(--fs-body-s)}.hero-sub{font-size:13px;margin:23px 0}.hero-actions{justify-content:center;gap:18px}.text-link{font-size:var(--fs-body-s)}.hero-proof{justify-content:center;gap:20px;margin-top:32px}.hero-art{height:480px;transform:none;justify-self:center;margin-top:25px;max-width:420px}.main-frame{width:290px;left:45px}.main-frame img{height:370px}.small-frame{width:135px;right:0}.small-frame img{height:165px}.floating-note{right:0;top:30px}.hero-seal{left:16px;bottom:45px}.art-shadow{width:280px;height:390px;left:75px}.hero-bottom{margin-top:15px}.hero-bottom>span{display:none}.process-grid{grid-template-columns:1fr 1fr;gap:35px 20px}.step-line{display:none}.process-item p{font-size:var(--fs-body-s)}.split-head{display:block}.split-head>.btn{display:inline-flex;width:100%;min-height:46px;justify-content:center;margin:0 0 20px}.filter-row{overflow-x:auto;padding-bottom:5px}.filter-row .chip{flex-shrink:0}.art-grid{grid-template-columns:1fr 1fr;gap:24px 12px}.gallery-note a{display:inline-flex;width:100%;min-height:44px;justify-content:center;margin:12px 0 0}.compare-grid{grid-template-columns:1fr;gap:40px}.compare-canvas{height:420px}.artist-grid{grid-template-columns:1fr;gap:45px}.artist-art{height:330px}.artist-copy{order:-1}.artist-stats{gap:28px}.artist-banner{padding:65px 0}.final-inner .eyebrow{font-size:var(--fs-caption)}.final-inner h2{font-size:29px}}
@media(max-width:480px){.hero-actions{flex-direction:column}.hero-proof{gap:13px}.hero-art{transform:scale(.9);transform-origin:center top;margin-bottom:-45px}.process-grid{grid-template-columns:1fr}.process-item{text-align:center}.step-top{justify-content:center}.process-item p{margin-inline:auto}.compare-canvas{height:360px}}
</style>
