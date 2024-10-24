import mysql.connector
import json

class kpi():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="",
            user="",
            passwd="",
            database=""
            )
        
    def get_data(self):
        return self.compare_batches(self.get_first_batch(), self.get_second_batch())

    def get_first_batch(self):
        query = ("SELECT op.real_product_id, op.product_description, SUM(op.quantity) AS aantal,ROUND(SUM(op.quantity*product_price_ex* ((100 - product_discount_percentage)/100))) AS omzet,ROUND(SUM(op.quantity*product_price_ex* ((100 - product_discount_percentage)/100))) - ROUND(SUM(op.quantity*product_purchase_price_ex))  AS `bruto winst`, COUNT(o.order_id) AS orders FROM order_products op LEFT JOIN orders o ON o.order_id = op.order_id WHERE o.order_date > NOW() - INTERVAL 14 DAY AND  op.real_product_id  NOT IN (11804,192999) GROUP BY op.real_product_id ORDER BY orders DESC")
        cursor = self.mydb.cursor()
        cursor.execute(query)
        products = []
        for item in cursor:
            product = {
                "Real_ID" : str(item[0]),
                "Desc"    : str(item[1]),
                "Aantal"  : int(item[2]),
                "Omzet"  : int(item[3]),
                "Orders"  : int(item[5])
            }
            products.append(product)
        return products
    
    def get_second_batch(self):
        query = ("SELECT op.real_product_id, op.product_description, SUM(op.quantity) AS aantal,ROUND(SUM(op.quantity*product_price_ex* ((100 - product_discount_percentage)/100))) AS omzet,ROUND(SUM(op.quantity*product_price_ex* ((100 - product_discount_percentage)/100))) - ROUND(SUM(op.quantity*product_purchase_price_ex))  AS `bruto winst`, COUNT(o.order_id) AS orders FROM order_products op LEFT JOIN orders o ON o.order_id = op.order_id WHERE o.order_date > NOW() - INTERVAL 84 DAY AND  op.real_product_id  NOT IN (11804,192999) GROUP BY op.real_product_id ORDER BY orders DESC")
        cursor = self.mydb.cursor()
        cursor.execute(query)
        products = []
        for item in cursor:
            product = {
                "Real_ID" : str(item[0]),
                "Desc"    : str(item[1]),
                "Aantal"  : int(item[2]),
                "Omzet"   : int(item[3]),
                "Orders"  : int(item[5])
            }
            products.append(product)
        products1 = self.get_first_batch()
        for prod1 in products1:
            for prod2 in products:
                if prod1["Real_ID"] == prod2["Real_ID"]:
                    prod2["Aantal"] - prod1["Aantal"]
                    prod2["Orders"] - prod1["Orders"]
                    prod2["Omzet"] - prod1["Omzet"]
        return products
    
    def compare_batches(self, prods1, prods2):
        products = []
        scores = self.get_difference(self.get_first_batch(), self.get_second_batch())
        for prod1 in prods1:
            for prod2 in prods2:
                if prod1["Real_ID"] == prod2["Real_ID"]:
                    for score in scores:
                        if prod1["Real_ID"] == score["ID"]:
                            productScore = score["Score"]
                    product = {
                        "Real_ID" : prod1["Real_ID"],
                        "Desc"    : prod1["Desc"],
                        "Score"   : productScore
                    }
                    weekPD = {
                        "Naam"   : "WeekPD",
                        "Aantal" : round(prod1["Aantal"] / 14, 2),
                        "Omzet"  : round(prod1["Omzet"] / 14, 2),
                    }
                    weekFull= {
                        "Naam"   : "WeekFull",
                        "Aantal" : prod1["Aantal"],
                        "Orders" : prod1["Orders"]
                    }
                    monthPD = {
                        "Naam"   : "MonthPD",
                        "Aantal" : round(prod2["Aantal"] / 70, 2),
                        "Omzet"  : round(prod2["Omzet"] / 70, 2),
                        
                    }
                    monthFull= {
                        "Naam"   : "MonthFull",
                        "Aantal" : prod2["Aantal"],
                        "Orders" : prod2["Orders"]
                    }
                    details = [weekPD, weekFull, monthPD, monthFull]
                    product["Details"] = details
                    #if :
                    if monthFull["Orders"] > 5 and monthPD["Omzet"] > 10 and weekPD["Omzet"] > 10:
                        #realProducts = RealProduct(product["Real_ID"], product["Desc"])
                        #realProducts.set_week_stats(weekPD["Aantal"], weekFull["Aantal"], weekFull["Orders"])
                        #realProducts.set_month_stats(monthPD["Aantal"], monthFull["Aantal"], monthFull["Orders"])
                        products.append(products)
        return products


    def get_difference(self, week, month):
        products = []
        for prod1 in week:
            for prod2 in month:
                if prod1["Real_ID"] == prod2["Real_ID"]:
                    product = {
                        "ID"  : prod1["Real_ID"]
                    }
                    rel = 0
                    if prod1["Aantal"] != 0:
                        rel = prod2["Aantal"] / prod1["Aantal"]
                    product["Rel"] = rel
                    abs = 0
                    if prod1["Aantal"] != 0:
                        abs = prod2["Aantal"] - prod1["Aantal"]
                    product["Abs"] = abs
                    products.append(product)
        self.get_score(self.bubble_sort(products, "Rel", True), "Rel")
        self.get_score(self.bubble_sort(products, "Abs", True), "Abs")
        for product in products:
            score = product["RelScore"] + product["AbsScore"] *2
            product["Score"] = score
        return products
        
    def get_score(self, _list, key):
        scoreKey = key + "Score"
        for i in range(len(_list)):
            if i == 0:
                _list[0][scoreKey] = 1
            elif i == len(_list) - 1:
                _list[i][scoreKey] = 0
            else:
                lastIndex = len(_list)-1
                lowestValue = _list[lastIndex][key]
                currentValue = _list[i][key]
                highestValue = _list[0][key]
                _list[i][scoreKey] = (currentValue - lowestValue) / (highestValue - lowestValue)
    
    def bubble_sort(self, array, key, reverse=False):
        '''
        Uses the bubble sorting algorithm to sort

        Parameters:
            array (list): A list with dictionaries items
            key (string): Wich value to sort by
            reverse (bool, optional): Wether to sort the array in ascending(default) or descending order
        '''
        n = len(array)

        for i in range(n):
            already_sorted = True

            for j in range(n - i - 1):
                value1 = float(array[j][key])
                value2 = float(array[j + 1][key])
                if reverse:
                    if value1 < value2:
                        array[j], array[j + 1] = array[j + 1], array[j]
                        already_sorted = False
                else:
                    if value1 > value2:
                        array[j], array[j + 1] = array[j + 1], array[j]
                        already_sorted = False

            if already_sorted:
                break

        return array

        
k = kpi()
products = k.get_data()
f = open("./kpiData.json", "w")
f.write(json.dumps(products, indent=2))
f.close()