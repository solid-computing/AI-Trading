# AI Trading Bot - Documentation

This directory contains comprehensive documentation for the AI Trading Bot project.

## 📚 Available Documentation

### 📖 User Guide (`USER_GUIDE.md`)
**Target Audience**: End users, traders, beginners

A comprehensive guide for end users covering:
- What is the AI Trading Bot
- Prerequisites and requirements
- Step-by-step setup instructions
- How to use the bot (dry-run and live trading)
- Configuration options
- Monitoring and managing trades
- Troubleshooting common issues
- Safety and best practices

**Perfect for**: Anyone who wants to use the bot without deep technical knowledge.

### 🏗️ Technical Architecture (`TECHNICAL_ARCHITECTURE.md`)
**Target Audience**: Developers, system administrators, technical users

A detailed technical document explaining how the system works behind the scenes:
- System architecture overview
- Component descriptions
- Infrastructure layer (Terraform, OVH Cloud)
- Application layer (Docker, Freqtrade)
- Trading strategy engine and algorithms
- Data flow and decision-making process
- CI/CD deployment pipeline
- Security architecture
- Monitoring and observability
- Technical specifications

**Perfect for**: Developers who want to understand, modify, or extend the system.

## 📄 PDF Versions

Both documents are also available as professionally formatted PDF files in the `pdf/` directory.

### Generating PDFs

To generate or regenerate the PDF documentation:

```bash
# From the project root
make generate-pdf
```

This will create:
- `docs/pdf/AI_Trading_Bot-User_Guide.pdf`
- `docs/pdf/AI_Trading_Bot-Technical_Architecture.pdf`

### Prerequisites for PDF Generation

The PDF generation requires:
- Pandoc (document converter)
- XeLaTeX (PDF engine with Unicode support)

**Installation**:

```bash
# Ubuntu/Debian
sudo apt-get install pandoc texlive-xetex

# macOS
brew install pandoc
brew install --cask basictex
```

## 📋 Quick Reference

### For End Users
1. Read the **User Guide** first
2. Follow the step-by-step setup instructions
3. Start with dry-run mode
4. Refer to troubleshooting section when needed

### For Developers
1. Read the **User Guide** to understand the user perspective
2. Study the **Technical Architecture** for system internals
3. Review the source code with this architectural context
4. Refer to both documents when making changes

## 🔄 Keeping Documentation Updated

When making changes to the system:

1. **Update markdown files** in this directory
2. **Regenerate PDFs** with `make generate-pdf`
3. **Commit both** markdown and updated PDFs (if needed)

## 📦 What's Included

```
docs/
├── README.md                        # This file
├── USER_GUIDE.md                    # End user documentation
├── TECHNICAL_ARCHITECTURE.md        # Technical documentation
└── pdf/                             # Generated PDFs
    ├── AI_Trading_Bot-User_Guide.pdf
    └── AI_Trading_Bot-Technical_Architecture.pdf
```

## 🎯 Documentation Standards

Our documentation follows these principles:

- **Clear and Concise**: Easy to understand for target audience
- **Comprehensive**: Covers all necessary topics
- **Up-to-Date**: Regularly updated with changes
- **Well-Structured**: Logical flow and organization
- **Accessible**: Available in both markdown and PDF formats

## 📝 Contributing to Documentation

When contributing to documentation:

1. Keep the target audience in mind
2. Use clear, simple language
3. Include examples where helpful
4. Update table of contents when adding sections
5. Test all commands and code snippets
6. Regenerate PDFs before committing

## 📞 Support

For questions or improvements to documentation:

- Create an issue on GitHub
- Submit a pull request with improvements
- Refer to the main project README for contact information

---

*Last Updated: 2024*  
*Version: 1.0*
