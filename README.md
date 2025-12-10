# AURIX v4.0

<div align="center">

![AURIX Logo](https://img.shields.io/badge/AURIX-v4.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**AUdit Risk Intelligence eXcellence**

*AI-Powered Internal Audit Platform for Indonesian Financial Industry*

[Demo](https://audit-risk-excellence-aurix.streamlit.app/) · [Documentation](#documentation) · [Features](#features) · [Installation](#installation)

</div>

---

## 🎯 Overview

AURIX is a comprehensive RAG-based AI platform specifically designed for Internal Audit in the Indonesian financial industry. Built with McKinsey Consulting and Big 4 firm methodologies, AURIX provides professional-grade audit tools accessible through free LLM providers.

### Key Highlights

- 🤖 **AI-Powered Intelligence** - Leverage LLMs for audit analysis, risk assessment, and procedure generation
- 📊 **Comprehensive Analytics** - Real-time dashboards, KRI monitoring, and trend analysis
- 🔍 **Fraud Detection** - Red flag analysis and case management tools
- 📋 **PTCF Framework** - Professional prompt engineering using Persona-Task-Context-Format
- 📚 **Regulatory Compliance** - Built-in Indonesian financial regulations (OJK, BI)
- 💰 **Free LLM Access** - Integration with Groq, Together AI, Google Gemini, OpenRouter

---

## ✨ Features

### Core Modules

| Module | Description |
|--------|-------------|
| 📊 **Dashboard** | Real-time overview of audit activities and key metrics |
| 📁 **Documents** | Multi-file upload with RAG integration for intelligent search |
| 🎭 **PTCF Builder** | Professional prompt engineering framework |
| ⚖️ **Risk Assessment** | Risk scoring matrix with control evaluation |
| 📋 **Findings Tracker** | Full lifecycle management with 5Cs documentation |
| 🔄 **Continuous Audit** | Real-time monitoring with custom rules and alerting |
| 📈 **KRI Dashboard** | Key Risk Indicators monitoring with threshold alerts |
| 🔍 **Fraud Detection** | Red flag scanner and case management |
| 📚 **Regulations** | Indonesian regulatory compliance tracking |
| 🤖 **AI Chat** | Context-aware conversational assistant |
| 📊 **Analytics** | Comprehensive audit analytics and reporting |

### Technical Features

- 🎨 **Modern UI/UX** - Enterprise-grade interface with dark/light mode
- 🔐 **Security First** - Environment-based credential management
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔄 **Session Persistence** - Data maintained across interactions
- 📤 **Export Options** - CSV, Excel, PDF, and Markdown exports

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git (optional)

### Quick Start

```bash
# Clone repository
git clone https://github.com/mshadianto/aurix.git
cd aurix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app/main.py
```

### Docker Installation

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application
APP_NAME=AURIX
APP_ENV=development
DEBUG=false

# Database (Optional - for visitor analytics)
DATABASE_URL=postgresql://user:pass@host:5432/aurix

# LLM Providers (Choose one or more)
GROQ_API_KEY=your_groq_key
TOGETHER_API_KEY=your_together_key
GOOGLE_API_KEY=your_google_key
OPENROUTER_API_KEY=your_openrouter_key
```

### Free LLM Providers

| Provider | Sign Up | Free Tier |
|----------|---------|-----------|
| **Groq** | [console.groq.com](https://console.groq.com) | Generous free tier |
| **Together AI** | [together.ai](https://together.ai) | $25 free credits |
| **Google AI** | [aistudio.google.com](https://aistudio.google.com) | Free Gemini access |
| **OpenRouter** | [openrouter.ai](https://openrouter.ai) | Free models available |

---

## 📁 Project Structure

```
aurix_v4/
├── app/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── router.py            # Page routing
│   └── constants.py         # Application constants
├── ui/
│   ├── styles/
│   │   └── css_builder.py   # Theme and styling
│   ├── components/
│   │   ├── __init__.py      # Reusable UI components
│   │   └── sidebar.py       # Sidebar navigation
│   └── pages/
│       ├── dashboard.py     # Dashboard page
│       ├── documents.py     # Document management
│       ├── ptcf_builder.py  # PTCF prompt builder
│       ├── risk_assessment.py
│       ├── findings.py
│       ├── continuous_audit.py
│       ├── kri_dashboard.py
│       ├── fraud_detection.py
│       ├── regulatory_compliance.py
│       ├── chat.py
│       ├── analytics.py
│       ├── settings.py
│       ├── help.py
│       └── about.py
├── data/
│   ├── models/              # Data models
│   └── seeds/
│       └── __init__.py      # Seed data (regulations, audit universe)
├── services/
│   ├── visitor_service.py   # Visitor analytics
│   └── audit_service.py     # Audit operations
├── infrastructure/
│   ├── database/            # Database connections
│   ├── llm/                 # LLM provider integrations
│   └── rag/                 # RAG implementation
├── core/
│   ├── audit/               # Audit domain logic
│   ├── analytics/           # Analytics logic
│   ├── fraud/               # Fraud detection logic
│   └── regulatory/          # Regulatory compliance logic
├── utils/
│   ├── logger.py            # Logging utilities
│   └── exceptions.py        # Custom exceptions
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker configuration
├── .env.example            # Environment template
└── README.md               # This file
```

---

## 🎓 Usage Guide

### 1. Setting Up AI Provider

1. Navigate to **Settings → AI Provider**
2. Select your preferred provider
3. Enter your API key
4. Click **Test Connection** to verify

### 2. Uploading Documents

1. Go to **Documents** module
2. Click **Upload Files** or drag and drop
3. Documents are automatically processed for RAG search
4. Use the search function to find relevant content

### 3. Using PTCF Builder

1. Open **PTCF Builder**
2. Select or create a **Persona** (e.g., Internal Audit Manager)
3. Define your **Task** (what you want to accomplish)
4. Add **Context** (audit area, regulations, background)
5. Choose **Format** (report style, checklist, matrix)
6. Generate and execute with AI

### 4. Risk Assessment

1. Go to **Risk Assessment**
2. Select audit category and area
3. Evaluate likelihood and impact
4. Assess control effectiveness
5. Generate risk matrix visualization

### 5. Managing Findings

1. Navigate to **Findings Tracker**
2. Create new findings with 5Cs documentation
3. Track status and due dates
4. Export reports for management

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** - Claude AI for development assistance
- **Streamlit** - For the amazing framework
- **McKinsey & Company** - Audit methodology frameworks
- **Big 4 Firms** - Professional audit standards
- **OJK & Bank Indonesia** - Regulatory frameworks

---

## 📞 Support

- 📧 Email: sopian.hadianto@gmail.com
- 💬 GitHub Issues: [Create Issue](https://github.com/mshadianto/aurix/issues)
- 📖 Documentation: [docs.aurix.id](https://docs.aurix.id)

---

<div align="center">

**Built with ❤️ for Indonesian Internal Auditors**

Copyright © 2024 AURIX Project

</div>
