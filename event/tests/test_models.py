from ..models import Category, Event
import pytest
# Category class tests


@pytest.mark.django_db
def test_category_name():
    category = Category.objects.create(name="Category 1")
    assert category.__str__() == "Category 1"

