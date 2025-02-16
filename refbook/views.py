from django.shortcuts import render
from rest_framework.views import APIView
from .models import ReferenceBook, ReferenceBookVersion, ReferenceBookElement
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from .serializers import ReferenceBookSerializer, ReferenceBookElementSerializer
from rest_framework import status
from django.utils.timezone import now


class ReferenceBookListView(APIView):
    def get(self, request):
        date_param = request.GET.get("date")

        # Получаем все справочники
        query = ReferenceBook.objects.all()

        if date_param:
            # Парсим дату из запроса
            filter_date = parse_date(date_param)

            if not filter_date:
                return Response({"error": "Неверный формат даты (ГГГГ-ММ-ДД)"}, status=status.HTTP_400_BAD_REQUEST)

            # Фильтруем справочники, у которых есть версия с `start_date <= filter_date`
            query = query.filter(versions__start_date__lte=filter_date).distinct()

        serializer = ReferenceBookSerializer(query, many=True)
        return Response({"refbooks": serializer.data})
    
    
class ReferenceBookElementsView(APIView):
    def get(self, request, refbook_id):
        version_param = request.GET.get("version")

        # Получаем все справочники
        try:
            refbook = ReferenceBook.objects.get(id=refbook_id)
        except ReferenceBook.DoesNotExist:
            return Response({"error": "Справочник не найден"}, status=status.HTTP_404_NOT_FOUND)

        if version_param:
            version = refbook.versions.filter(version=version_param).first()
            if not version:
                return Response({"error": "Версия не найдена"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Определяем текущую версию справочника (максимальный `start_date`, но не в будущем)
            version = refbook.versions.filter(start_date__lte=now().date()).order_by("-start_date").first()
            if not version:
                return Response({"error": "Нет актуальной версии справочника"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем элементы этой версии
        elements = version.elements.all()
        serializer = ReferenceBookElementSerializer(elements, many=True)
        
        return Response({"elements": serializer.data})            


class CheckElementView(APIView):
    def get(self, request, id):
        code = request.GET.get("code")
        value = request.GET.get("value")
        version = request.GET.get("version")

        if not code or not value:
            return Response({"error": "Параметры code и value обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refbook = ReferenceBook.objects.get(id=id)
        except Refbook.DoesNotExist:
            return Response({"error": "Справочник не найден"}, status=status.HTTP_404_NOT_FOUND)

        if version:
            refbook_version = refbook.versions.filter(version=version).first()
        else:
            refbook_version = refbook.versions.filter(start_date__lte=now()).order_by('-start_date').first()

        if not refbook_version:
            return Response({"error": "Актуальная версия не найдена"}, status=status.HTTP_404_NOT_FOUND)

        exists = ReferenceBookElement.objects.filter(version=refbook_version, code=code, value=value).exists()


        return Response({"valid": exists})