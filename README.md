# Markdown Reporter

一个用于以编程方式生成 Markdown 文档的 Python 库。

## 功能特性

- 支持 Markdown 标题（h1-h6），可选自动编号
- 支持段落、超链接、图片、粗体、斜体、引用块
- 支持有序列表、无序列表、任务列表、嵌套列表
- 支持表格和 Pandas DataFrame 转换
- 支持代码块（可去除缩进）
- 支持 Mermaid 图表（饼图、XY 图表）
- 支持上下文管理器
- 文档内容直接输出到终端并可保存为文件

## 安装

```bash
uv pip install markdown-reporter
```

## 快速开始

```python
from markdown_reporter import MarkdownReporter

with MarkdownReporter(use_section_number=True) as reporter:
    reporter.h1("项目报告")

    reporter.h2("简介")
    reporter.p("这是一个示例报告。")
    reporter.hyperlink("访问 Google", "https://google.com")

    reporter.h2("数据展示")
    reporter.table(
        headers=["名称", "分数"],
        rows=[["Alice", 95], ["Bob", 88]]
    )

    reporter.save("report.md")
```

## API 参考

### 标题

```python
reporter.h1("一级标题")
reporter.h2("二级标题")
reporter.h3("三级标题")
reporter.h4("四级标题")
reporter.h5("五级标题")
reporter.h6("六级标题")
```

启用章节编号后，二级到六级标题会自动添加编号（如 `1.1`, `1.2.1`）。

### 文本

```python
reporter.p("普通文本")
reporter.bold("粗体文本")  # 返回 **粗体文本**
reporter.italic("斜体文本")  # 返回 *斜体文本*
reporter.blockquote("引用文本")
reporter.horizontal_rule()  # 分隔线
```

### 链接与图片

```python
reporter.hyperlink("链接文字", "https://example.com")
reporter.image("图片描述", "https://example.com/image.png")
```

### 列表

```python
# 无序列表
reporter.ul(["苹果", "香蕉", "樱桃"])

# 带层级的无序列表
reporter.ul(["主项", "子项"], level=2)

# 有序列表
reporter.ol(["第一步", "第二步", "第三步"])

# 任务列表
reporter.task_list([
    ("已完成任务", True),
    ("未完成任务", False)
])

# 从字典生成嵌套列表
reporter.nested_list_from_dict({
    "水果": ["苹果", "香蕉"],
    "蔬菜": ["胡萝卜"]
})
```

### 表格

```python
# 普通表格
reporter.table(
    headers=["姓名", "年龄"],
    rows=[["张三", 25], ["李四", 30]]
)

# 从 Pandas DataFrame 生成
reporter.table_from_pandas(df, index=False)
```

### 代码块

```python
reporter.code_block("print('Hello')", lang="python", remove_indent=4)
```

### Mermaid 图表

```python
# 饼图
reporter.mermaid("pie", {
    "labels": [["已完成", 60], ["进行中", 30], ["未开始", 10]]
}, title="项目进度")

# 水平 XY 图表
reporter.mermaid("xy-horizontal", {
    "title": "月度销售额",
    "x_labels": ["1月", "2月", "3月"],
    "y_axis": "销售额（万元）",
    "values": [100, 150, 120]
})

# 垂直 XY 图表
reporter.mermaid("xy-vertical", {
    "title": "季度产量",
    "x_labels": ["Q1", "Q2", "Q3", "Q4"],
    "y_axis": "产量（件）",
    "values": [5000, 6000, 5500, 7000]
})
```

### 保存与重置

```python
# 保存到文件
reporter.save("report.md")

# 重置内容
reporter.reset()
```

## 依赖

- Python >= 3.12
- pandas >= 2.0.0

## 许可证

MIT
