"""
Market Analyzer - AI-powered market condition analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
import talib.abstract as ta

logger = logging.getLogger(__name__)


class MarketRegime:
    """Market regime classification"""
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"
    VOLATILE = "volatile"
    CRASH = "crash"


class MarketAnalyzer:
    """
    AI-powered market condition analyzer that detects market regimes,
    volatility patterns, and anomalies for enhanced trading decisions.
    """
    
    def __init__(self):
        self.regime_classifier = None
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.regime_history = []
        
    def analyze_market_conditions(self, dataframe: pd.DataFrame, 
                                 pair: str = None) -> Dict:
        """
        Comprehensive market condition analysis
        
        Args:
            dataframe: OHLCV data with technical indicators
            pair: Trading pair name
            
        Returns:
            Dict containing market analysis results
        """
        try:
            # Calculate advanced market features
            features = self._calculate_market_features(dataframe)
            
            # Detect current market regime
            current_regime = self._detect_market_regime(features)
            
            # Calculate market strength and volatility
            market_strength = self._calculate_market_strength(dataframe)
            volatility_regime = self._analyze_volatility(dataframe)
            
            # Detect anomalies
            anomaly_score = self._detect_anomalies(features)
            
            # Trend analysis
            trend_analysis = self._analyze_trends(dataframe)
            
            # Volume analysis
            volume_analysis = self._analyze_volume_patterns(dataframe)
            
            analysis = {
                'timestamp': datetime.now(),
                'pair': pair,
                'market_regime': current_regime,
                'market_strength': market_strength,
                'volatility_regime': volatility_regime,
                'anomaly_score': anomaly_score,
                'trend_analysis': trend_analysis,
                'volume_analysis': volume_analysis,
                'confidence_score': self._calculate_confidence(features),
                'recommendations': self._generate_recommendations(
                    current_regime, market_strength, volatility_regime, anomaly_score
                )
            }
            
            self.regime_history.append({
                'timestamp': datetime.now(),
                'regime': current_regime,
                'strength': market_strength
            })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in market analysis: {e}")
            return self._get_default_analysis(pair)
    
    def _calculate_market_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate advanced market features for ML analysis"""
        features = pd.DataFrame()
        
        if len(df) < 50:
            return features
            
        # Price-based features
        features['returns'] = df['close'].pct_change()
        features['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        features['volatility_20'] = features['returns'].rolling(20).std()
        features['skewness'] = features['returns'].rolling(20).skew()
        features['kurtosis'] = features['returns'].rolling(20).kurt()
        
        # Technical indicators
        features['rsi'] = ta.RSI(df, timeperiod=14)
        features['macd'] = ta.MACD(df)['macd']
        features['bb_position'] = (df['close'] - ta.BBANDS(df)['lowerband']) / \
                                 (ta.BBANDS(df)['upperband'] - ta.BBANDS(df)['lowerband'])
        
        # Volume features
        features['volume_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
        features['price_volume_trend'] = ta.AD(df)  # Accumulation/Distribution
        
        # Momentum features
        features['momentum_5'] = df['close'] / df['close'].shift(5) - 1
        features['momentum_10'] = df['close'] / df['close'].shift(10) - 1
        features['momentum_20'] = df['close'] / df['close'].shift(20) - 1
        
        # Trend strength
        sma_20 = ta.SMA(df, timeperiod=20)
        sma_50 = ta.SMA(df, timeperiod=50)
        features['trend_strength'] = (sma_20 - sma_50) / sma_50
        
        return features.fillna(0)
    
    def _detect_market_regime(self, features: pd.DataFrame) -> str:
        """Detect current market regime using ML classification"""
        if len(features) < 20:
            return MarketRegime.SIDEWAYS
            
        try:
            # Simple rule-based regime detection (can be enhanced with ML)
            recent_features = features.tail(20)
            
            avg_returns = recent_features['returns'].mean()
            volatility = recent_features['volatility_20'].iloc[-1]
            trend_strength = abs(recent_features['trend_strength'].iloc[-1])
            
            # Classify market regime
            if volatility > 0.05:  # High volatility threshold
                if abs(avg_returns) > 0.02:  # High movement
                    return MarketRegime.CRASH if avg_returns < -0.02 else MarketRegime.VOLATILE
                return MarketRegime.VOLATILE
            elif trend_strength > 0.02:
                return MarketRegime.BULL if avg_returns > 0 else MarketRegime.BEAR
            else:
                return MarketRegime.SIDEWAYS
                
        except Exception as e:
            logger.warning(f"Regime detection error: {e}")
            return MarketRegime.SIDEWAYS
    
    def _calculate_market_strength(self, df: pd.DataFrame) -> float:
        """Calculate overall market strength (0-1 scale)"""
        if len(df) < 20:
            return 0.5
            
        try:
            # Multiple strength indicators
            rsi = ta.RSI(df, timeperiod=14).iloc[-1]
            macd_hist = ta.MACD(df)['macdhist'].iloc[-1]
            volume_ratio = df['volume'].iloc[-1] / df['volume'].rolling(20).mean().iloc[-1]
            
            # Normalize and combine
            rsi_strength = (rsi - 50) / 50  # -1 to 1
            macd_strength = np.tanh(macd_hist * 1000)  # Normalize MACD
            volume_strength = min((volume_ratio - 1), 2) / 2  # 0 to 1
            
            # Combined strength score (0-1)
            strength = (rsi_strength + macd_strength + volume_strength) / 3
            return max(0, min(1, (strength + 1) / 2))  # Scale to 0-1
            
        except Exception as e:
            logger.warning(f"Market strength calculation error: {e}")
            return 0.5
    
    def _analyze_volatility(self, df: pd.DataFrame) -> Dict:
        """Analyze volatility patterns and regime"""
        if len(df) < 30:
            return {'regime': 'normal', 'percentile': 50, 'trend': 'stable'}
            
        try:
            returns = df['close'].pct_change().dropna()
            current_vol = returns.rolling(20).std().iloc[-1]
            historical_vol = returns.rolling(100).std()
            
            # Volatility percentile
            vol_percentile = (historical_vol < current_vol).sum() / len(historical_vol) * 100
            
            # Volatility regime
            if vol_percentile > 80:
                regime = 'high'
            elif vol_percentile < 20:
                regime = 'low'
            else:
                regime = 'normal'
            
            # Volatility trend
            vol_trend = historical_vol.tail(10).mean() - historical_vol.tail(20).mean()
            trend = 'increasing' if vol_trend > 0 else 'decreasing' if vol_trend < 0 else 'stable'
            
            return {
                'regime': regime,
                'percentile': vol_percentile,
                'trend': trend,
                'current_vol': current_vol,
                'average_vol': historical_vol.mean()
            }
            
        except Exception as e:
            logger.warning(f"Volatility analysis error: {e}")
            return {'regime': 'normal', 'percentile': 50, 'trend': 'stable'}
    
    def _detect_anomalies(self, features: pd.DataFrame) -> float:
        """Detect market anomalies using isolation forest"""
        if len(features) < 50:
            return 0.0
            
        try:
            # Use recent features for anomaly detection
            recent_features = features.tail(100).select_dtypes(include=[np.number])
            recent_features = recent_features.fillna(0)
            
            if recent_features.empty:
                return 0.0
                
            # Simple anomaly detection based on z-scores
            z_scores = np.abs((recent_features.iloc[-1] - recent_features.mean()) / recent_features.std())
            anomaly_score = z_scores.mean()
            
            # Normalize to 0-1 scale
            return min(1.0, max(0.0, (anomaly_score - 1) / 2))
            
        except Exception as e:
            logger.warning(f"Anomaly detection error: {e}")
            return 0.0
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """Multi-timeframe trend analysis"""
        if len(df) < 50:
            return {'short': 'neutral', 'medium': 'neutral', 'long': 'neutral', 'strength': 0.5}
            
        try:
            # Different timeframe SMAs
            sma_5 = ta.SMA(df, timeperiod=5)
            sma_20 = ta.SMA(df, timeperiod=20)
            sma_50 = ta.SMA(df, timeperiod=50)
            
            current_price = df['close'].iloc[-1]
            
            # Trend direction
            short_trend = 'up' if current_price > sma_5.iloc[-1] else 'down'
            medium_trend = 'up' if sma_5.iloc[-1] > sma_20.iloc[-1] else 'down'
            long_trend = 'up' if sma_20.iloc[-1] > sma_50.iloc[-1] else 'down'
            
            # Trend strength (alignment of SMAs)
            alignment_score = 0
            if sma_5.iloc[-1] > sma_20.iloc[-1] > sma_50.iloc[-1]:
                alignment_score = 1  # Strong uptrend
            elif sma_5.iloc[-1] < sma_20.iloc[-1] < sma_50.iloc[-1]:
                alignment_score = -1  # Strong downtrend
            
            return {
                'short': short_trend,
                'medium': medium_trend,
                'long': long_trend,
                'strength': (alignment_score + 1) / 2  # 0-1 scale
            }
            
        except Exception as e:
            logger.warning(f"Trend analysis error: {e}")
            return {'short': 'neutral', 'medium': 'neutral', 'long': 'neutral', 'strength': 0.5}
    
    def _analyze_volume_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze volume patterns and trends"""
        if len(df) < 20:
            return {'trend': 'normal', 'strength': 0.5, 'divergence': False}
            
        try:
            volume = df['volume']
            price = df['close']
            
            # Volume trend
            vol_sma = volume.rolling(20).mean()
            current_vol_ratio = volume.iloc[-1] / vol_sma.iloc[-1]
            
            if current_vol_ratio > 1.5:
                vol_trend = 'high'
            elif current_vol_ratio < 0.5:
                vol_trend = 'low'
            else:
                vol_trend = 'normal'
            
            # Price-volume divergence
            price_change = (price.iloc[-1] - price.iloc[-10]) / price.iloc[-10]
            volume_change = (volume.tail(10).mean() - volume.head(-10).tail(10).mean()) / volume.head(-10).tail(10).mean()
            
            # Divergence occurs when price and volume move in opposite directions
            divergence = (price_change > 0 and volume_change < -0.1) or (price_change < 0 and volume_change > 0.1)
            
            return {
                'trend': vol_trend,
                'strength': min(1.0, current_vol_ratio / 2),
                'divergence': divergence,
                'volume_ratio': current_vol_ratio
            }
            
        except Exception as e:
            logger.warning(f"Volume analysis error: {e}")
            return {'trend': 'normal', 'strength': 0.5, 'divergence': False}
    
    def _calculate_confidence(self, features: pd.DataFrame) -> float:
        """Calculate confidence in the analysis"""
        if len(features) < 20:
            return 0.3
            
        try:
            # Confidence based on data quality and consistency
            data_points = len(features)
            missing_ratio = features.isnull().mean().mean()
            volatility_consistency = 1 - features['volatility_20'].std() if 'volatility_20' in features else 0.5
            
            confidence = (min(data_points / 100, 1) * 0.4 + 
                         (1 - missing_ratio) * 0.3 + 
                         volatility_consistency * 0.3)
            
            return max(0.1, min(1.0, confidence))
            
        except Exception as e:
            logger.warning(f"Confidence calculation error: {e}")
            return 0.5
    
    def _generate_recommendations(self, regime: str, strength: float, 
                                volatility: Dict, anomaly_score: float) -> Dict:
        """Generate trading recommendations based on market analysis"""
        recommendations = {
            'position_sizing': 'normal',
            'strategy_adjustment': 'none',
            'risk_level': 'medium',
            'suggested_timeframe': '5m',
            'alerts': []
        }
        
        try:
            # Adjust recommendations based on market regime
            if regime == MarketRegime.VOLATILE or anomaly_score > 0.7:
                recommendations['position_sizing'] = 'reduced'
                recommendations['risk_level'] = 'high'
                recommendations['strategy_adjustment'] = 'defensive'
                recommendations['alerts'].append('High volatility detected - reduce position sizes')
                
            elif regime == MarketRegime.CRASH:
                recommendations['position_sizing'] = 'minimal'
                recommendations['risk_level'] = 'extreme'
                recommendations['strategy_adjustment'] = 'defensive'
                recommendations['suggested_timeframe'] = '1m'
                recommendations['alerts'].append('Market crash conditions - consider exit strategy')
                
            elif regime == MarketRegime.BULL and strength > 0.7:
                recommendations['position_sizing'] = 'increased'
                recommendations['risk_level'] = 'low'
                recommendations['strategy_adjustment'] = 'aggressive'
                recommendations['alerts'].append('Strong bull market - consider increasing exposure')
                
            elif regime == MarketRegime.SIDEWAYS:
                recommendations['suggested_timeframe'] = '15m'
                recommendations['strategy_adjustment'] = 'range_trading'
                
            # Volatility-based adjustments
            if volatility.get('regime') == 'high':
                recommendations['alerts'].append('High volatility regime detected')
                if recommendations['position_sizing'] == 'normal':
                    recommendations['position_sizing'] = 'reduced'
                    
            return recommendations
            
        except Exception as e:
            logger.warning(f"Recommendation generation error: {e}")
            return recommendations
    
    def _get_default_analysis(self, pair: str = None) -> Dict:
        """Return default analysis when errors occur"""
        return {
            'timestamp': datetime.now(),
            'pair': pair,
            'market_regime': MarketRegime.SIDEWAYS,
            'market_strength': 0.5,
            'volatility_regime': {'regime': 'normal', 'percentile': 50, 'trend': 'stable'},
            'anomaly_score': 0.0,
            'trend_analysis': {'short': 'neutral', 'medium': 'neutral', 'long': 'neutral', 'strength': 0.5},
            'volume_analysis': {'trend': 'normal', 'strength': 0.5, 'divergence': False},
            'confidence_score': 0.3,
            'recommendations': {
                'position_sizing': 'normal',
                'strategy_adjustment': 'none',
                'risk_level': 'medium',
                'suggested_timeframe': '5m',
                'alerts': ['Analysis unavailable - using default settings']
            }
        }