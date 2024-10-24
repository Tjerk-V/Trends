class ScoreStatisticsCalculator:
    def calculate_score_quantity_per_day(self, order_products, total_days):
        self.sort_order_products(order_products)
        self.remove_big_orders(order_products)
        return self.calculate_quantity_per_day(order_products, total_days)
        
    
    def sort_order_products(self, order_products):
        n = len(order_products)

        for i in range(n):
            already_sorted = True

            for j in range(n - i - 1):
                value1 = float(order_products[j].quantity)
                value2 = float(order_products[j + 1].quantity)
                if value1 > value2:
                    order_products[j], order_products[j + 1] = order_products[j + 1], order_products[j]
                    already_sorted = False

            if already_sorted:
                break

        return order_products

    def remove_big_orders(self, order_products):
        #if len(order_products) >= 20:
            self.remove_top_5_precent(order_products)
        #elif len(order_products) > 1:
        #    order_products.pop()
    
    def remove_top_5_precent(self, order_products):
        remove_ammount = int(round(len(order_products) * 0.05, 0))
        for i in range(remove_ammount):
            order_products.pop()

    def calculate_quantity_per_day(self, order_products, total_days):
        if total_days == 0:
            return 0
        return self.count_total_quantity(order_products) / total_days
    
    def count_total_quantity(self, order_products):
        total_quantity = 0
        for order_product in order_products:
            total_quantity += order_product.quantity
        return total_quantity