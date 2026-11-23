<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-head paper-card">
        <div class="head-left">
          <div class="avatar-ring"><span class="big-avatar serif">{{ auth.user?.nickname?.slice(0,1)||'镜' }}</span></div>
          <div>
            <h1 class="serif">{{ auth.user?.nickname||'镜绘用户' }}</h1>
            <p>{{ auth.user?.email }}</p>
            <div class="head-tags"><span class="tag">{{ auth.user?.role==='ADMIN'?'运营账号':'镜绘创作者' }}</span><span class="join-date">加入于 {{ joinDate }}</span></div>
          </div>
        </div>
        <div class="quota-card">
          <span class="quota-label">AI 创作次数</span>
          <strong>{{ auth.quota }}</strong>
          <small>次可用</small>
          <RouterLink to="/create" class="btn btn-primary btn-sm">去创作</RouterLink>
        </div>
      </div>

      <div class="profile-grid">
        <section class="paper-card profile-card">
          <div class="card-title"><h2 class="serif">快捷入口</h2></div>
          <div class="quick-links">
            <RouterLink v-for="item in quickLinks" :key="item.path" :to="item.path">
              <div class="quick-icon"><el-icon><component :is="item.icon"/></el-icon></div>
              <div><strong>{{ item.title }}</strong><span>{{ item.desc }}</span></div>
              <el-icon class="go"><ArrowRight /></el-icon>
            </RouterLink>
          </div>
        </section>
        <section class="paper-card profile-card">
          <div class="card-title"><h2 class="serif">账号信息</h2><button class="edit-btn" :aria-expanded="editing" :aria-label="editing?'完成编辑':'编辑账号信息'" @click="editing=!editing">{{ editing?'完成':'编辑' }}</button></div>
          <dl class="info-list">
            <div><dt>昵称</dt><dd v-if="!editing">{{ auth.user?.nickname }}</dd><el-input v-else v-model="editForm.nickname" size="small" style="max-width:200px"/></div>
            <div><dt>登录邮箱</dt><dd>{{ auth.user?.email }}</dd></div>
            <div><dt>账号角色</dt><dd>{{ auth.user?.role==='ADMIN'?'平台运营':'注册用户' }}</dd></div>
            <div><dt>创作配额</dt><dd>{{ quotaDetail }}</dd></div>
          </dl>
        </section>
        <section class="paper-card profile-card">
          <div class="card-title"><h2 class="serif">最近消息</h2></div>
          <div v-if="messages.length" class="message-list">
            <div v-for="m in messages" :key="m.id" class="message-item" role="link" tabindex="0" @click="m.ref_order_id?router.push(`/orders/${m.ref_order_id}`):null" @keydown.enter="m.ref_order_id?router.push(`/orders/${m.ref_order_id}`):null" @keydown.space.prevent="m.ref_order_id?router.push(`/orders/${m.ref_order_id}`):null">
              <span class="msg-dot" :class="{unread:!m.is_read}"></span>
              <div><strong>{{ m.title }}</strong><p>{{ m.content }}</p></div>
              <time>{{ dateTime(m.created_at) }}</time>
            </div>
          </div>
          <div v-else class="msg-empty"><el-icon><Bell /></el-icon><p>暂无新消息</p></div>
        </section>
        <section class="paper-card profile-card danger-zone">
          <div class="card-title"><h2 class="serif">账号操作</h2></div>
          <button class="logout-btn" @click="confirmLogout"><el-icon><SwitchButton /></el-icon>退出登录</button>
        </section>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/services/api'
import { dateTime } from '@/utils/format'

const router=useRouter(), auth=useAuthStore(), messages=ref<any[]>([]), editing=ref(false)
const editForm=reactive({nickname:''})
const joinDate=computed(()=>{const u:any=auth.user;return u?.created_at?new Date(u.created_at).toLocaleDateString('zh-CN'):'2026 年'})
const quotaDetail=computed(()=>{const q=(auth.user as any)?.quota;return q?`剩余 ${q.remaining_count} / 共 ${q.total_purchased} 次（已用 ${q.total_used} 次）`:`剩余 ${auth.quota} 次`})
const quickLinks=[
  {path:'/create',icon:'MagicStick',title:'AI 创作工坊',desc:'生成新的东方形象'},
  {path:'/gallery',icon:'Picture',title:'我的形象',desc:'查看全部 AI 作品'},
  {path:'/orders',icon:'Tickets',title:'我的定制',desc:'追踪画师创作进度'}
]
onMounted(async()=>{editForm.nickname=auth.user?.nickname||'';try{const {request}=await import('@/services/api');messages.value=await request<any[]>(api.get('/messages'))}catch{messages.value=[]}})
async function confirmLogout(){try{await ElMessageBox.confirm('确定退出当前账号吗？','退出登录',{confirmButtonText:'退出',cancelButtonText:'取消',type:'warning'});auth.logout()}catch{}}
</script>
<style scoped>
.profile-page{padding:50px 0 90px;min-height:75vh}
.profile-head{display:flex;justify-content:space-between;align-items:center;padding:32px 36px;margin-bottom:22px}
.head-left{display:flex;align-items:center;gap:22px}
.avatar-ring{width:86px;height:86px;border-radius:50%;border:2px solid rgba(181,148,97,.5);display:grid;place-items:center;padding:4px}
.big-avatar{width:100%;height:100%;border-radius:50%;background:linear-gradient(135deg,var(--azure),var(--cinnabar));color:#fff4e1;display:grid;place-items:center;font-size:38px}
.profile-head h1{font-size:var(--fs-h1);margin:0 0 6px;letter-spacing:.06em}
.profile-head p{font-size:var(--fs-body-s);color:var(--ink-2);margin:0 0 10px}
.head-tags{display:flex;align-items:center;gap:10px}.join-date{font-size:var(--fs-body-s);color:var(--ink-2)}
.quota-card{text-align:center;padding:18px 28px;background:var(--paper);border:1px solid rgba(181,148,97,.3)}
.quota-label{display:block;font-size:var(--fs-body-s);letter-spacing:.15em;color:var(--gilt-dark);margin-bottom:8px}
.quota-card strong{font-family:var(--serif);font-size:38px;color:var(--cinnabar);font-weight:500}
.quota-card small{display:block;font-size:var(--fs-body-s);color:var(--ink-2);margin:2px 0 12px}
.profile-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.profile-card{padding:26px}
.card-title{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding-bottom:15px;margin-bottom:8px}
.card-title h2{font-size:var(--fs-h3);margin:0}
.edit-btn{border:0;background:none;color:var(--cinnabar);font-size:var(--fs-body-s);min-height:44px}
.quick-links{display:grid;gap:6px;padding-top:10px}
.quick-links a{display:flex;align-items:center;gap:14px;padding:13px 12px;transition:.2s;border-radius:3px;min-height:44px}
.quick-links a:hover{background:var(--paper)}
.quick-icon{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;background:rgba(169,75,60,.08);color:var(--cinnabar);font-size:17px;flex-shrink:0}
.quick-links strong{display:block;font-size:12px;font-weight:500}
.quick-links span{display:block;font-size:var(--fs-body-s);color:var(--ink-2);margin-top:3px}
.quick-links .go{margin-left:auto;color:var(--gilt)}
.info-list{margin:0;padding-top:8px}
.info-list>div{display:flex;justify-content:space-between;align-items:center;padding:13px 0;border-bottom:1px solid var(--line)}
.info-list>div:last-child{border:0}
.info-list dt{font-size:var(--fs-body-s);color:var(--ink-2)}
.info-list dd{margin:0;font-size:var(--fs-body-s)}
.message-list{display:grid;gap:4px;padding-top:10px;max-height:260px;overflow:auto}
.message-item{display:flex;gap:10px;align-items:flex-start;padding:11px 10px;cursor:pointer;transition:.2s;border-radius:3px;min-height:44px}
.message-item:hover{background:var(--paper)}
.msg-dot{width:7px;height:7px;border-radius:50%;background:#cfc8bb;margin-top:6px;flex-shrink:0}
.msg-dot.unread{background:var(--cinnabar)}
.message-item strong{font-size:var(--fs-body-s);font-weight:500}
.message-item p{font-size:var(--fs-body-s);color:var(--ink-2);margin:3px 0 0;line-height:1.6}
.message-item time{font-size:var(--fs-body-s);color:var(--ink-2);margin-left:auto;white-space:nowrap}
.msg-empty{text-align:center;padding:45px 0;color:var(--muted)}
.msg-empty .el-icon{font-size:26px;margin-bottom:10px}.msg-empty p{font-size:var(--fs-body-s)}
.danger-zone{display:flex;flex-direction:column}
.logout-btn{margin-top:auto;align-self:flex-start;display:flex;align-items:center;gap:7px;border:1px solid rgba(169,75,60,.4);background:none;color:var(--cinnabar);padding:10px 20px;font-size:var(--fs-body-s);min-height:44px}
.logout-btn:hover{background:rgba(169,75,60,.06)}
.quota-card .btn,.quick-links a,.edit-btn,.message-item,.logout-btn{min-height:44px}
.quota-card .btn:focus-visible,.quick-links a:focus-visible,.edit-btn:focus-visible,.message-item:focus-visible,.logout-btn:focus-visible{outline:2px solid var(--focus-ring);outline-offset:3px}
@media(max-width:768px){
  .profile-page{padding:35px 0 60px}
  .profile-head{flex-direction:column;gap:20px;align-items:flex-start;padding:24px 20px}
  .quota-card{width:100%;display:flex;align-items:center;justify-content:space-between;text-align:left;padding:14px 18px}
  .quota-card strong{font-size:28px}
  .quota-card small{display:none}
  .profile-grid{grid-template-columns:1fr}
  .info-list>div{flex-direction:column;align-items:flex-start;gap:4px}
  .info-list dd{text-align:left;max-width:100%;white-space:normal;overflow-wrap:anywhere}
}
</style>
