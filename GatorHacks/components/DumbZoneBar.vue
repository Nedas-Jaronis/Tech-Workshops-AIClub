<script setup lang="ts">
import { ref, onMounted } from 'vue'

const filled = ref(false)
onMounted(() => setTimeout(() => (filled.value = true), 400))
</script>

<template>
  <div class="zone-wrap">
    <div class="zone-bar">
      <div class="zone-fill" :class="{ go: filled }" />
      <div class="zone-marker" style="left: 40%" />
      <div class="zone-marker" style="left: 70%" />
    </div>
    <div class="row">
      <span class="g" style="left: 20%">Smart zone</span>
      <span class="y" style="left: 55%">Slipping</span>
      <span class="r" style="left: 85%">Dumb zone</span>
    </div>
    <div class="row ticks">
      <span style="left: 0%">0%</span>
      <span style="left: 40%">40%</span>
      <span style="left: 70%">70%</span>
      <span style="left: 100%">100%</span>
    </div>
  </div>
</template>

<style scoped>
.zone-wrap { width: 100%; max-width: 760px; margin: 0 auto; }
.zone-bar {
  position: relative;
  height: 44px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.08);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.zone-fill {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #30d158 0%, #30d158 38%, #ffd60a 55%, #ff453a 80%);
  transition: width 6s linear;
}
.zone-fill.go { width: 100%; }
.zone-marker { position: absolute; top: 0; bottom: 0; border-left: 2px dashed rgba(255, 255, 255, 0.85); }
.row { position: relative; height: 1.6rem; margin-top: 10px; }
.row span { position: absolute; transform: translateX(-50%); white-space: nowrap; font-size: 1rem; font-weight: 600; }
.row .g { color: #30d158; }
.row .y { color: #ffd60a; }
.row .r { color: #ff453a; }
.row.ticks { margin-top: 0; }
.row.ticks span { color: #86868b; font-size: 0.85rem; font-weight: 500; }
.row.ticks span:first-child { transform: none; }
.row.ticks span:last-child { transform: translateX(-100%); }
</style>
