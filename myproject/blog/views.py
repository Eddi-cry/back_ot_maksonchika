from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import os
import zipfile
from django.conf import settings
from .models import File

def home(request):
    return render(request, 'main/product/base.html')

@csrf_exempt
def generate_download_link(request):
    if request.method == 'POST':
        try:
            # Парсим JSON данные
            try:
                data = json.loads(request.body.decode('utf-8'))
                start_date = data.get('start_date')
                end_date = data.get('end_date')
            except json.JSONDecodeError:
                return JsonResponse(
                    {'error': 'Неверный формат JSON'},
                    status=400
                )

            # Валидация дат
            if not start_date or not end_date:
                return JsonResponse(
                    {'error': 'Не указаны даты начала и/или конца периода'},
                    status=400
                )
            
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError as e:
                return JsonResponse(
                    {'error': f'Неверный формат даты: {str(e)}'},
                    status=400
                )

            if start_date > end_date:
                return JsonResponse(
                    {'error': 'Дата начала не может быть позже даты окончания'},
                    status=400
                )

            # Получаем файлы из БД
            files = File.objects.filter(
                date__gte=start_date,
                date__lte=end_date
            )

            if not files.exists():
                return JsonResponse(
                    {'error': 'Файлы за указанный период не найдены'},
                    status=404
                )

            # Создаем архив
            zip_filename = f'files_{start_date}_{end_date}.zip'
            zip_path = os.path.join('C:\\Work', settings.MEDIA_ROOT.strip('/\\'), zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in files:
                    # Формируем полный путь к файлу
                    unix_path = file.path.strip()  # Путь из БД в Unix-формате
                    windows_path = unix_path.replace('/', '\\')  # Конвертируем в Windows-формат
                    
                    # Собираем полный путь: C:\Work + путь из БД + имя файла
                    full_file_path = os.path.join(
                        'C:\\Work',
                        windows_path.lstrip('\\'),  # Удаляем начальный слеш если есть
                        file.filename
                    )
                    
                    # Нормализуем путь (убираем двойные слеши и т.д.)
                    full_file_path = os.path.normpath(full_file_path)
                    
                    if os.path.exists(full_file_path):
                        zipf.write(full_file_path, os.path.basename(file.filename))

            # Проверяем архив
            if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
                return JsonResponse(
                    {'error': 'Не удалось создать архив'},
                    status=500
                )

            return JsonResponse({
                'success': True,
                'download_url': f"/media/{zip_filename}",
                'file_count': files.count()
            })

        except Exception as e:
            return JsonResponse(
                {'error': f'Ошибка сервера: {str(e)}'},
                status=500
            )

    return JsonResponse(
        {'error': 'Метод не разрешен'},
        status=405
    )