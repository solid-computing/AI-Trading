"""
AI-Enhanced RSI + MA Strategy with Advanced AI Reasoning
========================================================

This strategy extends the original RsiMaStrategy with advanced AI capabilities:
- Market regime detection and adaptation
- Sentiment analysis integration
- Dynamic risk management
- Real-time parameter optimization
- Emergency condition detection
- Multi-modal decision making
"""

# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union, Dict, List
import logging

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# AI Engine imports
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai_engine.decision_engine import DecisionEngine
from ai_engine.market_analyzer import MarketAnalyzer
from ai_engine.sentiment_engine import SentimentEngine
from ai_engine.risk_manager import RiskManager, RiskAppetite

# Set up logging
logger = logging.getLogger(__name__)


class AIEnhancedRsiMaStrategy(IStrategy):
    """
    AI-Enhanced RSI + Moving Average Strategy
    
    This strategy combines traditional technical analysis with advanced AI reasoning:
    
    Core Features:
        - Traditional RSI + MA signals enhanced with AI
        - Market regime detection and adaptation
        - Sentiment analysis integration
        - Dynamic risk management
        - Real-time parameter optimization
        - Emergency condition detection
        
    AI Enhancements:
        - Multi-modal analysis (technical + sentiment + market conditions)
        - Adaptive position sizing based on market volatility and risk appetite
        - Dynamic stop-loss and take-profit optimization
        - Real-time strategy parameter adaptation
        - Anomaly detection for sudden market changes
        - AI-powered entry/exit timing optimization
    
    Risk Management:
        - AI-driven position sizing
        - Dynamic risk appetite adjustment
        - Portfolio correlation analysis
        - Emergency exit conditions
        - Volatility-adjusted stop losses
    """

    # Strategy interface version
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy (AI can override these)
    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04
    }

    # Optimal stoploss (AI will optimize this dynamically)
    stoploss = -0.05

    # Trailing stoploss
    trailing_stop = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0

    # Optimal timeframe for the strategy
    timeframe = '5m'

    # Run "populate_indicators" only for new candle
    process_only_new_candles = False

    # These values can be overridden in the config
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Enable custom stoploss for AI optimization
    use_custom_stoploss = True

    # Hyperoptable parameters (AI can dynamically adjust these)
    rsi_buy_threshold = IntParameter(20, 40, default=30, space="buy")
    rsi_sell_threshold = IntParameter(60, 80, default=70, space="sell")
    sma_period = IntParameter(10, 50, default=20, space="buy")
    volume_factor = DecimalParameter(1.0, 2.0, default=1.2, space="buy")
    
    # AI-specific parameters
    ai_confidence_threshold = DecimalParameter(0.4, 0.8, default=0.6, space="buy")
    risk_appetite = CategoricalParameter(['conservative', 'moderate', 'aggressive', 'dynamic'], 
                                       default='dynamic', space="buy")
    enable_sentiment_analysis = BooleanParameter(default=True, space="buy")
    enable_market_regime_adaptation = BooleanParameter(default=True, space="buy")
    enable_dynamic_parameters = BooleanParameter(default=True, space="buy")
    emergency_exit_enabled = BooleanParameter(default=True, space="buy")

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 50

    # Optional order type mapping
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force
    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }

    # Plot configuration for AI indicators
    plot_config = {
        'main_plot': {
            'sma': {'color': 'blue'},
            'ai_regime_signal': {'color': 'purple'},
        },
        'subplots': {
            "RSI": {
                'rsi': {'color': 'red'},
                'ai_rsi_threshold': {'color': 'orange'},
            },
            "AI Signals": {
                'ai_confidence': {'color': 'green'},
                'ai_sentiment': {'color': 'cyan'},
                'ai_market_strength': {'color': 'yellow'},
            }
        }
    }

    def __init__(self, config: dict = None) -> None:
        super().__init__(config)
        
        # Initialize AI components
        self.ai_config = {
            'risk': {
                'risk_appetite': self.risk_appetite.value if hasattr(self.risk_appetite, 'value') else 'moderate',
                'max_portfolio_risk': 0.05,
                'max_position_risk': 0.02,
                'volatility_adjustment': True,
                'correlation_adjustment': True
            },
            'sentiment': {
                'enable_social_sentiment': True,
                'enable_news_sentiment': True,
                'enable_fear_greed': True
            },
            'ai_confidence_threshold': self.ai_confidence_threshold.value if hasattr(self.ai_confidence_threshold, 'value') else 0.6,
            'enable_sentiment_override': self.enable_sentiment_analysis.value if hasattr(self.enable_sentiment_analysis, 'value') else True,
            'enable_market_regime_adaptation': self.enable_market_regime_adaptation.value if hasattr(self.enable_market_regime_adaptation, 'value') else True,
            'enable_dynamic_parameters': self.enable_dynamic_parameters.value if hasattr(self.enable_dynamic_parameters, 'value') else True
        }
        
        try:
            self.decision_engine = DecisionEngine(self.ai_config)
            self.ai_initialized = True
            logger.info("AI Decision Engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Decision Engine: {e}")
            self.ai_initialized = False
            
        # Track AI decisions and performance
        self.ai_decisions = []
        self.ai_performance = []
        self.current_positions = []
        
        # Adaptive parameters
        self.adaptive_params = {
            'rsi_buy_threshold': self.rsi_buy_threshold.value if hasattr(self.rsi_buy_threshold, 'value') else 30,
            'rsi_sell_threshold': self.rsi_sell_threshold.value if hasattr(self.rsi_sell_threshold, 'value') else 70,
            'sma_period': self.sma_period.value if hasattr(self.sma_period, 'value') else 20,
            'volume_factor': self.volume_factor.value if hasattr(self.volume_factor, 'value') else 1.2
        }

    def informative_pairs(self):
        """
        Define additional informative pair/interval combinations for AI analysis
        """
        return [
            # Add longer timeframes for multi-timeframe analysis
            (f"{self.dp.current_whitelist()[0]}", "1h"),
            (f"{self.dp.current_whitelist()[0]}", "4h"),
        ]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populate indicators including traditional TA and AI-enhanced signals
        """
        try:
            # Traditional technical indicators
            dataframe = self._populate_traditional_indicators(dataframe)
            
            # AI-enhanced indicators if AI is initialized
            if self.ai_initialized:
                dataframe = self._populate_ai_indicators(dataframe, metadata)
            
            return dataframe
            
        except Exception as e:
            logger.error(f"Error populating indicators: {e}")
            # Fallback to traditional indicators only
            return self._populate_traditional_indicators(dataframe)

    def _populate_traditional_indicators(self, dataframe: DataFrame) -> DataFrame:
        """Populate traditional technical indicators"""
        
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Simple Moving Average (adaptive period)
        current_sma_period = int(self.adaptive_params.get('sma_period', 20))
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=current_sma_period)

        # Volume moving average
        dataframe['volume_sma'] = ta.SMA(dataframe['volume'], timeperiod=20)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe["bb_percent"] = (
            (dataframe["close"] - dataframe["bb_lowerband"]) /
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"])
        )
        dataframe["bb_width"] = (
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe["bb_middleband"]
        )

        # Additional indicators for AI analysis
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)  # Average True Range
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)  # Average Directional Index
        dataframe['cci'] = ta.CCI(dataframe, timeperiod=20)  # Commodity Channel Index
        dataframe['williams_r'] = ta.WILLR(dataframe, timeperiod=14)  # Williams %R
        
        return dataframe

    def _populate_ai_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Populate AI-enhanced indicators"""
        try:
            if len(dataframe) < 30:
                # Initialize AI indicators with neutral values
                dataframe['ai_confidence'] = 0.5
                dataframe['ai_sentiment'] = 0.5
                dataframe['ai_market_strength'] = 0.5
                dataframe['ai_regime_signal'] = 0
                dataframe['ai_rsi_threshold'] = 50
                return dataframe
            
            # Get AI analysis for the current market conditions
            ai_decision = self.decision_engine.make_trading_decision(
                dataframe=dataframe,
                metadata=metadata,
                current_positions=self.current_positions,
                account_balance=1000  # This would come from the actual account balance
            )
            
            # Extract AI indicators
            market_analysis = ai_decision.get('market_analysis', {})
            sentiment_analysis = ai_decision.get('sentiment_analysis', {})
            
            # AI Confidence Score
            dataframe['ai_confidence'] = ai_decision.get('confidence_score', 0.5)
            
            # AI Sentiment Score
            overall_sentiment = sentiment_analysis.get('overall_sentiment', {})
            dataframe['ai_sentiment'] = overall_sentiment.get('normalized_score', 0.5)
            
            # AI Market Strength
            dataframe['ai_market_strength'] = market_analysis.get('market_strength', 0.5)
            
            # AI Regime Signal (encoded as number for plotting)
            regime = market_analysis.get('market_regime', 'sideways')
            regime_mapping = {'bull': 1, 'bear': -1, 'sideways': 0, 'volatile': 0.5, 'crash': -2}
            dataframe['ai_regime_signal'] = regime_mapping.get(regime, 0)
            
            # Dynamic RSI threshold based on AI analysis
            base_rsi_threshold = self.adaptive_params.get('rsi_buy_threshold', 30)
            if market_analysis.get('volatility_regime', {}).get('regime') == 'high':
                # Adjust thresholds in high volatility
                dataframe['ai_rsi_threshold'] = base_rsi_threshold + 5
            else:
                dataframe['ai_rsi_threshold'] = base_rsi_threshold
            
            # Store latest AI decision for use in entry/exit logic
            self.latest_ai_decision = ai_decision
            
        except Exception as e:
            logger.error(f"Error in AI indicator calculation: {e}")
            # Fallback values
            dataframe['ai_confidence'] = 0.3
            dataframe['ai_sentiment'] = 0.5
            dataframe['ai_market_strength'] = 0.5
            dataframe['ai_regime_signal'] = 0
            dataframe['ai_rsi_threshold'] = 30
            self.latest_ai_decision = None
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        AI-Enhanced entry signal generation
        """
        try:
            if self.ai_initialized and hasattr(self, 'latest_ai_decision') and self.latest_ai_decision:
                return self._populate_ai_entry_trend(dataframe, metadata)
            else:
                return self._populate_traditional_entry_trend(dataframe)
                
        except Exception as e:
            logger.error(f"Error in entry trend population: {e}")
            return self._populate_traditional_entry_trend(dataframe)

    def _populate_traditional_entry_trend(self, dataframe: DataFrame) -> DataFrame:
        """Traditional entry logic (fallback)"""
        current_rsi_threshold = self.adaptive_params.get('rsi_buy_threshold', 30)
        current_volume_factor = self.adaptive_params.get('volume_factor', 1.2)
        
        dataframe.loc[
            (
                # RSI is oversold (adaptive threshold)
                (dataframe['rsi'] < current_rsi_threshold) &
                
                # Price is above SMA (uptrend)
                (dataframe['close'] > dataframe['sma']) &
                
                # Volume is above average
                (dataframe['volume'] > (dataframe['volume_sma'] * current_volume_factor)) &
                
                # MACD is positive
                (dataframe['macd'] > dataframe['macdsignal']) &
                
                # Price is not at the upper Bollinger Band
                (dataframe['close'] < dataframe['bb_upperband']) &
                
                # Volume check
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def _populate_ai_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """AI-enhanced entry logic"""
        
        # Get AI decision
        ai_decision = self.latest_ai_decision
        final_decision = ai_decision.get('final_decision', {})
        entry_signals = ai_decision.get('entry_signals', {})
        
        # AI confidence check
        ai_confidence = ai_decision.get('confidence_score', 0.3)
        confidence_threshold = self.ai_config.get('ai_confidence_threshold', 0.6)
        
        # Traditional signals as base
        current_rsi_threshold = self.adaptive_params.get('rsi_buy_threshold', 30)
        current_volume_factor = self.adaptive_params.get('volume_factor', 1.2)
        
        # Enhanced conditions with AI
        dataframe.loc[
            (
                # Traditional conditions (baseline)
                (dataframe['rsi'] < current_rsi_threshold) &
                (dataframe['close'] > dataframe['sma']) &
                (dataframe['volume'] > (dataframe['volume_sma'] * current_volume_factor)) &
                (dataframe['macd'] > dataframe['macdsignal']) &
                (dataframe['close'] < dataframe['bb_upperband']) &
                (dataframe['volume'] > 0) &
                
                # AI Enhancement conditions
                (dataframe['ai_confidence'] > confidence_threshold) &  # AI is confident
                (
                    # AI recommends entry OR traditional signals are very strong with moderate AI confidence
                    (final_decision.get('action') == 'enter_long') |
                    (
                        (entry_signals.get('should_enter', False)) &
                        (dataframe['ai_confidence'] > confidence_threshold * 0.8) &
                        (dataframe['ai_sentiment'] > 0.4)  # Not bearish sentiment
                    )
                ) &
                
                # Market regime compatibility
                (dataframe['ai_regime_signal'] >= -0.5)  # Avoid bear/crash markets
                
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        AI-Enhanced exit signal generation
        """
        try:
            if self.ai_initialized and hasattr(self, 'latest_ai_decision') and self.latest_ai_decision:
                return self._populate_ai_exit_trend(dataframe, metadata)
            else:
                return self._populate_traditional_exit_trend(dataframe)
                
        except Exception as e:
            logger.error(f"Error in exit trend population: {e}")
            return self._populate_traditional_exit_trend(dataframe)

    def _populate_traditional_exit_trend(self, dataframe: DataFrame) -> DataFrame:
        """Traditional exit logic (fallback)"""
        current_rsi_threshold = self.adaptive_params.get('rsi_sell_threshold', 70)
        
        dataframe.loc[
            (
                # RSI is overbought
                (dataframe['rsi'] > current_rsi_threshold) |
                
                # Price is below SMA (downtrend)
                (dataframe['close'] < dataframe['sma']) |
                
                # MACD turns negative
                (dataframe['macd'] < dataframe['macdsignal']) |
                
                # Price hits upper Bollinger Band
                (dataframe['close'] >= dataframe['bb_upperband'])
            ),
            'exit_long'] = 1

        return dataframe

    def _populate_ai_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """AI-enhanced exit logic"""
        
        # Get AI decision
        ai_decision = self.latest_ai_decision
        final_decision = ai_decision.get('final_decision', {})
        exit_signals = ai_decision.get('exit_signals', {})
        emergency_conditions = ai_decision.get('emergency_conditions', {})
        
        # Traditional thresholds
        current_rsi_threshold = self.adaptive_params.get('rsi_sell_threshold', 70)
        
        # Emergency exit conditions
        emergency_exit = (
            emergency_conditions.get('has_emergency', False) &
            self.emergency_exit_enabled.value if hasattr(self.emergency_exit_enabled, 'value') else True
        )
        
        # AI-enhanced exit conditions
        dataframe.loc[
            (
                # Emergency conditions (highest priority)
                emergency_exit |
                
                # AI recommends exit
                (final_decision.get('action') == 'exit_long') |
                (final_decision.get('action') == 'emergency_exit') |
                
                # Strong AI exit signals
                (exit_signals.get('should_exit', False) & (dataframe['ai_confidence'] > 0.5)) |
                
                # Traditional signals enhanced with AI context
                (
                    (
                        (dataframe['rsi'] > current_rsi_threshold) |
                        (dataframe['close'] < dataframe['sma']) |
                        (dataframe['macd'] < dataframe['macdsignal']) |
                        (dataframe['close'] >= dataframe['bb_upperband'])
                    ) &
                    # AI context: avoid exits in strong bull markets unless confidence is high
                    (
                        (dataframe['ai_regime_signal'] <= 0.5) |  # Not in strong bull market
                        (dataframe['ai_confidence'] > 0.7) |       # High AI confidence
                        (dataframe['ai_sentiment'] < 0.3)          # Bearish sentiment
                    )
                ) |
                
                # Market regime-based exits
                (dataframe['ai_regime_signal'] <= -1.5)  # Crash conditions
            ),
            'exit_long'] = 1

        return dataframe

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        """
        AI-optimized custom stoploss
        """
        try:
            if not self.ai_initialized:
                return self.stoploss
            
            # Get current market analysis if available
            if hasattr(self, 'latest_ai_decision') and self.latest_ai_decision:
                market_analysis = self.latest_ai_decision.get('market_analysis', {})
                
                # Volatility-based stoploss adjustment
                volatility = market_analysis.get('volatility_regime', {})
                vol_regime = volatility.get('regime', 'normal')
                
                base_stoploss = self.stoploss
                
                # Adjust based on volatility
                if vol_regime == 'high':
                    # Wider stoploss in high volatility
                    adjusted_stoploss = base_stoploss * 1.5
                elif vol_regime == 'low':
                    # Tighter stoploss in low volatility
                    adjusted_stoploss = base_stoploss * 0.8
                else:
                    adjusted_stoploss = base_stoploss
                
                # Market regime adjustments
                regime = market_analysis.get('market_regime', 'sideways')
                if regime == 'crash':
                    # Tighter stoploss in crash conditions
                    adjusted_stoploss = max(adjusted_stoploss, -0.03)
                elif regime == 'volatile':
                    # Slightly wider stoploss in volatile conditions
                    adjusted_stoploss = adjusted_stoploss * 1.2
                
                # Ensure stoploss doesn't become too wide
                adjusted_stoploss = max(adjusted_stoploss, -0.10)  # Max 10% loss
                adjusted_stoploss = min(adjusted_stoploss, -0.01)  # Min 1% loss
                
                return adjusted_stoploss
            
            return self.stoploss
            
        except Exception as e:
            logger.error(f"Error in custom stoploss: {e}")
            return self.stoploss

    def custom_exit(self, pair: str, trade: 'Trade', current_time: datetime, 
                   current_rate: float, current_profit: float, **kwargs) -> Optional[Union[str, bool]]:
        """
        AI-powered custom exit logic for emergency conditions
        """
        try:
            if not self.ai_initialized:
                return None
            
            # Check for emergency conditions
            if hasattr(self, 'latest_ai_decision') and self.latest_ai_decision:
                emergency_conditions = self.latest_ai_decision.get('emergency_conditions', {})
                final_decision = self.latest_ai_decision.get('final_decision', {})
                
                # Emergency exit
                if emergency_conditions.get('has_emergency', False):
                    logger.warning(f"AI Emergency Exit triggered for {pair}: {emergency_conditions.get('reasons', [])}")
                    return "ai_emergency_exit"
                
                # AI override exit
                if final_decision.get('action') == 'emergency_exit':
                    logger.info(f"AI Override Exit triggered for {pair}")
                    return "ai_override_exit"
            
            return None
            
        except Exception as e:
            logger.error(f"Error in custom exit: {e}")
            return None

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                           time_in_force: str, current_time: datetime, entry_tag: Optional[str],
                           side: str, **kwargs) -> bool:
        """
        AI-powered trade entry confirmation with final safety checks
        """
        try:
            if not self.ai_initialized:
                return True  # Fallback to allow trade
            
            # Final AI safety check
            if hasattr(self, 'latest_ai_decision') and self.latest_ai_decision:
                emergency_conditions = self.latest_ai_decision.get('emergency_conditions', {})
                
                # Block entry in emergency conditions
                if emergency_conditions.get('has_emergency', False):
                    logger.warning(f"Blocking trade entry for {pair} due to emergency conditions: {emergency_conditions.get('reasons', [])}")
                    return False
                
                # Check AI confidence
                confidence = self.latest_ai_decision.get('confidence_score', 0.5)
                confidence_threshold = self.ai_config.get('ai_confidence_threshold', 0.6)
                
                if confidence < confidence_threshold:
                    logger.info(f"Blocking trade entry for {pair} due to low AI confidence: {confidence:.2f} < {confidence_threshold}")
                    return False
            
            # Log AI decision for this trade
            if hasattr(self, 'latest_ai_decision'):
                self.ai_decisions.append({
                    'timestamp': current_time,
                    'pair': pair,
                    'action': 'entry_confirmed',
                    'amount': amount,
                    'rate': rate,
                    'ai_decision': self.latest_ai_decision
                })
            
            return True
            
        except Exception as e:
            logger.error(f"Error in trade entry confirmation: {e}")
            return True  # Default to allow trade on error

    def confirm_trade_exit(self, pair: str, trade: 'Trade', order_type: str, amount: float,
                          rate: float, time_in_force: str, exit_reason: str,
                          current_time: datetime, **kwargs) -> bool:
        """
        AI-powered trade exit confirmation
        """
        try:
            # Always allow exit (safety first)
            
            # Log AI decision for this exit
            if hasattr(self, 'latest_ai_decision'):
                self.ai_decisions.append({
                    'timestamp': current_time,
                    'pair': pair,
                    'action': 'exit_confirmed',
                    'amount': amount,
                    'rate': rate,
                    'exit_reason': exit_reason,
                    'profit': trade.calc_profit_ratio(rate),
                    'ai_decision': self.latest_ai_decision
                })
                
                # Update AI performance tracking
                self.ai_performance.append({
                    'timestamp': current_time,
                    'pair': pair,
                    'profit': trade.calc_profit_ratio(rate),
                    'exit_reason': exit_reason
                })
            
            return True
            
        except Exception as e:
            logger.error(f"Error in trade exit confirmation: {e}")
            return True

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                proposed_leverage: float, max_leverage: float, entry_tag: Optional[str], 
                side: str, **kwargs) -> float:
        """
        AI-optimized leverage calculation (for futures trading)
        """
        try:
            if not self.ai_initialized:
                return 1.0  # No leverage for spot trading
            
            # This would implement AI-based leverage optimization
            # For now, return conservative leverage for safety
            return min(proposed_leverage, 2.0)  # Max 2x leverage
            
        except Exception as e:
            logger.error(f"Error in leverage calculation: {e}")
            return 1.0

    def get_ai_status(self) -> Dict:
        """
        Get current AI system status and performance
        """
        try:
            if not self.ai_initialized:
                return {'status': 'disabled', 'reason': 'AI initialization failed'}
            
            # Get AI insights
            ai_insights = self.decision_engine.get_ai_insights()
            
            # Performance metrics
            recent_performance = self.ai_performance[-50:] if self.ai_performance else []
            avg_profit = np.mean([p['profit'] for p in recent_performance]) if recent_performance else 0
            
            return {
                'status': 'active',
                'ai_initialized': self.ai_initialized,
                'total_decisions': len(self.ai_decisions),
                'recent_performance': {
                    'avg_profit': avg_profit,
                    'total_trades': len(recent_performance),
                    'win_rate': sum(1 for p in recent_performance if p['profit'] > 0) / len(recent_performance) if recent_performance else 0
                },
                'current_config': self.ai_config,
                'adaptive_parameters': self.adaptive_params,
                'ai_insights': ai_insights
            }
            
        except Exception as e:
            logger.error(f"Error getting AI status: {e}")
            return {'status': 'error', 'error': str(e)}

    def adapt_parameters(self, market_conditions: Dict, performance_data: Dict = None) -> Dict:
        """
        Dynamically adapt strategy parameters based on AI analysis
        """
        try:
            if not self.ai_initialized or not self.enable_dynamic_parameters.value:
                return self.adaptive_params
            
            # Get parameter adaptation from AI
            adaptation_result = self.decision_engine.adapt_strategy_parameters(
                current_params=self.adaptive_params,
                market_analysis=market_conditions,
                sentiment_analysis=self.latest_ai_decision.get('sentiment_analysis', {}) if hasattr(self, 'latest_ai_decision') else {},
                performance_data=performance_data
            )
            
            # Update adaptive parameters
            new_params = adaptation_result.get('adapted_parameters', self.adaptive_params)
            self.adaptive_params.update(new_params)
            
            logger.info(f"AI Parameter Adaptation: {adaptation_result.get('adaptations_made', [])}")
            
            return adaptation_result
            
        except Exception as e:
            logger.error(f"Error in parameter adaptation: {e}")
            return {'adapted_parameters': self.adaptive_params, 'error': str(e)}

    def bot_start(self, **kwargs) -> None:
        """
        Called when the bot starts - initialize AI components
        """
        try:
            logger.info("AI-Enhanced Strategy starting up...")
            
            if self.ai_initialized:
                logger.info("AI Decision Engine is ready")
                logger.info(f"AI Configuration: {self.ai_config}")
            else:
                logger.warning("AI components not initialized - falling back to traditional strategy")
            
        except Exception as e:
            logger.error(f"Error in bot_start: {e}")

    def bot_loop_start(self, current_time: datetime, **kwargs) -> None:
        """
        Called at the start of each bot loop - can be used for periodic AI updates
        """
        try:
            # Periodic AI maintenance (every hour)
            if hasattr(self, '_last_ai_maintenance'):
                if (current_time - self._last_ai_maintenance).total_seconds() > 3600:
                    self._perform_ai_maintenance()
                    self._last_ai_maintenance = current_time
            else:
                self._last_ai_maintenance = current_time
                
        except Exception as e:
            logger.error(f"Error in bot_loop_start: {e}")

    def _perform_ai_maintenance(self):
        """Perform periodic AI system maintenance"""
        try:
            # Clean up old decisions to prevent memory issues
            if len(self.ai_decisions) > 1000:
                self.ai_decisions = self.ai_decisions[-500:]
            
            if len(self.ai_performance) > 1000:
                self.ai_performance = self.ai_performance[-500:]
            
            logger.info("AI maintenance completed")
            
        except Exception as e:
            logger.error(f"Error in AI maintenance: {e}")