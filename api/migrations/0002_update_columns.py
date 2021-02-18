from django.db import migrations

def update_columns(apps, schema_editor):
    query='''
        ALTER TABLE api_searchhistory modify column video_title longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
        ALTER TABLE api_searchhistory modify column description longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
        ALTER TABLE api_searchhistory modify column filtered_title VARCHAR(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
    '''

class Migration(migrations.Migration):
    dependencies = [
        ('api','0001_initial'),
    ]
    operations = [
        migrations.RunPython(update_columns)
    ]