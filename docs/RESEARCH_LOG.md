# 研究日志维护

首页日志的数据源是 `data/research-log.json`。按 `America/Los_Angeles` 的实际工作日期记录，日期倒序展示，同日条目按文件中的顺序展示，最新更新放在前面。已有历史依据真实 Git 提交回填。

## 追加记录

每次更新公开页面、增加或上传研究文件、修改功能时，在 `entries` 中追加记录。相同日期允许多条；没有进展的日期不创建空记录。

- `id`：唯一且稳定的记录标识。
- `date`：实际发生日期，使用 `YYYY-MM-DD`。
- `type`：`page` 表示页面改动，`file` 表示文件新增、上传、修改或删除，`feature` 表示功能更新。
- `title` 与 `summary`：简短说明发生了什么，不将计划写成已完成成果。
- `files`：相关仓库文件，包含 `path` 和 `change`；`change` 可用 `added`、`uploaded`、`modified`、`deleted`。文件必须先进入仓库；此页面不提供在线上传服务。
- `files[].ref`：可选的完整提交 SHA，用于固定历史文件版本。新变更暂用 `main`；记录后来发生的变更时保留已有的版本链接。删除记录链接对应的提交页面。
- `commits`：可选的完整提交 SHA 数组，提供变更依据。提交记录与网站部署状态分别核验。

日期直接显示，不由访客浏览器转换时区。文件路径和文本在生成时校验、转义；不要在日志中记录凭据、私人材料或尚未公开的文件。

## 生成与发布

在仓库根目录运行：

```powershell
node scripts/build-research-log.mjs
node scripts/build-research-log.mjs --check
node --test tests/research-log.test.mjs
```

生成器更新 `site/index.html` 中的研究日志区域，其余介绍保持不变。无 JavaScript 时日志仍可阅读；浏览器脚本只提供分类筛选。修改样式或筛选脚本时，同步更新首页相应资源的 `v` 参数，避免浏览器继续使用旧缓存。

检查生成结果后，将数据、生成后的首页及其他改动一并提交，再发布：

```powershell
git push origin HEAD:main
git subtree push --prefix=site origin gh-pages
```

等待 GitHub Pages 完成对应提交的构建，并检查公开页面。日志随上述生成与发布流程更新，不会直接监听所有 GitHub 活动。
