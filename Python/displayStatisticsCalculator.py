class DisplayStatisticsCalculator:
    def count_orders(self, order_products):
        order_list = self.create_list_of_unique_order_ids(order_products)
        return len(order_list)
    
    def create_list_of_unique_order_ids(self, order_products):
        order_list = []
        for order_product in order_products:
            if order_product.order_id not in order_list:
                order_list.append(order_product.order_id)
        return order_list

    def count_total_quantity(self, order_products):
        total_quantity = 0
        for order_product in order_products:
            total_quantity += order_product.quantity
        return total_quantity
    
    def calculate_quantity_per_day(self, total_quantity, total_days):
        return round(total_quantity / total_days, 2)
    
       
    def calculate_revenue_per_day(self, order_products, total_days):
        total_revenue = self.calculate_total_revenue(order_products)
        return round(float(total_revenue) / total_days, 2)

    def calculate_total_revenue(self, order_products):
        total_revenue = 0
        for order_product in order_products:
            total_revenue += order_product.revenue
        return total_revenue
    
    def calculate_precentual_difference(self, startValue, endValue):
        if endValue == 0:
            return 0
        return round(startValue / endValue * 100 - 100, 0)