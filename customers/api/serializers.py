from rest_framework import serializers
from customers.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('id_card', 'first_name', 'last_name', 'birth_date', 
                  'desc', 'movile', 'telephone', 'full_name', 'address_set')
        depth = 2
