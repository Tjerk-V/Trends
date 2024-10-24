from datetime import datetime

class PeriodCalculator:
    def count_days_in_period(self, start_date_string, end_date_string):
        seconds_in_period = self.calculate_total_seconds_in_period(start_date_string, end_date_string)
        return self.get_days_from_seconds(seconds_in_period)
    
    def calculate_total_seconds_in_period(self, start_date_string, end_date_string):
        start_date = self.parse_date_string(start_date_string)
        end_date = self.parse_date_string(end_date_string)
        period = end_date - start_date
        return period.total_seconds()

    def parse_date_string(self, date):
        return datetime.strptime(date, '%Y-%m-%d')
    
    def get_days_from_seconds(self, seconds):
        seconds_per_day = 60 * 60 * 24
        return seconds / seconds_per_day
