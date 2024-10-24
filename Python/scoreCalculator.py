import dictionarySorter

class ScoreCalculator():  
    def get_real_product_score(self, real_products):
        self.add_relative_score(real_products)
        self.add_absolute_score(real_products)
        return real_products
    
    def add_relative_score(self, real_products):
        relative_differences = []
        for key in real_products:
            real_product = real_products[key]
            relative_difference = self.calculate_relative_difference(real_product.current_score_stats.quantityPerDay, real_product.reference_score_stats.quantityPerDay)
            relative_differences.append(self.create_difference_dict(real_product.real_product_id, relative_difference))
        relative_differences = dictionarySorter.sort(relative_differences, key="Difference")
        relative_differences = self.calculate_scores(relative_differences)
        self.set_product_scores(real_products, relative_differences)
    
    def add_absolute_score(self, real_products):
        absolute_differences = []
        for key in real_products:
            real_product = real_products[key]
            absolute_difference = self.calculate_absolute_difference(real_product.current_score_stats.quantityPerDay, real_product.reference_score_stats.quantityPerDay)
            absolute_differences.append(self.create_difference_dict(real_product.real_product_id, absolute_difference))
        absolute_differences = dictionarySorter.sort(absolute_differences, key="Difference")
        absolute_differences = self.calculate_scores(absolute_differences)
        self.set_product_scores(real_products, absolute_differences)

    def calculate_absolute_difference(self, current_quantity_per_day, reference_quantity_per_day):
        return abs(reference_quantity_per_day - current_quantity_per_day)
    
    def calculate_relative_difference(self, current_quantity_per_day, reference_quantity_per_day):
        absolute_difference = self.calculate_absolute_difference(current_quantity_per_day, reference_quantity_per_day)
        if reference_quantity_per_day == 0:
            return 0
        return absolute_difference / reference_quantity_per_day
    
    def set_product_scores(self, real_products, differences_list):
        for key in real_products:
            real_product = real_products[key]
            for difference in differences_list:
                if difference["Real_Product_ID"] == real_product.real_product_id:
                    real_product.score += difference["Score"]

    def calculate_scores(self, differences_list):
        for i in range(len(differences_list)):
            if i == 0:
                differences_list[0]["Score"] = 1
            elif i == len(differences_list) - 1:
                differences_list[i]["Score"] = 0
            else:
                lastIndex    = len(differences_list)-1
                lowestValue  = differences_list[lastIndex]["Difference"]
                currentValue = differences_list[i]["Difference"]
                highestValue = differences_list[0]["Difference"]
                differences_list[i]["Score"] = (currentValue - lowestValue) / (highestValue - lowestValue)
        return differences_list
    
    def create_difference_dict(self, real_product_id, difference):
        return {
            "Real_Product_ID" : real_product_id,
            "Difference"      : difference
        }
    
    
