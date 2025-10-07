##############################################################################
# pipeline/reporting.py — Stream the run log to CSV
# Why CSV? It's easy for reviewers to open, diff, or import elsewhere.
##############################################################################
import csv, os
from typing import Dict

class Reporter:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        header = [
            "campaign","product_id","product_name","market","aspect_ratio",
            "source_image","output_path","legal_flags","brand_flags"
        ]
        first = not os.path.exists(csv_path)
        # Open in append mode so multiple runs combine naturally
        self.fh = open(csv_path, "a", newline="")
        self.writer = csv.DictWriter(self.fh, fieldnames=header)
        if first:
            self.writer.writeheader()

    def write(self, row: Dict):
        """Write a single record for each generated creative."""
        self.writer.writerow(row)
        self.fh.flush()  # flush so the CSV appears even if the process exits early

    def __del__(self):
        try:
            self.fh.close()
        except:
            pass
