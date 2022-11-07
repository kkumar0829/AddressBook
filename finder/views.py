from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from finder.models import FinderModel
from finder.serializers import FinderSerializer


# Create your views here.
class FinderView(APIView):
    def post(self, request):
        serializer = FinderSerializer(data=request.data)
        if serializer.is_valid():
            latitude = serializer.validated_data['latitude']
            longitude = serializer.validated_data['longitude']
            if abs(latitude) <= 90:       # Checking the longitude and latitude values to be valid
                if abs(longitude) <= 180:
                    serializer.save()
                else:
                    return Response("Please give a valid Longitude", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Please give a valid latitude", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        obj = FinderModel.objects.get(id=id)  # Returning the details of a particular id
        if obj:
            name = FinderModel.objects.filter(id=id).values('name')
            address = FinderModel.objects.filter(id=id).values('address')
            latitude = FinderModel.objects.filter(id=id).values('latitude')
            longitude = FinderModel.objects.filter(id=id).values('longitude')
            res = ({
                "data": (name, address, latitude, longitude)
            })
            return Response(data=res)
        else:
            return Response("User not found..!!")

    def patch(self, request, id):
        obj = FinderModel.objects.get(id=id)    # Updating the details of a particular id
        serializer = FinderSerializer(instance=obj, data=request.data)
        if serializer.is_valid():
            latitude = serializer.validated_data['latitude']
            longitude = serializer.validated_data['longitude']
            if abs(latitude) <= 90:
                if abs(longitude) <= 180:
                    serializer.save()
                else:
                    return Response("Please give a valid Longitude", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Please give a valid latitude", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        obj = FinderModel.objects.get(id=id)   # Delete a record from DataBase
        name = obj.name
        obj.delete()
        return Response(f"User {name} has deleted Successfully..!!")


class FindAddress(APIView):
    def get(self, request, latitude_begin, latitude_end, longitude_begin, longitude_end):   # API to search adressess within a range
        latitude_start = float(latitude_begin)
        latitude_end = float(latitude_end)
        longitude_start = float(longitude_begin)
        longitude_end = float(longitude_end)
        if abs(latitude_start) <= 90.0 and abs(latitude_end) <= 90.0:
            if abs(longitude_start) <= 180.0 and abs(longitude_end) <= 180.0:
                pass
            else:
                return Response("Please give a valid Longitude", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please give a valid latitude", status=status.HTTP_400_BAD_REQUEST)

        id_list = FinderModel.objects.all()
        result_list = {}
        count = 1
        for item in id_list:
            latitude = item.latitude
            longitude = item.longitude
            if latitude_start <= latitude <= latitude_end:
                if longitude_start <= longitude <= longitude_end:
                    result_list[count] = item.address
                    count += 1

        return Response(result_list)
