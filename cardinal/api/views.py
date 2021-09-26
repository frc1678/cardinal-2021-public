from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from cardinal.api import cardinal_data_request
from .generate_test_data import DataGenerator
from .logger import request_logged
from django.shortcuts import render


CARDINAL_EMOJI = "🐦"


def api_docs(request):
    return render(request, "docs.html")


class InitialApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        """Return a cardinal"""
        return Response(CARDINAL_EMOJI, status=status.HTTP_200_OK)


class CollectionDataRequestApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):
        collection_name = kwargs["collection_name"]

        # Returns all the database documents that have not been sent
        data = cardinal_data_request.get_unsent_docs(collection_name)
        return Response(data, status=status.HTTP_200_OK)


class TestDataGeneratorApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    @request_logged
    def get(self, request, *args, **kwargs):

        filename = kwargs["data_structure_type"] + ".yml"
        generate_test_data = DataGenerator(filename)

        # If the "count" is specified, give that number to the data generator
        # Example "api/generate/calc_tba_team_schema/?format=json&count=10"
        if "count" in request.query_params:
            count = int(request.query_params["count"])
        else:
            count = 1

        return Response(generate_test_data.get_data(count), status=status.HTTP_200_OK)
