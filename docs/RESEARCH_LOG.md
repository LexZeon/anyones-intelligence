# 研究日志维护

首页日志的数据源是 `data/research-log.json`。按 `America/Los_Angeles` 的实际工作日期记录，日期倒序展示，同日条目按文件中的顺序展示，最新更新放在前面。已有历史依据真实 Git 提交回填。

网站默认首页 `site/index.html` 使用英文，`site/zh.html` 使用中文。两页展示同一份完整记录，语言切换不删减条目。原有中文记录、ID、日期、文件和提交引用永久保留；翻译作为补充字段维护。

## 追加记录

每次更新公开页面、增加或上传研究文件、修改功能时，在 `entries` 中追加记录。相同日期允许多条；没有进展的日期不创建空记录。

- `id`：唯一且稳定的记录标识。
- `date`：实际发生日期，使用 `YYYY-MM-DD`。
- `type`：`page` 表示页面改动，`file` 表示文件新增、上传、修改或删除，`feature` 表示功能更新。
- `title` 与 `summary`：简短说明发生了什么，不将计划写成已完成成果。
- `title_en` 与 `summary_en`：对应的英文标题与摘要。生成英文首页时，每条记录必须具备这两个非空字段；缺少翻译时生成失败，不能静默跳过条目或替换中文原文。
- `files`：相关仓库文件，包含 `path` 和 `change`；`change` 可用 `added`、`uploaded`、`modified`、`deleted`。文件必须先进入仓库；此页面不提供在线上传服务。
- `files[].ref`：可选的完整提交 SHA，用于固定历史文件版本。新变更暂用 `main`；记录后来发生的变更时保留已有的版本链接。删除记录链接对应的提交页面。
- `commits`：可选的完整提交 SHA 数组，提供变更依据。提交记录与网站部署状态分别核验。

日期直接显示，不由访客浏览器转换时区。文件路径和文本在生成时校验、转义；不要在日志中记录凭据、私人材料或尚未公开的文件。

## 生成与发布

完整研究文档的文字源位于 `docs/research/en.md` 和 `docs/research/zh-CN.md`，图表及可编辑源文件位于 `assets/figures/`。版式和交互分别由 `site/research/research.css` 与 `research.js` 维护，版本与记录时间来自 `version.json`。修改这些内容后，先重建双语研究页和网站图表副本：

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/build-research.py
python scripts/build-research.py --check
```

该构建只在维护文档时运行；公开网站使用静态 HTML、CSS、JavaScript 和图表，不需要访客安装 Python。`--check` 同时验证生成的页面及 `site/assets/` 与源图表是否一致。图表布局的重建方法见 `assets/figures/source/README.md`。

在仓库根目录运行：

```powershell
node scripts/build-research-log.mjs
node scripts/build-research-log.mjs --check
node --test tests/research-log.test.mjs
```

生成器同时更新 `site/index.html` 与 `site/zh.html` 中的研究日志区域，其余介绍保持不变。两页都会先通过数据与标记检查，再写入改动；`--check` 只报告是否同步，不写文件。函数 `renderLog(log)` 保持中文默认，`renderLog(log, 'en')` 生成英文，`renderLog(log, 'zh-CN')` 显式生成中文。

无 JavaScript 时，所有日期和记录仍完整可读；浏览器脚本只提供分类筛选和对应语言的状态提示。修改样式或筛选脚本时，同步更新两页相应资源的 `v` 参数，避免浏览器继续使用旧缓存。研究正文入口分别为 `./research/` 与 `./research/zh.html`。

检查生成结果后，将数据、生成后的首页及其他改动一并提交，再发布：

```powershell
git push origin HEAD:main
git subtree push --prefix=site origin gh-pages
```

等待 GitHub Pages 完成对应提交的构建，并检查公开页面。日志随上述生成与发布流程更新，不会直接监听所有 GitHub 活动。
