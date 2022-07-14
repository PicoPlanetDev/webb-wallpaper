from asyncore import read
import csv

SCREEN_RESOLUTIONS_FILE = 'screen_resolutions.csv'

class CSVReader:
    def __init__(self) -> None:
        self.read_csv()

    def read_csv(self):
        self.display_names = []
        self.short_names = []
        self.heights = []
        self.widths = []
        with open(SCREEN_RESOLUTIONS_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.display_names.append(row[0])
                self.short_names.append(row[1])
                self.heights.append(row[2])
                self.widths.append(row[3])

    def get_phone_resolution(self, display_name) -> tuple:
        index = self.display_names.index(display_name)
        return (self.heights[index], self.widths[index])

    def get_display_names(self) -> list:
        return self.display_names