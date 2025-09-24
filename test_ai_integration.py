#!/usr/bin/env python3
"""
AI Integration Test Script
=========================

This script tests the AI components to ensure they work correctly
before integrating with FreqTrade.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'user_data'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_data():
    """Create sample OHLCV data for testing"""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='5T')
    
    # Generate realistic price movement
    np.random.seed(42)
    returns = np.random.normal(0, 0.01, 100)
    prices = 100 * np.exp(np.cumsum(returns))
    
    # Create OHLCV data
    data = {
        'date': dates,
        'open': prices,
        'high': prices * (1 + np.abs(np.random.normal(0, 0.005, 100))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.005, 100))),
        'close': prices,
        'volume': np.random.uniform(1000, 10000, 100)
    }
    
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    
    # Add some basic technical indicators
    df['rsi'] = 50 + np.random.normal(0, 15, 100)  # Mock RSI
    df['sma'] = df['close'].rolling(20).mean()
    df['macd'] = np.random.normal(0, 0.1, 100)
    df['macdsignal'] = df['macd'].shift(1)
    
    return df

def test_market_analyzer():
    """Test the Market Analyzer component"""
    logger.info("Testing Market Analyzer...")
    
    try:
        from ai_engine.market_analyzer import MarketAnalyzer
        
        analyzer = MarketAnalyzer()
        sample_data = create_sample_data()
        
        analysis = analyzer.analyze_market_conditions(sample_data, 'BTC/USDT')
        
        assert 'market_regime' in analysis
        assert 'market_strength' in analysis
        assert 'volatility_regime' in analysis
        assert 'confidence_score' in analysis
        
        logger.info(f"✅ Market Analyzer test passed")
        logger.info(f"   Market Regime: {analysis['market_regime']}")
        logger.info(f"   Market Strength: {analysis['market_strength']:.2f}")
        logger.info(f"   Confidence: {analysis['confidence_score']:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Market Analyzer test failed: {e}")
        return False

def test_sentiment_engine():
    """Test the Sentiment Engine component"""
    logger.info("Testing Sentiment Engine...")
    
    try:
        from ai_engine.sentiment_engine import SentimentEngine
        
        engine = SentimentEngine()
        
        analysis = engine.analyze_market_sentiment('BTC/USDT')
        
        assert 'overall_sentiment' in analysis
        assert 'social_sentiment' in analysis
        assert 'news_sentiment' in analysis
        assert 'confidence_score' in analysis
        
        logger.info(f"✅ Sentiment Engine test passed")
        logger.info(f"   Overall Sentiment: {analysis['overall_sentiment']['classification']}")
        logger.info(f"   Confidence: {analysis['confidence_score']:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Sentiment Engine test failed: {e}")
        return False

def test_risk_manager():
    """Test the Risk Manager component"""
    logger.info("Testing Risk Manager...")
    
    try:
        from ai_engine.risk_manager import RiskManager
        
        manager = RiskManager()
        
        # Test position sizing
        position_size = manager.calculate_position_size(
            pair='BTC/USDT',
            entry_price=50000,
            stop_loss=49000,
            account_balance=10000
        )
        
        assert 'position_size' in position_size
        assert 'risk_percentage' in position_size
        assert 'confidence' in position_size
        
        # Test stop loss optimization
        stop_loss = manager.optimize_stop_loss(
            pair='BTC/USDT',
            entry_price=50000,
            direction='long'
        )
        
        assert 'stop_loss_price' in stop_loss
        assert 'confidence' in stop_loss
        
        logger.info(f"✅ Risk Manager test passed")
        logger.info(f"   Position Size: {position_size['position_size']:.2f}")
        logger.info(f"   Risk %: {position_size['risk_percentage']:.2f}%")
        logger.info(f"   Stop Loss: ${stop_loss['stop_loss_price']:.2f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Risk Manager test failed: {e}")
        return False

def test_decision_engine():
    """Test the Decision Engine component"""
    logger.info("Testing Decision Engine...")
    
    try:
        from ai_engine.decision_engine import DecisionEngine
        
        engine = DecisionEngine()
        sample_data = create_sample_data()
        
        metadata = {'pair': 'BTC/USDT'}
        
        decision = engine.make_trading_decision(
            dataframe=sample_data,
            metadata=metadata,
            current_positions=[],
            account_balance=10000
        )
        
        assert 'final_decision' in decision
        assert 'market_analysis' in decision
        assert 'sentiment_analysis' in decision
        assert 'confidence_score' in decision
        
        logger.info(f"✅ Decision Engine test passed")
        logger.info(f"   Decision: {decision['final_decision']['action']}")
        logger.info(f"   Confidence: {decision['confidence_score']:.2f}")
        logger.info(f"   Reasoning: {decision['final_decision']['reasoning']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Decision Engine test failed: {e}")
        return False

def test_ai_strategy():
    """Test the AI Enhanced Strategy"""
    logger.info("Testing AI Enhanced Strategy...")
    
    try:
        from strategies.AIEnhancedRsiMaStrategy import AIEnhancedRsiMaStrategy
        
        # This is a basic import test since full strategy testing requires FreqTrade
        strategy = AIEnhancedRsiMaStrategy()
        
        # Test that the strategy has the expected attributes
        assert hasattr(strategy, 'ai_initialized')
        assert hasattr(strategy, 'decision_engine')
        assert hasattr(strategy, 'adaptive_params')
        
        logger.info(f"✅ AI Enhanced Strategy test passed")
        logger.info(f"   AI Initialized: {strategy.ai_initialized}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ AI Enhanced Strategy test failed: {e}")
        return False

def main():
    """Run all AI component tests"""
    logger.info("🤖 Starting AI Integration Tests...")
    logger.info("=" * 50)
    
    tests = [
        test_market_analyzer,
        test_sentiment_engine,
        test_risk_manager,
        test_decision_engine,
        test_ai_strategy
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        logger.info("-" * 50)
    
    logger.info("=" * 50)
    logger.info(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All AI components are working correctly!")
        return True
    else:
        logger.error("❌ Some AI components have issues")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)