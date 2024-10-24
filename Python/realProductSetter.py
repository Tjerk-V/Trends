from realProduct import RealProduct
from database import Database
from orderProduct import OrderProduct
from periodCalculator import PeriodCalculator
from displayStatisticsCalculator import DisplayStatisticsCalculator
from scoreStatisticsCalculator import ScoreStatisticsCalculator

class RealProductSetter():
    def __init__(self):
        self.database = Database()
        self.period_calculator = PeriodCalculator()
        self.display_statistics_calculator = DisplayStatisticsCalculator()
        self.score_statisticts_calculator = ScoreStatisticsCalculator()
    
    def get_real_products(self, current_start_date, current_end_date, reference_start_date, reference_end_date):
        self.current_period_time = current_start_date + "/" + current_end_date
        self.reference_period_time = reference_start_date + "/" + reference_end_date

        self.days_in_current_period = self.period_calculator.count_days_in_period(current_start_date, current_end_date)
        self.days_in_reference_period = self.period_calculator.count_days_in_period(reference_start_date, reference_end_date)

        query_current = self.get_query_string(current_start_date, current_end_date)
        query_reference = self.get_query_string(reference_start_date, reference_end_date)


        current_data = self.database.run_query(query_current)
        reference_data = self.database.run_query(query_reference)
        
        return self.create_real_products(current_data, reference_data)

    def get_query_string(self, start_date, end_date):
        return """SELECT o.order_id, 
                         p.quantity,
                         p.real_product_id,
                         p.product_description AS NAME,
                         p.product_price_ex * p.quantity AS revenue

                  FROM orders o
                  JOIN order_products p ON o.order_id = p.order_id

                  WHERE o.order_date >= '"""+start_date+"""'
                    AND o.order_date < '"""+end_date+"""'
                    AND p.real_product_id NOT IN (11869, 11804)
                    ;""" 
    def create_real_products(self, current_data, reference_data):
        real_products = {}

        self.process_cursor_current(real_products, current_data)
        self.process_cursor_reference(real_products, reference_data)
        self.finish_statistics(real_products)
        return real_products

    def process_cursor_current(self, real_products, items):
        for item in items:
            real_product_id = item[2]
            name            = item[3]
            order_id        = item[0]
            quantity        = item[1]
            revenue         = item[4]
            real_product    = self.get_or_create_real_product(real_products, real_product_id, name)
            order_Product   = self.create_order_product(order_id, quantity, revenue)
            real_product.current_order_products.append(order_Product)

    def process_cursor_reference(self, real_products, items):
        for item in items:
            real_product_id = item[2]
            name            = item[3]
            order_id        = item[0]
            quantity        = item[1]
            revenue         = item[4]
            realProduct     = self.get_or_create_real_product(real_products, real_product_id, name)
            order_Product   = self.create_order_product(order_id, quantity, revenue)
            realProduct.reference_order_products.append(order_Product)
    
    def get_or_create_real_product(self, real_products, real_product_id, name):
        if real_product_id in real_products:
            real_product = real_products[real_product_id]
        else:
            real_product = self.create_real_product(real_product_id, name)
            real_products[real_product_id] = real_product
        return real_product
        
    def create_real_product(self, real_product_id, name):
        real_product                       = RealProduct()
        real_product.real_product_id       = int(real_product_id)
        real_product.current_period_time   = self.current_period_time
        real_product.reference_period_time = self.reference_period_time
        real_product.name                  = name
        return real_product
    
    def create_order_product(self, order_id, quantity, revenue):
        order_product          = OrderProduct()
        order_product.order_id = int(order_id)
        order_product.quantity = int(quantity)
        order_product.revenue  = float(revenue)
        return order_product

    def finish_statistics(self, real_products):
        for key in real_products:
            real_product = real_products[key]
            self.finish_real_product_statistics(real_product)

    def finish_real_product_statistics(self, real_product):
        real_product.current_display_stats.totalOrders      = self.display_statistics_calculator.count_orders(real_product.current_order_products)
        real_product.reference_display_stats.totalOrders    = self.display_statistics_calculator.count_orders(real_product.reference_order_products)
        real_product.current_display_stats.totalQuantity    = self.display_statistics_calculator.count_total_quantity(real_product.current_order_products)
        real_product.reference_display_stats.totalQuantity  = self.display_statistics_calculator.count_total_quantity(real_product.reference_order_products)
        real_product.current_display_stats.quantityPerDay   = self.display_statistics_calculator.calculate_quantity_per_day(real_product.current_display_stats.totalQuantity, self.days_in_current_period)
        real_product.reference_display_stats.quantityPerDay = self.display_statistics_calculator.calculate_quantity_per_day(real_product.reference_display_stats.totalQuantity, self.days_in_reference_period)
        real_product.current_display_stats.revenuePerDay    = self.display_statistics_calculator.calculate_revenue_per_day(real_product.current_order_products, self.days_in_current_period)
        real_product.reference_display_stats.revenuePerDay  = self.display_statistics_calculator.calculate_revenue_per_day(real_product.reference_order_products, self.days_in_reference_period)

        real_product.current_display_stats.quantityPerDayChange = self.display_statistics_calculator.calculate_precentual_difference(real_product.current_display_stats.quantityPerDay, real_product.reference_display_stats.quantityPerDay)
        #real_product.current_display_stats.totalQuantityChange  = self.display_statistics_calculator.calculate_precentual_difference(real_product.current_display_stats.totalQuantity, real_product.reference_display_stats.totalQuantity)
        
        weeks_in_reference_period = self.days_in_reference_period / 7
        weeks_in_current_period = self.days_in_current_period / 7
        difference_in_weeks = weeks_in_reference_period / weeks_in_current_period
        real_product.current_display_stats.totalOrdersChange    = self.display_statistics_calculator.calculate_precentual_difference(real_product.current_display_stats.totalOrders * difference_in_weeks, real_product.reference_display_stats.totalOrders)

        real_product.current_score_stats.quantityPerDay     = self.score_statisticts_calculator.calculate_score_quantity_per_day(real_product.current_order_products, self.days_in_current_period)
        real_product.reference_score_stats.quantityPerDay   = self.score_statisticts_calculator.calculate_score_quantity_per_day(real_product.reference_order_products, self.days_in_reference_period)