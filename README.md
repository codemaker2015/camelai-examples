# CamelAI Examples

🐫 CAMEL is an open-source community dedicated to finding the scaling laws of agents. We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks. To facilitate research in this field, we implement and support various types of agents, tasks, prompts, models, and simulated environments.

## What Can You Build With CAMEL?

### 🤖 Customize Agents
- Customizable agents are the fundamental entities of the CAMEL architecture. CAMEL empowers you to customize agents using our modular components for specific tasks.

### ⚙️ Build Multi-Agent Systems
- We propose a multi-agent framework to address agents' autonomous cooperation challenges, guiding agents toward task completion while maintaining human intentions.

### 💻 Practical Applications
- The CAMEL framework serves as a generic infrastructure for a wide range of multi-agent applications, including task automation, data generation, and world simulations.


## Why Should You Use CAMEL?

1. Comprehensive Customization and Collaboration:

    - Integrates over 20 advanced model platforms (e.g., commercial models like OpenAI, open-source models such as Llama3, and self-deployment frameworks like Ollama).

    - Supports extensive external tools (e.g., Search, Twitter, Github, Google Maps, Reddit, Slack utilities).
    - Includes memory and prompt components for deep customization.
    - Facilitates complex multi-agent systems with advanced collaboration features.


2. User-Friendly with Transparent Internal Structure:
    - Designed for transparency and consistency in internal structure.

    - Offers comprehensive [tutorials and detailed docstrings](https://docs.camel-ai.org/) for all functions.
    - Ensures an approachable learning curve for newcomers.

## Installation

### From PyPI

To install the base CAMEL library:
```bash
pip install camel-ai
```

> **Note**: Some features may not work without their required dependencies. Install `camel-ai[all]` to ensure all dependencies are available, or install specific extras based on the features you need.

```bash
pip install 'camel-ai[all]'  # Replace with options below
```

Available extras:
- `all`: Includes all features below
- `model_platforms`: OpenAI, Google, Mistral, Anthropic Claude, Cohere etc.
- `huggingface`: Transformers, Diffusers, Accelerate, Datasets, PyTorch etc.
- `rag`: Sentence Transformers, Qdrant, Milvus, BM25 etc.
- `storage`: Neo4j, Redis, Azure Blob, Google Cloud Storage, AWS S3  etc.
- `web_tools`: DuckDuckGo, Wikipedia, WolframAlpha, Google Maps, Weather API etc.
- `document_tools`: PDF, Word, OpenAPI, BeautifulSoup, Unstructured etc.
- `media_tools`: Image Processing, Audio Processing, YouTube Download, FFmpeg etc.
- `communication_tools`: Slack, Discord, Telegram, GitHub, Reddit, Notion etc.
- `data_tools`: Pandas, TextBlob, DataCommons, OpenBB, Stripe etc.
- `research_tools`: arXiv, Google Scholar etc.
- `dev_tools`: Docker, Jupyter, Tree-sitter, Code Interpreter etc.

Multiple extras can be combined using commas:
```bash
pip install 'camel-ai[rag,web_tools,document_tools]'  # Example: RAG system with web search and document processing
```

# Demo

![demo](outputs/brochure_generator.gif)