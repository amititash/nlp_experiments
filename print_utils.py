'''
Library for utility functions that will be reused across all 
code for spacy and testing of NLP stuff

'''

# Set up functions to help produce human-friendly printing.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def skip_and_print(*args):
    """ Act like print(), but skip a line before printing. """
    print('\n' + str(args[0]), *args[1:])

def print_table(rows, padding=0):
    """ Print `rows` with content-based column widths. """
    col_widths = [
        max(len(str(value)) for value in col) + padding
        for col in zip(*rows)
    ]
    total_width = sum(col_widths) + len(col_widths) - 1
    fmt = ' '.join('%%-%ds' % width for width in col_widths)
    print(fmt % tuple(rows[0]))
    print('~' * total_width)
    for row in rows[1:]:
        print(fmt % tuple(row))