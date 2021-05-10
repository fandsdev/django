import pytest

pytestmark = [pytest.mark.django_db]


def test_delete_sepulka_instance(as_user, sepulka):
    as_user.delete(f'/api/v1/sepulkas/{sepulka.id}/')

    with pytest.raises(sepulka.DoesNotExist):
        sepulka.refresh_from_db()
