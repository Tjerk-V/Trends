class RealProductsFilter:
    def filter_real_products(self, real_products):
        filtered_real_products = {}
        for key in real_products:
            real_product = real_products[key]
            if self.should_keep_real_product(real_product):
                filtered_real_products[key] = real_product

        return filtered_real_products
    
    def should_keep_real_product(self, real_product):
        return self.has_sufficient_orders(real_product) and self.has_sufficient_revenue(real_product)
    
    def has_sufficient_orders(self, real_product):
        return real_product.reference_display_stats.totalOrders > 15
    
    def has_sufficient_revenue(self, real_product):
        return real_product.reference_display_stats.revenuePerDay > 10 and real_product.current_display_stats.revenuePerDay > 10
