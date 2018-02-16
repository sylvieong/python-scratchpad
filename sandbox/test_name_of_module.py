from test_metaclasses import print_fn as tm_print_fn
import test_metaclasses

print(f'import test_metaclasses')
test_metaclasses.print_fn()


print(f'from test_metaclasses import print_fn as tm_print_fn')
tm_print_fn()