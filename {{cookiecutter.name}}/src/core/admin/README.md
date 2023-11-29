## App-wide admin customizations

This is a place for app-wide django-admin customizations. To make your admin interface customizable, scaffold your admin modules like this:

```python
from apps.books.models import Book
from core.admin import ModelAdmin, admin


@admin.register(Book)
class BookAdmin(ModelAdmin):
    fields = [
        "name",
    ]
```