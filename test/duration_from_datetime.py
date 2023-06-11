from datetime import datetime
then = datetime(2023, 6, 5, 23, 8, 15)        # Random date in the past
now  = datetime.now()                         # Now
duration = now - then                         # For build-in functions
duration_in_s = duration.total_seconds()
days  = duration.days                         # Build-in datetime function
print("------days before-----",days)
days  = divmod(duration_in_s, 86400)[0]
print("------days after-----",days)