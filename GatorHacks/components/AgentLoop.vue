<script setup lang="ts">
import { computed } from 'vue'

// focus picks which part of the loop is lit up; everything else dims
const props = withDefaults(defineProps<{ focus?: string }>(), { focus: 'all' })

const sets: Record<string, string[]> = {
  all: ['spec', 'prompt', 'review', 'pr', 'config', 'llm', 'env', 'guard'],
  spec: ['spec', 'prompt'],
  config: ['prompt', 'config', 'llm'],
  agent: ['config', 'llm', 'env', 'guard'],
  guardrails: ['env', 'guard', 'llm'],
  review: ['guard', 'review', 'prompt', 'pr'],
}
const active = computed(() => new Set(sets[props.focus] ?? sets.all))
const on = (...ids: string[]) => ids.every((i) => active.value.has(i))
const dim = (...ids: string[]) => ({ opacity: on(...ids) ? 1 : 0.2 })

// nodes you control get a green outline
const you = new Set(['spec', 'prompt', 'review', 'config', 'guard'])
</script>

<template>
  <svg viewBox="0 0 980 420" class="loop" role="img" aria-label="The developer loop and the agentic AI loop">
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" fill="#8e8e93" />
      </marker>
      <marker id="arrg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z" fill="#30d158" />
      </marker>
    </defs>

    <!-- regions -->
    <rect x="10" y="10" width="400" height="400" rx="32" class="region" />
    <text x="36" y="46" class="region-label">DEVELOPER LOOP</text>
    <text x="36" y="66" class="region-sub">you</text>

    <ellipse cx="720" cy="210" rx="250" ry="190" class="region dashed" />
    <text x="720" y="52" text-anchor="middle" class="region-label">AGENTIC AI LOOP</text>
    <text x="720" y="72" text-anchor="middle" class="region-sub">the agent</text>

    <!-- edges -->
    <g class="edges">
      <path d="M170 112 L238 112" marker-end="url(#arr)" :style="dim('spec', 'prompt')" />
      <path d="M390 130 C 470 130, 470 322, 560 322" class="go" marker-end="url(#arrg)" :style="dim('prompt', 'config')" />
      <text x="476" y="196" class="elabel" :style="dim('prompt', 'config')">hand off</text>

      <path d="M620 296 L620 164" marker-end="url(#arr)" :style="dim('config', 'llm')" />
      <text x="632" y="236" class="elabel" :style="dim('config', 'llm')">load</text>
      <path d="M690 142 L770 142" marker-end="url(#arr)" :style="dim('llm', 'env')" />
      <text x="730" y="132" text-anchor="middle" class="elabel" :style="dim('llm', 'env')">use</text>
      <path d="M840 164 L840 296" marker-end="url(#arr)" :style="dim('env', 'guard')" />
      <text x="852" y="236" class="elabel" :style="dim('env', 'guard')">enforce</text>
      <path d="M790 296 L700 166" marker-end="url(#arr)" :style="dim('guard', 'llm')" />
      <text x="722" y="244" class="elabel" :style="dim('guard', 'llm')">check</text>

      <path d="M560 372 C 490 372, 450 322, 396 322" class="dash" marker-end="url(#arr)" :style="dim('guard', 'review')" />
      <text x="470" y="398" class="elabel" :style="dim('guard', 'review')">AI outputs</text>

      <path d="M300 290 L300 154" marker-end="url(#arr)" :style="dim('review', 'prompt')" />
      <text x="312" y="230" class="elabel" :style="dim('review', 'prompt')">course correct</text>
      <path d="M238 322 C 190 322, 160 340, 130 352" marker-end="url(#arr)" :style="dim('review', 'pr')" />
    </g>

    <!-- nodes -->
    <g class="node" :class="{ you: you.has('spec') }" :style="dim('spec')">
      <rect x="50" y="90" width="120" height="46" rx="23" />
      <text x="110" y="118" text-anchor="middle">Feature spec</text>
    </g>
    <g class="node" :class="{ you: you.has('prompt') }" :style="dim('prompt')">
      <rect x="238" y="90" width="152" height="46" rx="14" />
      <text x="314" y="118" text-anchor="middle">Prompt</text>
    </g>
    <g class="node" :class="{ you: you.has('review') }" :style="dim('review')">
      <rect x="238" y="298" width="152" height="46" rx="14" />
      <text x="314" y="326" text-anchor="middle">Review</text>
    </g>
    <g class="node pr" :style="dim('pr')">
      <rect x="50" y="340" width="80" height="46" rx="23" />
      <text x="90" y="368" text-anchor="middle">PR</text>
    </g>

    <g class="node" :class="{ you: you.has('config') }" :style="dim('config')">
      <rect x="560" y="298" width="170" height="46" rx="14" />
      <text x="645" y="326" text-anchor="middle">Config</text>
    </g>
    <g class="node" :style="dim('llm')">
      <rect x="560" y="96" width="130" height="46" rx="14" />
      <text x="625" y="124" text-anchor="middle">LLM</text>
    </g>
    <g class="node" :style="dim('env')">
      <rect x="770" y="96" width="140" height="46" rx="14" />
      <text x="840" y="124" text-anchor="middle">Environment</text>
    </g>
    <g class="node" :class="{ you: you.has('guard') }" :style="dim('guard')">
      <rect x="770" y="298" width="140" height="46" rx="14" />
      <text x="840" y="326" text-anchor="middle">Guardrails</text>
    </g>
  </svg>
</template>

<style scoped>
.loop { width: 100%; height: auto; font-family: inherit; }
.loop * { transition: opacity 0.4s ease; }
.region { fill: rgba(255, 255, 255, 0.025); stroke: rgba(255, 255, 255, 0.14); stroke-width: 1.2; }
.region.dashed { stroke-dasharray: 7 6; stroke: rgba(255, 255, 255, 0.28); }
.region-label { font-size: 12px; font-weight: 600; letter-spacing: 0.16em; fill: #f5f5f7; }
.region-sub { font-size: 12px; fill: #86868b; }

.edges path { fill: none; stroke: #8e8e93; stroke-width: 1.6; }
.edges path.go { stroke: #30d158; }
.edges path.dash { stroke-dasharray: 5 5; }
.elabel { font-size: 14px; fill: #a1a1a6; paint-order: stroke; stroke: #000; stroke-width: 6px; stroke-linejoin: round; }

.node rect { fill: rgba(255, 255, 255, 0.07); stroke: rgba(255, 255, 255, 0.2); stroke-width: 1.2; }
.node text { font-size: 15px; font-weight: 600; fill: #f5f5f7; letter-spacing: -0.01em; }
.node.you rect { stroke: #30d158; fill: rgba(48, 209, 88, 0.1); }
.node.pr rect { fill: #f5f5f7; stroke: none; }
.node.pr text { fill: #000; }
</style>
