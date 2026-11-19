<template>
  <div class="nav-wrap">
    <div class="notice"><span>AI 试稿 · 画师亲绘 · 全程可溯</span><span class="notice-right">新用户赠 10 次创作机会 <RouterLink to="/create">即刻体验 <el-icon><ArrowRight /></el-icon></RouterLink></span></div>
    <header class="navbar">
      <div class="nav-inner container-wide">
        <RouterLink to="/" class="brand" aria-label="镜绘首页">
          <span class="brand-seal">镜</span>
          <span class="brand-name serif">镜绘<small>JINGHUI</small></span>
        </RouterLink>
        <nav class="desktop-nav" aria-label="主导航">
          <RouterLink v-for="item in links" :key="item.path" :to="item.path" :class="{ active: route.path === item.path }">{{ item.label }}</RouterLink>
        </nav>
        <div class="nav-actions">
          <template v-if="auth.loggedIn">
            <el-dropdown trigger="click">
              <button class="user-entry"><span class="avatar">{{ auth.user?.nickname?.slice(0,1) || '镜' }}</span><span class="user-name">{{ auth.user?.nickname || '我的镜绘' }}</span><el-icon><ArrowDown /></el-icon></button>
              <template #dropdown><el-dropdown-menu>
                <el-dropdown-item @click="router.push('/profile')">个人中心</el-dropdown-item>
                <el-dropdown-item @click="router.push('/gallery')">我的形象</el-dropdown-item>
                <el-dropdown-item @click="router.push('/orders')">我的订单</el-dropdown-item>
                <el-dropdown-item v-if="auth.isAdmin" @click="router.push('/admin')">运营后台</el-dropdown-item>
                <el-dropdown-item divided @click="auth.logout()">退出登录</el-dropdown-item>
              </el-dropdown-menu></template>
            </el-dropdown>
          </template>
          <RouterLink v-else to="/login" class="login-link">登录</RouterLink>
          <RouterLink to="/create" class="btn btn-primary create-btn"><el-icon><MagicStick /></el-icon>开始创作</RouterLink>
          <button class="mobile-toggle" aria-label="打开菜单" @click="mobileOpen = true"><el-icon><Menu /></el-icon></button>
        </div>
      </div>
    </header>
    <Transition name="drawer">
      <div v-if="mobileOpen" class="mobile-menu">
        <div class="mobile-top"><RouterLink to="/" class="brand" @click="mobileOpen=false"><span class="brand-seal">镜</span><span class="brand-name serif">镜绘<small>JINGHUI</small></span></RouterLink><button class="icon-btn" @click="mobileOpen=false"><el-icon><Close /></el-icon></button></div>
        <nav><RouterLink v-for="item in links" :key="item.path" :to="item.path" @click="mobileOpen=false"><span>{{ item.label }}</span><el-icon><ArrowRight /></el-icon></RouterLink></nav>
        <div class="mobile-bottom"><p>以 AI 为镜，以匠心成绘。</p><RouterLink v-if="!auth.loggedIn" to="/login" class="btn btn-outline" @click="mobileOpen=false">登录 / 注册</RouterLink><RouterLink to="/create" class="btn btn-primary" @click="mobileOpen=false">开始 AI 创作</RouterLink></div>
      </div>
    </Transition>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const route = useRoute(); const router = useRouter(); const auth = useAuthStore(); const mobileOpen = ref(false)
const links = [{path:'/create',label:'AI 创作'},{path:'/artists',label:'画师名录'},{path:'/orders',label:'进度追踪'}]
</script>
<style scoped>
.nav-wrap { position: sticky; top: 0; z-index: 50; }
.notice { height: 30px; padding: 0 28px; background: var(--azure); color: rgba(255,250,239,.78); font-size: 10px; letter-spacing: .15em; display: flex; align-items: center; justify-content: space-between; }
.notice-right { display: flex; gap: 15px; align-items: center; }.notice a { color: #e3c99e; display: inline-flex; align-items: center; gap: 3px; letter-spacing: .04em; }
.navbar { height: 76px; background: rgba(246,242,233,.92); backdrop-filter: blur(18px); border-bottom: 1px solid var(--line); }
.nav-inner { height: 100%; display: flex; align-items: center; justify-content: space-between; }
.brand { display: inline-flex; align-items: center; gap: 11px; }
.brand-seal { width: 39px; height: 39px; background: var(--cinnabar); color: #fff4e1; display: grid; place-items: center; font-family: var(--serif); font-size: 25px; border-radius: 2px; box-shadow: inset 0 0 0 3px var(--cinnabar), inset 0 0 0 4px rgba(255,244,225,.55); }
.brand-name { font-size: 24px; font-weight: 700; letter-spacing: .16em; line-height: 1.1; }
.brand-name small { display: block; font-family: var(--sans); font-size: 7px; letter-spacing: .42em; margin-top: 5px; font-weight: 500; color: var(--muted); }
.desktop-nav { display: flex; align-items: center; gap: clamp(20px,2.5vw,38px); margin-left: 60px; }
.desktop-nav a { position: relative; font-size: 13px; color: var(--ink-soft); padding: 28px 0; transition: .2s; }
.desktop-nav a::after { content: ''; position: absolute; left: 50%; right: 50%; bottom: 17px; height: 2px; background: var(--cinnabar); transition: .25s; }
.desktop-nav a:hover, .desktop-nav a.active { color: var(--cinnabar); }.desktop-nav a.active::after { left: 30%; right: 30%; }
.nav-actions { display: flex; align-items: center; gap: 18px; }
.login-link { font-size: 13px; color: var(--ink-soft); }.login-link:hover { color: var(--cinnabar); }
.create-btn { min-height: 40px; padding: 0 18px; font-size: 12px; }
.user-entry { display: flex; align-items: center; gap: 8px; background: none; border: 0; color: var(--ink); font-size: 12px; }
.avatar { width: 31px; height: 31px; border-radius: 50%; display: grid; place-items: center; color: var(--azure); background: #e4ded0; border: 1px solid var(--line); font-family: var(--serif); }
.mobile-toggle { display: none; border: 0; background: none; font-size: 23px; color: var(--ink); padding: 5px; }
.mobile-menu { position: fixed; inset: 0; z-index: 100; background: var(--paper); padding: 20px 24px 28px; display: flex; flex-direction: column; }
.mobile-top { display: flex; justify-content: space-between; align-items: center; padding-bottom: 28px; border-bottom: 1px solid var(--line); }
.mobile-menu nav { display: flex; flex-direction: column; padding: 24px 0; }
.mobile-menu nav a { display: flex; justify-content: space-between; align-items: center; font-family: var(--serif); font-size: 23px; letter-spacing: .1em; padding: 18px 2px; border-bottom: 1px solid var(--line); }
.mobile-menu nav a.router-link-active { color: var(--cinnabar); }
.mobile-bottom { margin-top: auto; display: grid; gap: 12px; }.mobile-bottom p { color: var(--muted); font-family: var(--serif); font-size: 13px; letter-spacing: .1em; text-align: center; }
.drawer-enter-active,.drawer-leave-active{transition:.3s}.drawer-enter-from,.drawer-leave-to{opacity:0;transform:translateX(30px)}
@media(max-width:1000px){.desktop-nav{gap:18px;margin-left:20px}.desktop-nav a{font-size:12px}.user-name{display:none}}
@media(max-width:768px){.notice{padding:0 16px;justify-content:center}.notice-right{display:none}.navbar{height:66px}.desktop-nav,.create-btn,.login-link,.user-entry{display:none}.mobile-toggle{display:block}.nav-actions{gap:8px}.brand-seal{width:35px;height:35px;font-size:22px}.brand-name{font-size:21px}}
</style>
