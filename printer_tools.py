import sys

class TablePrinter:

    def __init__(self, column_count, buffer_size = 1000):
        self._column_count = column_count
        self._table_width = 0
        self._format_str_row = ""
        self._buffered_printer = BufferedPrinter(buffer_size)
        self._column_headers = tuple()
        self._column_alignments = tuple(['^']*column_count)

    def begin(self):
        self._buffered_printer.print_buffered("-" * self._table_width)
        self._buffered_printer.print_buffered(self._format_str_row.format(*self._column_headers))
        self._buffered_printer.print_buffered("-" * self._table_width)

    def end(self):
        self._buffered_printer.print_buffered("-" * self._table_width)
        self._buffered_printer.flush()

    def set_column_headers(self, *args):
        self._column_headers = args

    def set_column_alignments(self, *args):
        self._column_alignments = args

    def set_column_widths(self, *args):
        format_str = ("{{{{:{}{{}}}}}}|" * len(args)).format(*self._column_alignments)
        self._format_str_row = format_str.format(*args)
        self._table_width = sum(args) + len(args)

    def append_row(self, *args):
        self._buffered_printer.print_buffered(self._format_str_row.format(*args))

class BufferedPrinter:
    def __init__(self, max_buffer_size):
        self._max_buffer_size = max_buffer_size
        self.buffer = []

    def set_max_buffer_size(self, max_buffer_size):
        self._max_buffer_size = max_buffer_size

    def flush(self, file = sys.stdout):
        print(''.join(self.buffer), end = '', file = file)
        self.buffer = []

    def print_buffered(self, *args, sep = ' ', end = '\n', file = sys.stdout, flush = False):
        self.buffer.append(sep.join(args) + end)
        if len(self.buffer) == self._max_buffer_size:
            self.flush(file)


def main():
    demo_buffered_printer()
    demo_table_printer()

def demo_buffered_printer():
    print("Following is a Demo for BufferedPrinter\n")
    buffered_printer = BufferedPrinter(30)
    for i in range(100):
        buffered_printer.print_buffered(str(i))
    buffered_printer.flush()
    print("\n")

def demo_table_printer():
    print("Following is a Demo for TablePrinter\n")
    table_printer = TablePrinter(3, 30)
    table_printer.set_column_headers("I", "SQUARE OF I", "CUBE OF I")
    table_printer.set_column_alignments('<', '^', '>')
    table_printer.set_column_widths(20, 20, 20)
    
    table_printer.begin()

    for i in range(100):
        table_printer.append_row(i, i**2, i**3)
        
    table_printer.end()

if __name__ == '__main__':
    main()
    
