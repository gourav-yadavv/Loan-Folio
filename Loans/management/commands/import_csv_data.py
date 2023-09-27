import csv
import uuid
from datetime import datetime
from django.core.management.base import BaseCommand
from Loans.models import Transaction 

class Command(BaseCommand):
    help = r'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help=r'C:\Users\gyada\OneDrive\Desktop\loan_management_project\transactions_data_Backend.csv')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                user_id = uuid.UUID(row['user'])
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                transaction_type = row['transaction_type']
                amount = float(row['amount'])

                transaction = Transaction(
                    user=user_id,
                    date=date,
                    transaction_type=transaction_type,
                    amount=amount
                )
                transaction.save()

        self.stdout.write(self.style.SUCCESS('CSV data has been imported as Transaction objects.'))

# python manage.py import_csv_data C:\Users\gyada\OneDrive\Desktop\loan_management_project\transactions_data_Backend.csv
