# Quick Start - Documentation Guide

## 🎯 Which Document Should I Read?

### I'm an end user who wants to use the trading bot
👉 **Read: [USER_GUIDE.md](USER_GUIDE.md)** or **[User Guide PDF](pdf/AI_Trading_Bot-User_Guide.pdf)**

This guide covers:
- How to set up the bot
- How to use it safely
- Configuration options
- Monitoring your trades
- Troubleshooting

### I'm a developer who wants to understand how it works
👉 **Read: [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)** or **[Technical Architecture PDF](pdf/AI_Trading_Bot-Technical_Architecture.pdf)**

This guide covers:
- System architecture
- How components work together
- Trading algorithm details
- Infrastructure and deployment
- Technical specifications

### I want both!
👉 **Start with the User Guide**, then read the Technical Architecture

---

## 📄 PDF Generation

To generate or regenerate PDF documentation:

```bash
# From the project root directory
make generate-pdf
```

This will create:
- `docs/pdf/AI_Trading_Bot-User_Guide.pdf`
- `docs/pdf/AI_Trading_Bot-Technical_Architecture.pdf`

### Prerequisites

The PDF generation requires:
- Pandoc (document converter)
- XeLaTeX (PDF engine)

**Installation:**

```bash
# Ubuntu/Debian
sudo apt-get install pandoc texlive-xetex

# macOS
brew install pandoc
brew install --cask basictex
```

---

## 📋 Document Overview

| Document | Format | Size | Target Audience | Content |
|----------|--------|------|-----------------|---------|
| User Guide | Markdown | ~16KB | End users, traders | How to use the bot |
| User Guide | PDF | ~86KB | End users, traders | How to use the bot |
| Technical Architecture | Markdown | ~23KB | Developers, admins | How it works |
| Technical Architecture | PDF | ~91KB | Developers, admins | How it works |

---

## 🚀 Quick Tips

### For First-Time Users
1. Read the User Guide introduction
2. Check the prerequisites section
3. Follow the Getting Started steps
4. Start with dry-run mode (no real money)
5. Refer to troubleshooting when needed

### For Developers
1. Skim the User Guide to understand user perspective
2. Study the Technical Architecture thoroughly
3. Review the code with architectural context
4. Refer to both documents when making changes

### For Offline Reading
- Download the PDFs from `docs/pdf/` directory
- PDFs include table of contents for easy navigation
- PDFs have clickable links to sections

---

## 📞 Need Help?

- **User Questions**: Check User Guide → Troubleshooting section
- **Technical Questions**: Check Technical Architecture → Relevant section
- **Still Stuck**: Create an issue on GitHub or check main README for support resources

---

## 🔄 Keeping Updated

When the system is updated:
1. Markdown documentation is updated first
2. Run `make generate-pdf` to regenerate PDFs
3. Both markdown and PDFs stay in sync

---

*Last Updated: 2024*  
*Happy Trading & Happy Coding! 🚀*
