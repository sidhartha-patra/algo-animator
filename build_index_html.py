import os

HTML_CONTENT = r'''<!doctype html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AlgoAnimator — Algorithm Visualization & Invariant Verification Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg-app: #09090b;
  --bg-surface: #121216;
  --bg-surface-elevated: #18181f;
  --bg-surface-active: #20202a;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-focus: rgba(255, 255, 255, 0.22);
  --border-highlight: rgba(245, 158, 11, 0.35);

  --text-primary: #f4f4f6;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;

  --accent-amber: #f59e0b;
  --accent-amber-glow: rgba(245, 158, 11, 0.15);
  --accent-cyan: #06b6d4;
  --accent-cyan-glow: rgba(6, 182, 212, 0.15);
  --accent-emerald: #10b981;
  --accent-emerald-glow: rgba(16, 185, 129, 0.15);
  --accent-rose: #f43f5e;
  --accent-purple: #a855f7;

  --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;

  --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.5), 0 0 0 1px var(--border-subtle);
  --shadow-active: 0 8px 30px -4px rgba(0, 0, 0, 0.7), 0 0 0 1px var(--border-focus);
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg-app);
  color: var(--text-primary);
  font-family: var(--font-sans);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  padding: 16px;
  min-height: 100vh;
}

#app {
  max-width: 1380px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Command Bar / Navigation */
.nav-header {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  box-shadow: var(--shadow-card);
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 12px;
}
.brand-mark {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #f59e0b, #d97706);
  display: grid;
  place-items: center;
  font-weight: 900;
  color: #000;
  font-size: 20px;
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.3);
}
.brand-title {
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
}
.version-pill {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.action-btn {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  transition: all 0.15s ease;
  font-family: var(--font-sans);
  text-decoration: none;
}
.action-btn:hover {
  background: var(--bg-surface-active);
  border-color: var(--border-focus);
  transform: translateY(-1px);
}
.action-btn.primary {
  background: #f59e0b;
  color: #09090b;
  border-color: #f59e0b;
  font-weight: 700;
}
.action-btn.primary:hover {
  background: #fbbf24;
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.4);
}

.tunnel-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
}
.tunnel-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--text-muted);
}
.tunnel-dot.active {
  background: var(--accent-emerald);
  box-shadow: 0 0 8px var(--accent-emerald);
}

/* Algorithm Presets Ribbon */
.ribbon-bar {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: var(--shadow-card);
}
.ribbon-title {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
}
.presets-list {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 2px;
}
.preset-chip {
  padding: 6px 13px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}
.preset-chip:hover {
  background: var(--bg-surface-active);
  color: #fff;
  border-color: var(--border-focus);
}
.preset-chip.active {
  background: rgba(245, 158, 11, 0.12);
  color: #fbbf24;
  border-color: rgba(245, 158, 11, 0.4);
  font-weight: 700;
}

/* Overview Header Card */
.overview-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}
.overview-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.4), transparent);
}
.overview-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 12px;
}
.algo-heading {
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.6px;
  margin: 0 0 4px 0;
  color: #ffffff;
}
.algo-meta {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
}
.metric-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.pill {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface-elevated);
}
.pill.time { background: var(--accent-emerald-glow); color: #34d399; border-color: rgba(52, 211, 153, 0.25); font-family: var(--font-mono); }
.pill.space { background: var(--accent-cyan-glow); color: #38bdf8; border-color: rgba(56, 189, 248, 0.25); font-family: var(--font-mono); }
.pill.paradigm { background: var(--accent-amber-glow); color: #fbbf24; border-color: rgba(245, 158, 11, 0.25); }

.intuition-box {
  margin-top: 14px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.6;
}
.intuition-box strong { color: #fbbf24; }

/* Stage Split Grid */
.stage-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}
@media (min-width: 1040px) {
  .stage-grid.with-code {
    grid-template-columns: 1fr 440px;
  }
}

.studio-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Comic Editorial Conversation */
#dialogue-stage {
  min-height: 110px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 10px;
}
.speech-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  animation: fadeIn 0.2s ease-out;
}
.speech-row.algo { align-self: flex-start; }
.speech-row.bug { align-self: flex-end; flex-direction: row-reverse; }
.speech-row.data { align-self: center; }

.char-badge {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: grid;
  place-items: center;
  font-size: 20px;
  flex-shrink: 0;
  border: 1px solid var(--border-subtle);
}
.char-badge.algo { background: #78350f; color: #fbbf24; border-color: #f59e0b; }
.char-badge.bug { background: #164e63; color: #22d3ee; border-color: #06b6d4; }
.char-badge.data { background: #064e3b; color: #34d399; border-color: #10b981; }

.speech-bubble {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  max-width: 520px;
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.5;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.speech-bubble b {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 2px;
}
.speech-row.algo .speech-bubble b { color: #fbbf24; }
.speech-row.bug .speech-bubble b { color: #22d3ee; }
.speech-row.data .speech-bubble b { color: #34d399; }

/* Visual Data Canvas */
#visual-canvas {
  background: #0d0d11;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  min-height: 230px;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 18px;
  overflow-x: auto;
  position: relative;
}

/* Bar Chart Canvas for Elevation / Rain */
.chart-container {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 8px;
  height: 110px;
  width: 100%;
}
.bar-col {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  width: 50px;
}
.water-block {
  width: 100%;
  background: rgba(14, 165, 233, 0.65);
  border: 1px dashed #38bdf8;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
  color: #e0f2fe;
}
.height-bar {
  width: 100%;
  background: #3f3f46;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 4px 4px 0 0;
  transition: all 0.25s ease;
}
.height-bar.active { background: #f59e0b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }

/* Array Structure Cells */
.array-strip {
  display: flex;
  justify-content: center;
  gap: 8px;
  position: relative;
  padding: 22px 0 32px 0;
}
.cell-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.cell-idx {
  position: absolute;
  top: -20px;
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
}
.array-cell {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  display: grid;
  place-items: center;
  font-size: 18px;
  font-family: var(--font-mono);
  font-weight: 700;
  color: #fff;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}
.array-cell.hot {
  background: rgba(245, 158, 11, 0.2);
  border-color: #f59e0b;
  color: #fbbf24;
  transform: translateY(-4px);
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.35);
}
.array-cell.left-active {
  border-color: var(--accent-rose);
  background: rgba(244, 63, 94, 0.15);
}
.array-cell.right-active {
  border-color: var(--accent-cyan);
  background: rgba(6, 182, 212, 0.15);
}
.array-cell.mid-active {
  border-color: var(--accent-purple);
  background: rgba(168, 85, 247, 0.2);
  box-shadow: 0 0 16px rgba(168, 85, 247, 0.35);
}
.array-cell.eliminated {
  opacity: 0.35;
  background: #18181b;
}

.pointer-chip {
  position: absolute;
  bottom: -28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 11px;
  font-family: var(--font-mono);
  font-weight: 800;
  letter-spacing: 0.5px;
  white-space: nowrap;
}
.pointer-chip.left { color: var(--accent-rose); }
.pointer-chip.right { color: var(--accent-cyan); }
.pointer-chip.mid { color: var(--accent-purple); }
.pointer-chip.general { color: var(--accent-amber); }

/* Variables Row */
.variables-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}
.var-card {
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.var-card.highlight {
  background: var(--accent-emerald-glow);
  border-color: rgba(16, 185, 129, 0.4);
  color: #34d399;
}

/* Scene Narration */
.narration-panel {
  padding: 14px 18px;
  border-radius: var(--radius-md);
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
}
.narration-title {
  font-size: 15px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.narration-body {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* The Killer Feature: "Why is this safe?" Inspector */
#why-inspector {
  border-radius: var(--radius-md);
  background: #151408;
  border: 1px solid rgba(245, 158, 11, 0.3);
  padding: 16px;
  display: none;
  animation: fadeIn 0.2s ease-out;
}
#why-inspector.active { display: block; }

.why-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.why-title {
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: #fbbf24;
  display: flex;
  align-items: center;
  gap: 6px;
}

.why-cards-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}
@media (min-width: 600px) {
  .why-cards-grid { grid-template-columns: 1fr 1fr; }
}

.why-cell {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  font-size: 13.5px;
}
.why-cell label {
  display: block;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  color: #d97706;
  margin-bottom: 3px;
  letter-spacing: 0.5px;
}

.why-debate-box {
  grid-column: 1 / -1;
  background: rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(245, 158, 11, 0.25);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  font-size: 13.5px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.why-debate-q { color: #38bdf8; font-weight: 600; }
.why-debate-a { color: #34d399; font-weight: 600; }

/* Side Code Panel */
#code-studio {
  background: #09090c;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-card);
  max-height: 640px;
}
.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 10px;
}
.code-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 8px;
}
.code-lines-scroll {
  overflow-y: auto;
  font-family: var(--font-mono);
  font-size: 12.5px;
  line-height: 1.6;
}
.code-row {
  display: flex;
  gap: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  white-space: pre;
  color: #d4d4d8;
}
.code-num {
  width: 24px;
  text-align: right;
  color: #52525b;
  user-select: none;
  font-size: 11.5px;
}
.code-row.active {
  background: rgba(245, 158, 11, 0.15);
  border-left: 2px solid #f59e0b;
  color: #fff;
  font-weight: 600;
}
.code-row.active .code-num { color: #f59e0b; }

/* Playback Control Bar */
.control-bar {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 14px 20px;
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.btn-media {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  color: #fff;
  border-radius: var(--radius-sm);
  padding: 7px 14px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
}
.btn-media:hover {
  background: var(--bg-surface-active);
  border-color: var(--border-focus);
}
.btn-media.play {
  background: #f59e0b;
  color: #09090b;
  border-color: #f59e0b;
  font-weight: 800;
}
.btn-media.play:hover { background: #fbbf24; }

input[type=range] {
  flex: 1;
  min-width: 140px;
  accent-color: #f59e0b;
  cursor: pointer;
}

.step-label {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-secondary);
  min-width: 55px;
}

.select-dropdown {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  border-radius: var(--radius-sm);
  padding: 7px 12px;
  font-size: 13px;
  font-weight: 600;
  font-family: var(--font-sans);
  cursor: pointer;
}

/* Modals */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  display: none;
  place-items: center;
  z-index: 9999;
  padding: 16px;
}
.modal-backdrop.open { display: grid; }

.modal-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-focus);
  border-radius: var(--radius-xl);
  padding: 24px;
  max-width: 680px;
  width: 100%;
  box-shadow: 0 20px 50px rgba(0,0,0,0.8);
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.modal-title {
  font-size: 20px;
  font-weight: 800;
  color: #fff;
  margin: 0;
}
.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.form-field label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-secondary);
}
.form-input {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  font-size: 13.5px;
  color: #fff;
  font-family: var(--font-mono);
}
.form-input:focus {
  outline: none;
  border-color: #f59e0b;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 6px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
</head>
<body>
<div id="app">
  <!-- Nav Bar -->
  <header class="nav-header">
    <div class="brand-group">
      <div class="brand-mark">🎬</div>
      <div>
        <div class="brand-title">AlgoAnimator <span class="version-pill">v2.0 Linear Edition</span></div>
      </div>
    </div>
    <div class="nav-actions">
      <div class="tunnel-indicator" id="tunnel-badge">
        <span class="tunnel-dot" id="tunnel-dot"></span>
        <span id="tunnel-status-text">Static Engine</span>
      </div>
      <button class="action-btn" onclick="openTunnelModal()">🔌 Dev Tunnel</button>
      <button class="action-btn primary" onclick="openUploadModal()">📁 Upload / Paste C#</button>
      <a href="https://github.com/sidhartha-patra/algo-animator" target="_blank" class="action-btn">⭐ GitHub</a>
    </div>
  </header>

  <!-- Algorithm Paradigms & Test Suites -->
  <div class="ribbon-bar">
    <div class="ribbon-title">Interactive Algorithm Paradigms & Corner Cases</div>
    <div class="presets-list" id="presets-ribbon">
      <button class="preset-chip active" onclick="switchParadigm('trapping')">💧 Trapping Rain Water (2-Pointer)</button>
      <button class="preset-chip" onclick="switchParadigm('binary_search')">🔍 Binary Search (O(log N))</button>
      <button class="preset-chip" onclick="switchParadigm('two_sum')">⚡ Two Sum (Hash Map)</button>
      <button class="preset-chip" onclick="switchParadigm('kadane')">📈 Max Subarray (Kadane / Sliding Window)</button>
    </div>
  </div>

  <!-- Header Card -->
  <div class="overview-card">
    <div class="overview-top">
      <div>
        <h1 class="algo-heading" id="algo-title">Trapping Rain Water</h1>
        <div class="algo-meta" id="algo-sub">Two Pointers — Elevation Basin Invariant</div>
      </div>
      <div class="metric-pills">
        <span class="pill time" id="pill-time">Time: O(N)</span>
        <span class="pill space" id="pill-space">Space: O(1)</span>
        <span class="pill paradigm" id="pill-paradigm">Two Pointers</span>
      </div>
    </div>
    <div class="intuition-box" id="intuition-card">
      <b>💡 Core Invariant:</b> <span id="intuition-text"></span>
    </div>
  </div>

  <!-- Main Split Studio Stage -->
  <div class="stage-grid with-code" id="stage-grid">
    <div class="studio-panel">
      <!-- Comic Dialogue -->
      <div id="dialogue-stage"></div>

      <!-- Visual Canvas -->
      <div id="visual-canvas"></div>

      <!-- Narration -->
      <div class="narration-panel">
        <div class="narration-title" id="narration-title">Scene</div>
        <div class="narration-body" id="narration-text">Explanation</div>
      </div>

      <!-- "Why is this safe?" Inspector -->
      <div id="why-inspector">
        <div class="why-top">
          <div class="why-title">🛡️ Formal Invariant Guarantee ("Why is this safe?")</div>
          <span style="font-size:11px; color:var(--text-muted);">Press <kbd style="background:rgba(255,255,255,0.1); padding:2px 5px; border-radius:3px;">W</kbd> to toggle</span>
        </div>
        <div class="why-cards-grid">
          <div class="why-cell">
            <label>1. Decision Rule</label>
            <span id="why-decision"></span>
          </div>
          <div class="why-cell">
            <label>2. Limiting Bottleneck</label>
            <span id="why-limiting"></span>
          </div>
          <div class="why-cell" style="grid-column: 1 / -1;">
            <label>3. Invariant Proof</label>
            <span id="why-invariant"></span>
          </div>
          <div class="why-debate-box">
            <div class="why-debate-q" id="why-q">🤔 Bug: "Couldn't an unseen element change this?"</div>
            <div class="why-debate-a" id="why-a">🧑 Algo: "No. The bounding invariant guarantees safety."</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Studio Panel -->
    <div id="code-studio">
      <div class="code-header">
        <div class="code-title">
          <span>Source Code</span>
          <span class="version-pill" id="code-lang-pill">C#</span>
        </div>
        <span class="version-pill" id="active-line-pill">Line: -</span>
      </div>
      <div class="code-lines-scroll" id="code-lines"></div>
    </div>
  </div>

  <!-- Playback Control Bar -->
  <div class="control-bar">
    <button class="btn-media" onclick="first()" title="Home">⏮</button>
    <button class="btn-media" onclick="prev()" title="Left Arrow">◀</button>
    <button class="btn-media play" onclick="togglePlay()" id="play-btn">▶ Play</button>
    <button class="btn-media" onclick="next()" title="Right Arrow">▶</button>
    <button class="btn-media" onclick="last()" title="End">⏭</button>

    <input type="range" id="timeline-slider" min="0" max="0" value="0" oninput="goToScene(+this.value)">
    <span class="step-label" id="step-counter">1/1</span>

    <select class="select-dropdown" id="scene-select" onchange="goToScene(+this.value)"></select>

    <button class="action-btn" onclick="toggleWhyMode()">💡 Why Mode</button>
  </div>
</div>

<!-- Upload / Custom C# Code Modal -->
<div class="modal-backdrop" id="upload-modal">
  <div class="modal-box">
    <h2 class="modal-title">📁 Upload Custom C# Solution</h2>
    <p style="font-size:13px; color:var(--text-secondary); margin:0;">
      Upload any C# algorithm file or paste code directly. You can provide a custom test case, or <b>leave the test case empty</b> to let AlgoAnimator auto-detect the algorithm and synthesize a complete corner-case test suite!
    </p>

    <div class="form-field">
      <label>Upload .cs File</label>
      <input type="file" id="code-file-input" accept=".cs,.txt,.py,.java,.cpp" class="form-input" onchange="handleFileUpload(event)">
    </div>

    <div class="form-field">
      <label>Algorithm Name</label>
      <input type="text" class="form-input" id="custom-algo-title" value="Binary Search">
    </div>

    <div class="form-field">
      <label>C# Source Code</label>
      <textarea id="custom-code-area" class="form-input" style="height:150px; font-size:12px; resize:vertical;">public int BinarySearch(int[] nums, int target)
{
    int left = 0, right = nums.Length - 1;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}</textarea>
    </div>

    <div class="form-field">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <label>Test Case Array & Target <span style="color:#10b981; font-weight:700;">(Optional)</span></label>
        <span style="font-size:11px; color:var(--text-muted);">Leave empty to auto-synthesize all corner cases</span>
      </div>
      <input type="text" class="form-input" id="custom-input-data" placeholder="Leave empty to auto-detect and synthesize edge cases (e.g. [-1, 0, 3, 5, 9, 12], target=9)">
    </div>

    <div class="modal-footer">
      <button class="action-btn" onclick="closeUploadModal()">Cancel</button>
      <button class="action-btn primary" onclick="runCustomCode()">Simulate & Animate</button>
    </div>
  </div>
</div>

<!-- Dev Tunnel Modal -->
<div class="modal-backdrop" id="tunnel-modal">
  <div class="modal-box">
    <h2 class="modal-title">🔌 Connect to Microsoft Dev Tunnel</h2>
    <p style="font-size:13px; color:var(--text-secondary); margin:0;">
      Connect to your local AlgoAnimator backend service (running with Copilot CLI or Gemini) via Microsoft Dev Tunnels.
    </p>
    <div class="form-field">
      <label>Tunnel Endpoint URL</label>
      <input type="text" class="form-input" id="tunnel-url-input" placeholder="https://<tunnel-id>.devtunnels.ms (or http://localhost:8000)">
    </div>
    <div class="modal-footer">
      <button class="action-btn" onclick="closeTunnelModal()">Cancel</button>
      <button class="action-btn primary" onclick="saveTunnelUrl()">Connect</button>
    </div>
  </div>
</div>

<script>
let currentSpec = null;
let currentIndex = 0;
let playTimer = null;
let devTunnelUrl = localStorage.getItem("algo_animator_tunnel") || "";

const $ = id => document.getElementById(id);

// --------------------------------------------------------------------------
// Multi-Paradigm Client-Side Invariant Simulators
// --------------------------------------------------------------------------


function buildTrappingRainWaterSpec(nums, sourceCode) {
  const n = nums.length;
  const rawStr = nums.join(",");
  const scenes = [];

  scenes.push({
    id: "trap_init",
    type: "title",
    title: "Trapping Rain Water — Two Pointers",
    narration: `Simulating elevation map [${rawStr}]. Computing trapped water units in O(N) time and O(1) space.`,
    dialogue: [
      { character_id: "algo", text: "Two climbers start from opposite ends and move toward each other. The shorter wall determines water height." },
      { character_id: "bug", text: "Why don't we need to know the entire opposing profile?" }
    ],
    states: [
      { kind: "array", name: "height", value: rawStr },
      { kind: "variable", name: "totalWater", value: "0" }
    ],
    code_line: 1
  });

  if (n < 3) {
    scenes.push({
      id: "trap_edge",
      type: "result",
      title: `Edge Case: Length ${n} < 3`,
      narration: `Array length ${n} < 3 cannot form a basin between walls. Returns 0.`,
      dialogue: [
        { character_id: "algo", text: "Zero water trapped. A container requires at least 2 boundaries and an interior dip." },
        { character_id: "bug", text: "Corner case boundary holds." }
      ],
      states: [{ kind: "variable", name: "totalWater", value: "0" }],
      code_line: 7
    });
    return {
      title: "Trapping Rain Water (Edge Case)",
      algorithm: "Two Pointers",
      problem: `Elevation map: [${rawStr}]`,
      intuition: "Requires at least 3 bars to form a depression.",
      invariant: "Length < 3 yields strictly 0 trapped volume.",
      time_complexity: "O(N)",
      space_complexity: "O(1)",
      source_code: sourceCode,
      scenes: scenes
    };
  }

  let left = 0, right = n - 1;
  let leftMax = 0, rightMax = 0;
  let totalWater = 0;
  const trapped = {};
  let step = 1;

  scenes.push({
    id: "trap_setup",
    type: "setup",
    title: "Initialize Two Pointers",
    narration: `left=0 (height ${nums[0]}), right=${n-1} (height ${nums[n-1]}). leftMax=0, rightMax=0.`,
    dialogue: [
      { character_id: "algo", text: "Left climber at index 0, right climber at index " + (n-1) + "." },
      { character_id: "data", text: `Outer walls established.` }
    ],
    states: [
      { kind: "array", name: "height", value: rawStr },
      { kind: "pointer", name: "left", value: String(left), target_index: left },
      { kind: "pointer", name: "right", value: String(right), target_index: right },
      { kind: "variable", name: "leftMax", value: "0" },
      { kind: "variable", name: "rightMax", value: "0" },
      { kind: "variable", name: "totalWater", value: "0" }
    ],
    code_line: 3
  });

  while (left < right) {
    step++;
    if (nums[left] < nums[right]) {
      const h = nums[left];
      if (h >= leftMax) {
        leftMax = h;
        scenes.push({
          id: `trap_${step}`,
          type: "step",
          title: `Update leftMax to ${leftMax} at Index ${left}`,
          narration: `height[${left}] (${h}) >= leftMax. New leftMax is ${leftMax}.`,
          dialogue: [{ character_id: "algo", text: `New left barrier height: ${leftMax}.` }],
          states: [
            { kind: "array", name: "height", value: rawStr, index: left, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            { kind: "variable", name: "leftMax", value: String(leftMax), highlight: true },
            { kind: "variable", name: "rightMax", value: String(rightMax) },
            { kind: "variable", name: "totalWater", value: String(totalWater) }
          ],
          code_line: 11
        });
      } else {
        const w = leftMax - h;
        totalWater += w;
        trapped[left] = w;
        scenes.push({
          id: `trap_${step}`,
          type: "decision",
          title: `Trapped +${w} Water at Index ${left}`,
          narration: `height[${left}] (${h}) < leftMax (${leftMax}). Trapped = ${leftMax} - ${h} = ${w}. totalWater = ${totalWater}.`,
          dialogue: [
            { character_id: "algo", text: `Trapped ${w} water! Bounded by leftMax (${leftMax}).` },
            { character_id: "bug", text: "Why can't water spill to the right?" }
          ],
          states: [
            { kind: "array", name: "height", value: rawStr, index: left, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            ...Object.entries(trapped).map(([idx, amt]) => ({ kind: "water", name: `water_${idx}`, value: String(amt), index: +idx })),
            { kind: "variable", name: "leftMax", value: String(leftMax) },
            { kind: "variable", name: "rightMax", value: String(rightMax) },
            { kind: "variable", name: "totalWater", value: String(totalWater), highlight: true }
          ],
          code_line: 14,
          why: {
            decision: `height[${left}] (${h}) < height[${right}] (${nums[right]})`,
            limiting_factor: "Left wall is strictly shorter than right wall",
            invariant_proof: `Since height[${right}] >= leftMax (${leftMax}), water ceiling at index ${left} cannot exceed ${leftMax}.`,
            skeptical_question: "Could a middle peak allow more water here?",
            airtight_answer: `No. Water spills over leftMax (${leftMax}) before any higher level could be reached.`
          }
        });
      }
      left++;
    } else {
      const h = nums[right];
      if (h >= rightMax) {
        rightMax = h;
        scenes.push({
          id: `trap_${step}`,
          type: "step",
          title: `Update rightMax to ${rightMax} at Index ${right}`,
          narration: `height[${right}] (${h}) >= rightMax. New rightMax is ${rightMax}.`,
          dialogue: [{ character_id: "algo", text: `New right barrier height: ${rightMax}.` }],
          states: [
            { kind: "array", name: "height", value: rawStr, index: right, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            { kind: "variable", name: "leftMax", value: String(leftMax) },
            { kind: "variable", name: "rightMax", value: String(rightMax), highlight: true },
            { kind: "variable", name: "totalWater", value: String(totalWater) }
          ],
          code_line: 19
        });
      } else {
        const w = rightMax - h;
        totalWater += w;
        trapped[right] = w;
        scenes.push({
          id: `trap_${step}`,
          type: "decision",
          title: `Trapped +${w} Water at Index ${right}`,
          narration: `height[${right}] (${h}) < rightMax (${rightMax}). Trapped = ${rightMax} - ${h} = ${w}. totalWater = ${totalWater}.`,
          dialogue: [
            { character_id: "algo", text: `Trapped ${w} water from right boundary!` },
            { character_id: "bug", text: "Symmetric invariant holds." }
          ],
          states: [
            { kind: "array", name: "height", value: rawStr, index: right, highlight: true },
            { kind: "pointer", name: "left", value: String(left), target_index: left },
            { kind: "pointer", name: "right", value: String(right), target_index: right },
            ...Object.entries(trapped).map(([idx, amt]) => ({ kind: "water", name: `water_${idx}`, value: String(amt), index: +idx })),
            { kind: "variable", name: "leftMax", value: String(leftMax) },
            { kind: "variable", name: "rightMax", value: String(rightMax) },
            { kind: "variable", name: "totalWater", value: String(totalWater), highlight: true }
          ],
          code_line: 22,
          why: {
            decision: `height[${right}] (${h}) <= height[${left}] (${nums[left]})`,
            limiting_factor: "Right wall is limiting boundary",
            invariant_proof: `Since leftMax >= rightMax (${rightMax}), water at index ${right} is strictly bounded by rightMax.`,
            skeptical_question: "Can water leak leftward?",
            airtight_answer: `No. The left side has a wall of at least ${rightMax}, so water cannot escape to the left.`
          }
        });
      }
      right--;
    }
  }

  scenes.push({
    id: "trap_final",
    type: "result",
    title: `Result: ${totalWater} Total Water Trapped`,
    narration: `Pointers met at index ${left}. Total water trapped: ${totalWater} units.`,
    dialogue: [
      { character_id: "algo", text: `Simulation complete. Total trapped water is ${totalWater}.` },
      { character_id: "bug", text: "All invariants held across all steps!" }
    ],
    states: [
      { kind: "array", name: "height", value: rawStr },
      ...Object.entries(trapped).map(([idx, amt]) => ({ kind: "water", name: `water_${idx}`, value: String(amt), index: +idx })),
      { kind: "variable", name: "totalWater", value: String(totalWater), highlight: true }
    ],
    code_line: 26
  });

  return {
    title: "Trapping Rain Water",
    algorithm: "Two Pointers",
    problem: `Elevation map: [${rawStr}]`,
    intuition: "Shorter wall completely bounds the water level, allowing one-pass O(N) evaluation.",
    visual_metaphor: "Climbers measuring elevation ridges and filling basins.",
    invariant: "min(leftMax, rightMax) provides the provable upper water ceiling.",
    time_complexity: "O(N)",
    space_complexity: "O(1)",
    source_code: sourceCode || `public int Trap(int[] height)\n{\n    int left = 0, right = height.Length - 1;\n    int leftMax = 0, rightMax = 0;\n    int totalWater = 0;\n    while (left < right)\n    {\n        if (height[left] < height[right])\n        {\n            if (height[left] >= leftMax) leftMax = height[left];\n            else totalWater += leftMax - height[left];\n            left++;\n        }\n        else\n        {\n            if (height[right] >= rightMax) rightMax = height[right];\n            else totalWater += rightMax - height[right];\n            right--;\n        }\n    }\n    return totalWater;\n}`,
    scenes: scenes
  };
}

function buildBinarySearchSpec(nums, target, sourceCode) {
  nums = nums.slice().sort((a,b) => a - b);
  const n = nums.length;
  const rawStr = nums.join(",");
  const scenes = [];

  scenes.push({
    id: "bs_init",
    type: "title",
    title: `Binary Search: Target ${target}`,
    narration: `Searching for target = ${target} in sorted array of ${n} elements: [${rawStr}].`,
    dialogue: [
      { character_id: "algo", text: `We need to find ${target}. Because array is strictly sorted, we halve the search space at every probe!` },
      { character_id: "bug", text: `Let's make sure our middle index calculation doesn't overflow or miss ${target}.` }
    ],
    states: [
      { kind: "array", name: "nums", value: rawStr },
      { kind: "variable", name: "target", value: String(target) }
    ],
    code_line: 1
  });

  let left = 0, right = n - 1, step = 1, foundIdx = -1;
  while (left <= right) {
    step++;
    const mid = Math.floor(left + (right - left) / 2);
    const midVal = nums[mid];

    scenes.push({
      id: `bs_${step}`,
      type: "decision",
      title: `Probe Midpoint: Index ${mid} (Value ${midVal})`,
      narration: `Search interval [${left}..${right}]. Calculate mid = ${mid}. nums[${mid}] = ${midVal} vs target ${target}.`,
      dialogue: [
        { character_id: "algo", text: `Probing mid = ${mid} (value ${midVal}). Comparing with target ${target}.` },
        { character_id: "data", text: `Active candidates: ${right - left + 1} elements.` }
      ],
      states: [
        { kind: "array", name: "nums", value: rawStr, index: mid, highlight: true },
        { kind: "pointer", name: "left", value: String(left), target_index: left },
        { kind: "pointer", name: "right", value: String(right), target_index: right },
        { kind: "pointer", name: "mid", value: String(mid), target_index: mid },
        { kind: "variable", name: "target", value: String(target) },
        { kind: "variable", name: "nums[mid]", value: String(midVal) }
      ],
      code_line: 5,
      why: {
        decision: `nums[${mid}] = ${midVal} vs target = ${target}`,
        limiting_factor: "Strict array monotonicity",
        invariant_proof: `If target exists, it is strictly within [${left}..${right}].`,
        skeptical_question: "Why can we eliminate the entire other half?",
        airtight_answer: `Because array is sorted. If nums[${mid}] ${midVal < target ? '<' : '>'} ${target}, no element in the discarded half can equal ${target}.`
      }
    });

    if (midVal === target) {
      foundIdx = mid;
      scenes.push({
        id: `bs_found`,
        type: "result",
        title: `Target ${target} Found at Index ${mid}!`,
        narration: `nums[${mid}] == ${target}. Target found in logarithmic time O(log N).`,
        dialogue: [
          { character_id: "algo", text: `Target ${target} located at index ${mid}!` },
          { character_id: "bug", text: `Optimal O(log N) search verified.` }
        ],
        states: [
          { kind: "array", name: "nums", value: rawStr, index: mid, highlight: true },
          { kind: "pointer", name: "found", value: String(mid), target_index: mid },
          { kind: "variable", name: "result", value: String(mid), highlight: true }
        ],
        code_line: 6
      });
      break;
    } else if (midVal < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  if (foundIdx === -1) {
    scenes.push({
      id: `bs_miss`,
      type: "result",
      title: `Target ${target} Not Present`,
      narration: `Pointers crossed (left > right). Target does not exist in array. Returns -1.`,
      dialogue: [
        { character_id: "algo", text: `Target ${target} is provably not in array. Return -1.` },
        { character_id: "bug", text: `All candidates systematically ruled out.` }
      ],
      states: [
        { kind: "array", name: "nums", value: rawStr },
        { kind: "variable", name: "result", value: "-1", highlight: true }
      ],
      code_line: 9
    });
  }

  return {
    title: `Binary Search — Target ${target}`,
    algorithm: "Binary Search",
    problem: `Find index of target ${target} in sorted array [${rawStr}]`,
    intuition: "Halve search space at each step by probing the middle element.",
    invariant: "Target is guaranteed to be within [left..right] if it exists in the array.",
    time_complexity: "O(log N)",
    space_complexity: "O(1)",
    source_code: sourceCode || `public int BinarySearch(int[] nums, int target)\n{\n    int left = 0, right = nums.Length - 1;\n    while (left <= right)\n    {\n        int mid = left + (right - left) / 2;\n        if (nums[mid] == target) return mid;\n        if (nums[mid] < target) left = mid + 1;\n        else right = mid - 1;\n    }\n    return -1;\n}`,
    scenes: scenes
  };
}

function buildTwoSumSpec(nums, target, sourceCode) {
  const n = nums.length;
  const rawStr = nums.join(",");
  const scenes = [];

  scenes.push({
    id: "ts_init",
    type: "title",
    title: `Two Sum: Target ${target}`,
    narration: `Find two indices in [${rawStr}] that sum to ${target} in a single O(N) pass using a Hash Map.`,
    dialogue: [
      { character_id: "algo", text: `Instead of O(N^2) pairwise check, we store seen elements in a hash map for O(1) lookup!` },
      { character_id: "bug", text: `For each number x, we check if complement (target - x) is in the table.` }
    ],
    states: [
      { kind: "array", name: "nums", value: rawStr },
      { kind: "variable", name: "target", value: String(target) }
    ],
    code_line: 1
  });

  const seen = {};
  for (let i = 0; i < n; i++) {
    const num = nums[i];
    const complement = target - num;
    const seenStr = "{" + Object.entries(seen).map(([k,v]) => `${k}:${v}`).join(", ") + "}";

    if (complement in seen) {
      scenes.push({
        id: `ts_found`,
        type: "result",
        title: `Complement Found! Indices [${seen[complement]}, ${i}]`,
        narration: `nums[${i}] = ${num}. Complement ${complement} found at index ${seen[complement]}. ${nums[seen[complement]]} + ${num} = ${target}!`,
        dialogue: [
          { character_id: "algo", text: `Match! nums[${seen[complement]}] + nums[${i}] = ${target}!` },
          { character_id: "bug", text: `Optimal O(N) time with O(N) hash table.` }
        ],
        states: [
          { kind: "array", name: "nums", value: rawStr, index: i, highlight: true },
          { kind: "pointer", name: "prev", value: String(seen[complement]), target_index: seen[complement] },
          { kind: "pointer", name: "curr", value: String(i), target_index: i },
          { kind: "variable", name: "complement", value: String(complement) },
          { kind: "variable", name: "hash_map", value: seenStr },
          { kind: "variable", name: "result", value: `[${seen[complement]}, ${i}]`, highlight: true }
        ],
        code_line: 7
      });
      break;
    } else {
      seen[num] = i;
      scenes.push({
        id: `ts_step_${i}`,
        type: "step",
        title: `Inspect Index ${i} (${num})`,
        narration: `Need complement ${complement}. Not seen yet. Store seen[${num}] = ${i}.`,
        dialogue: [
          { character_id: "algo", text: `nums[${i}]=${num}. Need ${complement}. Storing in hash table.` },
          { character_id: "data", text: `Added ${num} -> index ${i}.` }
        ],
        states: [
          { kind: "array", name: "nums", value: rawStr, index: i, highlight: true },
          { kind: "pointer", name: "curr", value: String(i), target_index: i },
          { kind: "variable", name: "needed", value: String(complement) },
          { kind: "variable", name: "hash_map", value: seenStr }
        ],
        code_line: 9
      });
    }
  }

  return {
    title: `Two Sum — Target ${target}`,
    algorithm: "Hash Map",
    problem: `Find indices in [${rawStr}] summing to ${target}`,
    intuition: "Maintain a lookup table of past elements to evaluate the required complement in O(1).",
    invariant: "All elements before index i are recorded in the hash table.",
    time_complexity: "O(N)",
    space_complexity: "O(N)",
    source_code: sourceCode || `public int[] TwoSum(int[] nums, int target)\n{\n    var seen = new Dictionary<int, int>();\n    for (int i = 0; i < nums.Length; i++)\n    {\n        int complement = target - nums[i];\n        if (seen.ContainsKey(complement))\n            return new int[] { seen[complement], i };\n        seen[nums[i]] = i;\n    }\n    return new int[0];\n}`,
    scenes: scenes
  };
}

function buildKadaneSpec(nums, sourceCode) {
  const n = nums.length;
  const rawStr = nums.join(",");
  const scenes = [];

  scenes.push({
    id: "kad_init",
    type: "title",
    title: "Maximum Subarray (Kadane's Algorithm)",
    narration: `Find contiguous subarray in [${rawStr}] with maximum sum.`,
    dialogue: [
      { character_id: "algo", text: "Kadane's invariant: if current running sum drops below 0, it can never help future extensions!" },
      { character_id: "bug", text: "So whenever currentSum < 0, we immediately discard the prefix and restart." }
    ],
    states: [
      { kind: "array", name: "nums", value: rawStr },
      { kind: "variable", name: "maxSum", value: String(nums[0] || 0) }
    ],
    code_line: 1
  });

  let currSum = 0, maxSum = nums[0] || 0;
  for (let i = 0; i < n; i++) {
    const num = nums[i];
    let restarted = false;
    if (currSum < 0) {
      currSum = num;
      restarted = true;
    } else {
      currSum += num;
    }
    const newBest = currSum > maxSum;
    if (newBest) maxSum = currSum;

    scenes.push({
      id: `kad_${i}`,
      type: restarted || newBest ? "decision" : "step",
      title: `Element ${i} (${num}): Running Sum = ${currSum}, Max = ${maxSum}`,
      narration: `At index ${i} (val=${num}). ${restarted ? 'Negative prefix discarded; restarted. ' : ''}${newBest ? 'New record max! ' : ''}currentSum = ${currSum}, maxSum = ${maxSum}.`,
      dialogue: [
        { character_id: "algo", text: `currentSum = ${currSum}. Record maxSum = ${maxSum}.` },
        { character_id: "data", text: `Inspecting index ${i}.` }
      ],
      states: [
        { kind: "array", name: "nums", value: rawStr, index: i, highlight: true },
        { kind: "pointer", name: "curr", value: String(i), target_index: i },
        { kind: "variable", name: "currentSum", value: String(currSum), highlight: restarted },
        { kind: "variable", name: "maxSum", value: String(maxSum), highlight: newBest }
      ],
      code_line: 6,
      why: restarted ? {
        decision: `currSum < 0, reset to ${num}`,
        limiting_factor: "Negative prefix diminishes any subsequent sum",
        invariant_proof: "A subarray ending at i either extends the best prefix or starts fresh.",
        skeptical_question: "Why can we discard the prefix?",
        airtight_answer: "Because any future positive segment would be larger without that negative prefix."
      } : null
    });
  }

  scenes.push({
    id: "kad_final",
    type: "result",
    title: `Result: Maximum Subarray Sum = ${maxSum}`,
    narration: `Evaluated in single O(N) pass. Maximum contiguous sum is ${maxSum}.`,
    dialogue: [
      { character_id: "algo", text: `Final answer: ${maxSum}!` },
      { character_id: "bug", text: "Optimal linear time without inspecting O(N^2) pairs." }
    ],
    states: [
      { kind: "array", name: "nums", value: rawStr },
      { kind: "variable", name: "maxSum", value: String(maxSum), highlight: true }
    ],
    code_line: 11
  });

  return {
    title: "Maximum Subarray (Kadane's Algorithm)",
    algorithm: "Sliding Window / DP",
    problem: `Find maximum contiguous sum in [${rawStr}]`,
    intuition: "Discard negative prefixes; keep extending as long as prefix contributes positive sum.",
    invariant: "At step i, currentSum holds maximum subarray sum ending strictly at index i.",
    time_complexity: "O(N)",
    space_complexity: "O(1)",
    source_code: sourceCode || `public int MaxSubArray(int[] nums)\n{\n    int currentSum = 0, maxSum = nums[0];\n    for (int i = 0; i < nums.Length; i++)\n    {\n        if (currentSum < 0) currentSum = 0;\n        currentSum += nums[i];\n        if (currentSum > maxSum) maxSum = currentSum;\n    }\n    return maxSum;\n}`,
    scenes: scenes
  };
}

// --------------------------------------------------------------------------
// Core UI & Runtime State
// --------------------------------------------------------------------------

let globalManifest = [];

async function init() {
  updateTunnelUI();
  try {
    const res = await fetch("cases/manifest.json");
    globalManifest = await res.json();
    renderFilteredRibbon("trapping");
    // Load first case
    if (globalManifest.length > 0) {
      loadCaseFile(globalManifest[0].file);
    }
  } catch (e) {
    console.warn("Could not load cases/manifest.json, using local default", e);
    switchParadigm("trapping");
  }
}

function renderFilteredRibbon(paradigm) {
  const ribbon = $("presets-ribbon");
  ribbon.innerHTML = "";

  // Paradigm Buttons
  const paradigms = [
    { id: "trapping", label: "💧 Trapping Rain Water" },
    { id: "binary_search", label: "🔍 Binary Search" },
    { id: "two_sum", label: "⚡ Two Sum" },
    { id: "kadane", label: "📈 Max Subarray" }
  ];

  paradigms.forEach(p => {
    const btn = document.createElement("button");
    btn.className = "preset-chip" + (p.id === paradigm ? " active" : "");
    btn.textContent = p.label;
    btn.onclick = () => switchParadigm(p.id);
    ribbon.appendChild(btn);
  });

  // Filter test cases
  const filtered = globalManifest.filter(m => !paradigm || m.paradigm === paradigm);
  filtered.forEach((c, idx) => {
    const btn = document.createElement("button");
    btn.className = "preset-chip";
    btn.style.borderColor = "rgba(255,255,255,0.15)";
    btn.innerHTML = `<span style="opacity:0.7;">Case:</span> <strong>${c.name.split(':')[1] || c.name}</strong>`;
    btn.onclick = () => loadCaseFile(c.file);
    ribbon.appendChild(btn);
  });
}

async function loadCaseFile(file) {
  try {
    const res = await fetch("cases/" + file);
    const spec = await res.json();
    setSpec(spec);
  } catch (err) {
    console.error("Failed to load case file", err);
  }
}

function updateTunnelUI() {
  if (devTunnelUrl) {
    $("tunnel-dot").classList.add("active");
    $("tunnel-status-text").textContent = "Tunnel Connected";
    $("tunnel-url-input").value = devTunnelUrl;
  } else {
    $("tunnel-dot").classList.remove("active");
    $("tunnel-status-text").textContent = "Static Engine";
  }
}

function switchParadigm(paradigm) {
  renderFilteredRibbon(paradigm);

  if (globalManifest.length > 0) {
    const match = globalManifest.find(m => m.paradigm === paradigm);
    if (match) {
      loadCaseFile(match.file);
      return;
    }
  }

  // Fallback to client-side generated defaults
  if (paradigm === 'binary_search') {
    setSpec(buildBinarySearchSpec([-1, 0, 3, 5, 9, 12], 9));
  } else if (paradigm === 'two_sum') {
    setSpec(buildTwoSumSpec([2, 7, 11, 15], 9));
  } else if (paradigm === 'kadane') {
    setSpec(buildKadaneSpec([-2, 1, -3, 4, -1, 2, 1, -5, 4]));
  } else {
    setSpec(buildTrappingRainWaterSpec([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]));
  }
}

function setSpec(spec) {
  currentSpec = spec;
  currentIndex = 0;
  stopPlay();

  $("algo-title").textContent = spec.title;
  $("algo-sub").textContent = spec.algorithm + " — " + spec.problem;
  $("pill-time").textContent = "Time: " + (spec.time_complexity || "O(N)");
  $("pill-space").textContent = "Space: " + (spec.space_complexity || "O(1)");
  $("pill-paradigm").textContent = spec.algorithm || "Algorithm";

  $("intuition-text").innerHTML = "<strong>" + (spec.intuition || "") + "</strong>" + (spec.invariant ? " — <em>" + spec.invariant + "</em>" : "");

  // Populate dropdown
  const select = $("scene-select");
  select.innerHTML = "";
  spec.scenes.forEach((s, idx) => {
    const opt = document.createElement("option");
    opt.value = idx;
    opt.textContent = `${idx + 1}. [${s.type.toUpperCase()}] ${s.title}`;
    select.appendChild(opt);
  });
  $("timeline-slider").max = Math.max(0, spec.scenes.length - 1);

  // Source code panel
  if (spec.source_code) {
    $("code-studio").style.display = "flex";
    $("stage-grid").classList.add("with-code");
    $("code-lang-pill").textContent = spec.source_language || "C#";
    const lines = spec.source_code.split("\n");
    const codeDiv = $("code-lines");
    codeDiv.innerHTML = "";
    lines.forEach((l, i) => {
      const row = document.createElement("div");
      row.className = "code-row";
      row.id = `code-line-${i + 1}`;
      row.innerHTML = `<span class="code-num">${i + 1}</span><span>${escapeHtml(l)}</span>`;
      codeDiv.appendChild(row);
    });
  } else {
    $("code-studio").style.display = "none";
    $("stage-grid").classList.remove("with-code");
  }

  renderScene(0);
}

function escapeHtml(s) {
  return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderScene(idx) {
  if (!currentSpec || !currentSpec.scenes[idx]) return;
  const s = currentSpec.scenes[idx];

  $("timeline-slider").value = idx;
  $("step-counter").textContent = `${idx + 1}/${currentSpec.scenes.length}`;
  $("scene-select").value = idx;

  $("narration-title").textContent = s.title;
  $("narration-text").innerHTML = s.narration;

  // Comic Editorial Speech
  const stage = $("dialogue-stage");
  stage.innerHTML = "";
  if (s.dialogue && s.dialogue.length) {
    s.dialogue.forEach(d => {
      const charId = (typeof d === "string") ? (d.includes("?") ? "bug" : "algo") : (d.character_id || "algo");
      const text = (typeof d === "string") ? d : d.text;
      const avatar = charId === "bug" ? "🤔" : (charId === "data" ? "🧱" : "🧑");
      const name = charId === "bug" ? "Bug (Skeptic)" : (charId === "data" ? "Data (State)" : "Algo (Lead)");

      const row = document.createElement("div");
      row.className = `speech-row ${charId}`;
      row.innerHTML = `
        <div class="char-badge ${charId}">${avatar}</div>
        <div class="speech-bubble">
          <b>${name}</b>
          ${escapeHtml(text)}
        </div>
      `;
      stage.appendChild(row);
    });
  }

  // Visual Canvas
  const canvas = $("visual-canvas");
  canvas.innerHTML = "";

  const arrayItem = s.states.find(x => x.kind === "array");
  const pointers = s.states.filter(x => x.kind === "pointer");
  const variables = s.states.filter(x => x.kind === "variable");
  const waterItems = s.states.filter(x => x.kind === "water");

  if (arrayItem && arrayItem.value) {
    const rawVals = arrayItem.value.split(",");
    const numVals = rawVals.map(v => parseInt(v.trim(), 10) || 0);
    const maxVal = Math.max(...numVals, 1);

    // If Elevation Bar Chart applies (Trapping Rain Water)
    if (waterItems.length > 0 || currentSpec.algorithm.toLowerCase().includes("trap")) {
      const chart = document.createElement("div");
      chart.className = "chart-container";
      numVals.forEach((h, j) => {
        const col = document.createElement("div");
        col.className = "bar-col";
        const wItem = waterItems.find(w => w.index === j);
        const wVal = wItem ? parseInt(wItem.value, 10) || 0 : 0;
        const barPx = Math.round((h / maxVal) * 75);
        const waterPx = Math.round((wVal / maxVal) * 75);

        if (waterPx > 0) {
          const wb = document.createElement("div");
          wb.className = "water-block";
          wb.style.height = `${waterPx}px`;
          wb.textContent = wVal;
          col.appendChild(wb);
        }
        const hb = document.createElement("div");
        hb.className = "height-bar" + (arrayItem.index === j ? " active" : "");
        hb.style.height = `${Math.max(4, barPx)}px`;
        col.appendChild(hb);
        chart.appendChild(col);
      });
      canvas.appendChild(chart);
    }

    // Array Cells
    const arrWrap = document.createElement("div");
    arrWrap.className = "array-strip";
    rawVals.forEach((v, j) => {
      const cellBox = document.createElement("div");
      cellBox.className = "cell-wrapper";
      const cell = document.createElement("div");
      cell.className = "array-cell" + (arrayItem.index === j ? " hot" : "");

      pointers.forEach(p => {
        const pIdx = p.target_index !== undefined ? p.target_index : parseInt(p.value, 10);
        if (pIdx === j) {
          if (p.name.includes("left")) cell.classList.add("left-active");
          else if (p.name.includes("right")) cell.classList.add("right-active");
          else if (p.name.includes("mid")) cell.classList.add("mid-active");
        }
      });

      cell.textContent = v.trim();
      cellBox.innerHTML = `<span class="cell-idx">${j}</span>`;
      cellBox.appendChild(cell);

      pointers.forEach(p => {
        const pIdx = p.target_index !== undefined ? p.target_index : parseInt(p.value, 10);
        if (pIdx === j) {
          const ptr = document.createElement("div");
          const pType = p.name.includes("left") ? "left" : (p.name.includes("right") ? "right" : (p.name.includes("mid") ? "mid" : "general"));
          ptr.className = `pointer-chip ${pType}`;
          ptr.innerHTML = `<span>▲</span><span>${escapeHtml(p.name)}</span>`;
          cellBox.appendChild(ptr);
        }
      });

      arrWrap.appendChild(cellBox);
    });
    canvas.appendChild(arrWrap);
  }

  // Variables Grid
  if (variables.length) {
    const vr = document.createElement("div");
    vr.className = "variables-grid";
    variables.forEach(v => {
      const card = document.createElement("div");
      card.className = "var-card" + (v.highlight ? " highlight" : "");
      card.innerHTML = `<span style="color:var(--text-muted);">${escapeHtml(v.name)}:</span> <span>${escapeHtml(v.value)}</span>`;
      vr.appendChild(card);
    });
    canvas.appendChild(vr);
  }

  // Invariant Inspector ("Why is this safe?")
  const whyCard = $("why-inspector");
  if (s.why) {
    whyCard.classList.add("active");
    $("why-decision").textContent = s.why.decision;
    $("why-limiting").textContent = s.why.limiting_factor;
    $("why-invariant").textContent = s.why.invariant_proof;
    $("why-q").textContent = `🤔 Bug: "${s.why.skeptical_question}"`;
    $("why-a").textContent = `🧑 Algo: "${s.why.airtight_answer}"`;
  } else {
    whyCard.classList.remove("active");
  }

  // Code line tracking
  if (currentSpec.source_code) {
    document.querySelectorAll(".code-row.active").forEach(el => el.classList.remove("active"));
    if (s.code_line) {
      const el = document.getElementById(`code-line-${s.code_line}`);
      if (el) {
        el.classList.add("active");
        $("active-line-pill").textContent = `Line: ${s.code_line}`;
        el.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }
}

function goToScene(n) {
  if (!currentSpec) return;
  currentIndex = Math.max(0, Math.min(currentSpec.scenes.length - 1, n));
  renderScene(currentIndex);
}
function next() { if (currentIndex < currentSpec.scenes.length - 1) goToScene(currentIndex + 1); else stopPlay(); }
function prev() { if (currentIndex > 0) goToScene(currentIndex - 1); }
function first() { goToScene(0); }
function last() { if (currentSpec) goToScene(currentSpec.scenes.length - 1); }

function togglePlay() { playTimer ? stopPlay() : startPlay(); }
function startPlay() {
  $("play-btn").textContent = "⏸ Pause";
  $("play-btn").style.background = "#eab308";
  function tick() {
    if (currentIndex >= currentSpec.scenes.length - 1) { stopPlay(); return; }
    next();
    const dur = (currentSpec.scenes[currentIndex]?.duration_ms || 2000);
    playTimer = setTimeout(tick, dur);
  }
  const dur = (currentSpec.scenes[currentIndex]?.duration_ms || 2000);
  playTimer = setTimeout(tick, dur);
}
function stopPlay() {
  if (playTimer) { clearTimeout(playTimer); playTimer = null; }
  $("play-btn").textContent = "▶ Play";
  $("play-btn").style.background = "#f59e0b";
}

function toggleWhyMode() {
  const card = $("why-inspector");
  card.style.display = card.style.display === "none" ? "block" : "none";
}

// Modals & Custom Upload
function openUploadModal() { $("upload-modal").classList.add("open"); }
function closeUploadModal() { $("upload-modal").classList.remove("open"); }

function openTunnelModal() { $("tunnel-modal").classList.add("open"); }
function closeTunnelModal() { $("tunnel-modal").classList.remove("open"); }

function saveTunnelUrl() {
  const url = $("tunnel-url-input").value.trim();
  devTunnelUrl = url;
  localStorage.setItem("algo_animator_tunnel", url);
  updateTunnelUI();
  closeTunnelModal();
}

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    $("custom-code-area").value = e.target.result;
    if (file.name) {
      $("custom-algo-title").value = file.name.replace(/\.[^/.]+$/, "");
    }
  };
  reader.readAsText(file);
}

async function runCustomCode() {
  const algoTitle = $("custom-algo-title").value.trim();
  const codeText = $("custom-code-area").value.trim();
  const inputStr = $("custom-input-data").value.trim();
  closeUploadModal();

  // If live Dev Tunnel connected, call backend API
  if (devTunnelUrl) {
    try {
      const res = await fetch(`${devTunnelUrl.replace(/\/$/, '')}/api/animate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm: algoTitle, code: codeText, input: inputStr })
      });
      const data = await res.json();
      if (data.spec) {
        setSpec(data.spec);
        if (data.spec.synthesized_corner_cases && data.spec.synthesized_corner_cases.length > 0) {
          renderSynthesizedRibbon(data.spec.synthesized_corner_cases, codeText, algoTitle);
        }
        return;
      }
    } catch (e) {
      console.warn("Dev tunnel call error, falling back to client simulation:", e);
    }
  }

  // Client-side Auto-Detection & Corner-Case Synthesizer
  const codeLower = (codeText + " " + algoTitle).toLowerCase();
  let nums = [];
  let target = 9;
  const matchTarget = inputStr.match(/target\s*[:=]\s*(-?\d+)/i);
  if (matchTarget) target = parseInt(matchTarget[1], 10);

  const cleanArrStr = inputStr.replace(/target\s*[:=]\s*(-?\d+)/i, "").replace(/[\[\]]/g, "");
  nums = cleanArrStr.split(",").map(x => parseInt(x.trim(), 10)).filter(x => !isNaN(x));

  let spec = null;
  let synthesizedCases = [];

  if (codeLower.includes("binary") || codeLower.includes("mid") || codeLower.includes("left <= right")) {
    if (!nums.length) nums = [-1, 0, 3, 5, 9, 12];
    spec = buildBinarySearchSpec(nums, target, codeText);
    synthesizedCases = [
      { name: "Standard Illustrative", input: "[-1, 0, 3, 5, 9, 12], target=9" },
      { name: "Target at Index 0", input: "[1, 3, 5, 7, 9], target=1" },
      { name: "Target at Rightmost", input: "[1, 3, 5, 7, 9], target=9" },
      { name: "Target Absent (Middle)", input: "[2, 4, 6, 8, 10], target=5" },
      { name: "Target Absent (Too Small)", input: "[2, 4, 6], target=1" },
      { name: "Single Element Match", input: "[5], target=5" },
      { name: "Single Element Miss", input: "[5], target=3" },
      { name: "Empty Array", input: "[], target=1" }
    ];
  } else if (codeLower.includes("twosum") || codeLower.includes("two_sum") || codeLower.includes("dictionary") || codeLower.includes("complement")) {
    if (!nums.length) nums = [2, 7, 11, 15];
    spec = buildTwoSumSpec(nums, target, codeText);
    synthesizedCases = [
      { name: "Standard Pair", input: "[2, 7, 11, 15], target=9" },
      { name: "Adjacent Pair at End", input: "[3, 2, 4], target=6" },
      { name: "Identical Duplicates", input: "[3, 3], target=6" },
      { name: "Negative Numbers", input: "[-1, -2, -3, -4, -5], target=-8" },
      { name: "Zero Boundary", input: "[0, 4, 3, 0], target=0" },
      { name: "No Valid Pair", input: "[1, 2, 3], target=10" }
    ];
  } else if (codeLower.includes("maxsubarray") || codeLower.includes("kadane") || codeLower.includes("currentsum")) {
    if (!nums.length) nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4];
    spec = buildKadaneSpec(nums, codeText);
    synthesizedCases = [
      { name: "Classic LeetCode", input: "[-2, 1, -3, 4, -1, 2, 1, -5, 4]" },
      { name: "All Negative Numbers", input: "[-5, -2, -8, -1, -4]" },
      { name: "All Positive Numbers", input: "[1, 2, 3, 4, 5]" },
      { name: "Alternating Signs", input: "[5, -3, 5]" },
      { name: "Single Positive", input: "[10]" },
      { name: "Single Negative", input: "[-7]" }
    ];
  } else if (codeLower.includes("trap") || codeLower.includes("rain") || codeLower.includes("water") || codeLower.includes("leftmax")) {
    if (!nums.length) nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1];
    spec = buildTrappingRainWaterSpec(nums, codeText);
    synthesizedCases = [
      { name: "Standard Basin", input: "[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]" },
      { name: "Empty Elevation Map", input: "[]" },
      { name: "Single Element", input: "[4]" },
      { name: "Two Elements", input: "[3, 1]" },
      { name: "All Equal Heights", input: "[2, 2, 2, 2]" },
      { name: "Strictly Decreasing", input: "[5, 4, 3, 2, 1]" },
      { name: "Strictly Increasing", input: "[1, 2, 3, 4, 5]" },
      { name: "Deep Single Basin", input: "[4, 0, 0, 4]" }
    ];
  } else {
    // Default fallback
    if (matchTarget || codeLower.includes("target")) {
      if (!nums.length) nums = [-1, 0, 3, 5, 9, 12];
      spec = buildBinarySearchSpec(nums, target, codeText);
    } else {
      if (!nums.length) nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1];
      spec = buildTrappingRainWaterSpec(nums, codeText);
    }
  }

  setSpec(spec);
  if (synthesizedCases.length > 0) {
    renderSynthesizedRibbon(synthesizedCases, codeText, algoTitle);
  }
}

function renderSynthesizedRibbon(cases, codeText, algoTitle) {
  const ribbon = $("presets-ribbon");
  ribbon.innerHTML = "";

  const titleChip = document.createElement("div");
  titleChip.className = "preset-chip active";
  titleChip.style.background = "rgba(16, 185, 129, 0.15)";
  titleChip.style.borderColor = "rgba(16, 185, 129, 0.4)";
  titleChip.style.color = "#34d399";
  titleChip.innerHTML = `<span>✨ Synthesized Suite:</span> <strong>${algoTitle || "Custom Algorithm"}</strong>`;
  ribbon.appendChild(titleChip);

  cases.forEach((c, idx) => {
    const btn = document.createElement("button");
    btn.className = "preset-chip" + (idx === 0 ? " active" : "");
    btn.style.borderColor = "rgba(255,255,255,0.18)";
    btn.innerHTML = `<span style="opacity:0.75;">Case ${idx + 1}:</span> <strong>${c.name}</strong>`;
    btn.onclick = () => {
      document.querySelectorAll(".preset-chip").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      $("custom-input-data").value = c.input;
      runCustomCode();
    };
    ribbon.appendChild(btn);
  });
}

window.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA" || e.target.tagName === "SELECT") return;
  if (e.code === "Space") { e.preventDefault(); togglePlay(); }
  else if (e.code === "ArrowRight") { e.preventDefault(); next(); }
  else if (e.code === "ArrowLeft") { e.preventDefault(); prev(); }
  else if (e.code === "KeyW") { e.preventDefault(); toggleWhyMode(); }
});

init();
</script>
</body>
</html>
'''

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print("docs/index.html generated successfully with elite design system and multi-paradigm simulation!")
