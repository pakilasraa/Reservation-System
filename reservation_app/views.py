from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment, AuditLog
from .forms import CustomerForm, TableCategoryForm, TableForm, ReservationStatusForm, ReservationForm, PaymentForm


def json_response(data, status=200):
    return JsonResponse(data, status=status, safe=False)


# --- Customer Views ---
def customer_list(request):
    customers = list(Customer.objects.values())
    return json_response(customers)

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return json_response({'id': customer.id, 'name': str(customer), 'email': customer.email, 'phone': customer.phone})

@csrf_exempt
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return json_response({'message': 'Customer created', 'id': customer.id}, status=201)
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method in ['POST', 'PUT']:
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return json_response({'message': 'Customer updated'})
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return json_response({'message': 'Customer deleted'})


# --- Table Category Views ---
def table_category_list(request):
    categories = list(TableCategory.objects.values())
    return json_response(categories)

def table_category_detail(request, pk):
    category = get_object_or_404(TableCategory, pk=pk)
    return json_response({'id': category.id, 'name': category.name, 'description': category.description})

@csrf_exempt
def table_category_create(request):
    if request.method == 'POST':
        form = TableCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            return json_response({'message': 'Category created', 'id': cat.id}, status=201)
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def table_category_update(request, pk):
    category = get_object_or_404(TableCategory, pk=pk)
    if request.method in ['POST', 'PUT']:
        form = TableCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return json_response({'message': 'Category updated'})
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def table_category_delete(request, pk):
    category = get_object_or_404(TableCategory, pk=pk)
    category.delete()
    return json_response({'message': 'Category deleted'})


# --- Table Views ---
def table_list(request):
    tables = list(Table.objects.values())
    return json_response(tables)

def table_detail(request, pk):
    table = get_object_or_404(Table, pk=pk)
    return json_response({'id': table.id, 'number': table.table_number, 'capacity': table.capacity, 'location': table.location})

@csrf_exempt
def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            tbl = form.save()
            return json_response({'message': 'Table created', 'id': tbl.id}, status=201)
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def table_update(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method in ['POST', 'PUT']:
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return json_response({'message': 'Table updated'})
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table.delete()
    return json_response({'message': 'Table deleted'})


# --- Reservation Status Views ---
def reservation_status_list(request):
    statuses = list(ReservationStatus.objects.values())
    return json_response(statuses)

@csrf_exempt
def reservation_status_create(request):
    if request.method == 'POST':
        form = ReservationStatusForm(request.POST)
        if form.is_valid():
            status_obj = form.save()
            return json_response({'message': 'Status created', 'id': status_obj.id}, status=201)
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def reservation_status_update(request, pk):
    status_obj = get_object_or_404(ReservationStatus, pk=pk)
    if request.method in ['POST', 'PUT']:
        form = ReservationStatusForm(request.POST, instance=status_obj)
        if form.is_valid():
            form.save()
            return json_response({'message': 'Status updated'})
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def reservation_status_delete(request, pk):
    status_obj = get_object_or_404(ReservationStatus, pk=pk)
    status_obj.delete()
    return json_response({'message': 'Status deleted'})


# --- Reservation Views ---
def reservation_list(request):
    queryset = Reservation.objects.all()
    customer_id = request.GET.get('customer')
    res_date = request.GET.get('date')

    if customer_id:
        queryset = queryset.filter(customer_id=customer_id)
    if res_date:
        queryset = queryset.filter(reservation_date=res_date)

    return json_response(list(queryset.values()))

def reservation_detail(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    return json_response({
        'id': res.id,
        'customer': str(res.customer),
        'table': str(res.table),
        'date': str(res.reservation_date),
        'start_time': str(res.start_time),
        'end_time': str(res.end_time),
        'guests': res.guests,
        'status': str(res.status),
    })

@csrf_exempt
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            res = form.save()
            AuditLog.objects.create(
                reservation=res,
                action='CREATE',
                performed_by='System/User',
                details='Reservation created successfully.'
            )
            return json_response({'message': 'Reservation created', 'id': res.id}, status=201)
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def reservation_update(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    if request.method in ['POST', 'PUT']:
        form = ReservationForm(request.POST, instance=res)
        if form.is_valid():
            res = form.save()
            AuditLog.objects.create(
                reservation=res,
                action='UPDATE',
                performed_by='System/User',
                details='Reservation updated.'
            )
            return json_response({'message': 'Reservation updated'})
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])

@csrf_exempt
def reservation_cancel(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    cancelled_status, _ = ReservationStatus.objects.get_or_create(name='CANCELLED')
    res.status = cancelled_status
    res.save()

    AuditLog.objects.create(
        reservation=res,
        action='CANCEL',
        performed_by='System/User',
        details='Reservation marked as cancelled.'
    )
    return json_response({'message': 'Reservation cancelled successfully'})


# --- Payment Views ---
def payment_list(request):
    queryset = Payment.objects.all()
    reservation_id = request.GET.get('reservation')
    if reservation_id:
        queryset = queryset.filter(reservation_id=reservation_id)
    return json_response(list(queryset.values()))

def payment_detail(request, pk):
    p = get_object_or_404(Payment, pk=pk)
    return json_response({
        'id': p.id,
        'reservation_id': p.reservation.id,
        'amount': str(p.amount),
        'method': p.payment_method,
        'status': p.payment_status
    })

@csrf_exempt
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            p = form.save()
            return json_response({'message': 'Payment created', 'id': p.id}, status=201)
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def payment_update(request, pk):
    p = get_object_or_404(Payment, pk=pk)
    if request.method in ['POST', 'PUT']:
        form = PaymentForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return json_response({'message': 'Payment updated'})
        return json_response({'errors': form.errors}, status=400)
    return HttpResponseNotAllowed(['POST', 'PUT'])


# --- Audit Log Views ---
def audit_log_list(request):
    queryset = AuditLog.objects.all()
    reservation_id = request.GET.get('reservation')
    if reservation_id:
        queryset = queryset.filter(reservation_id=reservation_id)
    return json_response(list(queryset.values()))

def audit_log_detail(request, pk):
    log = get_object_or_404(AuditLog, pk=pk)
    return json_response({
        'id': log.id,
        'reservation_id': log.reservation.id,
        'action': log.action,
        'performed_by': log.performed_by,
        'action_time': str(log.action_time),
        'details': log.details
    })