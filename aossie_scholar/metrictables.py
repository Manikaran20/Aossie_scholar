import django_tables2 as tables
from .models import Author

class NameTable(tables.Table):
    class Meta:
    	model = Author