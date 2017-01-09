# PyAirQualityCollector

A simple script to capture AQI (Air Quality Index) from [pm25.in](http://www.pm25.in/) public API and output as InfluxDB line protocol. 

## Example Site

Visit my [Grafana AQI dashboard](https://grafana.swineson.me/dashboard/db/air-quality)

Improvements & donation welcomed. Email to: aqi#public.swineson.me

## Usage

Clone this repo and run `./collect.py`. 

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