<script setup lang="ts">
import { computed } from 'vue'

// step comes from the slide's click count: 0 is the first state
const props = withDefaults(defineProps<{ step?: number }>(), { step: 0 })

const W = 880
const H = 300
const padL = 52
const padR = 24
const padT = 30
const padB = 54

interface Pt { pct: number; label: string; title: string; text: string; kind: 'grow' | 'drop' }

const pts: Pt[] = [
  { pct: 6, label: 'New session', title: 'A new session starts', text: 'Only the system prompt and your config files are loaded. The window is almost empty.', kind: 'grow' },
  { pct: 22, label: 'Read files', title: 'Reading files fills the window', text: 'Every file the agent opens is copied into its context. It stays there until the session ends.', kind: 'grow' },
  { pct: 46, label: 'Tool output', title: 'Tool output piles up', text: 'Test logs, search results and shell output all add to the window. Quality starts to slip past 40%.', kind: 'grow' },
  { pct: 14, label: '/compact', title: '/compact summarizes the history', text: 'The agent replaces the long history with a short summary. Space comes back, but details are lost.', kind: 'drop' },
  { pct: 32, label: 'Keep working', title: 'Work continues on the summary', text: 'The window grows again. Anything the summary left out is gone, so the agent can repeat old mistakes.', kind: 'grow' },
  { pct: 5, label: '/clear + handoff', title: '/clear starts fresh from a file', text: 'You write a plan or handoff file, clear the window, and the next session reads only that file. This is the cleanest reset.', kind: 'drop' },
]

const x = (i: number) => padL + (i * (W - padL - padR)) / (pts.length - 1)
const y = (p: number) => padT + (1 - p / 100) * (H - padT - padB)

const cur = computed(() => Math.min(Math.max(props.step, 0), pts.length - 1))
const zones = [
  { from: 0, to: 40, color: '#30d158' },
  { from: 40, to: 70, color: '#ffd60a' },
  { from: 70, to: 100, color: '#ff453a' },
]
const pctColor = (p: number) => (p < 40 ? '#30d158' : p < 70 ? '#ffd60a' : '#ff453a')

const segs = computed(() =>
  pts.slice(1).map((p, i) => ({
    d: `M${x(i)} ${y(pts[i].pct)} L${x(i + 1)} ${y(p.pct)}`,
    show: i + 1 <= cur.value,
    drop: p.kind === 'drop',
  })),
)
</script>

<template>
  <div class="ct">
    <svg :viewBox="`0 0 ${W} ${H}`" class="chart">
      <!-- zone bands -->
      <rect
        v-for="z in zones"
        :key="z.from"
        :x="padL"
        :y="y(z.to)"
        :width="W - padL - padR"
        :height="y(z.from) - y(z.to)"
        :fill="z.color"
        opacity="0.07"
      />
      <line v-for="v in [40, 70]" :key="v" :x1="padL" :x2="W - padR" :y1="y(v)" :y2="y(v)" class="thr" />
      <text :x="padL - 10" :y="y(40) + 4" text-anchor="end" class="axis">40%</text>
      <text :x="padL - 10" :y="y(70) + 4" text-anchor="end" class="axis">70%</text>
      <text :x="padL - 10" :y="y(0) + 4" text-anchor="end" class="axis">0%</text>
      <text :x="padL - 10" :y="y(100) + 4" text-anchor="end" class="axis">100%</text>
      <text :x="padL" y="12" class="axis">How full the context window is</text>

      <text :x="W - padR - 8" :y="y(20) + 4" text-anchor="end" class="zl" fill="#30d158">Smart zone</text>
      <text :x="W - padR - 8" :y="y(55) + 4" text-anchor="end" class="zl" fill="#ffd60a">Slipping</text>
      <text :x="W - padR - 8" :y="y(85) + 4" text-anchor="end" class="zl" fill="#ff453a">Dumb zone</text>

      <!-- line segments -->
      <path v-for="(s, i) in segs" :key="i" :d="s.d" class="seg" :class="{ drop: s.drop, show: s.show }" />

      <!-- points -->
      <g v-for="(p, i) in pts" :key="i" class="pt" :class="{ show: i <= cur, now: i === cur }">
        <circle v-if="i === cur" :cx="x(i)" :cy="y(p.pct)" r="14" class="halo" :fill="pctColor(p.pct)" />
        <circle :cx="x(i)" :cy="y(p.pct)" r="6" :fill="pctColor(p.pct)" />
        <text :x="i === pts.length - 1 ? x(i) + 18 : x(i)" :y="H - 28" :text-anchor="i === pts.length - 1 ? 'end' : 'middle'" class="plabel" :class="{ cmd: p.kind === 'drop' }">{{ p.label }}</text>
      </g>
    </svg>

    <div class="caption">
      <div class="title">{{ pts[cur].title }}</div>
      <div class="text">{{ pts[cur].text }}</div>
    </div>
  </div>
</template>

<style scoped>
.ct { width: 100%; }
.chart { width: 100%; height: auto; }
.zl { font-size: 13px; font-weight: 600; opacity: 0.7; }
.thr { stroke: rgba(255, 255, 255, 0.18); stroke-dasharray: 4 5; }
.axis { font-size: 13px; fill: #86868b; }
.seg { fill: none; stroke: #0a84ff; stroke-width: 3; stroke-linecap: round; opacity: 0; transition: opacity 0.5s ease; }
.seg.drop { stroke: #30d158; stroke-dasharray: 2 7; }
.seg.show { opacity: 1; }
.pt { opacity: 0; transition: opacity 0.5s ease; }
.pt.show { opacity: 1; }
.plabel { font-size: 14px; fill: #86868b; font-weight: 500; }
.pt.now .plabel { fill: #f5f5f7; font-weight: 600; }
.plabel.cmd { font-family: 'JetBrains Mono', monospace; }
.halo { opacity: 0.25; animation: pulse 1.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
@keyframes pulse { 0%, 100% { transform: scale(0.8); opacity: 0.3; } 50% { transform: scale(1.25); opacity: 0.08; } }
.caption {
  margin-top: 0.4rem; padding: 0.9rem 1.3rem; border-radius: 16px;
  background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12);
}
.title { font-weight: 600; font-size: 1.1rem; letter-spacing: -0.02em; }
.text { color: #a1a1a6; font-size: 0.95rem; margin-top: 0.15rem; line-height: 1.4; }
</style>
