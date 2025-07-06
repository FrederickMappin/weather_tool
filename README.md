```bash
# Install dependencies
pip3 install -r requirements.txt

# Make script executable
chmod +x weather.py
```

## Usage

### Basic Commands

```bash
# Get weather for a city
./weather.py --city London
./weather.py -c "New York"

# Get weather for coordinates
./weather.py --coords 40.7128 -74.0060
./weather.py -C 51.5074 -0.1278 --name "London"

# List available cities
./weather.py --list-cities
./weather.py -l

# Get help
./weather.py --help
```

### Output Formats

```bash
# Verbose output (default)
./weather.py --city Tokyo

# Compact output (good for scripting)
./weather.py --city Tokyo --compact
./weather.py --city Tokyo -q

# JSON output (perfect for automation)
./weather.py --city Tokyo --json
./weather.py --city Tokyo -j
```

### Global Installation

If you ran the setup script and chose global installation, you can use:

```bash
weather --city London
weather --coords 40.7128 -74.0060
weather --list-cities
```

## Available Cities

The tool includes coordinates for major cities worldwide:

- New York, Los Angeles, Chicago, Miami
- London, Paris, Berlin, Moscow
- Tokyo, Beijing, Mumbai, Sydney
- Toronto, Mexico City, Cairo, Johannesburg
- And more...

Use `./weather.py --list-cities` to see all available cities with their coordinates.

## Examples

### Basic Weather Check
```bash
$ ./weather.py --city London

🌤️  Current Weather for London
📍 Coordinates: 51.5074, -0.1278
🌡️  Temperature: 18°C
🌤️  Condition: Partly cloudy
💨 Wind: 12 km/h from 230°
🕐 Time: 2025-07-05T14:30
```

### Compact Output for Scripting
```bash
$ ./weather.py --city Tokyo --compact
Tokyo: 25°C, Clear sky, Wind: 8km/h
```

### JSON Output for Automation
```bash
$ ./weather.py --city Paris --json
{
  "current_weather": {
    "temperature": 22,
    "windspeed": 15,
    "winddirection": 180,
    "weathercode": 1,
    "time": "2025-07-05T14:30"
  },
  "current_weather_units": {
    "temperature": "°C",
    "windspeed": "km/h",
    "winddirection": "°",
    "time": "iso8601"
  }
}
```

### Custom Coordinates
```bash
$ ./weather.py --coords 34.0522 -118.2437 --name "Los Angeles"

🌤️  Current Weather for Los Angeles
📍 Coordinates: 34.0522, -118.2437
🌡️  Temperature: 24°C
🌤️  Condition: Clear sky
💨 Wind: 10 km/h from 270°
🕐 Time: 2025-07-05T11:30
```

## Interactive Mode

If you run the script without arguments, it enters interactive mode:

```bash
$ ./weather.py
```

This provides a menu-driven interface for exploring the weather tool.

## Requirements

- Python 3.6+
- `requests` library (automatically installed via requirements.txt)
- Internet connection

## API Information

This tool uses the [Open-Meteo API](https://open-meteo.com/), which is:
- Completely free
- No registration required
- No API key needed
- Reliable and fast

## Troubleshooting

### Permission Denied
```bash
chmod +x weather.py
```

### Module Not Found
```bash
pip3 install -r requirements.txt
```

### Global Command Not Found
Make sure `/usr/local/bin` is in your PATH, or run the setup script again.

## Contributing

Feel free to add more cities to the `city_coords` dictionary in the script, or integrate a proper geocoding service for unlimited city support.

## License

This project is open source and available under the MIT License.
