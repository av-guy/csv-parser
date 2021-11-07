import argparse
import csv


class CLI(argparse.ArgumentParser):
    def __init__(self):
        """
        CLI subclasses the argparse.ArgumentParser module and initializes the CLI portion of the application
        """
        super().__init__(
            description="Take a pipe delimited file and output a comma delimited one",
            add_help=True
        )
        self.__accept_old_file()
        self.__accept_new_file()
        self.__accept_in_delimiter()
        self.__accept_in_quote()
        self.args = self.parse_args()
        self.old = self.args.old_file
        self.new = self.args.new_file

    def __accept_in_delimiter(self):
        """
        Accept the optional in-delimiter argument.
        """
        self.__in_delimiter = self.add_argument(
            "--in-delimiter",
            type=str,
            help="The delimiter that separates each element in the file."
        )

    def __accept_in_quote(self):
        """
        Accept the optional in-quote argument.
        """
        self.__in_quote = self.add_argument(
            "--in-quote",
            type=str,
            help="The optional in-quote that should be used for quoted items"
        )

    def __accept_old_file(self):
        """
        Add old_file as a CLI positional argument
        """
        self.__old = self.add_argument('old_file', type=str, help="The file to be processed")

    def __accept_new_file(self):
        """
        Add new_file as a CLI positional argument
        """
        self.__new = self.add_argument('new_file', type=str, help="The output file")


class Application:
    def __init__(self):
        """
        Instantiates CLI, registers dialect, and runs the application.
        """
        self.cli = CLI()
        self.__chosen_dialect = "custom"
        self.__sniff = False
        self.__register_dialect(
            delimiter=self.cli.args.in_delimiter,
            quotechar=self.cli.args.in_quote
        )
        self.__run()

    def __register_dialect(self, delimiter=None, quotechar=None):
        """
        Check if the optional in-delimiter and in-quote values are present. If they aren't, set __sniff flag to True.
        Register the custom dialect to use with the CSV Reader.
        @param delimiter: Optional in-delimiter value from CLI.
        @param quotechar:  Optional in-quote value from CLI.
        """
        if not delimiter and not quotechar:
            self.__sniff = True
        if not delimiter:
            delimiter = ","
        if not quotechar:
            quotechar = '"'
        csv.register_dialect("custom", delimiter=delimiter, quotechar=quotechar)

    def __get_dialect(self):
        """
        Create a CSV sniffer and try to sniff the file. Do not pass any optional delimiter values along to
        sniffer.sniff. Register the auto-detected dialect with the Application class by assigning the result to
        __chosen_dialect
        """
        with open(self.cli.old) as old_file:
            sniffer = csv.Sniffer()
            self.__chosen_dialect = sniffer.sniff(old_file.read())

    def __run(self):
        """
        Run the application. If __sniff flag is set to True, call method __get_dialect to auto-detect the dialect.
        Read the CSV contents and create a list of rows. Open the new file and write the contents of the old file to
        the new file using a comma as the delimiter.
        """
        with open(self.cli.old, 'rt') as old_file:
            if self.__sniff:
                self.__get_dialect()
            reader = csv.reader(old_file, dialect=self.__chosen_dialect)
            rows = [row for row in reader]
            with open(self.cli.new, 'w', newline='\n') as new_file:
                writer = csv.writer(new_file)
                writer.writerows(rows)


if __name__ == "__main__":
    Application()
