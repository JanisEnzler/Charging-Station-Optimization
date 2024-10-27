
class TimeConverter():
    
    # Takes a value in minutes and returns a string DD:HH:MM, which represents the time passed since the start of the simulation
    def convert_time_to_string(self, minutes_absolute):
        days = minutes_absolute // 1440
        hours = (minutes_absolute % 1440) // 60
        minutes = minutes_absolute % 60
        return f"{days:02}:{hours:02}:{minutes:02}"