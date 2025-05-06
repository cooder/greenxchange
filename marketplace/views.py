from rest_framework import status
from rest_framework import status, viewsets
from rest_framework.response import Response
from marketplace.models import Energy
from rest_framework.permissions import IsAuthenticated, AllowAny
from marketplace.serializers import *
from django.utils import timezone
from django.db import transaction



class EnergyType_ViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def add_energy_type(request):
        try:
            serialized_data = EnergyTypeSerializers(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                response = {
                    "status": True,
                    "message": "Successfully Created",
                    "result":  serialized_data.data
                }
            else:
                response = {
                    "status": True,
                    "message": "Insertion failed",
                    "result":  ""
                }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_energy_type(request):
        try:
            energy_id = request.data.get("energy_id")
            energy_type = Energy_Type.objects.filter(id=energy_id).first()
            if not energy_type:
                return Response({"status": True, "message": "No record found" }, status=status.HTTP_200_OK)

            serialized_data = EnergyTypeSerializers(energy_type).data
            response = {
                    "status": True,
                    "message": "Successfully Retrieved Energy Types",
                    "result":  serialized_data
                }
            return Response(response, status.HTTP_200_OK)
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def list_energy_type(request):
        try:
            energy_types = Energy_Type.objects.all()
            if not energy_types:
                return Response({"status": True, "message": "No record found" }, status=status.HTTP_200_OK)

            serialized_data = EnergyTypeSerializers(energy_types, many=True).data
            response = {
                    "status": True,
                    "message": "Successfully Retrieved Energy Types",
                    "result":  serialized_data
                }
            return Response(response, status.HTTP_200_OK)
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def update_energy_type(request):
        try:
            energy = Energy_Type.objects.filter(id=request.data.get("energy_id")).first()
            if not energy:
                return Response({"status": True, "message": "No energy type found" }, status=status.HTTP_200_OK)
            
            serializer = EnergyTypeUpdateSerializers(energy, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()  
                return Response({"status": True, "message": "Energy type updated successfully", "result": serializer.data }, status=status.HTTP_200_OK)

            return Response({"status": False, "message": "Error Updating Energy Type"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete_energy_type(request):
        try:
            energy_id = request.data.get("energy_id")

            energy_type = Energy_Type.objects.filter(id=energy_id).first()
            if not energy_type:
                return Response({"status": True, "message": "No record found" }, status=status.HTTP_200_OK)

            energy_type.delete()
            response = {"status": True, "message": "Successfully Deleted Energy Type", "result":  ""}
            return Response(response, status.HTTP_200_OK)
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class Energy_ViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def add_energy(request):
        try:
            seller_id = request.data.get("seller_id")
            energy_type = request.data.get("energy_type")
            # quantity = request.data.get("quantity")
            # price = request.data.get("price")
            # unit = request.data.get("unit")
            # energy_status = request.data.get("status")
            # expiry_date = request.data.get("expiry_date")   

            is_already_exists = Energy.objects.filter(seller_id=seller_id, energy_type__id=energy_type).order_by('expiry_date')
            if is_already_exists:
                response = {"status": True, "message": "Energy against this seller already exists", "result":  ""}
                return Response(response, status.HTTP_200_OK)

            serialized_data = EnergySerializers(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                response = {"status": True, "message": "Successfully Created",  "result":  serialized_data.data}
                return Response(response, status.HTTP_200_OK)

            response = {"status": True, "message": "Adding energy failed",  "result":  ""}
            return Response(response, status.HTTP_400_BAD_REQUEST)
                
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_energy(request):
        try:
            energy_id = request.data.get("energy_id")

            energy = Energy.objects.filter(id=energy_id).first()
            if not energy:
                return Response({"status": False, "message": "Energy not found"}, status=status.HTTP_200_OK)
                
            # Changing energy status on runtime when user view specific energy 
            if energy.status=='expired':   # check if energy expiry date gets updated then change status then check units and change status accordingly
                if timezone.now() < each.expiry_date: 
                    if energy.unit > 0:
                        energy.status=='available'
                    else:
                        energy.status ='sold'
                    energy.save()
            else:                         # check if energy is not expired then check units and update status accordingly
                if energy.unit == 0 :
                    energy.status=='sold'
                energy.status=='available'
                energy.save()

            energy = Energy.objects.filter(id=energy_id).first()
            serialized_data = EnergySerializers(energy).data
            response = {
                    "status": True,
                    "message": "Successfully Retrieved Energy",
                    "result":  serialized_data
                }
            return Response(response, status.HTTP_200_OK)

        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def list_energy(request):
        try:
            energy = Energy.objects.all()
            if not energy:
                response = {"status": True, "message": "No record found", "result":  ""}
                return Response(response, status.HTTP_200_OK)

            # looping through each energy and updating status on runtime
            for each in energy:
                if timezone.now() > each.expiry_date:
                    each.status='expired'
                    each.save()
                else:
                    if each.quantity == 0:
                        each.status = 'sold'
                    elif each.quantity > 0:
                        each.status = 'available'
                    each.save()

            energy = Energy.objects.all()
            serialized_data = EnergySerializers(energy, many=True).data
            response = {
                    "status": True,
                    "message": "Successfully Retrieved Energy Types",
                    "result":  serialized_data
                }
            return Response(response, status.HTTP_200_OK)

        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @transaction.atomic
    def update_energy(request):
        try:
            energy_id = request.data.get("energy_id")

            energy = Energy.objects.filter(id=energy_id).first()
            if not energy:
                return Response({"status": False, "message": "Energy not found"}, status=status.HTTP_200_OK)

            serializer = EnergyUpdateSerializers(energy, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()

                # check after updating if the time is less or greater then update status accordingly
                energy = Energy.objects.filter(id=energy_id).first()
                if timezone.now() < energy.expiry_date: 
                    if energy.quantity > 0:
                        energy.status=='available'
                    else:
                        energy.status ='sold'
                else:
                    energy.status=='expired'
                energy.save()

                return Response({"status": True, "message": "Energy updated successfully", "result": serializer.data}, status=status.HTTP_200_OK)

            return Response({"status": False, "message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete_energy(request):
        try:
            energy_id = request.data.get("energy_id")

            energy = Energy.objects.filter(id=energy_id)
            if energy:
                energy.delete()
                response = {
                        "status": True,
                        "message": "Energy Deleted Successfully ",
                        "result":  ""
                    }
                return Response(response, status.HTTP_200_OK)

            return Response({"status": False, "message": "Energy not found"}, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class Offer_Energy_ViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def offer_energy_price(request):
        try:
            energy_id = request.data.get('energy_id')
            offered_quantity = request.data.get('offered_quantity')

            energy = Energy.objects.filter(id=energy_id).first()
            if energy.status != 'available':
                return Response({"status": False, "message": "Energy is expired/Sold"}, status=status.HTTP_200_OK)

            if offered_quantity > energy.quantity :
                return Response({"status": False, "message": "Required quantity is not present"}, status=status.HTTP_400_BAD_REQUEST)

            serialized_data = EnergyOfferSerializers(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                response = {"status": True, "message": "Successfully Created", "result":  serialized_data.data}
                return Response(response, status.HTTP_200_OK)

            response = {"status": True, "message": "Offering price failed", "result":  ""}
            return Response(response, status.HTTP_400_BAD_REQUEST)

        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def view_offer_energy_price(request):
        try:
            seller_id = request.data.get("seller_id")

            energy_offers = EnergyOffer.objects.filter(energy_id__seller_id=seller_id, status='pending')
            if not energy_offers:
                return Response({"status": True, "message": "No offers till" }, status=status.HTTP_200_OK)

            serialized_data = EnergyOfferSerializers(energy_offers, many=True).data
            return Response({"status": True, "message": "Successfully Retrieved Energy Types", "result":  serialized_data}, status.HTTP_200_OK)

        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @transaction.atomic
    def offer_accept_reject(request):
        try:
            offer_id = request.data.get("id")
            offer_status = request.data.get("status")
            energy_id  = 0 
            energy = ''

            energy_offer = EnergyOffer.objects.filter(id=offer_id).first()
            if not energy_offer:
                return Response({"status": True, "message": "No offer found" }, status=status.HTTP_200_OK)

            if offer_status == 'accepted':
                energy_id = energy_offer.energy_id
                energy = Energy.objects.filter(id=energy_id).first()
                if not energy:
                    return Response({"status": True, "message": "No energy against this offer" }, status=status.HTTP_200_OK)
                    
                if energy.offered_quantity <= energy.quantity and energy.status =='available':
                    energy_offer.status= offer_status
                    energy_offer.save()
                    energy.quantity = int(energy.quantity) - int(energy.offered_quantity)
                    energy.save()
                    return Response({"status": True, "message": "Offer accepted successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": True, "message": "Quantity is less than required quantity or energy not available"}, status=status.HTTP_200_OK)

            else:
                energy_offer.status= offer_status
                energy_offer.save()
                return Response({"status": True, "message": "Offer rejected successfully"}, status=status.HTTP_200_OK)
                
        except Exception as er:
            response = {"status": False, "message": "Internal server error", "result":  str(er)}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
            