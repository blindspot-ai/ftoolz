from cytoolz import curry

import ftoolz.itertoolz as it

associate = curry(it.associate)
associate_to = curry(it.associate_to)
collect = curry(it.collect)
empty = curry(it.empty)
enumerate_with_final = curry(it.enumerate_with_final)
filter_not_none = curry(it.filter_not_none)
find = curry(it.find)
first = curry(it.first)
