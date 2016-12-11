import sys

class TablePrinter:

    def __init__(self, column_count, buffer_size = 1000):
        self._column_count = column_count
        self._table_width = 0
        self._format_str_row = ""
        self._horizontal_seperator = '|'
        self._vertical_seperator = '-'
        self._column_pad = " "
        self._allow_initial_horizontal_seperator = False
        self._buffered_printer = BufferedPrinter(buffer_size)
        self._column_headers = tuple(['']*column_count)
        self._column_alignments = tuple(['^']*column_count)
        self._column_widths = tuple([0]*column_count)
        self._left_padding_widths = tuple([1]*column_count)
        self._right_padding_widths = tuple([1]*column_count)

    def begin(self):
        if self._allow_initial_horizontal_seperator is True:
            format_str = self._horizontal_seperator
        else:
            format_str = ''
        format_str = (format_str + (("{{{{:{}{{}}}}}}" + self._horizontal_seperator) * self._column_count)).format(*self._column_alignments)
        self._format_str_row = format_str.format(*self._column_widths)
        horizontal_seperator_count = self._column_count
        if self._allow_initial_horizontal_seperator is True:
            horizontal_seperator_count += 1
        self._table_width = sum(self._column_widths) + horizontal_seperator_count * len(self._horizontal_seperator)
        
        self._buffered_printer.print_buffered(self._vertical_seperator * int(self._table_width/len(self._vertical_seperator)))
        self.append_row(*self._column_headers)
        self._buffered_printer.print_buffered(self._vertical_seperator * int(self._table_width/len(self._vertical_seperator)))

    def end(self):
        self._buffered_printer.print_buffered(self._vertical_seperator * int(self._table_width/len(self._vertical_seperator)))
        self._buffered_printer.flush()

    def set_column_headers(self, *args):
        assert self._column_count == len(args)
        self._column_headers = args

    def set_column_alignments(self, *args):
        assert self._column_count == len(args)
        self._column_alignments = args

    def set_column_widths(self, *args):
        assert self._column_count == len(args)
        self._column_widths = args

    def allow_initial_horizontal_seperator(self, is_allowed):
        self._allow_initial_horizontal_seperator = is_allowed

    def set_left_padding_widths(self, *args):
        assert self._column_count == len(args)
        self._left_padding_widths = args

    def set_right_padding_widths(self, *args):
        assert self._column_count == len(args)
        self._right_padding_widths = args

    def set_padding_widths(self, *args):
        assert self._column_count == len(args)
        self._left_padding_widths = args
        self._right_padding_widths = args

    def set_horizontal_seperator(self, seperator):
        self._horizontal_seperator = seperator

    def set_vertical_seperator(self, seperator):
        self._vertical_seperator = seperator

    def _clamp_string(self, row_item, column_index):
        width = self._column_widths[column_index] - self._left_padding_widths[column_index] - self._right_padding_widths[column_index]
        row_item = str(row_item)
        if len(row_item) <= width:
            return row_item
        else:
            if width <= 3:
                ellipses_length = width
            else:
                ellipses_length = 3
            clamped_string = row_item[:width-ellipses_length] + '.'*ellipses_length
            assert len(clamped_string) == width
            return clamped_string

    def append_row(self, *args):
        assert self._column_count == len(args)
        row_item_list = []
        for i, row_item in enumerate(args):
            left_pad = self._column_pad * self._left_padding_widths[i]
            right_pad = self._column_pad * self._right_padding_widths[i]
            short_row_item = left_pad + self._clamp_string(row_item, i) + right_pad
            row_item_list.append(short_row_item)
        content = self._format_str_row.format(*row_item_list)
        self._buffered_printer.print_buffered(content)

class BufferedPrinter:
    
    def __init__(self, max_buffer_size):
        self._max_buffer_size = max_buffer_size
        self.buffer = []

    def set_max_buffer_size(self, max_buffer_size):
        self._max_buffer_size = max_buffer_size

    def flush(self, file = sys.stdout):
        print(''.join(self.buffer), end = '', file = file, flush = True)
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
    table_printer.set_column_headers("I"*34, "SQUARE OF I", "CUBE OF I")
    table_printer.set_column_alignments('<', '^', '>')
    table_printer.set_column_widths(20, 20, 20)
    table_printer.set_horizontal_seperator("|")
    table_printer.set_vertical_seperator('=')
    table_printer.allow_initial_horizontal_seperator(True)
    table_printer.set_padding_widths(1,1,1)
    
    table_printer.begin()

    for i in range(100):
        table_printer.append_row(i, i**2, i**3)

    table_printer.append_row('a'*50, 'b'*100, 'c'*233)
        
    table_printer.end()

if __name__ == '__main__':
    main()
    
