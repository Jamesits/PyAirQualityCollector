# PyAirQualityCollector

A simple script to capture AQI (Air Quality Index) from [PM25.in](http://www.pm25.in/) public API and output as InfluxDB line protocol. 

## Example Site

Visit my [Grafana AQI dashboard](https://grafana.swineson.me/dashboard/db/air-quality)

Improvements & donation welcomed. Email to: aqi#public.swineson.me

## Usage

1. Request a new API key from [PM25.in API](http://www.pm25.in/api_doc)
2. Clone this repo
3. Fill API key to `collect.py`
4. run `python3 ./collect.py`, capture `stdout` for data

Don't use public API key too frequently; it has limits. Cache the result if you need to debug other part of your program. If you are writing a scawler, 1 request every hour is enough.

### Select What to Collect

Settings are on the top of `collect.py`. Pretty self-explaining.

### Integrate with Telegraf

Add the following part to your `telegraf.conf`:

```ini
[[inputs.exec]]
  commands = ["/usr/local/src/PyAirQualityCollector/collect.py"]
  timeout = "120s"
  interval = "60m"
  data_format = "influx"
```

Then restart Telegraf.

## License

This script is provided in MIT license.