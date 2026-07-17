# 单 HTML 编辑与投递

只维护一份 HTML。它同时承担浏览器编辑、打印 PDF 和预览导出的职责；不要再生成 `-editable.html`。

## 实现方式

- 结构化源文件仍是内容事实源，HTML 是排版与轻量微调入口。
- 在同一 HTML 中加入 `contenteditable` 和编辑工具条。
- 使用 `@media print` 隐藏工具条、编辑轮廓和屏幕背景。
- 标题和文件名保持投递名称，不追加“可编辑版”字样。
- 重要内容变更必须同步回结构化源文件，再重新构建产物。

```css
.edit-toolbar {
  position: fixed;
  inset: 12px 12px auto auto;
  z-index: 999;
}

@media print {
  .edit-toolbar { display: none !important; }
  [contenteditable="true"] { outline: none !important; }
}
```

工具条至少提供打印和锁定编辑两个动作。刷新页面可能丢失直接编辑的内容，因此不要把浏览器编辑结果当作新的事实源。
