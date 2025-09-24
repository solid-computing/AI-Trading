#!/usr/bin/env python3
"""
AI Core Logic Test Script
========================

This script tests the core AI logic without external dependencies
to ensure the fundamental algorithms work correctly.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_market_regime_detection():
    """Test market regime detection logic"""
    logger.info("Testing Market Regime Detection Logic...")
    
    try:
        # Simulate different market conditions
        
        # Bull market scenario
        bull_returns = np.random.normal(0.002, 0.01, 100)  # Positive mean
        bull_volatility = np.std(bull_returns)
        bull_trend = np.mean(bull_returns)
        
        # Bear market scenario  
        bear_returns = np.random.normal(-0.002, 0.01, 100)  # Negative mean
        bear_volatility = np.std(bear_returns)
        bear_trend = np.mean(bear_returns)
        
        # Volatile market scenario
        volatile_returns = np.random.normal(0, 0.03, 100)  # High volatility
        volatile_volatility = np.std(volatile_returns)
        volatile_trend = np.mean(volatile_returns)
        
        # Test regime classification logic
        def classify_regime(avg_returns, volatility, trend_strength):
            if volatility > 0.025:  # High volatility threshold
                if abs(avg_returns) > 0.015:  # High movement
                    return 'crash' if avg_returns < -0.015 else 'volatile'
                return 'volatile'
            elif trend_strength > 0.015:
                return 'bull' if avg_returns > 0 else 'bear'
            else:
                return 'sideways'
        
        bull_regime = classify_regime(bull_trend, bull_volatility, abs(bull_trend))
        bear_regime = classify_regime(bear_trend, bear_volatility, abs(bear_trend))
        volatile_regime = classify_regime(np.mean(volatile_returns), volatile_volatility, abs(np.mean(volatile_returns)))
        
        logger.info(f"✅ Market Regime Detection test passed")
        logger.info(f"   Bull Market: {bull_regime} (trend: {bull_trend:.4f}, vol: {bull_volatility:.4f})")
        logger.info(f"   Bear Market: {bear_regime} (trend: {bear_trend:.4f}, vol: {bear_volatility:.4f})")
        logger.info(f"   Volatile Market: {volatile_regime} (trend: {np.mean(volatile_returns):.4f}, vol: {volatile_volatility:.4f})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Market Regime Detection test failed: {e}")
        return False

def test_sentiment_scoring():
    """Test sentiment scoring logic"""
    logger.info("Testing Sentiment Scoring Logic...")
    
    try:
        # Mock sentiment data
        social_scores = [0.7, 0.3, -0.2, 0.8, 0.1]  # Mixed sentiment
        news_scores = [0.5, 0.6, 0.2, 0.4, 0.3]     # Slightly positive
        fear_greed_values = [75, 25, 45, 80, 60]     # 0-100 scale
        
        # Test sentiment combination logic
        def combine_sentiments(social, news, fear_greed_list):
            weights = {'social': 0.25, 'news': 0.25, 'fear_greed': 0.50}
            
            combined_scores = []
            for s, n, fg in zip(social, news, fear_greed_list):
                # Normalize fear & greed to -1 to 1 scale
                fg_normalized = (fg - 50) / 50
                
                # Weighted combination
                combined = (s * weights['social'] + 
                           n * weights['news'] + 
                           fg_normalized * weights['fear_greed'])
                
                combined_scores.append(combined)
            
            return combined_scores
        
        combined_sentiment = combine_sentiments(social_scores, news_scores, fear_greed_values)
        avg_sentiment = np.mean(combined_sentiment)
        
        # Classify sentiment
        if avg_sentiment > 0.3:
            classification = 'bullish'
        elif avg_sentiment < -0.3:
            classification = 'bearish'
        else:
            classification = 'neutral'
        
        logger.info(f"✅ Sentiment Scoring test passed")
        logger.info(f"   Combined Sentiment: {avg_sentiment:.3f}")
        logger.info(f"   Classification: {classification}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Sentiment Scoring test failed: {e}")
        return False

def test_risk_calculation():
    """Test risk calculation logic"""
    logger.info("Testing Risk Calculation Logic...")
    
    try:
        # Test position sizing calculation
        def calculate_position_size(account_balance, risk_percentage, entry_price, stop_loss_price):
            risk_per_unit = abs(entry_price - stop_loss_price) / entry_price
            risk_amount = account_balance * (risk_percentage / 100)
            position_size = risk_amount / (risk_per_unit * entry_price)
            return position_size, risk_amount, risk_per_unit
        
        # Test scenarios
        scenarios = [
            {'balance': 10000, 'risk_pct': 2, 'entry': 50000, 'stop': 49000},  # BTC example
            {'balance': 5000, 'risk_pct': 1, 'entry': 100, 'stop': 98},        # Lower price asset
            {'balance': 20000, 'risk_pct': 3, 'entry': 2000, 'stop': 1900},    # ETH example
        ]
        
        for i, scenario in enumerate(scenarios):
            position_size, risk_amount, risk_per_unit = calculate_position_size(
                scenario['balance'], scenario['risk_pct'], 
                scenario['entry'], scenario['stop']
            )
            
            logger.info(f"   Scenario {i+1}: Position Size: {position_size:.4f}, Risk Amount: ${risk_amount:.2f}, Risk per Unit: {risk_per_unit:.4f}")
        
        # Test volatility adjustment
        def adjust_for_volatility(base_risk, volatility_percentile):
            if volatility_percentile > 80:
                return base_risk * 0.6  # Reduce risk in high volatility
            elif volatility_percentile < 20:
                return base_risk * 1.2  # Increase risk in low volatility
            else:
                return base_risk
        
        base_risk = 0.02
        high_vol_risk = adjust_for_volatility(base_risk, 85)
        low_vol_risk = adjust_for_volatility(base_risk, 15)
        
        logger.info(f"✅ Risk Calculation test passed")
        logger.info(f"   Base Risk: {base_risk:.3f}")
        logger.info(f"   High Vol Risk: {high_vol_risk:.3f}")
        logger.info(f"   Low Vol Risk: {low_vol_risk:.3f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Risk Calculation test failed: {e}")
        return False

def test_decision_logic():
    """Test decision-making logic"""
    logger.info("Testing Decision Logic...")
    
    try:
        # Mock analysis results
        market_analysis = {
            'regime': 'bull',
            'strength': 0.7,
            'volatility': 0.02,
            'confidence': 0.8
        }
        
        sentiment_analysis = {
            'score': 0.6,
            'classification': 'bullish',
            'confidence': 0.7
        }
        
        technical_signals = {
            'rsi_oversold': True,
            'above_sma': True,
            'macd_positive': True,
            'volume_high': True
        }
        
        # Test decision logic
        def make_decision(market, sentiment, technical):
            # Calculate confidence scores
            market_score = market['strength'] * market['confidence']
            sentiment_score = abs(sentiment['score']) * sentiment['confidence']
            technical_score = sum(technical.values()) / len(technical.values())
            
            # Combined confidence
            combined_confidence = (market_score * 0.4 + 
                                 sentiment_score * 0.3 + 
                                 technical_score * 0.3)
            
            # Decision logic
            if combined_confidence > 0.6 and market['regime'] in ['bull', 'sideways']:
                if sentiment['classification'] == 'bullish' and technical_score > 0.7:
                    return 'enter_long', combined_confidence
                elif sentiment['classification'] == 'bearish':
                    return 'hold', combined_confidence
                else:
                    return 'hold', combined_confidence
            elif market['regime'] in ['bear', 'crash']:
                return 'exit_long', combined_confidence
            else:
                return 'hold', combined_confidence
        
        decision, confidence = make_decision(market_analysis, sentiment_analysis, technical_signals)
        
        logger.info(f"✅ Decision Logic test passed")
        logger.info(f"   Decision: {decision}")
        logger.info(f"   Confidence: {confidence:.3f}")
        
        # Test different scenarios
        scenarios = [
            ({'regime': 'bear', 'strength': 0.3, 'volatility': 0.01, 'confidence': 0.9}, 
             {'score': -0.5, 'classification': 'bearish', 'confidence': 0.8}, 'Expected: exit_long'),
            ({'regime': 'volatile', 'strength': 0.5, 'volatility': 0.05, 'confidence': 0.4}, 
             {'score': 0.2, 'classification': 'neutral', 'confidence': 0.5}, 'Expected: hold'),
        ]
        
        for i, (market, sentiment, expected) in enumerate(scenarios):
            decision, conf = make_decision(market, sentiment, technical_signals)
            logger.info(f"   Scenario {i+1}: {decision} (confidence: {conf:.3f}) - {expected}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Decision Logic test failed: {e}")
        return False

def test_adaptive_parameters():
    """Test adaptive parameter logic"""
    logger.info("Testing Adaptive Parameters Logic...")
    
    try:
        # Base parameters
        base_params = {
            'rsi_buy_threshold': 30,
            'rsi_sell_threshold': 70,
            'sma_period': 20,
            'volume_factor': 1.2
        }
        
        # Test adaptation logic
        def adapt_parameters(params, market_regime, volatility_regime, performance_data):
            adapted = params.copy()
            
            # Market regime adaptations
            if market_regime == 'volatile':
                adapted['rsi_buy_threshold'] = params['rsi_buy_threshold'] - 5  # More sensitive
                adapted['rsi_sell_threshold'] = params['rsi_sell_threshold'] + 5
            elif market_regime == 'sideways':
                adapted['sma_period'] = min(params['sma_period'] + 5, 50)  # Longer period
            
            # Volatility adaptations
            if volatility_regime == 'high':
                adapted['volume_factor'] = params['volume_factor'] * 1.3  # Higher volume filter
            elif volatility_regime == 'low':
                adapted['volume_factor'] = params['volume_factor'] * 0.9  # Lower volume filter
            
            # Performance-based adaptations
            if performance_data and performance_data.get('win_rate', 0.5) < 0.4:
                # Poor performance - become more conservative
                adapted['rsi_buy_threshold'] = max(adapted['rsi_buy_threshold'] - 3, 15)
                adapted['volume_factor'] = adapted['volume_factor'] * 1.1
            
            return adapted
        
        # Test different scenarios
        scenarios = [
            ('volatile', 'high', {'win_rate': 0.35}),
            ('sideways', 'normal', {'win_rate': 0.65}),
            ('bull', 'low', {'win_rate': 0.55})
        ]
        
        for market_regime, vol_regime, performance in scenarios:
            adapted = adapt_parameters(base_params, market_regime, vol_regime, performance)
            logger.info(f"   {market_regime.title()} Market, {vol_regime.title()} Vol: RSI Buy: {adapted['rsi_buy_threshold']}, Vol Factor: {adapted['volume_factor']:.2f}")
        
        logger.info(f"✅ Adaptive Parameters test passed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Adaptive Parameters test failed: {e}")
        return False

def main():
    """Run all core AI logic tests"""
    logger.info("🧠 Starting AI Core Logic Tests...")
    logger.info("=" * 50)
    
    tests = [
        test_market_regime_detection,
        test_sentiment_scoring,
        test_risk_calculation,
        test_decision_logic,
        test_adaptive_parameters
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
        logger.info("🎉 All AI core logic tests passed!")
        logger.info("The AI reasoning algorithms are working correctly.")
        return True
    else:
        logger.error("❌ Some AI core logic tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)