from django.db import migrations

def clear_data(apps, schema_editor):
    Transaction = apps.get_model('myapp', 'Transaction')
    TransactionItem = apps.get_model('myapp', 'TransactionItem')

    # Menghapus semua data pada tabel Transaction dan TransactionItem
    Transaction.objects.all().delete()
    TransactionItem.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_member_email_alter_member_is_active_and_more'),
    ]

    operations = [
        migrations.RunPython(clear_data),
    ]
