(() => {
  const journal = document.querySelector('#research-log');
  if (!journal) return;

  const filters = journal.querySelector('.log-filters');
  const buttons = [...journal.querySelectorAll('[data-log-filter]')];
  const entries = [...journal.querySelectorAll('[data-log-type]')];
  const days = [...journal.querySelectorAll('[data-log-day]')];
  const status = journal.querySelector('.log-filter-status');
  if (!filters || !status || !buttons.length) return;

  filters.hidden = false;
  for (const button of buttons) {
    button.addEventListener('click', () => {
      const selected = button.dataset.logFilter;
      for (const candidate of buttons) {
        candidate.setAttribute('aria-pressed', String(candidate === button));
      }
      let count = 0;
      for (const entry of entries) {
        entry.hidden = selected !== 'all' && entry.dataset.logType !== selected;
        if (!entry.hidden) count += 1;
      }
      for (const day of days) {
        day.hidden = ![...day.querySelectorAll('[data-log-type]')].some(entry => !entry.hidden);
      }
      status.textContent = count ? `显示 ${count} 条更新` : '暂无该类型的更新';
    });
  }
})();
