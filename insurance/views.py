import random
from django.http import Http404
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Insurance, Modern
from .serializers import InsuranceSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone


class InsuranceList(APIView):

    def get(self, request, format=None):
        insurances = Insurance.objects.all()
        serializer = InsuranceSerializer(insurances, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InsuranceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceDetail(APIView):

    def get(self, request, pk, format=None):
        insurance = get_object_or_404(Insurance, pk=pk)
        serializer = InsuranceSerializer(insurance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        insurance = get_object_or_404(Insurance, pk=pk)
        serializer = InsuranceSerializer(insurance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        insurance = get_object_or_404(Insurance, pk=pk)
        insurance.delete()
        return Response(
            {"message": f"ID: {pk} is successfully deleted on the database!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class InsuranceCreateFakeData(APIView):

    def post(self, request, format=None):

        insurance = []
        for _ in range(1, 10):
            placeholder = random.choice(["Health", "Life", "Car"])
            insurance_obj = Insurance(
                insurance_name=f"{placeholder}-{timezone.now()}",
                policy_number=f"{random.randint(1_000, 9_999)}-{placeholder}-{timezone.now()}",
                policy_type=placeholder,
                provider="test",
                premium=random.uniform(10_50.74, 10_500.89),
                start_date="2025-04-23",
                end_date="2035-04-23",
                policy_owner_id=1,
            )

            insurance.append(insurance_obj)

        Insurance.objects.bulk_create(insurance)

        return Response(
            {"message": "Successfully created test data"},
            status=status.HTTP_201_CREATED,
        )


class InsuranceTest(APIView):

    def get(self, request, format=None):

        moderns = Modern.objects.all()

        return Response(
            {"hey": "If you see this then wow!", "data": [modern for modern in moderns]}
        )
