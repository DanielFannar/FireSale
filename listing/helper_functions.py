def calculate_listing_relatedness(listing1, listing2):
    score = 0
    if listing1.seller == listing2.seller:
        score += 1
    score += abs(5-abs((listing1.condition.id-listing2.condition.id))/5)
    matches = 0
    words = 0
    for word in listing1.name.split():
        if word in listing2.name.split():
            matches += 1
        words += 1
    score += 2*(matches*(matches/words))
    return score


def most_related_products(listing1, list_of_listings, n):
    scores = []
    for listing in list_of_listings:
        scores.append([listing.id, calculate_listing_relatedness(listing1, listing)])
    scores.sort(key=lambda x: x[1])
    return [item[0] for item in scores[:n]]
