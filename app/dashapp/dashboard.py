import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
from app.db.models import Record
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def init_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/")
    app.title = "Data Forecast Dashboard"

    app.layout = html.Div(style={"fontFamily": "Arial", "backgroundColor": "#f8f9fa", "padding": "40px"}, children=[
        html.Div(style={
            "maxWidth": "900px",
            "margin": "0 auto",
            "backgroundColor": "white",
            "padding": "30px",
            "borderRadius": "10px",
            "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)"
        }, children=[
            html.H2("📊 Daily Value Forecast Dashboard", style={"textAlign": "center", "marginBottom": "30px"}),

            dcc.Graph(id="grafico-valores"),  # Linear
            dcc.Graph(id="grafico-holt"),     # Holt-Winters
            dcc.Graph(id="comparison-graph"), # Comparison

            html.Div("The first chart shows a 7-day projection using linear regression. "
                     "The second uses Holt-Winters Exponential Smoothing. "
                     "The third compares both models visually.",
                     style={"textAlign": "center", "fontSize": "14px", "color": "#666", "marginTop": "20px"})
        ])
    ])

    @app.callback(
        Output("grafico-valores", "figure"),
        Output("grafico-holt", "figure"),
        Output("comparison-graph", "figure"),
        Input("grafico-valores", "id")
    )
    def update_graphs(_):
        with server.app_context():
            records = Record.query.all()

        df = pd.DataFrame([{
            "timestamp": r.timestamp,
            "value": r.value
        } for r in records])

        if df.empty:
            return px.bar(title="No data found"), px.bar(), px.line()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df_grouped = df.groupby("timestamp").sum(numeric_only=True).reset_index()

        # == Linear Regression ==
        df_grouped["day_number"] = range(len(df_grouped))
        X = df_grouped["day_number"].values.reshape(-1, 1)
        y = df_grouped["value"].values

        model_linear = LinearRegression()
        model_linear.fit(X, y)

        future_days = 7
        last_day = df_grouped["timestamp"].max()
        future_dates = [last_day + pd.Timedelta(days=i) for i in range(1, future_days + 1)]
        future_day_numbers = np.array(range(len(df_grouped), len(df_grouped) + future_days)).reshape(-1, 1)
        future_preds_linear = model_linear.predict(future_day_numbers)

        df_future_linear = pd.DataFrame({
            "timestamp": future_dates,
            "value": future_preds_linear,
            "type": "Forecast"
        })
        df_grouped["type"] = "Observed"
        df_linear = pd.concat([df_grouped[["timestamp", "value", "type"]], df_future_linear])

        fig_linear = px.bar(df_linear, x="timestamp", y="value", color="type",
                            color_discrete_map={"Observed": "#007BFF", "Forecast": "orange"},
                            title="Linear Regression Forecast (Next 7 Days)")
        fig_linear.update_layout(xaxis_title="Date", yaxis_title="Value")

        # == Holt-Winters ==
        df_hw = df_grouped.copy()
        df_hw.set_index("timestamp", inplace=True)
        model_hw = ExponentialSmoothing(df_hw["value"], trend="add", seasonal=None)
        fitted_hw = model_hw.fit()
        forecast_hw = fitted_hw.forecast(future_days)

        df_future_hw = pd.DataFrame({
            "timestamp": future_dates,
            "value": forecast_hw,
            "type": "Forecast"
        })
        df_grouped["type"] = "Observed"
        df_holt = pd.concat([df_grouped[["timestamp", "value", "type"]], df_future_hw])

        fig_holt = px.bar(df_holt, x="timestamp", y="value", color="type",
                          color_discrete_map={"Observed": "#6c757d", "Forecast": "green"},
                          title="Holt-Winters Forecast (Next 7 Days)")
        fig_holt.update_layout(xaxis_title="Date", yaxis_title="Value")

        # == Comparison Chart ==
        df_grouped["model"] = "Observed"
        df_linear_cmp = df_future_linear.copy()
        df_linear_cmp["model"] = "Linear Regression"
        df_hw_cmp = df_future_hw.copy()
        df_hw_cmp["model"] = "Holt-Winters"

        df_comparison = pd.concat([
            df_grouped[["timestamp", "value", "model"]],
            df_linear_cmp[["timestamp", "value", "model"]],
            df_hw_cmp[["timestamp", "value", "model"]]
        ])

        fig_comparison = px.line(df_comparison, x="timestamp", y="value", color="model", markers=True,
                                 title="Forecast Comparison: Linear vs Holt-Winters")
        fig_comparison.update_layout(xaxis_title="Date", yaxis_title="Value")

        return fig_linear, fig_holt, fig_comparison

    return app