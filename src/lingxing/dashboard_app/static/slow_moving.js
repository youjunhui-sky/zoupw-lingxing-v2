// 亚马逊 FBA 断货预警看板 — 前端
// 拉 /api/slow-moving, 渲染 KPI + 表格 + 两个 ECharts 图

let SNAPSHOT = null;       // 当前快照
let FILTERS = { country: '', shop: '', owner: '' };
let CHARTS = { country: null, owner: null };

const TEMPLATE = {
  text: '#e5e7eb',
  axis: '#94a3b8',
  panel: 'rgba(15, 12, 10, .72)',
  warn: '#fca5a5',
  crit: '#fee2e2',
  ok: '#bbf7d0',
};

const $ = (id) => document.getElementById(id);

function setStatus(state, text) {
  const pill = $('status-pill');
  pill.classList.remove('no-data', 'error');
  if (state !== 'ok') pill.classList.add(state);
  $('status-text').textContent = text;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  }[char]));
}

function badgeForDays(days, fba) {
  if (fba === 0) return `<span class="badge badge-zero">FBA=0</span>`;
  if (days < 3) return `<span class="badge badge-zero">${days.toFixed(1)}天</span>`;
  if (days < 7) return `<span class="badge badge-low">${days.toFixed(1)}天</span>`;
  return `<span class="badge badge-ok">${days.toFixed(1)}天</span>`;
}

async function loadSnapshot() {
  try {
    setStatus('ok', '加载中…');
    const resp = await fetch('/api/slow-moving');
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    SNAPSHOT = await resp.json();
  } catch (err) {
    setStatus('error', `加载失败: ${err.message}`);
    SNAPSHOT = null;
    return;
  }

  // 状态条
  const jd = SNAPSHOT.job_status;
  if (jd === 'success') setStatus('ok', `已就绪 · ${SNAPSHOT.kpi.red_count} 条红灯`);
  else if (jd === 'no_active') setStatus('no-data', '无 active 红灯 · 全部安全');
  else setStatus('no-data', '暂无数据 · 等首次 02:30 计算');

  $('data-date').textContent = SNAPSHOT.latest_event_date
    ? `数据日期: ${SNAPSHOT.latest_event_date}`
    : '数据日期: —';
  $('generated-at').textContent = `生成于: ${SNAPSHOT.generated_at}`;

  // KPI
  $('kpi-red').textContent = SNAPSHOT.kpi.red_count;
  $('kpi-min-days').textContent =
    SNAPSHOT.kpi.min_days_of_cover > 0 ? SNAPSHOT.kpi.min_days_of_cover.toFixed(1) : '—';
  $('kpi-owners').textContent = SNAPSHOT.kpi.owner_count;
  $('kpi-countries').textContent = SNAPSHOT.kpi.country_count;

  // 筛选下拉
  populateFilters();

  // 表格 + 图表
  renderTable();
  renderCharts();
}

function populateFilters() {
  const countries = [...new Set(SNAPSHOT.rows.map(r => r.country))].sort();
  const shops = [...new Set(SNAPSHOT.rows.map(r => r.shop_name))].sort();
  const owners = [...new Set(SNAPSHOT.rows.map(r => r.owner_name))].sort();

  fillSelect('filter-country', countries, FILTERS.country);
  fillSelect('filter-shop', shops, FILTERS.shop);
  fillSelect('filter-owner', owners, FILTERS.owner);

  $('filter-country').onchange = (e) => { FILTERS.country = e.target.value; renderTable(); };
  $('filter-shop').onchange = (e) => { FILTERS.shop = e.target.value; renderTable(); };
  $('filter-owner').onchange = (e) => { FILTERS.owner = e.target.value; renderTable(); };
}

function fillSelect(id, values, selected) {
  const sel = $(id);
  sel.innerHTML = `<option value="">全部 (${values.length})</option>` +
    values.map(v => `<option value="${escapeHtml(v)}"${v === selected ? ' selected' : ''}>${escapeHtml(v)}</option>`).join('');
}

function resetFilters() {
  FILTERS = { country: '', shop: '', owner: '' };
  populateFilters();
  renderTable();
}

function renderTable() {
  const filtered = SNAPSHOT.rows.filter(r =>
    (!FILTERS.country || r.country === FILTERS.country) &&
    (!FILTERS.shop || r.shop_name === FILTERS.shop) &&
    (!FILTERS.owner || r.owner_name === FILTERS.owner)
  );

  const tbody = $('rows-tbody');
  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="10" class="empty">没有匹配的红灯</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.slice(0, 50).map(row => {
    const daysClass = row.days_of_cover < 3 ? 'days-crit' : row.days_of_cover < 7 ? 'days-warn' : '';
    return `<tr>
      <td><code>${escapeHtml(row.asin)}</code></td>
      <td>${escapeHtml(row.sku)}</td>
      <td>${escapeHtml(row.country)}</td>
      <td>${escapeHtml(row.shop_name)}</td>
      <td>${escapeHtml(row.owner_name)}</td>
      <td style="text-align:right;">${row.fba_available}</td>
      <td style="text-align:right;">${row.avg_daily_sold.toFixed(1)}</td>
      <td style="text-align:right;" class="${daysClass}">${row.days_of_cover.toFixed(1)}</td>
      <td style="text-align:right;">${row.threshold_used}</td>
      <td>${badgeForDays(row.days_of_cover, row.fba_available)} <span style="color:#94a3b8;font-size:11px;">${escapeHtml(row.reason)}</span></td>
    </tr>`;
  }).join('');

  if (filtered.length > 50) {
    tbody.innerHTML += `<tr><td colspan="10" class="empty">…还有 ${filtered.length - 50} 条未显示</td></tr>`;
  }
}

function renderCharts() {
  const countryOpt = barOption(SNAPSHOT.by_country.map(c => c.country), SNAPSHOT.by_country.map(c => c.count), TEMPLATE.warn, '国家');
  const ownerOpt = barOption(SNAPSHOT.by_owner.map(o => o.owner_name), SNAPSHOT.by_owner.map(o => o.count), TEMPLATE.crit, '负责人');

  CHARTS.country = initOrUpdate(CHARTS.country, 'chart-country', countryOpt);
  CHARTS.owner = initOrUpdate(CHARTS.owner, 'chart-owner', ownerOpt);
}

function initOrUpdate(chart, domId, opt) {
  const dom = $(domId);
  if (!chart) {
    chart = echarts.init(dom, null, { renderer: 'canvas' });
  }
  chart.setOption(opt, true);
  return chart;
}

function barOption(categories, values, color, axisName) {
  return {
    backgroundColor: 'transparent',
    grid: { left: 50, right: 18, top: 16, bottom: 30 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'value', axisLabel: { color: TEMPLATE.axis } },
    yAxis: {
      type: 'category',
      data: categories,
      axisLabel: { color: TEMPLATE.axis, fontSize: 11 },
      name: axisName,
      nameTextStyle: { color: TEMPLATE.axis },
    },
    series: [{
      type: 'bar',
      data: values,
      itemStyle: { color, borderRadius: [0, 4, 4, 0] },
      label: { show: true, position: 'right', color: TEMPLATE.text, fontSize: 11 },
    }],
  };
}

window.addEventListener('resize', () => {
  if (CHARTS.country) CHARTS.country.resize();
  if (CHARTS.owner) CHARTS.owner.resize();
});

loadSnapshot();
// 每 60s 自动刷新 (看板 only, 不推送, 自动拉就行)
setInterval(loadSnapshot, 60_000);
