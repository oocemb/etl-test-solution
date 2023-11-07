import os
from datetime import datetime
from tempfile import NamedTemporaryFile

from openpyxl.workbook import Workbook
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext.filters import BaseFilter

from utils import get_report_data


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hi, Im a useless bot, only /hello and /report command')


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    report_data = get_report_data()
    wb = Workbook()
    ws = wb.active
    header = ["Субъект РФ", "Суммарное количество доз", "Среднее просрочено дней"]
    ws.append(header)
    for row in report_data:
        ws.append(row)
    with NamedTemporaryFile(mode="w", suffix=f"{datetime.now()}.xlsx") as tmp:
        temp_path = tmp.name
        wb.save(temp_path)
        await update.message.reply_document(
            document=open(temp_path, "rb"),
            filename="report.xlsx",
            caption="Ваш отчёт в прикреплённом файле"
        )
    wb.close()

app = ApplicationBuilder().token(os.getenv("TG_TOKEN")).build()
_filter = BaseFilter()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("report", report))
app.add_handler(MessageHandler(_filter, echo))


if __name__ == "__main__":
    app.run_polling()
