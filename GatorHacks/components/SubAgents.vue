<script setup lang="ts">
const subs = [
  { name: 'Sub-agent A', read: 'reads the auth code' },
  { name: 'Sub-agent B', read: 'reads the database code' },
  { name: 'Sub-agent C', read: 'reads the tests' },
]
</script>

<template>
  <div class="sa">
    <div class="main">
      <b>Main agent</b>
      <span>clean window</span>
    </div>

    <div class="subs">
      <div v-for="s in subs" :key="s.name" class="col">
        <div class="link">
          <span class="down">task</span>
          <i />
          <span class="up">summary</span>
        </div>
        <div class="sub">
          <b>{{ s.name }}</b>
          <span>{{ s.read }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sa { display: flex; flex-direction: column; align-items: center; margin-top: 0.6rem; }
.main, .sub {
  border-radius: 18px; padding: 0.9rem 1.6rem; text-align: center;
  display: flex; flex-direction: column; gap: 0.15rem;
  background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.16);
}
.main { border-color: #30d158; background: rgba(48, 209, 88, 0.1); min-width: 280px; }
.main b, .sub b { font-size: 1.15rem; }
.main span, .sub span { font-size: 0.9rem; color: #86868b; }
.subs { display: flex; gap: 1.2rem; }
.col { display: flex; flex-direction: column; align-items: center; }
.link { display: flex; align-items: center; gap: 0.6rem; height: 56px; font-size: 0.8rem; }
.link i { width: 2px; height: 100%; background: rgba(255, 255, 255, 0.3); }
.link .down { color: #86868b; }
.link .down::after { content: ' ↓'; }
.link .up { color: #30d158; }
.link .up::before { content: '↑ '; }
.sub { min-width: 210px; border-style: dashed; border-color: rgba(255, 255, 255, 0.35); }
</style>
