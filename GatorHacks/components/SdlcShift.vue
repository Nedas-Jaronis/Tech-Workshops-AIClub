<template>
  <div class="sdlc">
    <div class="row">
      <div class="tag">Before</div>
      <div class="chips">
        <span class="chip you">Plan</span><i />
        <span class="chip you">Build</span><i />
        <span class="chip you">Test</span><i />
        <span class="chip you">Review</span><i />
        <span class="chip you">Ship</span>
      </div>
      <div class="note">You did every step.</div>
    </div>

    <div v-click class="row">
      <div class="tag now">Now</div>
      <div class="chips">
        <span class="chip you">Plan</span><i />
        <span class="chip agent wide">Build + Test<small>the agent loop</small></span><i />
        <span class="chip you">Review</span><i />
        <span class="chip you">Ship</span>
      </div>
      <div class="note">The agent does the middle.</div>
    </div>
  </div>
</template>

<style scoped>
.sdlc { display: flex; flex-direction: column; gap: 2.2rem; margin-top: 1.2rem; }
.row { display: grid; grid-template-columns: 90px 1fr; grid-template-rows: auto auto; column-gap: 1.2rem; row-gap: 0.6rem; align-items: center; }
.tag { font-size: 0.8rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #86868b; }
.tag.now { color: #30d158; }
.chips { display: flex; align-items: center; gap: 0.5rem; }
.chips i { flex: 0 0 22px; height: 2px; background: rgba(255, 255, 255, 0.25); border-radius: 2px; }
.chip {
  padding: 0.7rem 1.3rem; border-radius: 999px; font-weight: 600; font-size: 1.05rem;
  background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.16);
  white-space: nowrap;
}
.chip.you { border-color: rgba(48, 209, 88, 0.7); background: rgba(48, 209, 88, 0.1); }
.chip.agent { border-color: rgba(10, 132, 255, 0.85); background: rgba(10, 132, 255, 0.14); }
.chip.wide { padding: 0.7rem 2.6rem; display: flex; flex-direction: column; align-items: center; line-height: 1.2; border-radius: 22px; }
.chip small { font-size: 0.72rem; font-weight: 500; color: #64d2ff; letter-spacing: 0.04em; }
.note { grid-column: 2; color: #86868b; font-size: 0.95rem; }
</style>
