## Hi, I'm Tim Ren

Full-stack developer focused on **Buddhist digital humanities** and **AI security** — building open-source tools that make ancient texts accessible to modern researchers, and securing LLM applications.

### Projects

- **[FoJin 佛津](https://github.com/xr843/fojin)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/fojin?style=flat-square&color=blue) — The world's encyclopedic Buddhist digital text platform. 500+ sources, 30 languages, full-text reading, AI Q&A, knowledge graph, parallel reader. FastAPI + React + Elasticsearch.

- **[Master-skill](https://github.com/xr843/Master-skill)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/Master-skill?style=flat-square) — Chinese Buddhist master AI skill generator powered by FoJin. 8 pre-built masters across Chan, Tiantai, Huayan, Pure Land, Yogācāra, Mādhyamaka, and cross-tradition. AgentSkills standard.

- **[llm-pgvector](https://github.com/xr843/llm-pgvector)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/llm-pgvector?style=flat-square) — PostgreSQL pgvector storage backend for [LLM](https://llm.datasette.io/). HNSW/IVFFlat indexes for sub-millisecond semantic search at scale. Born from [FoJin](https://fojin.app)'s 678K+ vector production workload.

- **[llm-seclint](https://github.com/xr843/llm-seclint)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/llm-seclint?style=flat-square) — Static security linter for LLM-powered applications. The Bandit for the AI era.

- **[Buddhist AI Translator](https://github.com/xr843/Buddhist-AI-Translator)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/Buddhist-AI-Translator?style=flat-square) — AI translation for Buddhist texts across Sanskrit, Pali, Tibetan, and Classical Chinese.

### Open Source Contributions

<!-- CONTRIBUTIONS:START -->

**Merged**

| Project | Stars | PR | Description |
|---------|-------|----|-------------|
| [Dify](https://github.com/langgenius/dify) | ![](https://img.shields.io/github/stars/langgenius/dify?style=flat-square&label=) | [#34456](https://github.com/langgenius/dify/pull/34456) | fix(security): add tenant_id validation to prevent IDOR |
| [Dify](https://github.com/langgenius/dify) | | [#34379](https://github.com/langgenius/dify/pull/34379) | refactor: migrate service_api and inner_api to sessionmaker pattern |
| [Dify](https://github.com/langgenius/dify) | | [#33769](https://github.com/langgenius/dify/pull/33769) | fix: remove legacy z-index overrides on model config popup |
| [Dify](https://github.com/langgenius/dify) | | [#33767](https://github.com/langgenius/dify/pull/33767) | fix(tests): correct keyword arguments in tool provider test constructors |
| [gstack](https://github.com/garrytan/gstack) | ![](https://img.shields.io/github/stars/garrytan/gstack?style=flat-square&label=) | [#128](https://github.com/garrytan/gstack/pull/128) | fix: eliminate duplicate command sets in chain, improve flush perf |
| [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | ![](https://img.shields.io/github/stars/CherryHQ/cherry-studio?style=flat-square&label=) | [#13892](https://github.com/CherryHQ/cherry-studio/pull/13892) | fix(security): validate URLs in shell.openExternal |
| [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | | [#13893](https://github.com/CherryHQ/cherry-studio/pull/13893) | fix(security): prevent XSS via dangerouslySetInnerHTML |
| [Gradio](https://github.com/gradio-app/gradio) | ![](https://img.shields.io/github/stars/gradio-app/gradio?style=flat-square&label=) | [#13182](https://github.com/gradio-app/gradio/pull/13182) | fix: make example field optional in gradio cc build |
| [Gradio](https://github.com/gradio-app/gradio) | | [#13204](https://github.com/gradio-app/gradio/pull/13204) | fix: preserve special characters in uploaded filenames |
| [Gradio](https://github.com/gradio-app/gradio) | | [#13159](https://github.com/gradio-app/gradio/pull/13159) | fix: add Starlette 1.0 compatibility |
| [LiteLLM](https://github.com/BerriAI/litellm) | ![](https://img.shields.io/github/stars/BerriAI/litellm?style=flat-square&label=) | [#24070](https://github.com/BerriAI/litellm/pull/24070) | fix: thinking blocks dropped when thinking field is null |
| [Haystack](https://github.com/deepset-ai/haystack) | ![](https://img.shields.io/github/stars/deepset-ai/haystack?style=flat-square&label=) | [#10969](https://github.com/deepset-ai/haystack/pull/10969) | docs: add AzureDocumentIntelligenceConverter documentation |
| [SurfSense](https://github.com/MODSetter/SurfSense) | ![](https://img.shields.io/github/stars/MODSetter/SurfSense?style=flat-square&label=) | [#886](https://github.com/MODSetter/SurfSense/pull/886) | fix: use asyncio.to_thread for embedding calls in search endpoints |
| [trailofbits/skills](https://github.com/trailofbits/skills) | ![](https://img.shields.io/github/stars/trailofbits/skills?style=flat-square&label=) | [#130](https://github.com/trailofbits/skills/pull/130) | docs(aflpp): add opinionated environment variables guide |

**In Review**

| Project | Stars | PR | Description |
|---------|-------|----|-------------|
| [Dify](https://github.com/langgenius/dify) | ![](https://img.shields.io/github/stars/langgenius/dify?style=flat-square&label=) | [#35267](https://github.com/langgenius/dify/pull/35267) | test(types): replace Account/Tenant status string literals with enum values |
| [Dify](https://github.com/langgenius/dify) | | [#34560](https://github.com/langgenius/dify/pull/34560) | fix(types): widen ToolProviderApiEntity icon to include EmojiIconDict |
| [Dify](https://github.com/langgenius/dify) | | [#34381](https://github.com/langgenius/dify/pull/34381) | refactor: migrate core, models and tasks to sessionmaker pattern |
| [Dify](https://github.com/langgenius/dify) | | [#33986](https://github.com/langgenius/dify/pull/33986) | fix: constant-time API key comparison + prevent IDOR |
| [SurfSense](https://github.com/MODSetter/SurfSense) | ![](https://img.shields.io/github/stars/MODSetter/SurfSense?style=flat-square&label=) | [#1229](https://github.com/MODSetter/SurfSense/pull/1229) | fix(web): drop react-dom/server from inline-mention-editor bundle |
| [SurfSense](https://github.com/MODSetter/SurfSense) | | [#1230](https://github.com/MODSetter/SurfSense/pull/1230) | fix(web): memoize Zero provider opts to prevent reconnect churn |
| [SurfSense](https://github.com/MODSetter/SurfSense) | | [#1231](https://github.com/MODSetter/SurfSense/pull/1231) | refactor(web): extract citation TYPE_ICONS into a shared module |
| [SurfSense](https://github.com/MODSetter/SurfSense) | | [#1232](https://github.com/MODSetter/SurfSense/pull/1232) | fix(web): clear announcement stagger timers on unmount |
| [crewAI](https://github.com/crewAIInc/crewAI) | ![](https://img.shields.io/github/stars/crewAIInc/crewAI?style=flat-square&label=) | [#5307](https://github.com/crewAIInc/crewAI/pull/5307) | fix(security): replace eval() with safe AST evaluator in calculator template |
| [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | ![](https://img.shields.io/github/stars/CherryHQ/cherry-studio?style=flat-square&label=) | [#14083](https://github.com/CherryHQ/cherry-studio/pull/14083) | fix: clean up OAuth tokens when deleting MCP server |
<!-- CONTRIBUTIONS:END -->

### Tech

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/-React-61DAFB?style=flat-square&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/-Elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

### Get in touch

If you're interested in Buddhist studies, digital humanities, or NLP for historical texts — open an issue or start a discussion on any of my repos.
