<template>
  <div class="section-head" :class="{ center }">
    <span class="eyebrow">{{ eyebrow }}</span>
    <h2 class="serif">{{ title }}</h2>
    <p v-if="description">{{ description }}</p>
    <slot />
  </div>
</template>
<script setup lang="ts">
defineProps<{ eyebrow: string; title: string; description?: string; center?: boolean }>()
</script>
<style scoped>
.section-head { margin-bottom: 44px; }
.section-head h2 { margin: 16px 0 12px; font-size: var(--fs-h2); font-weight: 600; letter-spacing: .05em; line-height: 1.45; }
.section-head p { max-width: 580px; color: var(--muted); font-size: var(--fs-body); line-height: 1.9; margin: 0; }
.center { text-align: center; }
.center p { margin-inline: auto; }
.center .eyebrow::after { content: ''; width: 26px; height: 1px; background: currentColor; }
</style>
