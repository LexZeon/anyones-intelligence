#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repository = 'https://github.com/LexZeon/anyones-intelligence';
const startMarker = '<!-- RESEARCH_LOG:START -->';
const endMarker = '<!-- RESEARCH_LOG:END -->';
const types = { page: '页面改动', file: '文件更新', feature: '功能更新' };
const changes = { added: '新增', modified: '更新', uploaded: '上传', deleted: '删除' };
const commitPattern = /^[0-9a-f]{40}$/i;

function fail(location, message) {
  throw new TypeError(`${location}: ${message}`);
}

function object(value, location) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail(location, '必须是对象');
}

function nonempty(value, location) {
  if (typeof value !== 'string' || !value.trim()) fail(location, '必须是非空文本');
}

function commit(value, location) {
  if (typeof value !== 'string' || !commitPattern.test(value)) fail(location, '必须是 40 位十六进制提交标识');
}

function validDate(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const [year, month, day] = value.split('-').map(Number);
  if (year < 1) return false;
  const date = new Date(0);
  date.setUTCFullYear(year, month - 1, day);
  return date.toISOString().slice(0, 10) === value;
}

function validPath(value, location) {
  nonempty(value, location);
  if (value !== value.trim() || /[\\:\u0000-\u001f\u007f]/.test(value)
      || value.startsWith('/') || value.split('/').some(part => !part || part === '.' || part === '..')) {
    fail(location, '必须是仓库相对路径，不能含绝对路径、协议、反斜杠或 . / .. 路径段');
  }
  try {
    value.split('/').map(encodeURIComponent);
  } catch {
    fail(location, '包含无效的 Unicode 字符');
  }
}

/** Validate the editable source before rendering or touching the homepage. */
export function validateLog(log) {
  object(log, 'research log');
  if (log.version !== 1) fail('version', '仅支持版本 1');
  if (log.timezone !== 'America/Los_Angeles') fail('timezone', '必须为 America/Los_Angeles');
  if (!Array.isArray(log.entries)) fail('entries', '必须是数组');
  const ids = new Set();
  log.entries.forEach((entry, index) => {
    const location = `entries[${index}]`;
    object(entry, location);
    nonempty(entry.id, `${location}.id`);
    if (ids.has(entry.id)) fail(`${location}.id`, '记录 ID 重复');
    ids.add(entry.id);
    if (!validDate(entry.date)) fail(`${location}.date`, '必须是真实日期 YYYY-MM-DD');
    if (typeof entry.type !== 'string' || !Object.hasOwn(types, entry.type)) fail(`${location}.type`, '必须为 page、file 或 feature');
    nonempty(entry.title, `${location}.title`);
    nonempty(entry.summary, `${location}.summary`);
    if (entry.commits !== undefined) {
      if (!Array.isArray(entry.commits)) fail(`${location}.commits`, '必须是数组');
      entry.commits.forEach((sha, i) => commit(sha, `${location}.commits[${i}]`));
    }
    if (entry.files !== undefined) {
      if (!Array.isArray(entry.files)) fail(`${location}.files`, '必须是数组');
      entry.files.forEach((file, i) => {
        const fileLocation = `${location}.files[${i}]`;
        object(file, fileLocation);
        validPath(file.path, `${fileLocation}.path`);
        if (typeof file.change !== 'string' || !Object.hasOwn(changes, file.change)) fail(`${fileLocation}.change`, '文件变更类型无效');
        if (file.ref !== undefined) commit(file.ref, `${fileLocation}.ref`);
        if (file.change === 'deleted' && !file.ref && !entry.commits?.length) {
          fail(fileLocation, '删除记录需要 ref 或 commits 中的提交标识');
        }
      });
    }
  });
  return log;
}

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[character]);
}

function fileURL(file, entry) {
  if (file.change === 'deleted') return `${repository}/commit/${file.ref || entry.commits[0]}`;
  const path = file.path.split('/').map(encodeURIComponent).join('/');
  return `${repository}/blob/${file.ref || 'main'}/${path}`;
}

/** Produce a complete readable journal; client-side filtering is optional. */
export function renderLog(source) {
  const log = validateLog(source);
  const entries = [...log.entries].sort((a, b) => b.date.localeCompare(a.date));
  const days = new Map();
  const counts = { all: entries.length, page: 0, file: 0, feature: 0 };
  for (const entry of entries) {
    if (!days.has(entry.date)) days.set(entry.date, []);
    days.get(entry.date).push(entry);
    counts[entry.type] += 1;
  }

  const lines = [
    `<div class="log-summary">${days.size} 天 · ${entries.length} 条更新</div>`,
    '<div class="log-filters" hidden role="group" aria-label="按更新类型筛选">',
  ];
  for (const [type, label] of Object.entries({ all: '全部', ...types })) {
    lines.push(`  <button type="button" data-log-filter="${type}" aria-pressed="${type === 'all'}" aria-controls="log-days">${label}<span class="filter-count">${counts[type]}</span></button>`);
  }
  lines.push('</div>', `<p class="log-filter-status" role="status" aria-live="polite">共 ${entries.length} 条更新</p>`, '<div id="log-days">');
  if (!entries.length) lines.push('  <p class="log-empty">尚无研究日志。</p>');
  for (const [date, dayEntries] of days) {
    const [year, month, day] = date.split('-').map(Number);
    lines.push(
      '  <section class="log-day" data-log-day>',
      `    <h3><time datetime="${date}">${year}年${month}月${day}日</time></h3>`,
      '    <ol class="log-entries">',
    );
    for (const entry of dayEntries) {
      lines.push(
        `      <li class="log-entry" data-log-type="${entry.type}">`,
        '        <article>',
        `          <span class="log-kind">${types[entry.type]}</span>`,
        `          <h4>${escapeHTML(entry.title)}</h4>`,
        `          <p class="log-description">${escapeHTML(entry.summary)}</p>`,
      );
      if (entry.files?.length) {
        lines.push('          <ul class="log-files">');
        for (const file of entry.files) {
          lines.push(`            <li><span class="file-change">${changes[file.change]}</span><a href="${escapeHTML(fileURL(file, entry))}">${escapeHTML(file.path)}</a></li>`);
        }
        lines.push('          </ul>');
      }
      if (entry.commits?.length) {
        lines.push('          <div class="log-commits">');
        for (const sha of entry.commits) {
          lines.push(`            <a href="${repository}/commit/${sha}">查看提交 ${sha.slice(0, 7)}</a>`);
        }
        lines.push('          </div>');
      }
      lines.push('        </article>', '      </li>');
    }
    lines.push('    </ol>', '  </section>');
  }
  lines.push('</div>');
  return lines.join('\n');
}

/** Replace only the content between a single correctly ordered marker pair. */
export function updateLogSection(html, renderedLog) {
  const start = html.indexOf(startMarker);
  const end = html.indexOf(endMarker);
  if (start < 0 || end < start + startMarker.length
      || html.indexOf(startMarker, start + startMarker.length) !== -1
      || html.indexOf(endMarker, end + endMarker.length) !== -1) {
    throw new Error('site/index.html 必须包含唯一、顺序正确的 RESEARCH_LOG 标记对');
  }
  const lineStart = html.lastIndexOf('\n', start) + 1;
  const prefix = html.slice(lineStart, start);
  const indent = /^[\t ]*$/.test(prefix) ? prefix : '';
  const newline = html.includes('\r\n') ? '\r\n' : '\n';
  const content = renderedLog.split('\n').map(line => `${indent}${line}`).join(newline);
  return `${html.slice(0, start + startMarker.length)}${newline}${content}${newline}${indent}${html.slice(end)}`;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.some(arg => arg !== '--check') || args.length > 1) {
    throw new Error('用法: node scripts/build-research-log.mjs [--check]');
  }
  const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
  const [source, html] = await Promise.all([
    readFile(resolve(root, 'data/research-log.json'), 'utf8'),
    readFile(resolve(root, 'site/index.html'), 'utf8'),
  ]);
  const updated = updateLogSection(html, renderLog(JSON.parse(source)));
  if (args.includes('--check')) {
    if (updated !== html) {
      console.error('研究日志尚未同步。请运行 node scripts/build-research-log.mjs');
      process.exitCode = 1;
    } else {
      console.log('研究日志已同步。');
    }
  } else if (updated !== html) {
    await writeFile(resolve(root, 'site/index.html'), updated, 'utf8');
    console.log('已更新首页研究日志。');
  } else {
    console.log('首页研究日志无需更新。');
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
