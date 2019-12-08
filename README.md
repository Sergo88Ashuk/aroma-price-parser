# aroma-price-parser

This is the web scrapper, developed to get prices of components used for handmade stuff produced by my wife.
The idea is to asynchronously get the web pages for components with prices by the means of aiohttp in one process and to pass the html contets to another process. Where this html is parsed by means of beautiful_soup4.
This scrapper cannot be used for any other tasks except scrapping the pages of some particular shops, because each shop has different html layout.
