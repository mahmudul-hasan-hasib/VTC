from datetime import datetime

from openpyxl import Workbook

from app.counter.vehicle_data import VEHICLE_CLASSES


class ExcelExporter:

    @staticmethod
    def export(counter, filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Vehicle Count"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ws.append(["Timestamp", "Direction"] + VEHICLE_CLASSES + ["Total"])

        in_total = sum(counter.incoming.values())
        in_row = [timestamp, "Incoming"] + [
            counter.incoming.get(v, 0) for v in VEHICLE_CLASSES
        ] + [in_total]
        ws.append(in_row)

        out_total = sum(counter.outgoing.values())
        out_row = [timestamp, "Outgoing"] + [
            counter.outgoing.get(v, 0) for v in VEHICLE_CLASSES
        ] + [out_total]
        ws.append(out_row)

        wb.save(filename)
