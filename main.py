import time
import requests


def find_percent(last, current):
    interval = abs(last - current)
    result = (100 * interval) / last

    return result


def main():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

    last_prices = []  # Empty list to store prices in the last 60 minutes, 1 request in 1 second so 3600 price in 1 hour

    while True:
        # Get the price
        response = requests.get(url=url)
        last_prices.append(float(response.json()['price']))

        if len(last_prices) >= 2:

            last_price = last_prices[0]
            current_price = last_prices[-1]

            # Clearing the list to only have prices for the last 60 minutes
            if len(last_prices) == 3600:
                del last_prices[0]

            # Follow the price movement
            if last_price:
                percent_change = find_percent(last_price, current_price)
                print(f'{percent_change}')
                if percent_change > 1:
                    print(f"Price has changed by {percent_change}% in the last 1 hour."
                          f"\nFrom {last_prices[0]} -> {last_prices[-1]} ")
                    last_prices.clear()

            # Wait for the next iteration
            time.sleep(1)


if __name__ == '__main__':
    main()
