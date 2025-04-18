import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from app.db.models import Record

def init_dashboard(server):
    app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/")
    app.title = "Daily Values Dashboard"

    app.layout = html.Div(style={"fontFamily": "Arial", "backgroundColor": "#f8f9fa", "padding": "40px"}, children=[
        html.Div(style={
            "maxWidth": "800px",
            "margin": "0 auto",
            "backgroundColor": "white",
            "padding": "30px",
            "borderRadius": "10px",
            "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)"
        }, children=[
            html.H2("\ud83d\udcca Daily Values Dashboard", style={"textAlign": "center", "marginBottom": "30px"}),
            dcc.Graph(id="value-chart"),
            html.Div(
                "Data is aggregated by date. The next 7 days are projected based on a linear trend.",
                style={"textAlign": "center", "fontSize": "14px", "color": "#666", "marginTop": "20px"}
            )
        ])
    ])

    @app.callback(
        Output("value-chart", "figure"),
        Input("value-chart", "id")
    )
    def update_chart(_):
        with server.app_context():
            records = Record.query.all()

        df = pd.DataFrame([{
            "timestamp": r.timestamp,
            "value": r.value
        } for r in records])

        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df_grouped = df.groupby("timestamp").sum(numeric_only=True).reset_index()

            df_grouped["day_number"] = range(len(df_grouped))
            X = df_grouped["day_number"].values.reshape(-1, 1)
            y = df_grouped["value"].values

            model = LinearRegression()
            model.fit(X, y)

            future_days = 7
            last_day = df_grouped["timestamp"].max()
            future_dates = [last_day + pd.Timedelta(days=i) for i in range(1, future_days + 1)]
            future_day_numbers = np.array(range(len(df_grouped), len(df_grouped) + future_days)).reshape(-1, 1)
            future_preds = model.predict(future_day_numbers)

            df_future = pd.DataFrame({
                "timestamp": future_dates,
                "value": future_preds
            })

            df_grouped["type"] = "Real"
            df_future["type"] = "Forecast"

            df_final = pd.concat([df_grouped[["timestamp", "value", "type"]], df_future])

            fig = px.bar(
                df_final,
                x="timestamp",
                y="value",
                color="type",
                color_discrete_map={"Real": "#007BFF", "Forecast": "orange"},
                labels={"value": "Value"},
                title="Daily Total Values with Forecast"
            )

            fig.update_layout(
                plot_bgcolor="#fff",
                paper_bgcolor="#fff",
                font=dict(color="#333", size=14),
                xaxis_title="Date",
                yaxis_title="Total Value",
                legend_title=""
            )
        else:
            fig = px.bar(title="No data found")

        return fig

    return app
