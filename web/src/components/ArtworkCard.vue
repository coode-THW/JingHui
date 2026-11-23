<template>
  <article class="art-card group">
    <div class="art-image">
      <img :src="mediaUrl(image)" :alt="title" loading="lazy" />
      <button class="card-hit" type="button" aria-hidden="true" tabindex="-1" @click="$emit('view')"></button>
      <span v-if="badge" class="badge">{{ badge }}</span>
      <div class="overlay">
        <slot name="actions">
          <button class="view-btn" :aria-label="'查看作品：'+title" @click="$emit('view')">查看作品 <el-icon><ArrowRight /></el-icon></button>
        </slot>
      </div>
    </div>
    <div class="art-info">
      <div><h3 class="serif">{{ title }}</h3><p>{{ subtitle }}</p></div>
      <button class="icon-btn small" aria-label="收藏" aria-hidden="true" tabindex="-1"><el-icon><Star /></el-icon></button>
    </div>
  </article>
</template>
<script setup lang="ts">
import { mediaUrl } from '@/services/api'
defineProps<{ image: string; title: string; subtitle?: string; badge?: string }>()
defineEmits(['view'])
</script>
<style scoped>
.art-image { position: relative; aspect-ratio: 4/5; border-radius: 3px; }
.card-hit { position: absolute; inset: 0; z-index: 1; border: 0; background: transparent; }
.badge { position: absolute; left: 14px; top: 14px; background: rgba(250,247,240,.88); backdrop-filter: blur(8px); color: var(--cinnabar); padding: 6px 10px; font-size: var(--fs-body-s); letter-spacing: .1em; }
.overlay { position: absolute; inset: 0; display: flex; align-items: flex-end; justify-content: center; padding: 22px; background: linear-gradient(transparent 55%, rgba(22,30,30,.42)); opacity: 0; visibility: hidden; transition: opacity .3s, visibility .3s; }
.art-card:hover .overlay, .art-card:focus-within .overlay { opacity: 1; visibility: visible; }
.view-btn { background: #faf7ef; color: var(--azure); border: 0; border-radius: 2px; min-height: 40px; padding: 0 18px; display: flex; align-items: center; gap: 8px; font-size: 12px; transform: translateY(8px); transition: .3s; }
.view-btn:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 3px; }
.art-card:hover .view-btn { transform: none; }
.art-info { display: flex; justify-content: space-between; align-items: center; padding: 17px 2px 4px; }
h3 { margin: 0 0 7px; font-size: 17px; font-weight: 600; letter-spacing: .06em; }
p { margin: 0; font-size: 12px; color: var(--muted); }
.small { width: 34px; height: 34px; color: var(--muted); position: relative; }
.small::after { content: ''; position: absolute; inset: -4px; }
@media(max-width:768px){
  /* Let the static overlay flow below the image instead of being clipped by overflow:hidden. */
  .art-image{aspect-ratio:auto;overflow:visible}
  .art-image img{height:auto;aspect-ratio:4/5;border-radius:3px}
  .overlay{position:static;opacity:1;visibility:visible;background:transparent;padding:10px 0 0;display:block}
  .view-btn{width:100%;min-height:46px;justify-content:center;transform:none;border:1px solid var(--line);background:var(--paper-light)}
  .art-info{padding-top:12px}
  h3{font-size:15px}
}
</style>
