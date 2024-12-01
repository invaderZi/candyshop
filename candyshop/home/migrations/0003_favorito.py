# Generated by Django 4.2.4 on 2023-09-12 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_alter_produto_produtocodigo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('FavoritoCodigo', models.AutoField(primary_key=True, serialize=False)),
                ('ClienteCodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ProdutoCodigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.produto')),
            ],
        ),
    ]