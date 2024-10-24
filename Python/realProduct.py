from displayStatistics import DisplayStatistics
from scoreStatistics import ScoreStatistics
import json

class RealProduct():
    def __init__(self):
        self.name                     = ""
        self.real_product_id          = 0
        self.score                    = 0
        self.current_period_time      = ""
        self.reference_period_time    = ""
        self.current_display_stats    = DisplayStatistics()
        self.reference_display_stats  = DisplayStatistics()
        self.current_score_stats      = ScoreStatistics()
        self.reference_score_stats    = ScoreStatistics()
        self.current_order_products   = []
        self.reference_order_products = []

        
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)