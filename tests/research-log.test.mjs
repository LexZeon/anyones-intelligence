import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderLog, updateLogSection, validateLog } from '../scripts/build-research-log.mjs';

const sha = '1234567890abcdef1234567890abcdef12345678';
const entry = { id: 'first-entry', date: '2026-10-19', type: 'page', title: '首页介绍', summary: '更新项目介绍。' };
const log = entries => ({ version: 1, timezone: 'America/Los_Angeles', entries });

test('rejects impossible dates, duplicate IDs, malformed records and unsafe paths', () => {
  for (const date of ['2026-02-29', '2026-04-31', '2026-13-01', '2026-00-19', '2026-10-00', '2026-1-19', '0000-01-01']) {
    assert.throws(() => validateLog(log([{ ...entry, date }])), /date/);
  }
  assert.doesNotThrow(() => validateLog(log([{ ...entry, date: '2024-02-29' }])));
  assert.throws(() => validateLog(log([entry, { ...entry }])), /ID/);
  assert.throws(() => validateLog({ ...log([entry]), timezone: 'UTC' }), /timezone/);
  assert.throws(() => validateLog(log([{ ...entry, type: 'experiment' }])), /type/);
  assert.throws(() => validateLog(log([{ ...entry, title: '   ' }])), /title/);
  assert.throws(() => validateLog(log([{ ...entry, commits: ['a50451a'] }])), /40/);
  for (const path of ['../secret', '/etc/passwd', 'C:/secret', 'docs\\secret', 'https://example.com/file', 'docs/../secret', 'docs//file', './README.md', 'docs/\u0000file']) {
    assert.throws(() => validateLog(log([{ ...entry, files: [{ path, change: 'added' }] }])), /path/);
  }
});

test('groups newest dates first, preserves same-day source order, and counts each entry once', () => {
  const html = renderLog(log([
    { ...entry, id: 'older', date: '2026-10-18', title: 'OLDER' },
    { ...entry, id: 'first', title: 'FIRST', type: 'feature' },
    { ...entry, id: 'second', title: 'SECOND', type: 'file' },
  ]));
  assert.ok(html.indexOf('FIRST') < html.indexOf('SECOND'));
  assert.ok(html.indexOf('SECOND') < html.indexOf('OLDER'));
  assert.match(html, /2 天 · 3 条更新/);
  assert.equal((html.match(/data-log-day>/g) || []).length, 2);
  assert.match(html, /data-log-filter="file"[^>]*>文件更新<span class="filter-count">1<\/span>/);
  assert.match(html, /class="log-filters" hidden/);
  assert.doesNotMatch(html, /class="log-entry"[^>]* hidden/);
});

test('escapes editable text and encodes file paths without permitting markup', () => {
  const html = renderLog(log([{
    ...entry,
    title: '<script>alert("x")</script>',
    summary: "A & B's <result>",
    files: [{ path: 'docs/研究 & "note".md', change: 'added', ref: sha }],
  }]));
  assert.doesNotMatch(html, /<script>/);
  assert.match(html, /&lt;script&gt;alert\(&quot;x&quot;\)&lt;\/script&gt;/);
  assert.match(html, /A &amp; B&#39;s &lt;result&gt;/);
  assert.match(html, new RegExp(`/blob/${sha}/docs/`));
  assert.match(html, /%E7%A0%94%E7%A9%B6%20%26%20%22note%22\.md/);
});

test('deleted file links identify a commit, and require a commit reference', () => {
  const deleted = { path: 'docs/removed.md', change: 'deleted' };
  assert.throws(() => renderLog(log([{ ...entry, files: [deleted] }])), /删除记录/);
  const html = renderLog(log([{ ...entry, files: [deleted], commits: [sha] }]));
  assert.match(html, new RegExp(`href="https://github.com/LexZeon/anyones-intelligence/commit/${sha}"`));
  assert.doesNotMatch(html, /\/blob\//);
});

test('replaces only the marked section, preserves CRLF and rejects ambiguous markers', () => {
  const prefix = '<main>DO NOT CHANGE\r\n  <!-- RESEARCH_LOG:START -->';
  const suffix = '<!-- RESEARCH_LOG:END -->\r\n</main>';
  const html = `${prefix}\r\n  OLD\r\n  ${suffix}`;
  const updated = updateLogSection(html, '<div>new</div>\n<p>more</p>');
  assert.equal(updated, `${prefix}\r\n  <div>new</div>\r\n  <p>more</p>\r\n  ${suffix}`);
  assert.equal(updateLogSection(updated, '<div>new</div>\n<p>more</p>'), updated);
  for (const malformed of ['', '<!-- RESEARCH_LOG:END --><!-- RESEARCH_LOG:START -->', `${html}<!-- RESEARCH_LOG:START -->`]) {
    assert.throws(() => updateLogSection(malformed, ''), /标记/);
  }
});

test('CLI check reports stale HTML without writing, then passes after generation', () => {
  const temporary = mkdtempSync(join(tmpdir(), 'anyones-research-log-'));
  try {
    for (const folder of ['scripts', 'data', 'site']) mkdirSync(join(temporary, folder));
    const script = join(temporary, 'scripts', 'build-research-log.mjs');
    copyFileSync(resolve(dirname(fileURLToPath(import.meta.url)), '../scripts/build-research-log.mjs'), script);
    writeFileSync(join(temporary, 'data', 'research-log.json'), JSON.stringify(log([entry])));
    const homepage = join(temporary, 'site', 'index.html');
    const initial = '<h1>Keep me</h1>\n<!-- RESEARCH_LOG:START -->\n<!-- RESEARCH_LOG:END -->\n<footer>Keep me too</footer>';
    writeFileSync(homepage, initial);
    const stale = spawnSync(process.execPath, [script, '--check'], { encoding: 'utf8', timeout: 10000 });
    assert.equal(stale.status, 1);
    assert.match(stale.stderr, /尚未同步/);
    assert.equal(readFileSync(homepage, 'utf8'), initial);
    execFileSync(process.execPath, [script], { timeout: 10000 });
    const generated = readFileSync(homepage, 'utf8');
    assert.ok(generated.startsWith('<h1>Keep me</h1>\n'));
    assert.ok(generated.endsWith('\n<footer>Keep me too</footer>'));
    assert.match(execFileSync(process.execPath, [script, '--check'], { encoding: 'utf8', timeout: 10000 }), /已同步/);
    assert.equal(readFileSync(homepage, 'utf8'), generated);
  } finally {
    const resolved = resolve(temporary);
    if (!resolved.startsWith(`${resolve(tmpdir())}${sep}`)) throw new Error('临时测试目录超出预期范围');
    rmSync(resolved, { recursive: true, force: true });
  }
});
