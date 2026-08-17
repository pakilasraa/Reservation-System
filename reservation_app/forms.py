from django import forms
from .models import Customer, TableCategory, Table, ReservationStatus, Reservation, Payment


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']


class TableCategoryForm(forms.ModelForm):
    class Meta:
        model = TableCategory
        fields = ['name', 'description']


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['table_number', 'category', 'capacity', 'location', 'is_active']
        widgets = {
            'capacity': forms.NumberInput(attrs={'min': 1}),
        }


class ReservationStatusForm(forms.ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ['name', 'description', 'is_active']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'table', 'reservation_date', 'start_time', 'end_time', 'guests', 'status', 'notes']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'guests': forms.NumberInput(attrs={'min': 1}),
        }

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests is None or guests <= 0:
            raise forms.ValidationError("Number of guests must be a positive integer.")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        table = cleaned_data.get('table')
        guests = cleaned_data.get('guests')

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("Reservation end time must be later than start time.")

        if table and guests and guests > table.capacity:
            raise forms.ValidationError(
                f"The selected table capacity is {table.capacity}, which cannot accommodate {guests} guests."
            )

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['reservation', 'amount', 'payment_method', 'payment_status', 'paid_at', 'transaction_id']
        widgets = {
            'paid_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }