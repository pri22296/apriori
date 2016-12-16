import sys

class TablePrinter:
    """Utility Class to print data in tabular format to console.

    Parameters
    ----------

    column_count : int
        Number of columns in the table

    buffer_size : int, optional
        maximum size of the internal buffer after which buffer is
        emptied by flushing it's content. Larger buffer size usually leads
        to efficient printing.
        
    """
    
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
        """Performs initial tasks prior to printing table.

        It is recommended to perform all customization to the TablePrinter
        instance before calling this method. This method is necessary to call
        for printing table.
        """
        
        if self._allow_initial_horizontal_seperator is True:
            format_str = self._horizontal_seperator
        else:
            format_str = ''
        format_str += ("{{{{:{}{{}}}}}}" + self._horizontal_seperator) * self._column_count
        format_str = format_str.format(*self._column_alignments)
        self._format_str_row = format_str.format(*self._column_widths)
        horizontal_seperator_count = self._column_count
        
        if self._allow_initial_horizontal_seperator is True:
            horizontal_seperator_count += 1
            
        self._table_width = sum(self._column_widths)\
                                + horizontal_seperator_count\
                                * len(self._horizontal_seperator)
        
        self._buffered_printer.print_buffered(
            self._vertical_seperator
                * int(self._table_width/len(self._vertical_seperator)))
        
        self.append_row(*self._column_headers)
        
        self._buffered_printer.print_buffered(
            self._vertical_seperator
                * int(self._table_width/len(self._vertical_seperator)))

    def end(self):
        """Performs clean up tasks after printing table.

        This method should always be called after printing all rows of the
        table to ensure that all rows have been flushed. It also closes the
        table visually.
        """
        
        self._buffered_printer.print_buffered(
            self._vertical_seperator
                * int(self._table_width/len(self._vertical_seperator)))
        
        self._buffered_printer.flush()

    def set_column_headers(self, *args):
        """Set titles for the columns of the table.

        Parameters
        ----------

        *args
            titles for the columns.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        assert self._column_count == len(args)
        self._column_headers = args

    def set_column_alignments(self, *args):
        """Set titles for the columns of the table.

        Parameters
        ----------

        *args
            alignment for the columns. It follows the default alignment
            rules of the format method.
            '<' - left alignment
            ':' - center alignment
            '>' - right alignment

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        assert self._column_count == len(args)
        self._column_alignments = args

    def set_column_widths(self, *args):
        """Set width for the columns of the table.

        Width of the column specifies the max number of characters
        a column can contain. Larger characters are clamped and appended
        with ellipses to fit in the available space.

        Parameters
        ----------

        *args
            width for the columns.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        assert self._column_count == len(args)
        self._column_widths = args

    def allow_initial_horizontal_seperator(self, is_allowed : bool):
        """Set whether to display the initial horizontal seperator.

        Initial horizontal seperator allowed
        |  column1  |  column2  |  column3  |
        Initial horizontal seperator not allowed
          column1  |  column2  |  column3  |

        Parameters
        ----------

        is_allowed
            Horizontal seperator is printed at beginning of row if
            value is True.

        Note
        ----
        
        This method should be called prior to calling begin().
        """
        
        self._allow_initial_horizontal_seperator = is_allowed

    def set_left_padding_widths(self, *args):
        """Set width for left padding of the columns of the table.

        Left Width of the padding specifies the number of characters
        on the left of a column reserved for padding. By Default It is 1.

        Parameters
        ----------

        *args
            left pad widths for the columns.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        assert self._column_count == len(args)
        self._left_padding_widths = args

    def set_right_padding_widths(self, *args):
        """Set width for rigth padding of the columns of the table.

        Right Width of the padding specifies the number of characters
        on the rigth of a column reserved for padding. By default It is 1.

        Parameters
        ----------

        *args
            rigth pad widths for the columns.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        assert self._column_count == len(args)
        self._right_padding_widths = args

    def set_padding_widths(self, *args):
        """Set width for left and rigth padding of the columns of the table.

        Parameters
        ----------

        *args
            pad widths for the columns.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        assert self._column_count == len(args)
        self._left_padding_widths = args
        self._right_padding_widths = args

    def set_horizontal_seperator(self, seperator : str):
        """Set the horizontal seperator string.

        All columns are seperated by the horizontal seperator character.
        By default it is |.

        Parameters
        ----------

        seperator
            value of the horizontal seperator character.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        self._horizontal_seperator = seperator

    def set_vertical_seperator(self, seperator):
        """Set the horizontal seperator string.

        Heading row is covered by vertical seperator both below and above.
        table is also closed in the end by the vertical seperator.
        By default it is -.

        Parameters
        ----------

        seperator
            value of the vertical seperator character.

        Note
        ----
        This method should be called prior to calling begin().
        """
        
        self._vertical_seperator = seperator

    def _clamp_string(self, row_item, column_index):
        width = self._column_widths[column_index]\
                    - self._left_padding_widths[column_index]\
                    - self._right_padding_widths[column_index]
        row_item = str(row_item)
        if len(row_item) <= width:
            return row_item
        else:
            if width <= 3:
                ellipses_length = width
            else:
                ellipses_length = 3
            clamped_string = row_item[:width-ellipses_length]\
                                + ('.' * ellipses_length)
            assert len(clamped_string) == width
            return clamped_string

    def append_row(self, *args):
        """append a row to the internal buffer.

        All row items are properly aligned, padded and clamped
        to column width and printed to the table.

        Parameters
        ----------

        *args
            values to be printed in the table.

        Note
        ----
        This method should be called after calling begin().
        """
        
        assert self._column_count == len(args)
        row_item_list = []
        for i, row_item in enumerate(args):
            left_pad = self._column_pad * self._left_padding_widths[i]
            right_pad = self._column_pad * self._right_padding_widths[i]
            short_row_item = left_pad\
                                + self._clamp_string(row_item, i)\
                                + right_pad
            row_item_list.append(short_row_item)
        content = self._format_str_row.format(*row_item_list)
        self._buffered_printer.print_buffered(content)

class BufferedPrinter:
    """Utility Class to print to console with a fixed buffer size.

    Parameters
    ----------

    max_buffer_size
        maximum size of the internal buffer after which buffer is
        emptied by flushing it's content. Larger buffer size usually leads
        to efficient printing.
    """
    
    def __init__(self, max_buffer_size : int):
        self._max_buffer_size = max_buffer_size
        self.buffer = []

    def set_max_buffer_size(self, max_buffer_size : int):
        """Set max buffer size.

        Parameters
        ----------

        max_buffer_size
            new size for the internal buffer.
        """
        
        self._max_buffer_size = max_buffer_size

    def flush(self, file = sys.stdout):
        """flush the buffer to a stream, or to sys.stdout by default.

        Parameters
        ----------

        file : optional
            the file where buffer should be flushed. default value is sys.stdout
            which flushes to the console.

        Note
        ----
        It is recommended to always call this method before exiting otherwise
        you could lose important information.
        """
        
        print(''.join(self.buffer), end = '', file = file, flush = True)
        self.buffer = []

    def print_buffered(self, *args, sep = ' ', end = '\n', file=sys.stdout, flush=False):
        """Prints the values to the internal buffer.

        Parameters
        ----------

        *args
            values to be printed

        sep : str, optional
            string inserted between values, default a space.

        end : str, optional
            string appended after the last value, default a newline.

        file : obj, optional
            a file-like object (stream); defaults to the current sys.stdout.

        flush : bool, optional
            whether to forcibly flush the stream.

        """
        
        self.buffer.append(sep.join(args) + end)
        if len(self.buffer) == self._max_buffer_size:
            self.flush(file)


def main():
    demo_buffered_printer()
    demo_table_printer()

def demo_buffered_printer():
    """Basic Demo for the BufferedPrinter class.
    """
    print("Following is a Demo for BufferedPrinter\n")
    buffered_printer = BufferedPrinter(30)
    for i in range(100):
        buffered_printer.print_buffered(str(i))
    buffered_printer.flush()
    print("\n")

def demo_table_printer():
    """Basic Demo for the TablePrinter class.
    """
    
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
    
