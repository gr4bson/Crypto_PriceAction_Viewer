import plotly.graph_objects as go

def generate_candlestick_chart(data, symbol):
    # Dane potrzebne do stworzenia wykresu świeczkowego
    candlestick_data = [
        go.Candlestick(
            x=[item.date for item in data],
            open=[round(item.open_price, 2) for item in data],
            high=[round(item.high_price, 2) for item in data],
            low=[round(item.low_price,2) for item in data],
            close=[round(item.close_price, 2) for item in data],
            name='Świeczki'
        )
    ]

    # Ustalam liczbę punktów na wykresie
    #num_points = min(20, len(data))
    #candlestick_data = candlestick_data[-num_points:]

    # Tworzę wykres
    candlestick_fig = go.Figure(data=candlestick_data)
    candlestick_fig.update_layout(
        title=symbol,
        xaxis_title="Data",
        yaxis_title="Cena",
        xaxis_rangeslider_visible=False,
        width=960,  # Ustawia rozmiar wykresu
        height=480  # Ustawia rozmiar wykresu
    )

    return candlestick_fig.to_html(full_html=False)
