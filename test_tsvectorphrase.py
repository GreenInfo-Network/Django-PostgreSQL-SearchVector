#!/bin/env python
"""
a test of the new SearchVectorField capability, contains=''
this will use phraseto_tsquery() instead of to_tsquery() which gives very different matching
for phrase-like strings e.g. "superior court" is a phrase, not a request for "court" and/or "superior"

python manage.py runscript test_tsvectorphrase --traceback
"""

# define the two query strings. one is a phrase, the other is jumbled up so as not to be a phrase anymore
# the point here,
# is that treating the words as simple keywords means that their sequence doesn't matter,
# while treating them as a phrase means that one has matches and the other will not
PHRASE_PAIRS = [
    ("lee vining creek", "creek vining lee"),
    ("superior court", "court superior"),
    ("aqueduct model", "model aqueduct"),
]


############################################################################################################################################################


from datasystems import models

from django.db.models import F
from datasystems.django_contrib_postgres_search import SearchVector, SearchQuery, SearchRank


def run():
    for querypair in PHRASE_PAIRS:
        search_phrase = querypair[0]
        search_jumble = querypair[1]

        print("Default behavior phrase=False")
        print("This uses simple plainto_tsquery() which means that the phrase and the mixup give the exact same results")
        print("Filter for '{}' and '{}'".format(search_phrase, search_jumble))

        query1 = SearchQuery(search_phrase, config='english')
        query2 = SearchQuery(search_jumble, config='english')

        r1 = models.DocumentText.objects.annotate(rank=SearchRank(F('search'), query1)).filter(search=query1).order_by('-rank').defer('filetext', 'search')
        r2 = models.DocumentText.objects.annotate(rank=SearchRank(F('search'), query2)).filter(search=query2).order_by('-rank').defer('filetext', 'search')
        print("    Phrase: {} matches".format( len(r1) ) )
        print("    Top 3 hits:")
        for doc in r1[:3]:
            print("        {} {}".format(doc.id, doc.document.title))
    
        print("    Mixed Up: {} matches".format( len(r2) ) )
        print("    Top 3 hits:")
        for doc in r2[:3]:
            print("        {} {}".format(doc.id, doc.document.title))

        print("")

    print("")

    for querypair in PHRASE_PAIRS:
        search_phrase = querypair[0]
        search_jumble = querypair[1]

        print("With the phrase=True modifier")
        print("This uses phraseto_tsquery() which means that the phrase and the mixup give very different results")
        print("Filter for '{}' and '{}'".format(search_phrase, search_jumble))

        query1 = SearchQuery(search_phrase, config='english', phrase=True)
        query2 = SearchQuery(search_jumble, config='english', phrase=True)

        r1 = models.DocumentText.objects.annotate(rank=SearchRank(F('search'), query1)).filter(search=query1).order_by('-rank').defer('filetext', 'search')
        r2 = models.DocumentText.objects.annotate(rank=SearchRank(F('search'), query2)).filter(search=query2).order_by('-rank').defer('filetext', 'search')
        print("    Phrase: {} matches".format( len(r1) ) )
        print("    Top 3 hits:")
        for doc in r1[:3]:
            print("        {} {}".format(doc.id, doc.document.title))

        print("    Mixed Up: {} matches".format( len(r2) ) )
        print("    Top 3 hits:")
        for doc in r2[:3]:
            print("        {} {}".format(doc.id, doc.document.title))

        print("")
