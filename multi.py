from tmx_scraper import *

s1 = TMXScraper(ID=1)
s2 = TMXScraper(ID=2)
s3 = TMXScraper(ID=3)

r1 = s1.scrap_pages("ABCT")
r2 = s2.scrap_pages("ABR")
r3 = s3.scrap_pages("LWRK")

print(r1)
print(r2)
print(r3)


