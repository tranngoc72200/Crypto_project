from ta.trend import MACD 
from ta.momentum import StochasticOscillator 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
def plot_graph(df):
        # MACD 
        macd = MACD(close=df['Close'], 
                window_slow=26,
                window_fast=12, 
                window_sign=9)
        # Stochastic
        stoch = StochasticOscillator(high=df['High'],
                                close=df['Close'],
                                low=df['Low'],
                                window=14, 
                                smooth_window=3)
        fig= go.Figure()
        # add subplot properties when initializing fig variable ***don't forget to import plotly!!!***
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.7, 0.3])
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        # Plot price data on the 1st subplot (using code from last article)
        fig.add_trace(go.Candlestick(x=df.index, 
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'], name='market data'))
        fig.add_trace(go.Scatter(x=df.index, 
                                y=df['MA5'], 
                                opacity=0.7, 
                                line=dict(color='blue', width=2), 
                                name='MA 5'))
        fig.add_trace(go.Scatter(x=df.index, 
                                y=df['MA20'], 
                                opacity=0.7, 
                                line=dict(color='orange', width=2), 
                                name='MA 20'))
        # # Plot volume trace on 2nd row in our figure
        # fig.add_trace(go.Bar(x=df.index, 
        #                 y=df['Volume']
        #                 ), row=2, col=1)
        # # Plot MACD trace on 3rd row
        # fig.add_trace(go.Bar(x=df.index, 
        #                 y=macd.macd_diff()
        #                 ), row=3, col=1)
        # fig.add_trace(go.Scatter(x=df.index,
        #                         y=macd.macd(),
        #                         line=dict(color='black', width=2)
        #                         ), row=3, col=1)
        # fig.add_trace(go.Scatter(x=df.index,
        #                         y=macd.macd_signal(),
        #                         line=dict(color='blue', width=1)
        #                         ), row=3, col=1)
        # # Plot stochastics trace on 4th row
        # fig.add_trace(go.Scatter(x=df.index,
        #                         y=stoch.stoch(),
        #                         line=dict(color='black', width=1)
        #                         ), row=4, col=1)
        # fig.add_trace(go.Scatter(x=df.index,
        #                         y=stoch.stoch_signal(),
        #                         line=dict(color='blue', width=1)
        #                         ), row=4, col=1)
        # # Update the layout by changing the figure size, hiding the legend and rangeslider
        # fig.update_layout(height=1000, width=1200, 
        #                 showlegend=False, 
        #                 xaxis_rangeslider_visible=False)
        # update y-axis label
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        # fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)
        # fig.update_yaxes(title_text="Stoch", row=4, col=1)
        # Plot volume trace on 2nd row
        colors = ['green' if row['Open'] - row['Close'] >= 0 
                else 'red' for index, row in df.iterrows()]
        fig.add_trace(go.Bar(x=df.index, 
                        y=df['Volume'],
                        marker_color=colors
                        ), row=2, col=1)
        # # Plot MACD trace on 3rd row
        # colors = ['green' if val >= 0 
        #         else 'red' for val in macd.macd_diff()]
        # fig.add_trace(go.Bar(x=df.index, 
        #                 y=macd.macd_diff(),
        #                 marker_color=colors
        #                 ), row=3, col=1)
        return fig

def plot_percent(df, data_symbol):
        fig= go.Figure()
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.01)
        X = df.Close.values
        X_open = data_symbol.Open.values
        percent = []
        for i in range(len(X)):
                percent.append(100 * (X[i] - X_open[0])/ X_open[0])   
        chart_data = pd.DataFrame(
                percent,
                columns=['Percent (%)'], index=df.index.copy())     

        fig.add_trace(go.Scatter(x=chart_data.index, 
                                y=chart_data['Percent (%)'], 
                                opacity=0.7, 
                                line=dict(color='blue', width=2), 
                                name='MA 5'))
        fig.update_yaxes(title_text="Percent (%)")
        fig.update_xaxes(title_text="Time")

        # chart_data.index = df.index
        return fig