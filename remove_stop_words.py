import csv
from stop_words import get_stop_words

stop_words = get_stop_words('en')
stop_words = get_stop_words('english')
with open('data/cleansquared.csv', newline = '', mode = 'w', encoding = 'UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(['English','Chinese'])

from stop_words import safe_get_stop_words

#stop_words = safe_get_stop_words('unsupported language')

with open('data/medical_translations_clean.csv', newline ='', encoding = 'UTF-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if(row[0] not in stop_words):
            with open('data/cleansquared.csv', newline = '', mode = 'a', encoding = 'UTF-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)
