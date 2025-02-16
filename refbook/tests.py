from django.test import TestCase
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import ReferenceBook, ReferenceBookVersion, ReferenceBookElement
from django.utils.dateparse import parse_date
from datetime import date


#Тесты для ReferenceBookListView
@pytest.mark.django_db
def test_reference_book_list_view_no_date():
    client = APIClient()
    url = reverse('refbooks')

    # Создаем тестовые данные
    refbook = ReferenceBook.objects.create(code="MS1", name="Медицинские специальности")
    version = ReferenceBookVersion.objects.create(
        reference_book=refbook,
        version="1.0",
        start_date=date(2022, 1, 1)
    )

    # Выполняем запрос
    response = client.get(url)

    # Проверяем ответ
    assert response.status_code == 200
    assert len(response.data["refbooks"]) == 1
    assert response.data["refbooks"][0]["code"] == "MS1"


@pytest.mark.django_db
def test_reference_book_list_view_with_date():
    client = APIClient()
    url = reverse('refbooks')

    # Создаем тестовые данные
    refbook = ReferenceBook.objects.create(code="MS1", name="Медицинские специальности")
    version = ReferenceBookVersion.objects.create(
        reference_book=refbook,
        version="1.0",
        start_date=date(2022, 1, 1)
    )

    # Выполняем запрос с параметром даты
    response = client.get(url, {"date": "2022-01-01"})

    # Проверяем ответ
    assert response.status_code == 200
    assert len(response.data["refbooks"]) == 1
    assert response.data["refbooks"][0]["code"] == "MS1"


@pytest.mark.django_db
def test_reference_book_list_view_invalid_date():
    client = APIClient()
    url = reverse('refbooks')

    # Выполняем запрос с неверным форматом даты
    response = client.get(url, {"date": "2022/01/01"})

    # Проверяем ответ
    assert response.status_code == 400
    assert response.data["error"] == "Неверный формат даты (ГГГГ-ММ-ДД)"
    
    
#Тесты для ReferenceBookElementsView
@pytest.mark.django_db
def test_reference_book_elements_view_with_version():
    client = APIClient()

    # Создаем тестовые данные
    refbook = ReferenceBook.objects.create(code="MS1", name="Медицинские специальности")
    version = ReferenceBookVersion.objects.create(
        reference_book=refbook,
        version="1.0",
        start_date=date(2022, 1, 1)
    )
    element = ReferenceBookElement.objects.create(
        version=version,
        code="1",
        value="Врач-терапевт"
    )

    # Выполняем запрос с указанием версии
    url = reverse('refbook-elements', args=[refbook.id])
    response = client.get(url, {"version": "1.0"})

    # Проверяем ответ
    assert response.status_code == 200
    assert len(response.data["elements"]) == 1
    assert response.data["elements"][0]["code"] == "1"


@pytest.mark.django_db
def test_reference_book_elements_view_without_version():
    client = APIClient()

    # Создаем тестовые данные
    refbook = ReferenceBook.objects.create(code="MS1", name="Медицинские специальности")
    version = ReferenceBookVersion.objects.create(
        reference_book=refbook,
        version="1.0",
        start_date=date(2022, 1, 1)
    )
    element = ReferenceBookElement.objects.create(
        version=version,
        code="1",
        value="Врач-терапевт"
    )

    # Выполняем запрос без указания версии
    url = reverse('refbook-elements', args=[refbook.id])
    response = client.get(url)

    # Проверяем ответ
    assert response.status_code == 200
    assert len(response.data["elements"]) == 1
    assert response.data["elements"][0]["code"] == "1"


@pytest.mark.django_db
def test_reference_book_elements_view_not_found():
    client = APIClient()

    # Выполняем запрос для несуществующего справочника
    url = reverse('refbook-elements', args=[999])
    response = client.get(url)

    # Проверяем ответ
    assert response.status_code == 404
    assert response.data["error"] == "Справочник не найден"
    
  
#Тесты для CheckElementView
@pytest.mark.django_db
def test_check_element_view_valid():
    client = APIClient()

    # Создаем тестовые данные
    refbook = ReferenceBook.objects.create(code="MS1", name="Медицинские специальности")
    version = ReferenceBookVersion.objects.create(
        reference_book=refbook,
        version="1.0",
        start_date=date(2022, 1, 1)
    )
    element = ReferenceBookElement.objects.create(
        version=version,
        code="1",
        value="Врач-терапевт"
    )

    # Выполняем запрос для проверки элемента
    url = reverse('check_element', args=[refbook.id])
    response = client.get(url, {"code": "1", "value": "Врач-терапевт"})

    # Проверяем ответ
    assert response.status_code == 200
    assert response.data["valid"] is True


@pytest.mark.django_db
def test_check_element_view_invalid():
    client = APIClient()

    # Создаем тестовые данные
    refbook = ReferenceBook.objects.create(code="MS1", name="Медицинские специальности")
    version = ReferenceBookVersion.objects.create(
        reference_book=refbook,
        version="1.0",
        start_date=date(2022, 1, 1)
    )

    # Выполняем запрос для проверки несуществующего элемента
    url = reverse('check_element', args=[refbook.id])
    response = client.get(url, {"code": "999", "value": "Несуществующий элемент"})

    # Проверяем ответ
    assert response.status_code == 200
    assert response.data["valid"] is False


@pytest.mark.django_db
def test_check_element_view_missing_params():
    client = APIClient()

    # Выполняем запрос без обязательных параметров
    url = reverse('check_element', args=[1])
    response = client.get(url)

    # Проверяем ответ
    assert response.status_code == 400
    assert response.data["error"] == "Параметры code и value обязательны"
    
        