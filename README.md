# Django-PostgreSQL-SearchVector

Finally, use `phraseto_tsquery()` in Django!

This is the django.contrib.postgres.search from Django, with a single patch to `SearchVector` to suport phrase querying.

`SearchVector(*expressions, config=None, weight=None, phrase=False)`

Setting the `phrase` parameter to `True` will treat the query as a phrase and use `phraseto_tsquery()` to treat the keywords as a phrase. If `phrase=False` which is the default, then `plainto_tsquery()` and text is treated as space-separated keywords.

## Example

When "Cheese Blue" is treated as separate keywords, it gives identical results to a search for "Blue Cheese". When treated as a phrase, "Blue Cheese" and "Cheese Blue" aren't at all the same and give different results.

```
words1 = SearchVector('Blue Cheese')
words2 = SearchVector('Cheese Blue')
phrase1 = SearchVector('Blue Cheese', phrase=True)
phrase2 = SearchVector('Cheese Blue', phrase=True)

Entry.objects.filter(search=words1)
Entry.objects.filter(search=words2)
Entry.objects.filter(search=phrase1)
Entry.objects.filter(search=phrase2)
```
