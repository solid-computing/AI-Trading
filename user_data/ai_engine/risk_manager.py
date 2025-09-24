"""
Risk Manager - AI-powered risk management and position sizing
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class RiskAppetite(Enum):
    """Risk appetite levels"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    DYNAMIC = "dynamic"  # AI-adjusted based on market conditions


class RiskManager:
    """
    AI-powered risk management system that:
    - Dynamically adjusts position sizes based on market conditions
    - Manages portfolio risk across multiple positions
    - Optimizes stop-loss and take-profit levels
    - Adapts to user's risk appetite
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.risk_appetite = RiskAppetite(self.config.get('risk_appetite', 'moderate'))
        self.max_portfolio_risk = self.config.get('max_portfolio_risk', 0.05)  # 5% max portfolio risk
        self.max_position_risk = self.config.get('max_position_risk', 0.02)  # 2% max per position
        self.volatility_adjustment = self.config.get('volatility_adjustment', True)
        self.correlation_adjustment = self.config.get('correlation_adjustment', True)
        
        # Risk history for adaptive learning
        self.risk_history = []
        self.performance_history = []
        
    def calculate_position_size(self, pair: str, entry_price: float, 
                              stop_loss: float, account_balance: float,
                              market_analysis: Dict = None, 
                              sentiment_analysis: Dict = None) -> Dict:
        """
        Calculate optimal position size based on risk management rules
        
        Args:
            pair: Trading pair
            entry_price: Planned entry price
            stop_loss: Stop loss price
            account_balance: Current account balance
            market_analysis: Market condition analysis
            sentiment_analysis: Sentiment analysis results
            
        Returns:
            Dict with position sizing recommendations
        """
        try:
            # Base risk calculation
            base_risk = self._calculate_base_risk(entry_price, stop_loss)
            
            # Market condition adjustments
            market_multiplier = self._get_market_risk_multiplier(market_analysis)
            
            # Sentiment adjustments
            sentiment_multiplier = self._get_sentiment_risk_multiplier(sentiment_analysis)
            
            # Volatility adjustments
            volatility_multiplier = self._get_volatility_multiplier(market_analysis)
            
            # Portfolio correlation adjustments
            correlation_multiplier = self._get_correlation_multiplier(pair)
            
            # Risk appetite adjustments
            appetite_multiplier = self._get_risk_appetite_multiplier()
            
            # Calculate adjusted risk per trade
            adjusted_risk = min(
                self.max_position_risk * market_multiplier * sentiment_multiplier * 
                volatility_multiplier * correlation_multiplier * appetite_multiplier,
                self.max_position_risk * 2  # Never exceed 2x max position risk
            )
            
            # Calculate position size
            risk_amount = account_balance * adjusted_risk
            position_size = risk_amount / base_risk if base_risk > 0 else 0
            
            # Additional safety checks
            position_size = self._apply_safety_limits(position_size, account_balance, entry_price)
            
            return {
                'position_size': position_size,
                'risk_amount': risk_amount,
                'risk_percentage': adjusted_risk * 100,
                'base_risk': base_risk,
                'multipliers': {
                    'market': market_multiplier,
                    'sentiment': sentiment_multiplier,
                    'volatility': volatility_multiplier,
                    'correlation': correlation_multiplier,
                    'appetite': appetite_multiplier
                },
                'safety_applied': position_size != risk_amount / base_risk if base_risk > 0 else False,
                'confidence': self._calculate_sizing_confidence(market_analysis, sentiment_analysis),
                'recommendations': self._generate_sizing_recommendations(
                    adjusted_risk, market_analysis, sentiment_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Position sizing calculation error: {e}")
            return self._get_default_position_size(account_balance)
    
    def optimize_stop_loss(self, pair: str, entry_price: float, 
                          direction: str, market_analysis: Dict = None,
                          volatility_data: Dict = None) -> Dict:
        """
        AI-optimized stop loss calculation
        
        Args:
            pair: Trading pair
            entry_price: Entry price
            direction: 'long' or 'short'
            market_analysis: Market condition analysis
            volatility_data: Volatility analysis
            
        Returns:
            Dict with stop loss recommendations
        """
        try:
            # Base stop loss (traditional approach)
            base_stop_loss = self._calculate_base_stop_loss(entry_price, direction)
            
            # Volatility-adjusted stop loss
            volatility_stop_loss = self._calculate_volatility_stop_loss(
                entry_price, direction, volatility_data
            )
            
            # Support/resistance-based stop loss
            technical_stop_loss = self._calculate_technical_stop_loss(
                entry_price, direction, market_analysis
            )
            
            # Market regime-adjusted stop loss
            regime_stop_loss = self._calculate_regime_stop_loss(
                entry_price, direction, market_analysis
            )
            
            # Choose optimal stop loss
            optimal_stop_loss = self._select_optimal_stop_loss([
                base_stop_loss, volatility_stop_loss, technical_stop_loss, regime_stop_loss
            ], entry_price, direction)
            
            # Calculate risk-reward ratio
            risk_distance = abs(entry_price - optimal_stop_loss) / entry_price
            
            return {
                'stop_loss_price': optimal_stop_loss,
                'risk_distance': risk_distance,
                'risk_percentage': risk_distance * 100,
                'method_used': self._determine_stop_loss_method(
                    [base_stop_loss, volatility_stop_loss, technical_stop_loss, regime_stop_loss],
                    optimal_stop_loss
                ),
                'alternative_levels': {
                    'base': base_stop_loss,
                    'volatility': volatility_stop_loss,
                    'technical': technical_stop_loss,
                    'regime': regime_stop_loss
                },
                'confidence': self._calculate_stop_loss_confidence(market_analysis),
                'recommendations': self._generate_stop_loss_recommendations(
                    optimal_stop_loss, entry_price, market_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Stop loss optimization error: {e}")
            return self._get_default_stop_loss(entry_price, direction)
    
    def optimize_take_profit(self, pair: str, entry_price: float, 
                           stop_loss: float, direction: str,
                           market_analysis: Dict = None,
                           sentiment_analysis: Dict = None) -> Dict:
        """
        AI-optimized take profit calculation
        
        Args:
            pair: Trading pair
            entry_price: Entry price
            stop_loss: Stop loss price
            direction: 'long' or 'short'
            market_analysis: Market condition analysis
            sentiment_analysis: Sentiment analysis
            
        Returns:
            Dict with take profit recommendations
        """
        try:
            # Calculate risk distance
            risk_distance = abs(entry_price - stop_loss)
            
            # Base risk-reward ratios
            base_ratios = self._get_base_risk_reward_ratios()
            
            # Market condition adjustments
            market_adjustment = self._get_market_reward_adjustment(market_analysis)
            
            # Sentiment adjustments
            sentiment_adjustment = self._get_sentiment_reward_adjustment(sentiment_analysis)
            
            # Calculate multiple take profit levels
            take_profit_levels = []
            for i, ratio in enumerate(base_ratios):
                adjusted_ratio = ratio * market_adjustment * sentiment_adjustment
                
                if direction == 'long':
                    tp_price = entry_price + (risk_distance * adjusted_ratio)
                else:
                    tp_price = entry_price - (risk_distance * adjusted_ratio)
                
                take_profit_levels.append({
                    'level': i + 1,
                    'price': tp_price,
                    'ratio': adjusted_ratio,
                    'percentage': (abs(tp_price - entry_price) / entry_price) * 100
                })
            
            # Primary take profit (first level)
            primary_tp = take_profit_levels[0] if take_profit_levels else None
            
            return {
                'primary_take_profit': primary_tp['price'] if primary_tp else entry_price * 1.02,
                'take_profit_levels': take_profit_levels,
                'risk_reward_ratio': primary_tp['ratio'] if primary_tp else 2.0,
                'scaling_strategy': self._recommend_scaling_strategy(market_analysis, sentiment_analysis),
                'confidence': self._calculate_take_profit_confidence(market_analysis, sentiment_analysis),
                'recommendations': self._generate_take_profit_recommendations(
                    take_profit_levels, market_analysis, sentiment_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Take profit optimization error: {e}")
            return self._get_default_take_profit(entry_price, stop_loss, direction)
    
    def assess_portfolio_risk(self, current_positions: List[Dict],
                            new_position: Dict = None) -> Dict:
        """
        Assess overall portfolio risk and correlations
        
        Args:
            current_positions: List of current position data
            new_position: Optional new position to assess
            
        Returns:
            Dict with portfolio risk assessment
        """
        try:
            if not current_positions:
                return {
                    'total_risk': 0.0,
                    'risk_percentage': 0.0,
                    'correlation_risk': 0.0,
                    'diversification_score': 1.0,
                    'max_drawdown_estimate': 0.0,
                    'recommendations': ['Portfolio is empty - safe to start trading']
                }
            
            # Calculate current portfolio risk
            total_risk = sum(pos.get('risk_amount', 0) for pos in current_positions)
            total_value = sum(pos.get('position_value', 0) for pos in current_positions)
            risk_percentage = (total_risk / total_value) * 100 if total_value > 0 else 0
            
            # Assess correlations between positions
            correlation_risk = self._calculate_correlation_risk(current_positions)
            
            # Calculate diversification score
            diversification_score = self._calculate_diversification_score(current_positions)
            
            # Simulate potential maximum drawdown
            max_drawdown_estimate = self._estimate_max_drawdown(current_positions)
            
            # Assess impact of new position
            impact_analysis = None
            if new_position:
                impact_analysis = self._assess_new_position_impact(current_positions, new_position)
            
            # Generate risk warnings
            warnings = self._generate_risk_warnings(
                risk_percentage, correlation_risk, diversification_score
            )
            
            return {
                'total_risk': total_risk,
                'risk_percentage': risk_percentage,
                'correlation_risk': correlation_risk,
                'diversification_score': diversification_score,
                'max_drawdown_estimate': max_drawdown_estimate,
                'new_position_impact': impact_analysis,
                'warnings': warnings,
                'recommendations': self._generate_portfolio_recommendations(
                    risk_percentage, correlation_risk, diversification_score
                )
            }
            
        except Exception as e:
            logger.error(f"Portfolio risk assessment error: {e}")
            return self._get_default_portfolio_risk()
    
    # Helper methods
    def _calculate_base_risk(self, entry_price: float, stop_loss: float) -> float:
        """Calculate base risk per unit"""
        return abs(entry_price - stop_loss) / entry_price
    
    def _get_market_risk_multiplier(self, market_analysis: Dict) -> float:
        """Get risk multiplier based on market conditions"""
        if not market_analysis:
            return 1.0
        
        regime = market_analysis.get('market_regime', 'sideways')
        volatility = market_analysis.get('volatility_regime', {})
        anomaly_score = market_analysis.get('anomaly_score', 0)
        
        multiplier = 1.0
        
        # Market regime adjustments
        if regime == 'crash':
            multiplier *= 0.3  # Drastically reduce position size
        elif regime == 'volatile':
            multiplier *= 0.6  # Reduce position size
        elif regime == 'bear':
            multiplier *= 0.8  # Slightly reduce
        elif regime == 'bull':
            multiplier *= 1.2  # Slightly increase
        
        # Volatility adjustments
        vol_regime = volatility.get('regime', 'normal')
        if vol_regime == 'high':
            multiplier *= 0.7
        elif vol_regime == 'low':
            multiplier *= 1.1
        
        # Anomaly adjustments
        if anomaly_score > 0.7:
            multiplier *= 0.5  # High anomaly = reduce risk
        
        return max(0.1, min(2.0, multiplier))
    
    def _get_sentiment_risk_multiplier(self, sentiment_analysis: Dict) -> float:
        """Get risk multiplier based on sentiment"""
        if not sentiment_analysis:
            return 1.0
        
        overall_sentiment = sentiment_analysis.get('overall_sentiment', {})
        confidence = sentiment_analysis.get('confidence_score', 0.5)
        
        sentiment_score = overall_sentiment.get('normalized_score', 0.5)
        
        # Adjust based on sentiment strength and confidence
        if confidence > 0.7:
            if sentiment_score > 0.7:  # Very bullish
                return 1.2
            elif sentiment_score < 0.3:  # Very bearish
                return 0.8
        
        return 1.0
    
    def _get_volatility_multiplier(self, market_analysis: Dict) -> float:
        """Get multiplier based on volatility analysis"""
        if not market_analysis:
            return 1.0
        
        volatility = market_analysis.get('volatility_regime', {})
        percentile = volatility.get('percentile', 50)
        
        # Reduce position size in high volatility
        if percentile > 80:
            return 0.6
        elif percentile > 60:
            return 0.8
        elif percentile < 20:
            return 1.2
        else:
            return 1.0
    
    def _get_correlation_multiplier(self, pair: str) -> float:
        """Get multiplier based on portfolio correlations"""
        # Simplified correlation check
        # In production, this would analyze actual correlations
        return 1.0
    
    def _get_risk_appetite_multiplier(self) -> float:
        """Get multiplier based on risk appetite"""
        if self.risk_appetite == RiskAppetite.CONSERVATIVE:
            return 0.7
        elif self.risk_appetite == RiskAppetite.MODERATE:
            return 1.0
        elif self.risk_appetite == RiskAppetite.AGGRESSIVE:
            return 1.4
        elif self.risk_appetite == RiskAppetite.DYNAMIC:
            # AI-adjusted based on recent performance
            return self._calculate_dynamic_risk_appetite()
        else:
            return 1.0
    
    def _calculate_dynamic_risk_appetite(self) -> float:
        """Calculate dynamic risk appetite based on recent performance"""
        if not self.performance_history:
            return 1.0
        
        # Analyze recent performance and adjust risk appetite
        recent_performance = self.performance_history[-10:]  # Last 10 trades
        win_rate = sum(1 for p in recent_performance if p > 0) / len(recent_performance)
        
        if win_rate > 0.7:
            return 1.2  # Increase risk after good performance
        elif win_rate < 0.3:
            return 0.8  # Decrease risk after poor performance
        else:
            return 1.0
    
    def _apply_safety_limits(self, position_size: float, account_balance: float, entry_price: float) -> float:
        """Apply safety limits to position size"""
        # Maximum position size (e.g., 50% of account)
        max_position_value = account_balance * 0.5
        max_position_size = max_position_value / entry_price
        
        # Minimum position size (e.g., $10 equivalent)
        min_position_value = 10
        min_position_size = min_position_value / entry_price
        
        return max(min_position_size, min(position_size, max_position_size))
    
    def _calculate_base_stop_loss(self, entry_price: float, direction: str) -> float:
        """Calculate base stop loss (simple percentage)"""
        stop_loss_percentage = 0.02  # 2% stop loss
        
        if direction == 'long':
            return entry_price * (1 - stop_loss_percentage)
        else:
            return entry_price * (1 + stop_loss_percentage)
    
    def _calculate_volatility_stop_loss(self, entry_price: float, direction: str, volatility_data: Dict) -> float:
        """Calculate volatility-based stop loss"""
        if not volatility_data:
            return self._calculate_base_stop_loss(entry_price, direction)
        
        # Use volatility to set dynamic stop loss
        current_vol = volatility_data.get('current_vol', 0.02)
        volatility_multiplier = max(1.0, min(3.0, current_vol / 0.02))  # Scale based on normal volatility
        
        stop_loss_percentage = 0.02 * volatility_multiplier
        
        if direction == 'long':
            return entry_price * (1 - stop_loss_percentage)
        else:
            return entry_price * (1 + stop_loss_percentage)
    
    def _calculate_technical_stop_loss(self, entry_price: float, direction: str, market_analysis: Dict) -> float:
        """Calculate technical analysis-based stop loss"""
        # Simplified technical stop loss
        # In production, this would use support/resistance levels
        return self._calculate_base_stop_loss(entry_price, direction)
    
    def _calculate_regime_stop_loss(self, entry_price: float, direction: str, market_analysis: Dict) -> float:
        """Calculate market regime-adjusted stop loss"""
        if not market_analysis:
            return self._calculate_base_stop_loss(entry_price, direction)
        
        regime = market_analysis.get('market_regime', 'sideways')
        base_percentage = 0.02
        
        # Adjust stop loss based on market regime
        if regime == 'volatile':
            base_percentage = 0.035  # Wider stops in volatile markets
        elif regime == 'crash':
            base_percentage = 0.015  # Tighter stops in crash conditions
        elif regime == 'bull':
            base_percentage = 0.025  # Slightly wider in bull markets
        
        if direction == 'long':
            return entry_price * (1 - base_percentage)
        else:
            return entry_price * (1 + base_percentage)
    
    def _select_optimal_stop_loss(self, stop_losses: List[float], entry_price: float, direction: str) -> float:
        """Select the optimal stop loss from multiple calculations"""
        valid_stops = [sl for sl in stop_losses if sl is not None and sl > 0]
        
        if not valid_stops:
            return self._calculate_base_stop_loss(entry_price, direction)
        
        # Use median as optimal (balances different approaches)
        return np.median(valid_stops)
    
    def _get_base_risk_reward_ratios(self) -> List[float]:
        """Get base risk-reward ratios for take profit levels"""
        return [2.0, 3.0, 4.0]  # 1:2, 1:3, 1:4 ratios
    
    def _get_market_reward_adjustment(self, market_analysis: Dict) -> float:
        """Adjust reward targets based on market conditions"""
        if not market_analysis:
            return 1.0
        
        regime = market_analysis.get('market_regime', 'sideways')
        strength = market_analysis.get('market_strength', 0.5)
        
        # Adjust targets based on market regime
        if regime == 'bull' and strength > 0.7:
            return 1.3  # Higher targets in strong bull markets
        elif regime == 'bear':
            return 0.8  # Lower targets in bear markets
        elif regime == 'volatile':
            return 0.9  # Conservative targets in volatile markets
        
        return 1.0
    
    def _get_sentiment_reward_adjustment(self, sentiment_analysis: Dict) -> float:
        """Adjust reward targets based on sentiment"""
        if not sentiment_analysis:
            return 1.0
        
        overall_sentiment = sentiment_analysis.get('overall_sentiment', {})
        confidence = sentiment_analysis.get('confidence_score', 0.5)
        sentiment_score = overall_sentiment.get('normalized_score', 0.5)
        
        # Adjust based on sentiment strength
        if confidence > 0.7:
            if sentiment_score > 0.7:
                return 1.2  # Higher targets with strong bullish sentiment
            elif sentiment_score < 0.3:
                return 0.8  # Lower targets with strong bearish sentiment
        
        return 1.0
    
    # Default/fallback methods
    def _get_default_position_size(self, account_balance: float) -> Dict:
        """Default position sizing when calculations fail"""
        default_risk = 0.01  # 1% risk
        return {
            'position_size': account_balance * default_risk / 100,  # Simplified
            'risk_amount': account_balance * default_risk,
            'risk_percentage': default_risk * 100,
            'base_risk': default_risk,
            'multipliers': {'market': 1.0, 'sentiment': 1.0, 'volatility': 1.0, 'correlation': 1.0, 'appetite': 1.0},
            'safety_applied': True,
            'confidence': 0.3,
            'recommendations': ['Using default conservative position sizing due to calculation error']
        }
    
    def _get_default_stop_loss(self, entry_price: float, direction: str) -> Dict:
        """Default stop loss when calculations fail"""
        stop_loss = self._calculate_base_stop_loss(entry_price, direction)
        return {
            'stop_loss_price': stop_loss,
            'risk_distance': 0.02,
            'risk_percentage': 2.0,
            'method_used': 'default',
            'alternative_levels': {'base': stop_loss, 'volatility': stop_loss, 'technical': stop_loss, 'regime': stop_loss},
            'confidence': 0.3,
            'recommendations': ['Using default 2% stop loss due to calculation error']
        }
    
    def _get_default_take_profit(self, entry_price: float, stop_loss: float, direction: str) -> Dict:
        """Default take profit when calculations fail"""
        risk_distance = abs(entry_price - stop_loss)
        if direction == 'long':
            tp_price = entry_price + (risk_distance * 2)
        else:
            tp_price = entry_price - (risk_distance * 2)
        
        return {
            'primary_take_profit': tp_price,
            'take_profit_levels': [{'level': 1, 'price': tp_price, 'ratio': 2.0, 'percentage': 4.0}],
            'risk_reward_ratio': 2.0,
            'scaling_strategy': 'single_target',
            'confidence': 0.3,
            'recommendations': ['Using default 1:2 risk-reward ratio due to calculation error']
        }
    
    def _get_default_portfolio_risk(self) -> Dict:
        """Default portfolio risk when calculations fail"""
        return {
            'total_risk': 0.0,
            'risk_percentage': 0.0,
            'correlation_risk': 0.0,
            'diversification_score': 1.0,
            'max_drawdown_estimate': 0.0,
            'new_position_impact': None,
            'warnings': ['Portfolio risk calculation unavailable'],
            'recommendations': ['Use conservative position sizing until risk analysis is available']
        }
    
    # Additional helper methods would be implemented here for:
    # - _calculate_sizing_confidence
    # - _generate_sizing_recommendations
    # - _determine_stop_loss_method
    # - _calculate_stop_loss_confidence
    # - _generate_stop_loss_recommendations
    # - _recommend_scaling_strategy
    # - _calculate_take_profit_confidence
    # - _generate_take_profit_recommendations
    # - _calculate_correlation_risk
    # - _calculate_diversification_score
    # - _estimate_max_drawdown
    # - _assess_new_position_impact
    # - _generate_risk_warnings
    # - _generate_portfolio_recommendations
    
    def _calculate_sizing_confidence(self, market_analysis: Dict, sentiment_analysis: Dict) -> float:
        """Calculate confidence in position sizing"""
        confidence = 0.5
        if market_analysis and market_analysis.get('confidence_score'):
            confidence += market_analysis['confidence_score'] * 0.3
        if sentiment_analysis and sentiment_analysis.get('confidence_score'):
            confidence += sentiment_analysis['confidence_score'] * 0.2
        return min(1.0, confidence)
    
    def _generate_sizing_recommendations(self, risk_percentage: float, market_analysis: Dict, sentiment_analysis: Dict) -> List[str]:
        """Generate position sizing recommendations"""
        recommendations = []
        
        if risk_percentage > 3:
            recommendations.append("High risk position - consider reducing size")
        elif risk_percentage < 0.5:
            recommendations.append("Very conservative sizing - consider increasing if confident")
        
        if market_analysis and market_analysis.get('anomaly_score', 0) > 0.7:
            recommendations.append("Market anomaly detected - extra caution advised")
        
        return recommendations or ["Position sizing looks appropriate"]