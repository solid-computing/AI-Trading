"""
AI Engine for Enhanced FreqTrade Trading
=====================================

This module provides AI-powered enhancements for FreqTrade including:
- Market sentiment analysis
- Risk appetite management
- Dynamic strategy optimization
- Real-time decision making
"""

__version__ = "1.0.0"
__author__ = "AI Trading Team"

from .market_analyzer import MarketAnalyzer
from .sentiment_engine import SentimentEngine
from .risk_manager import RiskManager
from .decision_engine import DecisionEngine

__all__ = [
    'MarketAnalyzer',
    'SentimentEngine', 
    'RiskManager',
    'DecisionEngine'
]