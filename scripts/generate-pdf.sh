#!/bin/bash

# PDF Generation Script for AI Trading Bot Documentation
# This script converts markdown documentation to professional PDF files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directory setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"
OUTPUT_DIR="$PROJECT_ROOT/docs/pdf"

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if pandoc is installed
check_pandoc() {
    if ! command -v pandoc &> /dev/null; then
        log_error "Pandoc is not installed!"
        echo "Please install pandoc:"
        echo "  Ubuntu/Debian: sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra"
        echo "  macOS: brew install pandoc basictex"
        exit 1
    fi
    log_success "Pandoc found: $(pandoc --version | head -n1)"
}

# Create output directory
create_output_dir() {
    mkdir -p "$OUTPUT_DIR"
    log_info "Output directory: $OUTPUT_DIR"
}

# Generate PDF from markdown
generate_pdf() {
    local input_file=$1
    local output_file=$2
    local title=$3
    
    log_info "Generating PDF: $output_file"
    
    pandoc "$input_file" \
        -o "$output_file" \
        --pdf-engine=xelatex \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --variable documentclass=article \
        --variable colorlinks=true \
        --variable linkcolor=blue \
        --variable urlcolor=blue \
        --variable toccolor=blue \
        --toc \
        --toc-depth=3 \
        --number-sections \
        --highlight-style=tango \
        --metadata title="$title" \
        --metadata author="AI Trading Bot Project" \
        --metadata date="$(date +%Y-%m-%d)" \
        -V geometry:a4paper \
        2>&1 | grep -E "(Error|Failed)" || true
    
    if [ -f "$output_file" ]; then
        local size=$(du -h "$output_file" | cut -f1)
        log_success "Created: $output_file ($size)"
    else
        log_error "Failed to create: $output_file"
        return 1
    fi
}

# Main function
main() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  AI Trading Bot - PDF Documentation Generator  "
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Check prerequisites
    check_pandoc
    create_output_dir
    
    echo ""
    log_info "Starting PDF generation..."
    echo ""
    
    # Generate User Guide PDF
    if [ -f "$DOCS_DIR/USER_GUIDE.md" ]; then
        generate_pdf \
            "$DOCS_DIR/USER_GUIDE.md" \
            "$OUTPUT_DIR/AI_Trading_Bot-User_Guide.pdf" \
            "AI Trading Bot - User Guide"
    else
        log_error "USER_GUIDE.md not found"
    fi
    
    # Generate Technical Architecture PDF
    if [ -f "$DOCS_DIR/TECHNICAL_ARCHITECTURE.md" ]; then
        generate_pdf \
            "$DOCS_DIR/TECHNICAL_ARCHITECTURE.md" \
            "$OUTPUT_DIR/AI_Trading_Bot-Technical_Architecture.pdf" \
            "AI Trading Bot - Technical Architecture"
    else
        log_error "TECHNICAL_ARCHITECTURE.md not found"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_success "PDF Generation Complete!"
    echo ""
    log_info "Generated PDFs:"
    ls -lh "$OUTPUT_DIR"/*.pdf 2>/dev/null || log_error "No PDFs generated"
    echo ""
    log_info "Location: $OUTPUT_DIR"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Run main function
main
