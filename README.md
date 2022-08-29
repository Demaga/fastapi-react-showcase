# showcase

Hi! I'm Bohdan Kholodenko, and I created this small web app to show you my skills. Please note that this is work in progress ;)


## Technology

 - Backend: FastAPI
 - Frontend: React*
 - DB: PostgreSQL
 - Cache: Redis

*HTML files are served by FastAPI and React components are rendered in-browser by Babel.


## Apps

**1. Who said that?**

Mini game - you have to guess who does the quote belongs to. 
Quotes were parsed from [quotes.toscrape.com](https://quotes.toscrape.com/)
    
**2. Reddit feed**

Fetches posts from my favourite subreddits every day at 2 pm. 
Posts are sorted by rating, which is calculated by adding comments' upvotes to post upvotes. This way I can be sure the most interesting posts will be on top (including controversial ones).

**3. I hate crypto**

Fetches [coinmarketcap.com](https://coinmarketcap.com/) API for coin listings. Data is stored in local Redis server.
All colors are inverted so that coins that have decreased in value in the last 24 hours are green. I hope and wait for the day when I see all page in green.
		

## Deployment
This app is deployed on a linux-based VPS. Nginx is used as a web-server. PostgreSQL and Redis are both hosted on the same VPS.
