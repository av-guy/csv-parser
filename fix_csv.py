import argparse
import csv


class CLI(argparse.ArgumentParser):
    def __init__(self, *args: object, **kwargs: object):
        """
        CLI subclasses the argparse.ArgumentParser module and initializes the CLI portion of the application
        @param args: Optional args [FUTURE]
        @param kwargs: Optional kwargs [FUTURE]
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
        self.__in_delimiter = self.add_argument(
            "--in-delimiter",
            type=str,
            help="The delimiter that separates each element in the file."
        )

    def __accept_in_quote(self):
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
        self.cli = CLI()
        self.__chosen_dialect = "custom"
        self.__register_dialect(delimiter=self.cli.args.in_delimiter)
        self.__run()

    @staticmethod
    def __register_dialect(delimiter=None):
        if not delimiter:
            delimiter = "|"
        csv.register_dialect("custom", delimiter=delimiter)

    def __run(self):
        with open(self.cli.old, 'rt') as old_file:
            reader = csv.reader(old_file, dialect=self.__chosen_dialect)
            rows = [row for row in reader]
            with open(self.cli.new, 'w', newline='\n') as new_file:
                writer = csv.writer(new_file)
                writer.writerows(rows)


if __name__ == "__main__":
    Application()
