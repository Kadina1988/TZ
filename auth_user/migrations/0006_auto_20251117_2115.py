from django.db import migrations

def add_roles_and_admin(apps, schema_editor):
    Role = apps.get_model('auth_user', 'Role')
    User = apps.get_model('auth_user', 'User')
    
    admin = Role.objects.create(name='admin')
    manager = Role.objects.create(name='manager') 
    user = Role.objects.create(name='user')
    
    User.objects.create(name='Admin', email='admin@mail.ru', password='admin', role=admin)
    User.objects.create(name='Manager', email='manager@mail.ru', password='manager', role=manager)
    User.objects.create(name='User', email='user@mail.ru', password='user', role=user)

class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0005_alter_user_role'),
    ]

    operations = [
        migrations.RunPython(add_roles_and_admin),
    ]
