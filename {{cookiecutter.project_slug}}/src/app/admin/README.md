## App-wide admin customizations

This is a place for app-wide django-admin customizations. To make your admin interface customizable, scaffold your admin modules like this:

```python
from app.admin import ModelAdmin, admin
from books.models import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    fields = [
        'name',
    ]
```