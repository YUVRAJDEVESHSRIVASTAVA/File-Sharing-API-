document.addEventListener('DOMContentLoaded', function () {
  const copyBtn = document.getElementById('copyLinkBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const input = document.getElementById('shareLink');
      if (!input) return;
      navigator.clipboard.writeText(input.value).then(() => {
        const original = copyBtn.textContent;
        copyBtn.textContent = 'Copied';
        setTimeout(() => { copyBtn.textContent = original; }, 2000);
      }).catch(() => {
        copyBtn.textContent = 'Copy failed';
      });
    });
  }

  const timerEl = document.getElementById('expiryTimer');
  if (timerEl && timerEl.dataset.expires) {
    const expiry = new Date(timerEl.dataset.expires);
    const tick = () => {
      const now = new Date();
      const diff = expiry - now;
      if (diff <= 0) {
        timerEl.textContent = 'Expired';
        return;
      }
      const mins = Math.floor(diff / 60000);
      const secs = Math.floor((diff % 60000) / 1000);
      timerEl.textContent = `${mins}m ${secs}s`;
      setTimeout(tick, 1000);
    };
    tick();
  }
});
