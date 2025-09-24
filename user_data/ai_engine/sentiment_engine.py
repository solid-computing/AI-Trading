"""
Sentiment Engine - AI-powered market sentiment analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import requests
from textblob import TextBlob
import json
import time

logger = logging.getLogger(__name__)


class SentimentEngine:
    """
    AI-powered sentiment analysis engine that analyzes:
    - Social media sentiment (Twitter, Reddit)
    - News sentiment
    - Market fear & greed indicators
    - On-chain metrics sentiment
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.sentiment_cache = {}
        self.cache_duration = timedelta(minutes=15)  # Cache sentiment for 15 minutes
        
    def analyze_market_sentiment(self, pair: str, timeframe: str = '1h') -> Dict:
        """
        Comprehensive market sentiment analysis
        
        Args:
            pair: Trading pair (e.g., 'BTC/USDT')
            timeframe: Analysis timeframe
            
        Returns:
            Dict containing sentiment analysis results
        """
        try:
            cache_key = f"{pair}_{timeframe}"
            
            # Check cache first
            if self._is_cache_valid(cache_key):
                return self.sentiment_cache[cache_key]['data']
            
            # Get base asset from pair
            base_asset = pair.split('/')[0].upper()
            
            # Analyze different sentiment sources
            social_sentiment = self._analyze_social_sentiment(base_asset)
            news_sentiment = self._analyze_news_sentiment(base_asset)
            fear_greed = self._get_fear_greed_index()
            market_sentiment = self._analyze_market_metrics_sentiment(base_asset)
            
            # Combine all sentiment sources
            combined_sentiment = self._combine_sentiments([
                social_sentiment,
                news_sentiment,
                fear_greed,
                market_sentiment
            ])
            
            result = {
                'timestamp': datetime.now(),
                'pair': pair,
                'timeframe': timeframe,
                'overall_sentiment': combined_sentiment,
                'social_sentiment': social_sentiment,
                'news_sentiment': news_sentiment,
                'fear_greed_index': fear_greed,
                'market_sentiment': market_sentiment,
                'confidence_score': self._calculate_sentiment_confidence([
                    social_sentiment, news_sentiment, fear_greed, market_sentiment
                ]),
                'recommendations': self._generate_sentiment_recommendations(combined_sentiment)
            }
            
            # Cache the result
            self.sentiment_cache[cache_key] = {
                'timestamp': datetime.now(),
                'data': result
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return self._get_default_sentiment(pair, timeframe)
    
    def _analyze_social_sentiment(self, asset: str) -> Dict:
        """Analyze social media sentiment"""
        try:
            # Simulated social sentiment analysis
            # In production, this would connect to Twitter API, Reddit API, etc.
            
            # Mock sentiment data based on common patterns
            mock_tweets = [
                f"{asset} looking bullish today! 🚀",
                f"Hodling {asset} through this dip 💎",
                f"{asset} technical analysis shows strong support",
                f"Bearish on {asset} short term, but long term bullish",
                f"{asset} breaking resistance levels!"
            ]
            
            sentiments = []
            for tweet in mock_tweets:
                blob = TextBlob(tweet)
                sentiments.append(blob.sentiment.polarity)
            
            avg_sentiment = np.mean(sentiments) if sentiments else 0
            
            # Simulate volume and engagement metrics
            volume_score = np.random.uniform(0.3, 1.0)  # Mock social volume
            engagement_score = np.random.uniform(0.4, 0.9)  # Mock engagement
            
            return {
                'score': avg_sentiment,  # -1 to 1
                'normalized_score': (avg_sentiment + 1) / 2,  # 0 to 1
                'volume': volume_score,
                'engagement': engagement_score,
                'trending': volume_score > 0.7,
                'source': 'social_media'
            }
            
        except Exception as e:
            logger.warning(f"Social sentiment analysis error: {e}")
            return {
                'score': 0.0,
                'normalized_score': 0.5,
                'volume': 0.5,
                'engagement': 0.5,
                'trending': False,
                'source': 'social_media'
            }
    
    def _analyze_news_sentiment(self, asset: str) -> Dict:
        """Analyze news sentiment"""
        try:
            # Mock news sentiment analysis
            # In production, this would use News API, CoinDesk API, etc.
            
            mock_headlines = [
                f"{asset} adoption increases among institutional investors",
                f"Regulatory clarity boosts {asset} outlook",
                f"{asset} technical upgrade scheduled for next month",
                f"Market volatility affects {asset} trading volume",
                f"{asset} partnership announcement drives interest"
            ]
            
            sentiments = []
            for headline in mock_headlines:
                blob = TextBlob(headline)
                sentiments.append(blob.sentiment.polarity)
            
            avg_sentiment = np.mean(sentiments) if sentiments else 0
            
            # Simulate news metrics
            news_volume = np.random.uniform(0.2, 0.8)
            news_importance = np.random.uniform(0.3, 0.9)
            
            return {
                'score': avg_sentiment,
                'normalized_score': (avg_sentiment + 1) / 2,
                'volume': news_volume,
                'importance': news_importance,
                'trending_topics': [f"{asset}_adoption", f"{asset}_technical"],
                'source': 'news'
            }
            
        except Exception as e:
            logger.warning(f"News sentiment analysis error: {e}")
            return {
                'score': 0.0,
                'normalized_score': 0.5,
                'volume': 0.5,
                'importance': 0.5,
                'trending_topics': [],
                'source': 'news'
            }
    
    def _get_fear_greed_index(self) -> Dict:
        """Get crypto fear & greed index"""
        try:
            # Try to get real fear & greed index
            url = "https://api.alternative.me/fng/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data and len(data['data']) > 0:
                    fng_data = data['data'][0]
                    value = int(fng_data['value'])
                    classification = fng_data['value_classification']
                    
                    return {
                        'value': value,  # 0-100
                        'normalized_score': value / 100,  # 0-1
                        'classification': classification,
                        'timestamp': fng_data['timestamp'],
                        'source': 'fear_greed_index'
                    }
            
            # Fallback to mock data
            mock_value = np.random.randint(20, 80)
            if mock_value < 25:
                classification = "Extreme Fear"
            elif mock_value < 45:
                classification = "Fear"
            elif mock_value < 55:
                classification = "Neutral"
            elif mock_value < 75:
                classification = "Greed"
            else:
                classification = "Extreme Greed"
                
            return {
                'value': mock_value,
                'normalized_score': mock_value / 100,
                'classification': classification,
                'timestamp': str(int(time.time())),
                'source': 'fear_greed_index'
            }
            
        except Exception as e:
            logger.warning(f"Fear & Greed index error: {e}")
            return {
                'value': 50,
                'normalized_score': 0.5,
                'classification': 'Neutral',
                'timestamp': str(int(time.time())),
                'source': 'fear_greed_index'
            }
    
    def _analyze_market_metrics_sentiment(self, asset: str) -> Dict:
        """Analyze market metrics for sentiment signals"""
        try:
            # Mock market metrics sentiment
            # In production, this would analyze on-chain metrics, derivatives data, etc.
            
            # Simulate various market sentiment indicators
            funding_rate_sentiment = np.random.uniform(-0.3, 0.3)  # Futures funding rates
            options_put_call_ratio = np.random.uniform(0.5, 2.0)  # Options sentiment
            whale_activity = np.random.uniform(0.2, 0.8)  # Large holder activity
            exchange_inflows = np.random.uniform(0.1, 0.9)  # Exchange deposit patterns
            
            # Combine metrics into sentiment score
            metrics_score = (
                funding_rate_sentiment * 0.3 +
                (1 - min(options_put_call_ratio, 2) / 2) * 0.25 +  # Lower put/call ratio = more bullish
                whale_activity * 0.25 +
                (1 - exchange_inflows) * 0.2  # Lower inflows = less selling pressure
            )
            
            return {
                'score': metrics_score,
                'normalized_score': (metrics_score + 1) / 2,
                'funding_rate_sentiment': funding_rate_sentiment,
                'put_call_ratio': options_put_call_ratio,
                'whale_activity': whale_activity,
                'exchange_flows': exchange_inflows,
                'source': 'market_metrics'
            }
            
        except Exception as e:
            logger.warning(f"Market metrics sentiment error: {e}")
            return {
                'score': 0.0,
                'normalized_score': 0.5,
                'funding_rate_sentiment': 0.0,
                'put_call_ratio': 1.0,
                'whale_activity': 0.5,
                'exchange_flows': 0.5,
                'source': 'market_metrics'
            }
    
    def _combine_sentiments(self, sentiments: List[Dict]) -> Dict:
        """Combine multiple sentiment sources into overall sentiment"""
        try:
            if not sentiments:
                return {'score': 0.0, 'normalized_score': 0.5, 'classification': 'neutral'}
            
            # Weight different sentiment sources
            weights = {
                'social_media': 0.25,
                'news': 0.25,
                'fear_greed_index': 0.30,
                'market_metrics': 0.20
            }
            
            weighted_scores = []
            total_weight = 0
            
            for sentiment in sentiments:
                if sentiment and 'normalized_score' in sentiment:
                    source = sentiment.get('source', 'unknown')
                    weight = weights.get(source, 0.1)
                    weighted_scores.append(sentiment['normalized_score'] * weight)
                    total_weight += weight
            
            if total_weight == 0:
                combined_score = 0.5
            else:
                combined_score = sum(weighted_scores) / total_weight
            
            # Classification
            if combined_score < 0.2:
                classification = 'very_bearish'
            elif combined_score < 0.4:
                classification = 'bearish'
            elif combined_score < 0.6:
                classification = 'neutral'
            elif combined_score < 0.8:
                classification = 'bullish'
            else:
                classification = 'very_bullish'
            
            return {
                'score': (combined_score - 0.5) * 2,  # Convert to -1 to 1 scale
                'normalized_score': combined_score,
                'classification': classification
            }
            
        except Exception as e:
            logger.warning(f"Sentiment combination error: {e}")
            return {'score': 0.0, 'normalized_score': 0.5, 'classification': 'neutral'}
    
    def _calculate_sentiment_confidence(self, sentiments: List[Dict]) -> float:
        """Calculate confidence in sentiment analysis"""
        try:
            if not sentiments:
                return 0.1
            
            # Check data availability and consistency
            valid_sentiments = [s for s in sentiments if s and 'normalized_score' in s]
            data_availability = len(valid_sentiments) / len(sentiments)
            
            if len(valid_sentiments) < 2:
                return 0.3
            
            # Check consistency (lower variance = higher confidence)
            scores = [s['normalized_score'] for s in valid_sentiments]
            variance = np.var(scores)
            consistency_score = max(0, 1 - variance * 4)  # Scale variance to confidence
            
            # Volume/engagement factors
            volume_scores = [s.get('volume', 0.5) for s in valid_sentiments if 'volume' in s]
            avg_volume = np.mean(volume_scores) if volume_scores else 0.5
            
            confidence = (data_availability * 0.4 + 
                         consistency_score * 0.4 + 
                         avg_volume * 0.2)
            
            return max(0.1, min(1.0, confidence))
            
        except Exception as e:
            logger.warning(f"Sentiment confidence calculation error: {e}")
            return 0.3
    
    def _generate_sentiment_recommendations(self, sentiment: Dict) -> Dict:
        """Generate trading recommendations based on sentiment"""
        try:
            score = sentiment.get('normalized_score', 0.5)
            classification = sentiment.get('classification', 'neutral')
            
            recommendations = {
                'bias': 'neutral',
                'strength': 'medium',
                'suggested_action': 'hold',
                'risk_adjustment': 'none',
                'alerts': []
            }
            
            if classification == 'very_bullish':
                recommendations.update({
                    'bias': 'bullish',
                    'strength': 'strong',
                    'suggested_action': 'buy',
                    'risk_adjustment': 'increase_position',
                    'alerts': ['Very bullish sentiment detected across multiple sources']
                })
            elif classification == 'bullish':
                recommendations.update({
                    'bias': 'bullish',
                    'strength': 'medium',
                    'suggested_action': 'buy',
                    'risk_adjustment': 'slight_increase',
                    'alerts': ['Bullish sentiment detected']
                })
            elif classification == 'very_bearish':
                recommendations.update({
                    'bias': 'bearish',
                    'strength': 'strong',
                    'suggested_action': 'sell',
                    'risk_adjustment': 'reduce_position',
                    'alerts': ['Very bearish sentiment - consider reducing exposure']
                })
            elif classification == 'bearish':
                recommendations.update({
                    'bias': 'bearish',
                    'strength': 'medium',
                    'suggested_action': 'sell',
                    'risk_adjustment': 'slight_decrease',
                    'alerts': ['Bearish sentiment detected']
                })
            
            return recommendations
            
        except Exception as e:
            logger.warning(f"Sentiment recommendations error: {e}")
            return {
                'bias': 'neutral',
                'strength': 'medium',
                'suggested_action': 'hold',
                'risk_adjustment': 'none',
                'alerts': []
            }
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached sentiment data is still valid"""
        if cache_key not in self.sentiment_cache:
            return False
        
        cache_time = self.sentiment_cache[cache_key]['timestamp']
        return datetime.now() - cache_time < self.cache_duration
    
    def _get_default_sentiment(self, pair: str, timeframe: str) -> Dict:
        """Return default sentiment when errors occur"""
        return {
            'timestamp': datetime.now(),
            'pair': pair,
            'timeframe': timeframe,
            'overall_sentiment': {'score': 0.0, 'normalized_score': 0.5, 'classification': 'neutral'},
            'social_sentiment': {'score': 0.0, 'normalized_score': 0.5, 'volume': 0.5, 'engagement': 0.5, 'trending': False, 'source': 'social_media'},
            'news_sentiment': {'score': 0.0, 'normalized_score': 0.5, 'volume': 0.5, 'importance': 0.5, 'trending_topics': [], 'source': 'news'},
            'fear_greed_index': {'value': 50, 'normalized_score': 0.5, 'classification': 'Neutral', 'timestamp': str(int(time.time())), 'source': 'fear_greed_index'},
            'market_sentiment': {'score': 0.0, 'normalized_score': 0.5, 'source': 'market_metrics'},
            'confidence_score': 0.2,
            'recommendations': {
                'bias': 'neutral',
                'strength': 'medium',
                'suggested_action': 'hold',
                'risk_adjustment': 'none',
                'alerts': ['Sentiment analysis unavailable - using neutral stance']
            }
        }