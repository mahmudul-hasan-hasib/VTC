from openpyxl import Workbook


class ExcelExporter:

    @staticmethod
    def export(counter, filename):

        wb = Workbook()

        ws = wb.active

        ws.title = "Vehicle Count"

        ws.append(["Vehicle", "Incoming", "Outgoing"])

        for vehicle in counter.incoming:

            ws.append([
                vehicle,
                counter.incoming[vehicle],
                counter.outgoing[vehicle]
            ])

        wb.save(filename)