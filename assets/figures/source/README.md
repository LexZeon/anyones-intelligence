# Editable research figures / 可编辑研究图

These nine diagrams organize the author's account of Anyone's Intelligence. They are conceptual diagrams, not experimental results or computed simulations.

九张图均由文字、节点、连线、分层区域等矢量图元构成，不使用生成式图片。图中的坐标、曲线与线宽是排版及概念表达，不是测量数据。页面使用深色主题；插图保留适合阅读与导出的浅色画布。

## Files / 文件

Chinese exports are in `../`; English exports are in `../en/`.

- `.drawio`: uncompressed XML with individually editable text, nodes, lines, and regions. The file contains native diagram elements, not an embedded screenshot.
- `.svg`: scalable vector artwork with native text and geometry.
- `.png`: a 2× raster export for convenient sharing.

`.drawio` 文件可在 draw.io / diagrams.net 中继续编辑；文字与连线均为独立图元。该格式使用 XML 保存图形结构，参见 [draw.io 官方格式说明](https://www.drawio.com/docs/manual/editor/save-file-formats/)。

| Figure | File stem | Subject |
| --- | --- | --- |
| 01 | `01_intellectual_roots` | 学习与思考的来源 / Intellectual roots |
| 02 | `02_research_direction` | 模型模拟的研究方向 / Research direction |
| 03 | `03_chain_to_model` | 参考链与模型目标 / Reference chain and modeling |
| 04 | `04_memory_encoding` | 记忆写入与基色 / Memory encoding and affective tone |
| 05 | `01_single_chain` | 单条认知链 / A single cognitive chain |
| 06 | `02_intersecting_memory_chains` | 共享词／词元与记忆连接 / Shared words, tokens, and memory |
| 07 | `07_foundation_and_history` | 先天基础与经历后的状态 / Foundation and history |
| 08 | `08_transformer_analogy` | 两个 Transformer 类比角度 / Two angles of analogy |
| 09 | `03_state_dependent_participation` | 多条联系共同参与 / State-dependent joint contribution |

The three original filename stems remain stable; figure numbers follow reading order.

## Visual conventions / 视觉约定

- For memory-chain figures, blue solid lines denote sweets/feeding-related paths; orange dashed lines denote mockery/avoidance-related paths. These identify paths, not positive/negative value or excitation/inhibition.
- Filled neutral nodes mark shared connections. A geometric crossing alone does not define a connection.
- In Figure 09, line width indicates qualitative contribution only. Both paths remain present. The common initial segment is neutral and does not encode contribution strength.
- Foundation is distinct from the current physiological state. Register names follow the author's project-specific usage.
- Proposed relations, modeling goals, analogies, and the technical account of attention are labeled separately. No tokenization scheme or final model architecture is established by these diagrams.

## Rebuild / 重建

Use Python with an existing Matplotlib installation and a CJK font:

```text
python assets/figures/source/render_figures.py
```

An existing dependency directory can be supplied without downloading anything:

```text
python assets/figures/source/render_figures.py --dependency-path PATH_TO_EXISTING_PACKAGES
```

On Windows the renderer uses Microsoft YaHei for Chinese. `DIAGRAM_CJK_FONT` and `DIAGRAM_CJK_BOLD_FONT` can specify alternative local font files.

The layout scripts are `render_figures.py`, `render_supporting_overview.py`, and `render_supporting_mechanisms.py`. `diagram_scene.py` exports their shared diagram elements to all three formats. Editing a `.drawio` file changes that copy; export it in the editor to update its SVG/PNG. Running the scripts again rebuilds the diagrams from the Python layouts.
