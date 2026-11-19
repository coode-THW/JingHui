<template>
  <div class="artists-page">
    <section class="artists-hero">
      <div class="container hero-grid">
        <div class="hero-copy fade-up">
          <span class="eyebrow">THE HANDS BEHIND THE ART</span>
          <h1 class="display-title">让每一幅定制<br>都有<span>执笔的名字</span></h1>
          <p>他们研习线条、矿物色、水墨与丝线，也愿意倾听一个当代人的故事。镜绘让画师从作品背后走到你眼前，以本名或笔名署名，让每一份心意都有清晰的来处。</p>
          <div class="hero-actions"><a href="#artist-story" class="btn btn-primary btn-lg">走进画师故事<el-icon><ArrowDown /></el-icon></a><RouterLink to="/create" class="btn btn-outline btn-lg">创作我的形象</RouterLink></div>
          <div class="hero-stats"><div><strong>{{ artists.length || 5 }}<sup>位</sup></strong><span>不同领域的创作者</span></div><i></i><div><strong>1 : 1</strong><span>专属定稿沟通</span></div><i></i><div><strong>100<sup>%</sup></strong><span>手绘作品署名</span></div></div>
        </div>
        <div class="hero-art fade-up-delay">
          <div class="portrait-back"></div>
          <div class="portrait-main"><img src="/assets/art-6.svg" alt="东方水墨人物创作" /><div><span>松间清影</span><span>水墨写意 · 镜绘作品</span></div></div>
          <blockquote class="serif">“画得像，是起点。<br>画出那个人的神采，<br>才算真正落笔。”</blockquote>
          <span class="seal">画者</span>
        </div>
      </div>
    </section>

    <section class="section section-light artist-directory">
      <div class="container">
        <div class="directory-head"><SectionHeader eyebrow="ARTIST DIRECTORY" title="循着技艺，认识与你相宜的人" description="选择你偏好的创作方向。每位画师都有独特的观察方式，也会依据你的定稿与载体给出专业建议。" /><span class="directory-count">{{ filteredArtists.length.toString().padStart(2, '0') }} / {{ artists.length.toString().padStart(2, '0') }}</span></div>
        <div class="filter-row"><button v-for="item in categories" :key="item" class="chip" :class="{ active: category === item }" @click="setCategory(item)">{{ item }}</button></div>
        <div v-if="loading" class="directory-grid"><div v-for="i in 5" :key="i" class="artist-skeleton"><div class="skeleton"></div><span class="skeleton"></span><span class="skeleton"></span></div></div>
        <div v-else class="directory-grid">
          <button v-for="artist in filteredArtists" :key="artist.id" class="artist-card" :class="{ active: activeId === artist.id }" @click="selectArtist(artist)">
            <div class="artist-photo"><img :src="artistImage(artist)" :alt="`${artist.pen_name}的创作风格`" loading="lazy" /><span>{{ artist.location }}</span><i><el-icon><ArrowUpRight /></el-icon></i></div>
            <div class="artist-info"><div><h3 class="serif">{{ artist.pen_name }}</h3><span>{{ artist.years || 10 }} 年创作</span></div><p>{{ specialtiesText(artist.specialties) }}</p><div class="artist-card-foot"><span><el-icon><StarFilled /></el-icon>{{ Number(artist.rating || 5).toFixed(1) }}</span><span>{{ artist.works_count || 0 }} 件定制作品</span></div></div>
          </button>
        </div>
      </div>
    </section>

    <section v-if="activeArtist" class="section artist-story" id="artist-story">
      <div class="container">
        <div class="story-grid">
          <div class="story-portrait">
            <div class="story-image"><img :src="artistImage(activeArtist)" :alt="`${activeArtist.pen_name}画师作品意象`" /></div>
            <div class="story-signature"><span>本期画师</span><strong class="serif">{{ activeArtist.pen_name }}</strong><small>{{ activeArtist.location }} · {{ activeArtist.years || 10 }} 年研习</small></div>
          </div>
          <div class="story-copy">
            <span class="eyebrow">ARTIST STORY · {{ String(activeArtist.id).padStart(2, '0') }}</span>
            <h2 class="serif">{{ activeArtist.pen_name }}<span>{{ specialtiesText(activeArtist.specialties) }}</span></h2>
            <blockquote class="serif">“{{ activeArtist.quote }}”</blockquote>
            <p v-for="paragraph in activeArtist.story" :key="paragraph">{{ paragraph }}</p>
            <div class="story-meta"><div><strong>{{ activeArtist.years || 10 }}</strong><span>年技艺研习</span></div><div><strong>{{ activeArtist.works_count || 0 }}</strong><span>件定制作品</span></div><div><strong>{{ Number(activeArtist.rating || 5).toFixed(1) }}</strong><span>收藏者评分</span></div></div>
            <div class="story-tags"><span v-for="tag in activeArtist.specialties" :key="tag">{{ tag }}</span></div>
          </div>
        </div>
        <div class="works-head"><div><span class="eyebrow">SELECTED WORKS</span><h3 class="serif">笔墨之外，看见每个人的故事</h3></div><span>代表作品 · {{ activeArtist.pen_name }}</span></div>
        <div class="works-grid">
          <article v-for="(work, index) in activeArtist.works" :key="work.title" class="work-card"><div class="art-image"><img :src="work.image" :alt="work.title" loading="lazy" /><span>0{{ index + 1 }}</span></div><div><h4 class="serif">{{ work.title }}</h4><p>{{ work.medium }}</p></div></article>
        </div>
        <div class="story-bottom"><p>定制时会依据你的形象、载体与构图偏好匹配画师；你也可以在沟通时表达对某位画师的偏好。</p><RouterLink to="/create" class="btn btn-primary">带着故事去创作<el-icon><ArrowRight /></el-icon></RouterLink></div>
      </div>
    </section>

    <section class="collaboration-section">
      <div class="container collaboration-grid">
        <div><span class="eyebrow">A SHARED CREATION</span><h2 class="serif">不是把照片交给画笔<br>而是把故事交给彼此</h2></div>
        <div class="collaboration-steps"><div v-for="(step, index) in collaboration" :key="step.title"><span>0{{ index + 1 }}</span><div><h3 class="serif">{{ step.title }}</h3><p>{{ step.description }}</p></div></div></div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref } from 'vue'
import SectionHeader from '@/components/SectionHeader.vue'
import { contentApi, mediaUrl } from '@/services/api'
import type { Artist } from '@/types'

interface ArtistWork { title: string; medium: string; image: string }
interface ArtistProfile extends Omit<Artist, 'specialties'> {
  specialties: string[]
  story: string[]
  quote: string
  location: string
  works: ArtistWork[]
}

const artists = ref<ArtistProfile[]>([])
const loading = ref(true)
const category = ref('全部技艺')
const activeId = ref<number>(1)

const localArtists: ArtistProfile[] = [
  {
    id: 1, pen_name: '沈砚青', specialties: ['工笔人物', '宋代美学'], intro: '以细密线条与层层设色，描绘人物安静而绵长的神采。', avatar: '/assets/art-1.svg', rating: 4.9, works_count: 86, years: 12, location: '杭州',
    quote: '一根衣纹的转折里，也藏着人物没有说出口的情绪。',
    story: ['砚青从宋代院体画里学会克制，也从日常肖像里寻找新的表达。她习惯在动笔前读完定制者写下的故事，先确定一个眼神、一处手势，再让衣饰与背景慢慢生长出来。', '她尤其在意工笔的“慢”：勾线之后反复分染，颜色不喧哗，人物却逐渐有了呼吸。收到她的作品时，你也会在落款旁读到几句关于构图与用色的小手记。'],
    works: [{ title: '月下仕女', medium: '绢本设色 · 工笔人物', image: '/assets/art-1.svg' }, { title: '青花映照', medium: '纸本设色 · 青花美学', image: '/assets/art-4.svg' }, { title: '海棠春深', medium: '绢本设色 · 人物小像', image: '/assets/art-8.svg' }]
  },
  {
    id: 2, pen_name: '林晚樵', specialties: ['水墨写意', '文人山水'], intro: '以浓淡干湿回应人物气质，在留白里安放山水与心绪。', avatar: '/assets/art-6.svg', rating: 4.8, works_count: 64, years: 10, location: '苏州',
    quote: '留白不是没有画，是把余下的想象还给看画的人。',
    story: ['晚樵早年习山水，后来开始把人物放进自己熟悉的林泉之间。他不追求面面俱到的复刻，更关心一笔淡墨能否留下清冷，一道飞白能否写出行走时的风。', '每一幅写意定制，他都会先画两三张小幅墨稿，与定制者确认人物和场景的关系。正式落笔时则尽量一次成形，保留水墨不可复制的偶然与生机。'],
    works: [{ title: '松间清影', medium: '宣纸水墨 · 写意人物', image: '/assets/art-6.svg' }, { title: '青山如故', medium: '纸本水墨 · 山水人物', image: '/assets/art-3.svg' }, { title: '溪山独行', medium: '宣纸水墨 · 文人意趣', image: '/assets/art-7.svg' }]
  },
  {
    id: 3, pen_name: '苏青遥', specialties: ['青花美学', '釉下彩'], intro: '让黛蓝纹样从瓷面走入人物衣饰，在窑火中封存清澈颜色。', avatar: '/assets/art-4.svg', rating: 5, works_count: 52, years: 9, location: '景德镇',
    quote: '青花只有蓝与白，却能画出远近、阴晴和一个人的温度。',
    story: ['青遥在景德镇学习传统纹饰，也持续尝试人物题材的当代表达。她会先把 AI 定稿拆解为适合瓷绘的线面，再用分水技法让青色呈现由浓到淡的自然过渡。', '瓷板入窑之后，颜色会经历无法完全预料的变化。她把这种变化看作材料参与创作的过程，并为每件作品保留烧制记录，让收藏者看见火焰留下的独特痕迹。'],
    works: [{ title: '青花映照', medium: '釉下青花 · 瓷板画', image: '/assets/art-4.svg' }, { title: '月白风清', medium: '青花分水 · 人物瓷绘', image: '/assets/art-2.svg' }, { title: '瓷上故人', medium: '釉下彩 · 当代肖像', image: '/assets/art-7.svg' }]
  },
  {
    id: 4, pen_name: '周复礼', specialties: ['敦煌壁画', '岩彩'], intro: '研习矿物色与壁画肌理，让古老色彩承载今日的东方想象。', avatar: '/assets/art-5.svg', rating: 4.9, works_count: 47, years: 14, location: '敦煌',
    quote: '矿物色经得起时间，人物的故事也应该被认真地留下来。',
    story: ['复礼长期从事壁画临摹与岩彩创作，熟悉赭石、石绿与青金石色层的叠加方式。他的定制作品不直接复制洞窟图像，而是从色彩、飘带与构图中提取灵感。', '为了让现代人物与古朴质感自然相融，他会保留面部清晰的神采，再让衣饰与背景呈现壁画般的斑驳层次。每一次落色都有记录，作品也因此有了自己的时间纹理。'],
    works: [{ title: '敦煌遗韵', medium: '矿物岩彩 · 壁画人物', image: '/assets/art-5.svg' }, { title: '飞天新语', medium: '纸本岩彩 · 东方幻想', image: '/assets/art-2.svg' }, { title: '大漠花雨', medium: '矿物设色 · 人物群像', image: '/assets/art-3.svg' }]
  },
  {
    id: 5, pen_name: '贺小满', specialties: ['剪纸', '团扇'], intro: '以阴阳刻与轻快构图，把人物故事化为可以随风摇动的心意。', avatar: '/assets/art-8.svg', rating: 4.8, works_count: 71, years: 8, location: '西安',
    quote: '剪掉的是纸，留下的是人与人之间牵连不断的线。',
    story: ['小满从家乡窗花里认识剪纸，后来把人物侧影、宠物与纪念场景融入传统纹样。她讲究线条相连、虚实相生，让一张纸即使被镂空，依然保有完整的叙事。', '除了剪纸小像，她也把简洁的刻纸语言带入团扇设计。那些看似轻巧的花枝与衣纹，需要先经过严谨的构图，才能在扇面上显得自然、舒展。'],
    works: [{ title: '花间小像', medium: '手工剪纸 · 人物侧影', image: '/assets/art-8.svg' }, { title: '执扇听风', medium: '绢面团扇 · 人物小品', image: '/assets/art-1.svg' }, { title: '朱砂旧梦', medium: '剪纸衍生 · 新中式肖像', image: '/assets/art-2.svg' }]
  }
]

const collaboration = [
  { title: '读懂你的定稿', description: '画师阅读人物设定、服饰与场景偏好，结合载体判断适合保留与调整的细节。' },
  { title: '确认创作方向', description: '正式制作前沟通构图与风格；手绘作品先确认起稿，避免想象与成品之间出现偏差。' },
  { title: '让过程留下痕迹', description: '关键节点以实拍图文同步，成品附画师署名，让一件定制品也成为一段共同的创作记忆。' }
]

const categories = computed(() => ['全部技艺', ...Array.from(new Set(artists.value.flatMap(artist => artist.specialties)))])
const filteredArtists = computed(() => category.value === '全部技艺' ? artists.value : artists.value.filter(artist => artist.specialties.includes(category.value)))
const activeArtist = computed(() => artists.value.find(artist => artist.id === activeId.value) || filteredArtists.value[0])

onMounted(async () => {
  try {
    const data = await contentApi.artists()
    artists.value = data?.length ? data.map(normalizeArtist) : localArtists
  } catch {
    artists.value = localArtists
  } finally {
    activeId.value = artists.value[0]?.id || 1
    loading.value = false
  }
})

function normalizeArtist(artist: Artist, index: number): ArtistProfile {
  const fallback = localArtists[index % localArtists.length]
  const specialties = Array.isArray(artist.specialties) ? artist.specialties : String(artist.specialties || '工笔人物').split(/[,，、/]/).map(item => item.trim()).filter(Boolean)
  return {
    ...fallback,
    ...artist,
    specialties,
    intro: artist.intro || fallback.intro,
    story: artist.intro ? [artist.intro, fallback.story[1]] : fallback.story,
    quote: fallback.quote,
    location: fallback.location,
    works: fallback.works,
    avatar: artist.avatar || artist.avatar_url || fallback.avatar
  }
}

function artistImage(artist: ArtistProfile) {
  return mediaUrl(artist.avatar_url || artist.avatar || '/assets/art-1.svg')
}
function specialtiesText(specialties: string[]) {
  return specialties.join(' · ')
}
function setCategory(item: string) {
  category.value = item
  if (activeArtist.value && !filteredArtists.value.some(artist => artist.id === activeArtist.value.id)) activeId.value = filteredArtists.value[0]?.id || 1
}
async function selectArtist(artist: ArtistProfile) {
  activeId.value = artist.id
  await nextTick()
  document.getElementById('artist-story')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<style scoped>
.artists-hero { padding: 76px 0 90px; overflow: hidden; position: relative; }
.artists-hero::after { content: ''; position: absolute; width: 440px; height: 440px; border: 1px solid rgba(181,148,97,.12); border-radius: 50%; right: -270px; top: 30px; }
.hero-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 85px; align-items: center; }
.hero-copy h1 { margin-top: 22px; }
.hero-copy h1 span { color: var(--cinnabar); }
.hero-copy > p { max-width: 510px; margin: 28px 0 30px; color: var(--ink-soft); font-size: 14px; line-height: 2.1; }
.hero-actions { display: flex; gap: 13px; }
.hero-stats { display: flex; align-items: center; gap: 25px; margin-top: 40px; }
.hero-stats > div { display: flex; flex-direction: column; gap: 6px; }
.hero-stats strong { color: var(--azure); font: 500 24px var(--serif); }
.hero-stats sup { color: var(--gilt); font: 10px var(--sans); margin-left: 3px; }
.hero-stats span { color: var(--muted); font-size: 9px; letter-spacing: .05em; }
.hero-stats i { width: 1px; height: 30px; background: var(--line); }
.hero-art { position: relative; height: 565px; max-width: 520px; width: 100%; justify-self: end; }
.portrait-back { position: absolute; width: 350px; height: 490px; background: #e4ddcf; left: 60px; top: 28px; transform: rotate(5deg); }
.portrait-main { position: absolute; left: 30px; top: 0; width: 355px; padding: 11px 11px 0; background: var(--paper-light); box-shadow: 0 25px 60px rgba(48,45,35,.14); transform: rotate(-2deg); }
.portrait-main img { width: 100%; height: 470px; object-fit: cover; }
.portrait-main > div { display: flex; justify-content: space-between; align-items: center; height: 43px; color: var(--muted); font-size: 9px; letter-spacing: .1em; }
.portrait-main > div span:last-child { font-size: 8px; }
.hero-art blockquote { position: absolute; right: -5px; bottom: 30px; margin: 0; padding: 22px 26px; background: var(--azure); color: #f4eddf; box-shadow: 0 18px 45px rgba(46,72,88,.22); font-size: 16px; line-height: 1.9; letter-spacing: .05em; }
.hero-art .seal { position: absolute; right: 28px; top: 35px; transform: rotate(7deg); }
.directory-head { display: flex; align-items: flex-end; justify-content: space-between; }
.directory-count { color: var(--gilt); font: 14px var(--serif); letter-spacing: .15em; margin-bottom: 45px; }
.filter-row { display: flex; gap: 9px; flex-wrap: wrap; margin-bottom: 30px; }
.directory-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
.artist-card { min-width: 0; padding: 0; border: 1px solid var(--line); background: transparent; color: inherit; text-align: left; transition: .3s; }
.artist-card:hover, .artist-card.active { transform: translateY(-5px); border-color: rgba(169,75,60,.45); box-shadow: 0 16px 35px rgba(48,45,35,.07); }
.artist-card.active { box-shadow: inset 0 -2px var(--cinnabar), 0 16px 35px rgba(48,45,35,.07); }
.artist-photo { position: relative; height: 260px; overflow: hidden; background: #eae3d6; }
.artist-photo img { width: 100%; height: 100%; object-fit: cover; transition: transform .6s; }
.artist-card:hover img { transform: scale(1.04); }
.artist-photo > span { position: absolute; left: 10px; top: 10px; padding: 4px 8px; background: rgba(252,250,245,.86); color: var(--azure); font-size: 9px; }
.artist-photo > i { position: absolute; right: 10px; bottom: 10px; width: 30px; height: 30px; display: grid; place-items: center; background: rgba(252,250,245,.9); color: var(--cinnabar); border-radius: 50%; opacity: 0; transition: .25s; }
.artist-card:hover .artist-photo > i, .artist-card.active .artist-photo > i { opacity: 1; }
.artist-info { padding: 16px 14px; }
.artist-info > div:first-child { display: flex; align-items: baseline; justify-content: space-between; gap: 5px; }
.artist-info h3 { margin: 0; font-size: 18px; font-weight: 600; letter-spacing: .06em; }
.artist-info > div:first-child > span { color: var(--gilt); font-size: 8px; white-space: nowrap; }
.artist-info > p { height: 30px; margin: 8px 0 14px; color: var(--muted); font-size: 10px; line-height: 1.5; }
.artist-card-foot { display: flex; justify-content: space-between; gap: 5px; padding-top: 11px; border-top: 1px solid var(--line); color: var(--muted); font-size: 8px; }
.artist-card-foot span:first-child { display: flex; align-items: center; gap: 3px; color: var(--gilt); }
.artist-skeleton { padding-bottom: 20px; border: 1px solid var(--line); }
.artist-skeleton > div { height: 260px; margin-bottom: 16px; }
.artist-skeleton > span { display: block; height: 15px; margin: 10px 14px; }
.artist-skeleton > span:last-child { width: 60%; height: 10px; }
.artist-story { scroll-margin-top: 25px; }
.story-grid { display: grid; grid-template-columns: .85fr 1.15fr; gap: 90px; align-items: center; }
.story-portrait { position: relative; padding: 0 0 50px 30px; }
.story-image { height: 465px; padding: 10px; background: var(--paper-light); box-shadow: 0 20px 55px rgba(48,45,35,.12); transform: rotate(-2deg); }
.story-image img { width: 100%; height: 100%; object-fit: cover; }
.story-signature { position: absolute; left: 0; bottom: 0; min-width: 205px; padding: 18px 22px; background: var(--paper-light); border-left: 3px solid var(--cinnabar); box-shadow: 0 12px 35px rgba(48,45,35,.09); }
.story-signature > span { display: block; color: var(--gilt); font-size: 8px; letter-spacing: .18em; }
.story-signature strong { display: block; margin: 6px 0; font-size: 25px; font-weight: 600; letter-spacing: .1em; }
.story-signature small { color: var(--muted); font-size: 9px; }
.story-copy h2 { display: flex; align-items: baseline; gap: 17px; margin: 17px 0 15px; font-size: 39px; font-weight: 600; letter-spacing: .08em; }
.story-copy h2 span { color: var(--muted); font: 10px var(--sans); letter-spacing: .08em; }
.story-copy blockquote { margin: 0 0 20px; padding: 14px 18px; border-left: 1px solid var(--gilt); background: rgba(181,148,97,.055); color: var(--azure); font-size: 15px; line-height: 1.8; }
.story-copy > p { margin: 12px 0; color: var(--muted); font-size: 12px; line-height: 2.05; text-align: justify; }
.story-meta { display: flex; gap: 35px; margin-top: 23px; }
.story-meta > div { display: flex; flex-direction: column; gap: 3px; }
.story-meta strong { color: var(--cinnabar); font: 22px var(--serif); }
.story-meta span { color: var(--muted); font-size: 9px; }
.story-tags { display: flex; gap: 8px; margin-top: 20px; }
.story-tags span { padding: 5px 11px; border: 1px solid var(--line); color: var(--azure); font-size: 10px; }
.works-head { display: flex; align-items: flex-end; justify-content: space-between; margin: 75px 0 25px; padding-top: 30px; border-top: 1px solid var(--line); }
.works-head h3 { margin: 12px 0 0; font-size: 24px; font-weight: 600; letter-spacing: .06em; }
.works-head > span { color: var(--muted); font-size: 10px; }
.works-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 23px; }
.work-card { margin: 0; }
.work-card .art-image { position: relative; height: 330px; }
.work-card .art-image > span { position: absolute; left: 12px; top: 12px; width: 28px; height: 28px; display: grid; place-items: center; background: rgba(252,250,245,.85); color: var(--gilt); font: 9px var(--serif); }
.work-card h4 { margin: 14px 0 5px; font-size: 17px; font-weight: 600; letter-spacing: .06em; }
.work-card p { margin: 0; color: var(--muted); font-size: 10px; }
.story-bottom { display: flex; align-items: center; justify-content: space-between; gap: 25px; margin-top: 35px; padding: 23px 26px; background: #eee8dc; }
.story-bottom p { max-width: 670px; margin: 0; color: var(--muted); font-size: 11px; line-height: 1.8; }
.collaboration-section { padding: 85px 0; background: var(--azure); color: var(--paper-light); }
.collaboration-grid { display: grid; grid-template-columns: .85fr 1.15fr; gap: 90px; }
.collaboration-section .eyebrow { color: #d0b482; }
.collaboration-section h2 { margin: 20px 0 0; font-size: 32px; line-height: 1.65; font-weight: 500; letter-spacing: .05em; }
.collaboration-steps > div { display: flex; gap: 20px; padding: 18px 0; border-bottom: 1px solid rgba(246,242,233,.13); }
.collaboration-steps > div:first-child { padding-top: 0; }
.collaboration-steps > div > span { color: #d0b482; font: 12px var(--serif); padding-top: 4px; }
.collaboration-steps h3 { margin: 0 0 6px; font-size: 17px; font-weight: 500; }
.collaboration-steps p { margin: 0; color: rgba(246,242,233,.58); font-size: 11px; line-height: 1.8; }
@media (max-width: 1050px) {
  .hero-grid { gap: 35px; }
  .hero-art { transform: scale(.9); transform-origin: right center; }
  .directory-grid { grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .artist-photo { height: 320px; }
  .story-grid { gap: 50px; }
  .collaboration-grid { gap: 50px; }
}
@media (max-width: 768px) {
  .artists-hero { padding: 48px 0 65px; }
  .hero-grid { grid-template-columns: 1fr; }
  .hero-copy { text-align: center; }
  .hero-copy > p { font-size: 13px; margin: 22px auto 25px; }
  .hero-actions, .hero-stats { justify-content: center; }
  .hero-art { justify-self: center; transform: none; height: 510px; margin-top: 20px; max-width: 450px; }
  .portrait-main { width: 310px; left: 20px; }
  .portrait-main img { height: 415px; }
  .portrait-back { width: 310px; height: 435px; left: 55px; }
  .hero-art blockquote { right: 0; font-size: 14px; }
  .directory-head { display: block; }
  .directory-count { display: none; }
  .filter-row { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 5px; }
  .filter-row .chip { flex-shrink: 0; }
  .directory-grid { grid-template-columns: repeat(2, 1fr); gap: 14px; }
  .artist-photo { height: 270px; }
  .story-grid { grid-template-columns: 1fr; gap: 45px; }
  .story-portrait { max-width: 480px; width: 100%; margin: auto; }
  .story-copy h2 { font-size: 33px; }
  .works-head { margin-top: 55px; }
  .work-card .art-image { height: 240px; }
  .story-bottom { padding: 20px; }
  .collaboration-grid { grid-template-columns: 1fr; gap: 40px; }
}
@media (max-width: 480px) {
  .hero-actions { flex-direction: column; }
  .hero-stats { gap: 15px; }
  .hero-stats strong { font-size: 20px; }
  .hero-art { height: 465px; transform: scale(.92); transform-origin: center top; margin-bottom: -35px; }
  .directory-grid { grid-template-columns: 1fr 1fr; gap: 12px 9px; }
  .artist-photo { height: 215px; }
  .artist-info { padding: 13px 10px; }
  .artist-info > div:first-child { display: block; }
  .artist-info > div:first-child > span { display: block; margin-top: 4px; }
  .artist-card-foot span:last-child { display: none; }
  .story-portrait { padding-left: 15px; }
  .story-image { height: 390px; }
  .works-grid { grid-template-columns: 1fr; gap: 28px; }
  .work-card .art-image { height: 390px; }
  .works-head > span { display: none; }
  .story-bottom { display: block; }
  .story-bottom .btn { margin-top: 18px; width: 100%; }
  .collaboration-section h2 { font-size: 27px; }
}
</style>
