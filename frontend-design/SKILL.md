---
name: frontend-design
description: 前端设计与开发规范
---

# 前端设计规范

## CSS规范

### 类名命名
- 组件：PascalCase (Button, Card)
- 工具类：kebab-case (text-center, mt-4)
- BEM：block__element--modifier

### 常用CSS属性
```css
/* 布局 */
display: flex/grid/block
justify-content: center/space-between
align-items: center

/* 定位 */
position: relative/absolute/fixed
top/right/bottom/left: 0

/* 尺寸 */
width/height: 100% / auto
max-width: 1200px

/* 圆角 */
border-radius: 4px/8px/12px/9999px

/* 阴影 */
box-shadow: 0 2px 8px rgba(0,0,0,0.1)
```

## 设计转代码

### 从设计稿提取
- 颜色：HEX值
- 字体：font-family / font-size / font-weight
- 间距：padding / margin
- 圆角：border-radius

### 响应式适配
```css
/* 移动优先 */
.selector { /* 基础样式 */ }

@media (min-width: 768px) {
  .selector { /* 平板 */ }
}

@media (min-width: 1024px) {
  .selector { /* 桌面 */ }
}
```

## 常见组件

- Button / IconButton
- Input / Textarea / Select
- Card / Modal / Drawer
- Table / List
- Tabs / Collapse
- Loading / Empty
