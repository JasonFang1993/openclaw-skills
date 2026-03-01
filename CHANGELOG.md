# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- (2026-03-01) weixin-reader: 优化微信文章提取算法，增加 js_content 区域识别，提升长文章提取能力

### Added
- (2026-02-27) Added local skills: notion, obsidian, summarize, tavily-search
- (2026-02-27) Added tech-news-digest
- (2026-02-27) Added Khazix-Skills: github-to-skills, skill-manager, skill-evolution-manager

---

## [v1.7.0] - 2026-02-25

### Added
- Three GitHub Skills management tools (from KKKKhazix/Khazix-Skills)
  - github-to-skills: Convert GitHub repos to AI Skills
  - skill-manager: Manage skill lifecycle
  - skill-evolution-manager: Improve skills based on feedback

### Changed
- README documentation updated with full Chinese instructions

---

## [v1.6.0] - 2026-02-12

### Added
- drawio-diagrams: Generate Draw.io charts from Mermaid/CSV/XML
- vue-auto-tester: Vue 3 auto testing with Vitest + Playwright

---

## [v1.5.0] - 2026-02-09

### Added
- github-search: GitHub repository search

---

## [v1.4.0] - 2026-02-06

### Added
- http-client: HTTP client with config, history, auth

---

## [v1.0.0] - 2026-02-03

### Added
- Initial release with 7 core skills

---

## [v2.0.0] - 2026-02-28

### Added
- link-to-knowledge: 网页链接自动转为知识库（PARA结构）
- pm-toolkit: 去中心化项目管理（多AI协作、代码审查、测试整合）
- cron-tools: 定时任务（每日简报、每周复盘）
- init-all: 一键初始化配置
- x-post-fetch: X(Twitter)帖子抓取

### Features
- 多AI员工协作模式
- 自动代码审查（3个AI）
- 自动测试整合
- 阻塞自动通知
- 一键换电脑恢复
