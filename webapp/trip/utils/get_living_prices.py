from webapp.trip.models import City


def get_living_prices(city):
    """rеturnig dict with keys (below) and float prices

    Meal, Inexpensive Restaurant
    Meal for 2 People, Mid-range Restaurant, Three-course
    McMeal at McDonalds (or Equivalent Combo Meal)
    Domestic Beer (0.5 liter draught)
    Imported Beer (0.33 liter bottle)
    Cappuccino (regular)
    Coke/Pepsi (0.33 liter bottle)
    Water (0.33 liter bottle)
    Milk (regular), (1 liter)
    Loaf of Fresh White Bread (500g)
    Rice (white), (1kg)
    Eggs (regular) (12)
    Local Cheese (1kg)
    Chicken Fillets (1kg)
    Beef Round (1kg) (or Equivalent Back Leg Red Meat)
    Apples (1kg)
    Banana (1kg)
    Oranges (1kg)
    Tomato (1kg)
    Potato (1kg)
    Onion (1kg)
    Lettuce (1 head)
    Water (1.5 liter bottle)
    Bottle of Wine (Mid-Range)
    Domestic Beer (0.5 liter bottle)
    Cigarettes 20 Pack (Marlboro)
    One-way Ticket (Local Transport)
    Monthly Pass (Regular Price)
    Taxi Start (Normal Tariff)
    Taxi 1km (Normal Tariff)
    Taxi 1hour Waiting (Normal Tariff)
    Gasoline (1 liter)
    Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car)
    Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car)
    Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment
    1 min. of Prepaid Mobile Tariff Local (No Discounts or Plans)
    Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)
    Fitness Club, Monthly Fee for 1 Adult
    Tennis Court Rent (1 Hour on Weekend)
    Cinema, International Release, 1 Seat
    Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child
    International Primary School, Yearly for 1 Child
    1 Pair of Jeans (Levis 501 Or Similar)
    1 Summer Dress in a Chain Store (Zara, H&M, ...)
    1 Pair of Nike Running Shoes (Mid-Range)
    1 Pair of Men Leather Business Shoes
    Apartment (1 bedroom) in City Centre
    Apartment (1 bedroom) Outside of Centre
    Apartment (3 bedrooms) in City Centre
    Apartment (3 bedrooms) Outside of Centre
    Price per Square Meter to Buy Apartment in City Centre
    Price per Square Meter to Buy Apartment Outside of Centre
    Average Monthly Net Salary (After Tax)
    Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate
    """
    prices = City.query.filter_by(ru_name=city.lower()).first()
    return prices.living_prices
