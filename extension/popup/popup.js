// popup placeholder
document.getElementById('app').textContent = 'History RecALI — popup';

(async () => {
  const statusEl = document.getElementById('status');
  const btn = document.getElementById('summarize-btn');
  const listEl = document.getElementById('history-list');
  const summaryResultEl = document.getElementById('summary-result');

  // Tab switching
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(`${tab.dataset.tab}-tab`).classList.add('active');
      if (tab.dataset.tab === 'history') loadHistory();
    });
  });

  async function getPageText(tabId) {
    try {
      const [result] = await chrome.scripting.executeScript({
        target: { tabId },
        func: () => {
          try { return document.body.innerText.slice(0, 3000); } catch { return ''; }
        }
      });
      return result?.result || '';
    } catch (e) {
      console.error('executeScript error', e);
      return '';
    }
  }

  async function summarizeCurrent() {
    statusEl.textContent = 'Fetching page content...';
    statusEl.className = 'status loading';
    summaryResultEl.style.display = 'none';

    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tabs?.[0]) {
      statusEl.textContent = 'No active tab found';
      statusEl.className = 'status error';
      return;
    }

    const tab = tabs[0];
    const snippet = await getPageText(tab.id);

    if (!snippet) {
      statusEl.textContent = 'No text found on this page';
      statusEl.className = 'status error';
      return;
    }

    statusEl.textContent = 'Analyzing with AI...';

    try {
      // Get summary
      const sumRes = await fetch('http://127.0.0.1:8000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: tab.url, title: tab.title, snippet })
      });
      const sumData = await sumRes.json();
      const summary = sumData.summary || 'No summary generated';

      // Get trust score
      const analyzeRes = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: snippet })
      });
      const trustData = await analyzeRes.json();
      const trustScore = trustData.score || 0.5;
      const trustLabel = trustData.label || 'neutral';

      // Display results
      summaryResultEl.innerHTML = `
        <div class="summary-result">
          <h3 style="font-size:14px;margin-bottom:8px">📝 Summary</h3>
          <div class="summary-text">${summary}</div>
          <div class="trust-badge ${trustLabel}">
            ${trustLabel === 'credible' ? '✅' : trustLabel === 'neutral' ? '⚠️' : '❌'}
            ${trustLabel.charAt(0).toUpperCase() + trustLabel.slice(1)} (${(trustScore * 100).toFixed(0)}%)
          </div>
        </div>
      `;
      summaryResultEl.style.display = 'block';

      statusEl.textContent = 'Summary generated successfully!';
      statusEl.className = 'status success';

      // Save to storage
      const entry = {
        url: tab.url,
        title: tab.title,
        summary,
        trustScore,
        trustLabel,
        ts: Date.now()
      };

      chrome.storage.local.get({ summaries: [] }, (obj) => {
        const s = obj.summaries || [];
        s.unshift(entry);
        chrome.storage.local.set({ summaries: s.slice(0, 100) });
      });

    } catch (e) {
      console.error(e);
      statusEl.textContent = `Error: ${e.message || 'Connection failed. Is backend running?'}`;
      statusEl.className = 'status error';
    }
  }

  function loadHistory() {
    chrome.storage.local.get({ summaries: [] }, (obj) => {
      const items = obj.summaries || [];
      
      if (items.length === 0) {
        listEl.innerHTML = `<div class="empty-state"><div style="font-size:48px;margin-bottom:12px">📭</div><p>No captures yet. Start summarizing pages!</p></div>`;
        return;
      }

      listEl.innerHTML = items.slice(0, 20).map(e => `
        <div class="history-item" data-url="${e.url}">
          <div class="history-item-title">${e.title || 'Untitled'}</div>
          <div class="history-item-time">${new Date(e.ts).toLocaleString()}</div>
          <div class="history-item-summary">${(e.summary || '').slice(0, 150)}...</div>
          <div class="trust-badge ${e.trustLabel || 'neutral'}">
            ${e.trustLabel || 'neutral'} (${((e.trustScore || 0.5) * 100).toFixed(0)}%)
          </div>
        </div>
      `).join('');

      document.querySelectorAll('.history-item').forEach(item => {
        item.addEventListener('click', () => {
          chrome.tabs.create({ url: item.dataset.url });
        });
      });
    });
  }

  btn.addEventListener('click', summarizeCurrent);
  loadHistory();
})();
