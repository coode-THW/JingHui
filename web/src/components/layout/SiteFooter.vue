<template>
  <footer class="footer">
    <div class="cloud-line" aria-hidden="true"></div>
    <div class="container footer-main">
      <div class="footer-brand">
        <RouterLink to="/" class="brand"><span class="brand-seal">镜</span><span class="brand-name serif">镜绘<small>JINGHUI</small></span></RouterLink>
        <p>以 AI 为镜，照见心中之形；<br>以画师之手，绘成传世之作。</p>
        <span>让每一份想象，都有手可触摸的温度。</span>
      </div>
      <div class="footer-links"><h4>开始探索</h4><RouterLink to="/create">AI 形象创作</RouterLink><RouterLink to="/gallery">我的形象</RouterLink><RouterLink to="/orders">订单进度</RouterLink><RouterLink to="/profile">个人中心</RouterLink></div>
      <div class="footer-links"><h4>了解镜绘</h4><RouterLink to="/artists">签约画师</RouterLink><span class="footer-static">服务协议</span><span class="footer-static">隐私政策</span></div>
      <div class="footer-contact"><h4>创作咨询</h4><p>周一至周日 09:00–21:00</p><a href="mailto:hello@jinghui.art">hello@jinghui.art</a><div class="social"><button class="icon-btn" aria-label="微信" aria-hidden="true" tabindex="-1"><el-icon><ChatDotRound /></el-icon></button><button class="icon-btn" aria-label="分享" aria-hidden="true" tabindex="-1"><el-icon><Share /></el-icon></button></div></div>
    </div>
    <div class="container footer-bottom"><span>© 2026 镜绘 JINGHUI · 三创赛非遗创新项目</span><span>AI 辅助创意 · 尊重原创 · 匠心手作</span></div>
  </footer>
</template>
<style scoped>
.footer { background: #eee8dc; border-top: 1px solid var(--line); }
.cloud-line { margin: 0 auto; transform: translateY(-9px); width: 70%; }
.footer-main { display: grid; grid-template-columns: 2fr 1fr 1fr 1.3fr; gap: 60px; padding-block: 55px 45px; }
.brand { display: inline-flex; align-items: center; gap: 11px; }.brand-seal { width: 38px; height: 38px; background: var(--cinnabar); color: #fff4e1; display: grid; place-items: center; font-family: var(--serif); font-size: 24px; border-radius: 2px; }.brand-name { font-size: 23px; font-weight: 700; letter-spacing: .16em; line-height: 1.1; }.brand-name small { display: block; font-family: var(--sans); font-size: var(--fs-caption); letter-spacing: .42em; margin-top: 5px; color: var(--muted); }
.footer-brand p { font-family: var(--serif); font-size: 14px; line-height: 2.1; letter-spacing: .06em; margin: 24px 0 12px; }.footer-brand>span { font-size: var(--fs-body-s); color: var(--muted); }
h4 { font-size: 12px; font-weight: 600; letter-spacing: .12em; margin: 5px 0 22px; }
.footer-links { display: flex; flex-direction: column; gap: 14px; }.footer-links a,.footer-contact p,.footer-contact a,.footer-static { font-size: 12px; color: var(--muted); margin: 0; }.footer-links a:hover,.footer-contact a:hover { color: var(--cinnabar); }
.footer a:focus-visible, .footer button:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px; }
.social { display: flex; gap: 9px; margin-top: 22px; }
.footer-bottom { border-top: 1px solid var(--line); padding-block: 20px; display: flex; justify-content: space-between; font-size: 12px; letter-spacing: .05em; color: var(--muted); }
@media(max-width:768px){.footer-main{grid-template-columns:1fr 1fr;gap:35px 25px;padding-block:35px}.footer-brand{grid-column:1/-1}.footer-contact{grid-column:1/-1}.footer-bottom{flex-direction:column;gap:8px}.social{margin-top:14px}}
</style>
