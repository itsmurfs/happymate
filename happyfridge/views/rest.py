#TODO update naming convention
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from common.views import JSONResponse
from happyfridge.models import get_shopping_run
from happyfridge.serializers import ItemSerializer



class GetItemPool(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        sr = get_shopping_run(request.user)

        items = sr.item_pool.all()
        serializer = ItemSerializer(items, many=True)
        return JSONResponse(serializer.data)


class CheckItem(APIView):
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        sr = get_shopping_run(request.user)

        items = sr.item_pool.all()

        item_id = request.POST['item_id']
        item = items.get(pk=item_id)
        item.process(request.user.roommate)
        item.check(request.user.roommate)
        item.save()

        return JSONResponse(None)