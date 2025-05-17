from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
import requests

from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer

# BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# @api_view(['GET'])
# def api_test(request):
#     URL = BASE_URL + 'depositProductsSearch.json'
#     params = {
#         'auth' : settings.API_KEY,
#         'topFinGrpNo' : '020000',
#         'pageNo' : 1
#     }
#     response = requests.get(URL, params=params).json()
#     return JsonResponse({'response':response})
    

# requests 모듈을 활용하여 정기예금 상품 목록 데이터를 가져와 정기예금 상품 목록과 옵션 목록을 DB에 저장

@api_view(['GET'])
def save_deposit_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(BASE_URL, params = params).json()
    # return JsonResponse({'response':response})
    data = response["result"]
    
    # 상품 정보 저장 및 직렬화
    product_instances = []
    for product in data['baseList']:
        product_data = {
            'fin_prdt_cd': product['fin_prdt_cd'],
            'kor_co_nm': product['kor_co_nm'],
            'fin_prdt_nm': product['fin_prdt_nm'],
            'etc_note': product.get('etc_note', ''),
            'join_deny': int(product.get('join_deny', 0)),
            'join_member': product.get('join_member', ''),
            'join_way': product.get('join_way', ''),
            'spcl_cnd': product.get('spcl_cnd', ''),
        }
        serializer = DepositProductsSerializer(data=product_data)
        if serializer.is_valid():
            product = serializer.save()
            product_instances.append(product)
        else:
            # 유효성 오류 발생 시 에러 반환
            return Response(serializer.errors, status=400)

        
    # 옵션 정보 저장 및 직렬화
    option_instances = []
    for opt in data['optionList']:
        print(opt)
        # 금리 비어있으면 -1로 저장
        opt_data = {
            'product': DepositProducts.objects.get(fin_prdt_cd=opt['fin_prdt_cd']).id,
            'fin_prdt_cd': opt['fin_prdt_cd'],
            'intr_rate_type_nm': opt.get('intr_rate_type_nm', ''),
            'intr_rate': float(opt['intr_rate']) if opt.get('intr_rate') not in [None, ''] else -1,
            'intr_rate2': float(opt['intr_rate2']) if opt.get('intr_rate2') not in [None, ''] else -1,
            'save_trm': int(opt.get('save_trm', 0)),
        }
        serializer = DepositOptionsSerializer(data=opt_data)
        if serializer.is_valid():
            option = serializer.save()
            option_instances.append(option)
        else:
            print(serializer.error_messages)
            return Response(serializer.errors, status=400)

    # 저장된 객체를 serializer로 응답
    products_serializer = DepositProductsSerializer(product_instances, many=True)
    options_serializer = DepositOptionsSerializer(option_instances, many=True)
    return Response({
        'products': products_serializer.data,
        'options': options_serializer.data,
    })


# GET: 전체 정기예금 상품 목록 반환 / POST: 상품 데이터 저장
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        deposit_products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(deposit_products, many=True)
        return Response(serializer.data)    
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(product__fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

# 가입 기간에 상관없이 금리가 가장 높은 상품과 해당 상품의 옵션 리스트 출력
@api_view(['GET'])
def deposit_products_top_rate(request):
 # intr_rate2 = models.FloatField()    # 최고 우대 금리   <= depositOptions에 있는거
    top_rate = DepositOptions.objects.order_by('-intr_rate2').first()  
    if top_rate:
        product = top_rate.product
        product_serializer = DepositProductsSerializer(product)
        options = DepositOptions.objects.filter(product=product)
        option_serializer = DepositOptionsSerializer(options, many=True)
        return Response({
            'product': product_serializer.data,
            'options': option_serializer.data,
        })
    return Response({'message': '데이터 없음'}, status=status.HTTP_404_NOT_FOUND)