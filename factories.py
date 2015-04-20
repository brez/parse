import re
from exceptions import UnknownOrAmbiguousPattern


PHONE_LENGTH, ENTRY_LENGTH, ZIP_LENGTH = (10, 5, 5)


# normalize phone string to 123-123-1231
def normalize_phone(phone):
    digits = re.sub('[^0-9]', '', phone)
    return "%s-%s-%s" % (digits[:3], digits[3:6], digits[6:])


# use a decorator to validate further
def validate(func):
    def _validate(self):
        result = func(self)
        if(len(result['zipcode']) != ZIP_LENGTH):
            raise UnknownOrAmbiguousPattern
        return result
    return _validate


class Entry(object):
    """Abstract Base Class"""
    def __init__(self, select):
        self.select = select

    @validate
    def parse(self):
        if(not hasattr(self, 'pattern')):
            raise NotImplementedError
        return {
            'color': self.select[self.pattern['color']],
            'firstname': self.select[self.pattern['first']],
            'lastname': self.select[self.pattern['last']],
            'phonenumber': normalize_phone(self.select[self.pattern['phone']]),
            'zipcode': self.select[self.pattern['zip']],
            }


class AlphaEntry(Entry):
    """Represents the Alpha pattern (phone number last) for an Entry"""
    pattern = {'color': 3, 'first': 1, 'last': 0, 'phone': 2, 'zip': 4}


class BetaEntry(Entry):
    """Represents Beta pattern (number second to last) for an Entry"""
    pattern = {'color': 4, 'first': 0, 'last': 1, 'phone': 3, 'zip': 2}


class GammaEntry(Entry):
    """Represents Gamma pattern (number third to last) for an Entry"""
    pattern = {'color': 2, 'first': 0, 'last': 1, 'phone': 4, 'zip': 3}


# key is position of phone number in pattern, value is appropriate class
factories = {2: AlphaEntry, 3: BetaEntry, 4: GammaEntry}


def factory(pattern):
    matches = []
    select = list(map(str.strip, pattern.split(',')))

    # give up if things aren't what we're expecting
    if(len(select) != ENTRY_LENGTH):
        raise UnknownOrAmbiguousPattern()

    # use phone number position value to check for pattern matches
    for i in range(2, 5):
        if(len(re.sub("[^0-9]", "", select[i])) == PHONE_LENGTH):
            matches.append(i)

    # avoid ambigious match on more than one pattern
    if(len(matches) == 1):
        return factories[matches.pop()](select)

    raise UnknownOrAmbiguousPattern()
