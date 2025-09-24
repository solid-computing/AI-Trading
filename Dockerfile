FROM freqtradeorg/freqtrade:stable

# Copy requirements and install additional dependencies
COPY requirements.txt /freqtrade/
RUN pip install -r requirements.txt

# Copy user data and configurations
COPY user_data/ /freqtrade/user_data/
COPY config.dryrun.json /freqtrade/
COPY pairs.json /freqtrade/

# Create config.live.json from template if it doesn't exist
COPY config.live.template.json /freqtrade/

# Set working directory
WORKDIR /freqtrade

# Default command
CMD ["freqtrade", "trade", "--config", "config.dryrun.json"]