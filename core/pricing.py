REGIONAL_MULTIPLIERS={"IN":1.0,"US":1.25,"GB":1.20,"DE":1.22,"SG":1.10}
PLANS=[
 {"name":"Free","price":0,"currency":"INR","period":"forever","features":["Project planner","Component catalog","Cost calculator","Saved local projects"]},
 {"name":"Premium Monthly","price":99,"currency":"INR","period":"month","features":["Everything in Free","AI generation when API is configured","Premium project tools"]},
 {"name":"Premium Annual","price":799,"currency":"INR","period":"year","features":["Everything in Free","AI generation when API is configured","Premium project tools"]},
]
def regional_price(price,country): return round(price*REGIONAL_MULTIPLIERS.get(country.upper(),1.15),2)

