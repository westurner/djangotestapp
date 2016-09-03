
import collections
import functools

import jsonfield

JSONField_odict = functools.partial(
    jsonfield.JSONField,
    load_kwargs={'object_pairs_hook': collections.OrderedDict})
