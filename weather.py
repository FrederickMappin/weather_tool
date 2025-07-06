#!/usr/bin/env python3
import requests
import json
import argparse
import sys
from datetime import datetime

def get_current_weather(latitude, longitude, location_name="Unknown Location", verbose=True):
    """
    Get current weather for a given latitude and longitude using Open-Meteo API
    No API key required!
    """
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': 'true',
        'timezone': 'auto'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        current_weather = data['current_weather']
        
        # Parse and display weather information
        temperature = current_weather['temperature']
        windspeed = current_weather['windspeed']
        winddirection = current_weather['winddirection']
        weathercode = current_weather['weathercode']
        
        # Weather code meanings (simplified)
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy", 
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        weather_desc = weather_descriptions.get(weathercode, f"Weather code: {weathercode}")
        
        if verbose:
            print(f"\n🌤️  Current Weather for {location_name}")
            print(f"📍 Coordinates: {latitude}, {longitude}")
            print(f"🌡️  Temperature: {temperature}°C")
            print(f"🌤️  Condition: {weather_desc}")
            print(f"💨 Wind: {windspeed} km/h from {winddirection}°")
            print(f"🕐 Time: {current_weather['time']}")
        else:
            # Compact output for scripting
            print(f"{location_name}: {temperature}°C, {weather_desc}, Wind: {windspeed}km/h")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching weather data: {e}", file=sys.stderr)
        return None
    except KeyError as e:
        print(f"❌ Error parsing weather data: {e}", file=sys.stderr)
        return None

def get_weather_by_city(city_name, verbose=True):
    """
    Get weather by city name (requires geocoding)
    This is a simple example - you might want to use a proper geocoding service
    """
    # Some common city coordinates (you can expand this)
    city_coords = {
        'new york': (40.7128, -74.0060),
        'london': (51.5074, -0.1278),
        'paris': (48.8566, 2.3522),
        'tokyo': (35.6762, 139.6503),
        'sydney': (-33.8688, 151.2093),
        'los angeles': (34.0522, -118.2437),
        'chicago': (41.8781, -87.6298),
        'miami': (25.7617, -80.1918),
        'berlin': (52.5200, 13.4050),
        'moscow': (55.7558, 37.6176),
        'beijing': (39.9042, 116.4074),
        'mumbai': (19.0760, 72.8777),
        'toronto': (43.6532, -79.3832),
        'mexico city': (19.4326, -99.1332),
        'cairo': (30.0444, 31.2357),
        'johannesburg': (-26.2041, 28.0473)
    }
    
    city_lower = city_name.lower()
    if city_lower in city_coords:
        lat, lon = city_coords[city_lower]
        return get_current_weather(lat, lon, city_name.title(), verbose)
    else:
        print(f"❌ City '{city_name}' not found in database.", file=sys.stderr)
        if verbose:
            print("Available cities:", ", ".join(sorted(city_coords.keys())), file=sys.stderr)
        return None

def list_cities():
    """List all available cities"""
    city_coords = {
        'new york': (40.7128, -74.0060),
        'london': (51.5074, -0.1278),
        'paris': (48.8566, 2.3522),
        'tokyo': (35.6762, 139.6503),
        'sydney': (-33.8688, 151.2093),
        'los angeles': (34.0522, -118.2437),
        'chicago': (41.8781, -87.6298),
        'miami': (25.7617, -80.1918),
        'berlin': (52.5200, 13.4050),
        'moscow': (55.7558, 37.6176),
        'beijing': (39.9042, 116.4074),
        'mumbai': (19.0760, 72.8777),
        'toronto': (43.6532, -79.3832),
        'mexico city': (19.4326, -99.1332),
        'cairo': (30.0444, 31.2357),
        'johannesburg': (-26.2041, 28.0473)
    }
    
    print("Available cities:")
    for city in sorted(city_coords.keys()):
        lat, lon = city_coords[city]
        print(f"  {city.title():<15} ({lat:7.4f}, {lon:8.4f})")

def main():
    parser = argparse.ArgumentParser(
        description="Get current weather information using the Open-Meteo API",
        epilog="Examples:\n"
               "  %(prog)s --city London\n"
               "  %(prog)s --coords 40.7128 -74.0060 --name \"New York\"\n"
               "  %(prog)s --city Tokyo --compact\n"
               "  %(prog)s --list-cities",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create mutually exclusive group for city vs coordinates
    location_group = parser.add_mutually_exclusive_group(required=True)
    
    location_group.add_argument(
        '--city', '-c',
        help='Get weather for a city by name'
    )
    
    location_group.add_argument(
        '--coords', '-C',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Get weather for specific coordinates (latitude longitude)'
    )
    
    location_group.add_argument(
        '--list-cities', '-l',
        action='store_true',
        help='List all available cities'
    )
    
    parser.add_argument(
        '--name', '-n',
        help='Custom name for the location (only used with --coords)'
    )
    
    parser.add_argument(
        '--compact', '-q',
        action='store_true',
        help='Show compact output (useful for scripting)'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output raw JSON data'
    )
    
    args = parser.parse_args()
    
    # Handle list cities
    if args.list_cities:
        list_cities()
        return 0
    
    # Determine verbosity
    verbose = not args.compact and not args.json
    
    # Get weather data
    weather_data = None
    
    if args.city:
        weather_data = get_weather_by_city(args.city, verbose)
    elif args.coords:
        lat, lon = args.coords
        location_name = args.name or f"Coordinates ({lat}, {lon})"
        weather_data = get_current_weather(lat, lon, location_name, verbose)
    
    # Handle JSON output
    if args.json and weather_data:
        print(json.dumps(weather_data, indent=2))
    
    # Return exit code
    return 0 if weather_data else 1

def interactive_mode():
    """Legacy interactive mode for backwards compatibility"""
    print("🌍 Weather App using Open-Meteo API")
    print("💡 Tip: Use command line arguments for faster access!")
    print("    Example: python weather.py --city London")
    
    # Get weather for New York City
    get_current_weather(40.7128, -74.0060, "New York City")
    
    # Get weather by city name
    get_weather_by_city("London")
    
    # Interactive mode
    print("\n" + "="*50)
    print("Interactive Mode:")
    
    while True:
        choice = input("\nChoose option:\n1. Get weather by coordinates\n2. Get weather by city\n3. Exit\nEnter choice (1-3): ")
        
        if choice == "1":
            try:
                lat = float(input("Enter latitude: "))
                lon = float(input("Enter longitude: "))
                location = input("Enter location name (optional): ") or "Custom Location"
                get_current_weather(lat, lon, location)
            except ValueError:
                print("❌ Please enter valid numbers for coordinates")
                
        elif choice == "2":
            city = input("Enter city name: ")
            get_weather_by_city(city)
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    # If no arguments provided, run interactive mode for backwards compatibility
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        exit_code = main()
        sys.exit(exit_code)