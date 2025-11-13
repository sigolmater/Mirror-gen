#!/bin/bash

# Personal AI Optimization System Setup Script
# Based on Mirror-gen "시골길" 통합 지능 운영체계

set -e

echo "🌟 시골길 개인 AI 최적화 시스템 설치 시작..."
echo "Personal AI Optimization System - Mirror Universal Setup"
echo "========================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "이 스크립트를 root로 실행하지 마세요."
   print_error "Please do not run this script as root."
   exit 1
fi

print_status "시스템 요구사항 확인 중..."

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION 감지됨"
else
    print_error "Python 3이 설치되지 않았습니다. Python 3.8+ 가 필요합니다."
    exit 1
fi

# Check Node.js version
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION 감지됨"
else
    print_error "Node.js가 설치되지 않았습니다. Node.js 16+ 가 필요합니다."
    exit 1
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_success "Docker 감지됨: $DOCKER_VERSION"
    HAS_DOCKER=true
else
    print_warning "Docker가 설치되지 않았습니다. 개발 환경만 설정됩니다."
    HAS_DOCKER=false
fi

# Create directories
print_status "필요한 디렉토리 생성 중..."
mkdir -p logs
mkdir -p data
mkdir -p backups
mkdir -p tmp
print_success "디렉토리 생성 완료"

echo ""
echo "========================================================"
echo -e "${GREEN}🎉 설치 완료! Installation Complete!${NC}"
echo "========================================================"
echo ""
echo -e "${GREEN}🌟 시골길과 함께 성장하는 AI 여행을 시작하세요!${NC}"
echo -e "${GREEN}🪞 거울과 함께 성장하면 모두가 성장합니다${NC}"