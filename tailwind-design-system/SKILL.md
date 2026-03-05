---
name: tailwind-design-system
description: Tailwind CSS设计系统
---

# Tailwind CSS设计系统

## 常用配置

### 1. 颜色
```js
// tailwind.config.js
colors: {
  primary: {
    50: '#eff6ff',
    500: '#3b82f6',
    900: '#1e3a8a',
  }
}
```

### 2. 间距
```js
spacing: {
  '18': '4.5rem',
  '88': '22rem',
}
```

### 3. 字体
```js
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
}
```

## 常用类

### 布局
- flex / grid
- flex-col / flex-row
- justify-center / between / around
- items-center / start / end
- gap-4 / gap-x-4 / gap-y-4

### 尺寸
- w-full / w-auto / w-1/2
- h-screen / h-full
- max-w-screen-md

### 间距
- p-4 / px-4 / py-4
- m-4 / mx-auto
- space-y-4

### 响应式
- md:flex / lg:w-1/2
- sm:hidden / md:block

### 状态
- hover:bg-blue-500
- focus:ring
- active:scale-95
- disabled:opacity-50

## 组件示例

### 按钮
```html
<button class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-300">
  Button
</button>
```

### 输入框
```html
<input class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
```

### 卡片
```html
<div class="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
  Card Content
</div>
```
