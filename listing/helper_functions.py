from listing.models import Listing
from offer.models import Offer


def listing_relatedness_v2(listing, n=4):
    result = Listing.objects.raw("""WITH Tafla as (select t.*, x.cnt_matches
from (
SELECT l.name as name1, l2.name as name2, l.id as l1_id, l2.id as l2_id, CASE
    WHEN l.seller_id=l2.seller_id THEN 1
    ELSE 0
  END
  AS same_seller,
ABS(5-ABS((l.condition_id-l2.condition_id))) as condition_likeness
from listing_listing as l
CROSS JOIN listing_listing l2
WHERE l.id =%s and l.id != l2.id) t



cross join lateral (
    select count(*) cnt_matches
    from regexp_split_to_table(lower(%s), ' ') w1(word)
    inner join regexp_split_to_table(lower(t.name2), ' ') w2(word)
        on w1.word = w2.word
) x)


SELECT l2_id as id FROM Tafla ORDER BY (cnt_matches*cnt_matches)+same_seller+condition_likeness/5 DESC LIMIT %s """, [listing.id, listing.name, n])
    for r in result:
        print(r)
    return result



def calculate_listing_relatedness(listing1, listing2):
    '''This function calculates a relatedness score for two listings.
    The relatedness score is primarily based on name similarity,
    but also takes the condition and identity of the seller.
    In the next iteration of FireSale this function should be reworked into a database query.'''
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


def most_related_products(listing1, list_of_listings, n=4):
    '''This function takes as it's input a single listing, listing1, a list of listings and an integer, n.
    It calculates the most related products from list_of_listings to listing1,
    according to the function calculate_listing_relatedness.
    It then returns the n most related listings, in order.
    If n is negative, it returns the least related listings.
    In the next iteration of FireSale, this function, along with calculate_listing_relatedness,
    should be reworked into a function using a single database query.'''
    scores = []
    for listing in list_of_listings:
        scores.append([listing.id, calculate_listing_relatedness(listing1, listing)])
    scores.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in scores[:n]]

def listing_has_accepted_offer(listing):
    return Offer.objects.all().filter(listing=listing, accepted=True).count() != 0