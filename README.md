# Simple "on call" bot for catch news from VK to Telegram
## How to use
1. Install requirements by `pip install -r requirements.txt`.
2. In file 'gen_constants.py' replace <***> by your values. Then, run it (`python3 gen_constants.py`). You'll get *.json for bot.
3. In file 'gen_communities.py' describe communities for parser. Then, run it (`python3 gen_communities.py`). You'll get the second *.json for bot.
4. From now, when you run `python3 __main__.py` the bot will send posts following rules from 'gen_constant.py'. It boring, yes, becase VK and TG have a limit for responses.
## Additional: set 'autocall' in linux
1. By `crontab -e` edit a file with cron tasks.
2. Add to it `0,10,20,30,40,50 * * * * python3 <path to __main.py__>` - this will catch news each 10 minutes.
3. Save and exit. Thats all.