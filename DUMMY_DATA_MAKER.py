import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FireSale.settings")
import django
django.setup()

from listing.models import Listing, ListingImage
from offer.models import Offer
from checkout.models import PaymentInfo, ContactInfo, Purchase
from user.models import Rating
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from random import Random, choice

""" This file has some code to add dummy data to the database for testing purposes.
    In the next iteration of FireSale dummy data generation for 
    messages, purchases, users, contact_info and payment_info should be added.
    The dummy data generation for the existing models should also be improved to be consistent.
    For example offers generated should have a timestamp later than the listing they are placed on, etc.
    The data should also be given a slightly nicer feel and some ideas are added in a comment at the bottom."""


def populate_listing(n):
    """This function generates n listings for each user."""
    rand = Random()
    users = User.objects.all()
    listings = []
    listing_images = []
    word1 = ["Old", "Used", "Dirty", "Broken", "Smelly", "Terrible", "Disgusting", "Useless", "Moldy", "Filthy"]
    word2 = ["TV", "grandfather", "soap", "chair", "dildo", "steak", "pants", "cupboard", "lamp", "sock"]
    description_list = ["I have really loved using this.", "I hate this with a passion and want to get rid of it.", "It didn't use to be like this", "If I could make it better I wouldn't sell it", "My ex gave this to me. He's a cheating douche.", "ACCIDENTALLY LISTED THIS, PLEASE DON'T BUY IT!", "helo butifull i wana make marry to you butiful ladie", "How do you describe something so exquisite?", "How do you describe something so disgusting?", "If I had a penny for every time this thing got me laid...", "It kind of looks like it smells"]

    image_list = ["https://scontent-lhr8-1.xx.fbcdn.net/v/t1.6435-9/91098831_102378194756178_5553014417303535616_n.jpg?_nc_cat=109&ccb=1-6&_nc_sid=09cbfe&_nc_ohc=sh01kaK2L2EAX_WjBpL&_nc_ht=scontent-lhr8-1.xx&oh=00_AT_iZf27VSCBvdyt0t2EIIF-p5b2kwTMl_AAOLUqTFAEbg&oe=6299A874",
             "https://external-preview.redd.it/igFrDgxtwkbZo7opFHeqluSt-QFSz33NjQysEmmulOY.jpg?auto=webp&s=98adff93c2306277f1b74c1b32b51e96a19d2ac8",
             "http://3.bp.blogspot.com/_1pbE50AEwIY/THr7A0i7PMI/AAAAAAAACwE/oiaw7f8xops/s1600/IMG_20100829_140639.jpg",
             "https://cdn.pixabay.com/photo/2020/06/03/22/30/chair-5256589_960_720.jpg",
             "https://qph.fs.quoracdn.net/main-qimg-9eed1d5d67e7f5668ff4f0185062e9b7-lq",
             "https://external-preview.redd.it/Ifh35qgeruOPhlV72R0QhwrRM4Oj5PScf6OSO83GXJ4.jpg?auto=webp&s=c80c6f3d2606b90ef685e60c574cbb27ace79a9a",
             "https://i.insider.com/58ff52247522ca87088b5f02?width=1000&format=jpeg&auto=webp",
             "https://thumbs.dreamstime.com/b/old-broken-cupboard-not-used-things-160433391.jpg",
             "https://media-cdn.tripadvisor.com/media/photo-s/01/55/d6/bf/filthy-bed-side-lamp.jpg",
             "https://www.brickunderground.com/sites/default/files/blog/images/dirty-socks.jpg"]


    for user in users:
        for i in range(n):
            item = rand.randint(0,len(word2)-1)
            name = word1[rand.randint(0,len(word1)-1)] + " " + word2[item]
            description = description_list[rand.randint(0,len(description_list)-1)]
            seller = user
            image = image_list[item]
            condition = rand.randint(1, 3)
            listed = timezone.now() - datetime.timedelta(days=rand.randint(0, 365))
            available = True
            listing = Listing(name=name, description=description, seller=seller, condition=condition, listed=listed, available=available)
            listing.save()
            listing_image = ListingImage(image=image, listing=listing)
            listing_image.save()


def populate_offer(n):
    """This function generates n offers."""
    rand = Random()
    user_pks = list(User.objects.values_list('pk', flat=True))
    listing_pks = list(Listing.objects.values_list('pk', flat=True))

    for i in range(n):
        random_listing_pk = choice(listing_pks)
        listing = Listing.objects.get(pk=random_listing_pk)
        temp_user_pks = [user_pk for user_pk in user_pks if user_pk != listing.seller.id]  # We don't want a user to create offers on their own listings.
        random_user_pk = choice(temp_user_pks)
        buyer = User.objects.get(pk=random_user_pk)
        amount = rand.randint(1,100000)
        placed = timezone.now() - datetime.timedelta(days=rand.randint(0, 365))
        accepted = False
        offer = Offer(listing=listing, buyer=buyer, amount=amount, placed=placed, accepted=accepted)
        offer.save()

def populate_purchases(n, r):
    """This function accepts an offer on n listings.
    If there are less than n listings available, it accepts an offer for every listing.
    It also leaves a review with r% chance.
    In the next iteration of FireSale, this function should be improved to work better with a database that
    includes listings with 0 offers."""
    rand = Random()
    listings = Listing.objects.all().filter(available=True)[:n]
    payment_info_pks = PaymentInfo.objects.values_list('pk', flat=True)
    contact_info_pks = ContactInfo.objects.values_list('pk', flat=True)
    for listing in listings:
        offer = Offer.objects.all().filter(listing_id=listing.id).order_by('-amount').first()
        contact_info = ContactInfo.objects.get(pk=choice(contact_info_pks))# TODO: add user to contact info, select contact info from DB if offer.buyer has contact info in DB. Otherwise create new with random data.
        payment_info = PaymentInfo.objects.get(pk=choice(payment_info_pks))# TODO: add user to payment info, select payment info from DB if offer.buyer has payment info in DB. Otherwise create new with random data.
        purchase = Purchase(offer=offer, contact_info=contact_info, payment_info=payment_info)
        purchase.save()
        if rand.randint(0, 100) < r:
            rate_purchase(purchase)


def rate_purchase(purchase):
    """This function generates a rating on a specific purchase."""
    rand = Random()
    rating = rand.randint(1, 5)
    purchase = purchase
    rater = purchase.offer.buyer
    ratee = purchase.offer.listing.seller
    comment = "No comment"
    ratingmodel = Rating(rater=rater, ratee=ratee, rating=rating, comment=comment, purchase=purchase)
    ratingmodel.save()



'''Here is a more pg friendly list of words to populate the data base'''

'''
Names:
“TV”, “Sofa”, “Bed”, “Barrel”, “Lawn mower”, “Car, Laptop”, “Water bottle”, “Keyboard”, “Piano”, “Football”, “Dices”, “Runescape Account”

Adjective:
“Used”, “Hardly used”, “Brand new”, “A bit broken”, “Well worn”, “Never used”, “Smelly”, “Large”, “Tiny”, “Bright”

Small Text:
“Beautiful product that is”, “Just moved and had to sell some stuff, would highly recommend this”, “After the devastating divorce I had to sell this”, “My dog wasn’t a huge fan of my”, “Need the cash quickly so selling my,”, “Look no further, you can now finally get this,”

Image link list:
https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.samsung.com%2Fin%2Ftvs%2Ffull-hd-tv%2Fte50fa-43-inch-full-hd-smart-tv-ua43te50fakxxl%2F&psig=AOvVaw2XL5tXm5lJOq7HsFoWJfdc&ust=1652541987129000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCPDU3OXk3PcCFQAAAAAdAAAAABAT ,
http://cdn.shopify.com/s/files/1/2660/5106/products/d1rjiawy0pznxn6875ba_b6e0f2d6-0076-4a01-af48-0faf30d8c021_800x.jpg?v=1610981031 ,
https://cdn.shopify.com/s/files/1/2660/5202/products/xoir1j2ihw9b4bw2apj5_1400x.jpg?v=1633467118 ,
https://media.istockphoto.com/photos/wine-barrel-over-white-background-picture-id969515288?k=20&m=969515288&s=612x612&w=0&h=4pg8hYh6g_1vuDlgQlKKYiTSssZGpB-GZeqVXQncg8s= ,
https://www.thespruce.com/thmb/W8gAUV1qubf5UppA3AQJUiFu9VM=/1500x1500/filters:no_upscale()/_hero_SQ_Ryobi-Electric-Riding-Lawn-Mower-1-376b4abaf7534fe88d53f31e6d4778ae.jpg ,
https://www.motortrend.com/uploads/sites/10/2015/11/2015-fiat-500-pop-3door-hatchback-angular-front.png?fit=around%7C875:492.1875 ,
https://www.notebookcheck.net/uploads/tx_nbc2/MicrosoftSurfaceLaptop3-15__1__02.JPG ,
https://media.istockphoto.com/photos/water-bottle-on-white-background-picture-id1126933760?k=20&m=1126933760&s=612x612&w=0&h=XiYk9aT68Iru-OeENe1JXi0-8BU8wXKKj7dfgkbjy9A= ,
https://resource.logitech.com/content/dam/logitech/en/products/keyboards/k120/gallery/k120-gallery-01-fr.png ,
https://www.ubuy.is/productimg/?image=aHR0cHM6Ly9tLm1lZGlhLWFtYXpvbi5jb20vaW1hZ2VzL0kvODFhK3FvdVFObUwuX0FDX1NMMTUwMF8uanBn.jpg ,
https://image.cnbcfm.com/api/v1/image/106991253-1639786378304-GettyImages-1185558312r.jpg?v=1639786403 ,
https://m.media-amazon.com/images/I/71CevzRBAfL._AC_SX425_.jpg ,
https://www.account4rs.com/uploads/product/5289c9d9393485ca37fec4fdecbcb790.png ,

'''


