import email.utils
import datetime

DATA_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

read_iso_datetime = lambda x: datetime.datetime.fromisoformat(x)
write_iso_datetime = lambda x: x.isoformat(sep=" ", timespec="seconds")
write_rss_datetime = lambda x: email.utils.formatdate(x.timestamp(), localtime=True)
