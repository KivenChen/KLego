"""
this module provides certain methods to remove python features as follows
- Unwrap all with statements
    - which means, to include support for the_other_side and mutex
- Unwrap all with statements
- Unwrap all important essentials

"""

from pprint import pprint
import ast
import inspect as isp
code = """
with []:
    pass
"""
pprint(
    ast.dump(ast.parse(code))
)


