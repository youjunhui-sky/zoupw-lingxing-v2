const TEMPLATE = window.DASHBOARD_TEMPLATE;

const money = (value) => `¥${Number(value || 0).toLocaleString('zh-CN', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})}`;
const number = (value) => Number(value || 0).toLocaleString('zh-CN', { maximumFractionDigits: 0 });
const percent = (value) => `${(Number(value || 0) * 100).toFixed(2)}%`;

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;',
  }[char]));
}

function text(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function setError(message) {
  const errorBox = document.getElementById('error-box');
  if (!errorBox) return;
  errorBox.textContent = message;
  errorBox.style.display = message ? 'block' : 'none';
}

const params = new URLSearchParams(window.location.search);
const filters = {
  reportDate: params.get('date') || '',
  trendDays: params.get('trend_days') || '30',
};

function filterQueryString() {
  const query = new URLSearchParams();
  if (filters.reportDate) query.set('date', filters.reportDate);
  query.set('trend_days', filters.trendDays);
  return query.toString();
}

function updateBrowserUrl() {
  const query = filterQueryString();
  window.history.replaceState(null, '', `${window.location.pathname}?${query}`);
}

function renderTemplateSwitch() {
  const element = document.getElementById('template-switch');
  if (!element) return;
  const query = filterQueryString();
  const suffix = query ? `?${query}` : '';
  const templates = [
    ['tech', '科技深色大屏版'],
    ['light', '商务浅色报表版'],
    ['ops', '简洁运营看板版'],
  ];
  element.innerHTML = templates.map(([key, label]) => `
    <a class="${key === TEMPLATE.key ? 'active' : ''}" href="/templates/${key}${suffix}">${label}</a>
  `).join('');
}

function renderControls() {
  const element = document.getElementById('dashboard-controls');
  if (!element) return;
  element.innerHTML = `
    <label>报表日期<input type="date" id="report-date-input" value="${escapeHtml(filters.reportDate)}"></label>
    <label>趋势范围<select id="trend-days-select">
      <option value="7" ${filters.trendDays === '7' ? 'selected' : ''}>近 7 天</option>
      <option value="30" ${filters.trendDays === '30' ? 'selected' : ''}>近 30 天</option>
      <option value="90" ${filters.trendDays === '90' ? 'selected' : ''}>近 90 天</option>
    </select></label>
    <button type="button" id="refresh-dashboard-button">刷新</button>
    <span>日期留空时默认使用 PG 最新数据</span>
  `;

  document.getElementById('report-date-input')?.addEventListener('change', (event) => {
    filters.reportDate = event.target.value;
    updateBrowserUrl();
    renderTemplateSwitch();
    loadDashboard();
  });
  document.getElementById('trend-days-select')?.addEventListener('change', (event) => {
    filters.trendDays = event.target.value;
    updateBrowserUrl();
    renderTemplateSwitch();
    loadDashboard();
  });
  document.getElementById('refresh-dashboard-button')?.addEventListener('click', loadDashboard);
}

function kpiItems(data) {
  const daily = data.daily || {};
  const weekly = data.weekly || {};
  return [
    ['GMV', money(daily.gmv), '当日销售额'],
    ['订单数', number(daily.order_count), '当日订单'],
    ['客单价', money(daily.avg_order_value), 'GMV / 订单数'],
    ['ACOS', percent(daily.acos), '广告成本销售比'],
    ['库存预警', number(daily.inventory_alerts), '低库存 SKU 数'],
    ['周 GMV', money(weekly.gmv), '本周累计'],
    ['周订单数', number(weekly.order_count), '本周累计'],
    ['周环比', percent(weekly.gmv_wow), 'GMV week-over-week'],
  ];
}

function renderKpis(data) {
  const element = document.getElementById('kpis');
  if (!element) return;
  element.innerHTML = kpiItems(data).map(([label, value, note]) => `
    <div class="kpi-card">
      <div class="kpi-label">${escapeHtml(label)}</div>
      <div class="kpi-value">${escapeHtml(value)}</div>
      <div class="kpi-note">${escapeHtml(note)}</div>
    </div>
  `).join('');
}

function renderMetricRail(data) {
  const element = document.getElementById('metric-rail');
  if (!element) return;
  element.innerHTML = kpiItems(data).slice(0, 5).map(([label, value]) => `
    <div class="rail-item"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>
  `).join('');
}

function renderDataStatus(data) {
  const element = document.getElementById('data-status');
  if (!element) return;
  const status = data.data_status || {};
  const warnings = status.warnings || [];
  element.innerHTML = `
    <div class="status-grid">
      <div><span>数据源</span><strong>${escapeHtml(status.data_source || '-')}</strong></div>
      <div><span>数据范围</span><strong>${escapeHtml(status.dws_min_date || '-')} ~ ${escapeHtml(status.dws_max_date || '-')}</strong></div>
      <div><span>最近同步</span><strong>${escapeHtml(status.latest_sync_time || '-')}</strong></div>
      <div><span>DWS行数</span><strong>${number(status.dws_row_count)}</strong></div>
    </div>
    ${warnings.length ? `<div class="status-warnings">${warnings.map(escapeHtml).join('；')}</div>` : '<div class="status-ok">数据状态正常</div>'}
  `;
}

function renderSummary(data) {
  text('report-meta', `报表日期：${data.report_date} ｜ 生成时间：${data.generated_at}`);
  text('refresh-meta', `最近刷新：${new Date().toLocaleString('zh-CN')}`);
  const daily = data.daily || {};
  const weekly = data.weekly || {};
  text('hero-gmv', money(daily.gmv));
  text('hero-orders', number(daily.order_count));
  text('hero-week', money(weekly.gmv));
  text('hero-acos', percent(daily.acos));
}

function makeChart(id) {
  const element = document.getElementById(id);
  return element ? echarts.init(element) : null;
}

const charts = {
  trend: makeChart('trend-chart'),
  shop: makeChart('shop-chart'),
  sku: makeChart('sku-chart'),
};

function renderTrendChart(rows) {
  if (!charts.trend) return;
  charts.trend.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    legend: { textStyle: { color: TEMPLATE.axis } },
    grid: TEMPLATE.trendGrid || { left: 48, right: 48, top: 42, bottom: 40 },
    xAxis: { type: 'category', data: rows.map((item) => item.date), axisLabel: { color: TEMPLATE.axis } },
    yAxis: [
      { type: 'value', name: 'GMV / 客单价', axisLabel: { color: TEMPLATE.axis }, splitLine: { lineStyle: { color: TEMPLATE.split } } },
      { type: 'value', name: '订单数', axisLabel: { color: TEMPLATE.axis }, splitLine: { show: false } },
    ],
    series: [
      { name: 'GMV', type: 'line', smooth: true, data: rows.map((item) => item.gmv), color: TEMPLATE.colors[0], areaStyle: TEMPLATE.area ? { opacity: TEMPLATE.area } : undefined },
      { name: '客单价', type: 'line', smooth: true, data: rows.map((item) => item.aov), color: TEMPLATE.colors[1] },
      { name: '订单数', type: 'bar', yAxisIndex: 1, data: rows.map((item) => item.orders), color: TEMPLATE.colors[2], barMaxWidth: 24 },
    ],
  });
}

function renderBarChart(chart, rows, nameKey, valueKey, label) {
  if (!chart) return;
  const sorted = [...rows].reverse();
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: TEMPLATE.barGrid || { left: 88, right: 28, top: 20, bottom: 24 },
    xAxis: { type: 'value', axisLabel: { color: TEMPLATE.axis }, splitLine: { lineStyle: { color: TEMPLATE.split } } },
    yAxis: { type: 'category', data: sorted.map((item) => item[nameKey] || '-'), axisLabel: { color: TEMPLATE.axis, width: 88, overflow: 'truncate' } },
    series: [{ name: label, type: 'bar', data: sorted.map((item) => item[valueKey] || 0), color: TEMPLATE.colors[0], barMaxWidth: TEMPLATE.barMaxWidth || 22 }],
  });
}

function renderRankingTable(rows) {
  const element = document.getElementById('ranking-table');
  if (!element) return;
  const html = (rows || []).slice(0, 12).map((item) => `
    <tr>
      <td>${escapeHtml(item.ranking_type)}</td>
      <td>${escapeHtml(item.name)}</td>
      <td class="money">${money(item.amount)}</td>
      <td class="money">${number(item.quantity)}</td>
    </tr>
  `).join('');
  element.innerHTML = html || '<tr><td colspan="4">暂无排行明细</td></tr>';
}

function renderTopList(id, rows, nameKey, valueKey) {
  const element = document.getElementById(id);
  if (!element) return;
  element.innerHTML = (rows || []).slice(0, 6).map((item) => `
    <div class="top-row">
      <span>${escapeHtml(item.rank)}. ${escapeHtml(item[nameKey] || '-')}</span>
      <strong>${money(item[valueKey])}</strong>
    </div>
  `).join('') || '<div class="top-row"><span>暂无数据</span><strong>-</strong></div>';
}

async function loadDashboard() {
  try {
    setError('');
    const response = await fetch(`/api/dashboard?${filterQueryString()}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`API 返回 ${response.status}`);
    const data = await response.json();
    renderSummary(data);
    renderKpis(data);
    renderMetricRail(data);
    renderDataStatus(data);
    renderTrendChart(data.trends || []);
    renderBarChart(charts.shop, data.shop_rankings || [], 'shop_name', 'gmv', 'GMV');
    renderBarChart(charts.sku, data.sku_rankings || [], 'sku', 'sales_amount', '销售额');
    renderRankingTable(data.rankings || []);
    renderTopList('shop-list', data.shop_rankings || [], 'shop_name', 'gmv');
    renderTopList('sku-list', data.sku_rankings || [], 'sku', 'sales_amount');
  } catch (error) {
    setError(`看板数据加载失败：${error.message}`);
  }
}

renderTemplateSwitch();
renderControls();
updateBrowserUrl();
loadDashboard();
setInterval(loadDashboard, 300000);
window.addEventListener('resize', () => Object.values(charts).forEach((chart) => chart?.resize()));
