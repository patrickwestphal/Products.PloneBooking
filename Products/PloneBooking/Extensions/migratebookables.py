"""
    Correct use of this external method is to create
    a EM in a booking center then call it...
    It should be safe to call it on an already migrated booking center
"""

from Products.CMFPlone.utils import normalizeString

def migrate(self):
    """
        Migrate types and categories of bookables
        self is the booking center
    """
    bookables = self.objectValues()
    charset = self.getCharset()
    
    count = 0
    for bookable in bookables:
        try:
            if bookable.portal_type != "BookableObject":
                continue
        except AttributeError:
            ## external methods don't have any portal_type...
            continue

        oldCat = bookable.getCategory()
        cat = normalizeString(oldCat, encoding=charset)
        bookable.setCategory(cat)

        oldType = bookable.getType()
        type = normalizeString(oldType, encoding=charset)
        bookable.setType(type)
        count += 1

    return "%d bookables updated\ndon't forget to update catalog..." % count



