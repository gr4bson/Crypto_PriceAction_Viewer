import plotly.graph_objects as go

def generate_candlestick_chart(data):
    # Dane potrzebne do stworzenia wykresu świeczkowego
    candlestick_data = [
        go.Candlestick(
            x=[item.date for item in data],
            open=[item.open_price for item in data],
            high=[item.high_price for item in data],
            low=[item.low_price for item in data],
            close=[item.close_price for item in data],
            name='Świeczki'
        )
    ]

    # Ustalam liczbę punktów na wykresie
    #num_points = min(20, len(data))
    #candlestick_data = candlestick_data[-num_points:]

    # Tworzę wykres
    candlestick_fig = go.Figure(data=candlestick_data)
    candlestick_fig.update_layout(
        title="Wykres świeczkowy",
        xaxis_title="Czas",
        yaxis_title="Cena",
        xaxis_rangeslider_visible=False,
    )

    return candlestick_fig.to_html(full_html=False)
