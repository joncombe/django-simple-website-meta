django-simple-website-meta
====

If you type a URL into most social media apps, they automatically give you a preview to that website address. I needed that, and I needed it now. Zero frills. Hence the word "simple" in the title.

This tiny, tiny app uses [jvanasco](https://github.com/jvanasco)'s excellent [metadata_parser](https://github.com/jvanasco/metadata_parser) library (and it's default settings) to return a dict of just four fields:
 - description
 - image
 - title
 - canonical_url

Any missing field will have the value `None`. If the requested URL is unparseable for any reason at all, a simple `None` is returned instead of a dict.

Results are stored in your database. In theory, only the first ever request for each URL should be "fetched" once over the internet (slow), but subsequent ones will be available straight from the database (fast).

## Install

- Add `'simplewebsitemeta'` to your `settings.py` `INSTALLED_APPS`
- Run `python manage.py migrate` to add the one database table
- Retrieve the dict as follows:

   ```
   from simplewebsitemeta.models import SimpleWebsiteMeta

   SimpleWebsiteMeta.objects.get_url('http://example.com')
   ```

## Things to note

- Tested on Django 2.1 and Python 3.5. Probably works on much earlier versions too.

- Pass an optional [headers](http://docs.python-requests.org/en/master/user/quickstart/#custom-headers) dict to the `get_url()` command. I've found some popular websites were 403'ing requests, easily circumvented by passing a user agent, e.g.:

   ```
   SimpleWebsiteMeta.objects.get_url('http://example.com', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
   ```

- The amount of code here is tiny: if you want this app to do anything peculiar to your needs, it is likely easier to copy and paste this app's code into your own app and adjust it to your needs, rather than ask me to create a one-size-fits-all app.

- Maybe you only want to store the results for a limited duration? One solution would be to run a scheduled task (e.g a cronjob) to remove older values from the database, e.g.
    ```
    SimpleWebsiteMeta.objects.filter(created__lt=my_cutoff_datetime).delete()
    ```
