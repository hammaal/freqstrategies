# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy as np


# --------------------------------


class Rsiqui(IStrategy):
    # Random ROI chosen
    minimal_roi = {
        "0": 0.10,
    }

    # Random stoploss
    stoploss = -0.25

    timeframe = '5m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Calculates slope of the RSI
        dataframe['rsi_gra'] = np.gradient(dataframe['rsi'], 60)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Buy signal generated when RSI lower than 30 and the slope becomes positive.
        dataframe.loc[
            (
                    (dataframe['rsi'] < 30) &
                    qtpylib.crossed_above(dataframe['rsi_gra'], 0)

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Sell signal generated when RSI above 60 and the slope becomes negative.
        dataframe.loc[
            (
                    (dataframe['rsi'] > 60) &
                    qtpylib.crossed_below(dataframe['rsi_gra'], 0)

            ),
            'sell'] = 1
        return dataframe
