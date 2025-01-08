import time

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime, timedelta
from asyncio import sleep
from django.db.models.functions import TruncHour
import os
from django.db.models import Max
from sklearn.ensemble import IsolationForest

MODEL_MAIN_PATH = 'all_models/'


async def my_async_view(request):
    await sleep(5)  # Simulate a time-consuming operation
    return JsonResponse({"message": "This is an async response!"})


@api_view(['GET'])
def is_server_live(requests):
    return JsonResponse({"status": "True"}, safe=False)


@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def datalog(request):
    if request.method == 'POST':
        datalog_serializer = SensorDataLogSerializer(data=request.data)
        if datalog_serializer.is_valid():
            datalog_serializer.save()
            return Response({"message": "data saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(datalog_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_sensor_list(request):
    sensor_list = SettingsElement.objects.filter(prediction=True, active=True)
    sensor = list(sensor_list.values())
    return JsonResponse(sensor, safe=False)


@api_view(['POST'])
def get_sensor_data(request):
    try:
        MANDATORY_FIELD = ['element_id', 'count', 'end_date']
        sensor_params = request.data

        if set(MANDATORY_FIELD).issubset(set(sensor_params)):
            if sensor_params['end_date'] == '': sensor_params['end_date'] = datetime.now().date()
            start_date = sensor_params['end_date'] - timedelta(days=int(sensor_params['count']))

            sensor_data = SensorDataLog.objects.filter(element_id=sensor_params['element_id'],
                                                       timestamp__range=['2024-12-28 00:00:00.00',
                                                                         '2024-12-28 23:00:00.00'])  # [sensor_params['end_date'] , start_date])
            return JsonResponse(list(sensor_data.values()), safe=False)
        else:
            return JsonResponse({'message': f'some parameters in {MANDATORY_FIELD} are missing'}, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'{e}'}, safe=False)


@api_view(['POST'])
def train_model(requests):
    if requests.method == 'POST':
        MANDATORY_FIELD = ['element_id', 'start_time', 'end_time', 'epochs']
        min_data_to_train = 80
        train_params = requests.data
        if set(MANDATORY_FIELD).issubset(set(train_params)):
            element_list = SettingsElement.objects.filter(prediction='True').values('element_id')
            if train_params['element_id'] in [element['element_id'] for element in list(element_list)]:
                hour_labeled = SensorDataLog.objects.filter(
                    timestamp__range=[train_params['start_time'], train_params['end_time']], element_id='S19').annotate(
                    hour=TruncHour('timestamp')).values('hour').annotate(hourly_max=Max('max')).values('hour',
                                                                                                       'hourly_max')
                train_data = [int(object['hourly_max']) for object in hour_labeled]
                if len(train_data) >= min_data_to_train:
                    modeling_start_time = datetime.now()
                    model_path = f'{MODEL_MAIN_PATH}{train_params['element_id']}'
                    try:
                        from .LSTM import ModelBuilder
                        model = ModelBuilder( train_params['element_id'] , model_path, train_data, train_params['epochs'])
                        res , msg = model.build_model()
                        if res:
                            ModelLog(start_time=str(modeling_start_time),model_path=model_path,model_created='True',remarks='Successfully created',log_time=str(datetime.now())).save()
                            SettingsElement.objects.filter( element_id = train_params['element_id']).update(model_path = msg)
                            return JsonResponse({"message": f"Model Created"}, safe=False)
                        else:
                            ModelLog(start_time=str(modeling_start_time), model_path=msg, model_created='True',remarks= msg, log_time=str(datetime.now())).save()
                            return JsonResponse({"message":msg }, safe=False)
                    except Exception as e:
                        ModelLog(start_time=str(modeling_start_time), model_path=model_path, model_created='False',remarks= e, log_time=str(datetime.now())).save()
                        return JsonResponse({"message": e}, safe=False)
                else:
                    return JsonResponse({"message": f"Need min of {min_data_to_train} datas got {len(train_data)}"},
                                        safe=False)
            else:
                return JsonResponse({"message": f"check element id in settings with prediction enabled"}, safe=False)

        else:
            return JsonResponse({"message": f"parameters not matched , expected {MANDATORY_FIELD}"}, safe=False)


@receiver(post_save, sender=SettingsElement)
def create_model_folder(sender, instance, created, **kwargs):
    if created:
        os.mkdir(MODEL_MAIN_PATH + str(instance.element_id))


@receiver(post_delete, sender=SettingsElement)
def delete_model_folder(sender, instance, **kwargs):
    os.rmdir(MODEL_MAIN_PATH + str(instance.element_id))


@api_view(['POST'])
def datalog_sensor_list(request):
    res = {}
    sensor_list = SettingsElement.objects.filter(active=True)
    sensor = list(sensor_list.values('element_id', 'tag', 'org_id', 'server_ip'))

    for i in sensor:
        try:
            res[i['server_ip']]
        except:
            res[i['server_ip']] = {}
        res[i['server_ip']][i['element_id']] = [i['tag'], i['org_id']]

    return JsonResponse(res, safe=False)


@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def error_log(request):
    if request.method == 'POST':
        error_log_serializer = ErrorLogSerializer(data=request.data)
        if error_log_serializer.is_valid():
            error_log_serializer.save()
            return Response({"message": "error logged successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(error_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test_function(requests):
    start_time = '2024-12-20 00:00:00'
    end_time = '2024-12-21 00:00:00'

    hour_labeled = SensorDataLog.objects.filter(timestamp__range=[start_time, end_time], element_id='S19').annotate(
        hour=TruncHour('timestamp')).values('hour').annotate(hourly_max=Max('max')).values('hour', 'hourly_max')

    train_data = [object['hourly_max'] for object in hour_labeled]

    return JsonResponse(train_data, safe=False)
