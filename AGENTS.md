# 项目协作约定

## 项目定位

项目暂名 Anyone's Intelligence，用于研究并 prototype 新型语言模型。思想来源包括现代语言哲学、语言学与拉康精神分析；“拉康精神分析”已由用户确认。

保留消除幻觉、消除黑箱、提升安全、探索意识、深化艺术文化政治理解与自主创新解题的长期愿景。阶段交付使用可检验假设和证据，不把愿景写成已实现能力。

## 研究与实现

- 先阅读 README.md、docs/RESEARCH_PLAN.md 和 docs/SAFETY.md，再开展相关实现。
- 哲学原义、工程映射与实验证据分别说明。概念命名不算机制实现。
- 最终模型架构保持开放；区分模型本体创新与提示词、检索、外部检查器的工程收益。
- 保留基线、消融、状态干预、未见组合测试和负结果，匹配资料与资源预算。
- 不以流畅解释、模型自述或人格化表达证明内部机制忠实性或意识。
- 文化艺术政治分析区分事实、解释与价值立场，不以认同单一立场作为理解标准。
- 更新公开页面、增加或上传文件、修改功能时，按实际洛杉矶日期维护 `data/research-log.json`，运行 `node scripts/build-research-log.mjs` 同步首页日志；遵循 `docs/RESEARCH_LOG.md` 的记录与发布流程。保留已有历史，只记录实际发生的更新。

## 开发阶段安全

- 模型实验默认离线，不暴露浏览器、Shell、桌面控制或外部工具接口。
- 输入语料只读，输出限专用目录；限制资源与迭代次数，不执行模型生成内容。
- 资料查证和依赖准备与实验运行分开，不向实验进程传递联网和用户凭据访问权限。
- 权限限制必须由运行环境实施；没有测试证据时，不声称已经隔离。
- 新增网络或本地 agent 能力作为独立设计变更处理，不静默启用。

## 用户偏好

所有新配置的邮箱字段默认使用 `lexzeonstudio@gmail.com`，除非用户明确指定其他地址；包括新项目联系邮箱和新的作者／邮箱配置。不迁移已有账户，不改写历史记录。

For newly configured email fields, use `lexzeonstudio@gmail.com` unless the user specifies another address. This does not authorize migration of existing accounts or rewriting historical records.
