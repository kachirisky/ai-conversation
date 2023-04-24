import pytz
from datetime import datetime

# Define the time zones you want to display
timezones = {
    'Eastern Time': 'US/Eastern',
    'Central Time': 'US/Central',
    'Mountain Time': 'US/Mountain',
    'Pacific Time': 'US/Pacific',
    'Mexico City Time': 'America/Mexico_City',
    'Guadalajara Time': 'America/Mexico_City'
}

# Get the current time in Guadalajara
guadalajara_time = datetime.now(pytz.timezone(timezones['Guadalajara Time']))
print(f"Current time in Guadalajara: {guadalajara_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Display the current time in the other time zones
for tz_name, tz in timezones.items():
    if tz != 'America/Mexico_City':
        tz_time = guadalajara_time.astimezone(pytz.timezone(tz))
        print(f"Current time in {tz_name}: {tz_time.strftime('%Y-%m-%d %H:%M:%S %Z')} ({tz_time.tzname()})")

