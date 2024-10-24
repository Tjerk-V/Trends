from realProductSetter import RealProductSetter
from scoreCalculator import ScoreCalculator
from realProductsFilter import RealProductsFilter
import realProductSerializer
import json
from datetime import datetime, timedelta

current_start_date = datetime.today() - timedelta(days=14)
current_end_date = datetime.today()
reference_start_date = current_start_date - timedelta(days=77)
reference_end_date = current_start_date

real_product_setter  = RealProductSetter()
score_calculator     = ScoreCalculator()
real_products_filter = RealProductsFilter()

real_products = real_product_setter.get_real_products(str(datetime.date(current_start_date)), str(datetime.date(current_end_date)), str(datetime.date(reference_start_date)), str(datetime.date(reference_end_date)))
real_products = real_products_filter.filter_real_products(real_products)
real_products = score_calculator.get_real_product_score(real_products)
real_products = realProductSerializer.serialize_real_products_to_json(real_products)

f = open("../realproducts.json", "w")
f.write(json.dumps(real_products, indent=4))
f.close()
