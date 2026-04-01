from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from .models import Jobs
from .serializers import JobSerializer,JobCreateSerializer
import logging
from users.permissions import IsHR, IsHROrManager, IsApplicant, IsOwnerOrHR
from rest_framework.views import APIView
from .services import get_latest_jobs_qs
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import JobSerializer
from .filters import JobFilter
from rest_framework.generics import ListAPIView

# Create your views here.

logger = logging.getLogger(__name__)

class JobsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHR]
    renderer_classes = [JSONRenderer]
    queryset = Jobs.objects.all()

    def get_serializer_class(self):
            if self.action in ['create', 'update', 'partial_update']:
                return JobCreateSerializer      
            return JobSerializer   
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            return [AllowAny()]                                # anyone can view/search
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsHR()]                                    #only HR can modify
        if self.action == 'my_jobs':
            return [IsAuthenticated()]                         # any logged-in user
        return [IsHR()]    
    
    def perform_create(self, serializer):
            logger.info(f"Job created by: {self.request.user.email}")
            serializer.save(posted_by=self.request.user)  
    
    def perform_update(self, serializer):
            job = self.get_object()
            # only the user who posted the job can update it
            if job.posted_by != self.request.user:
                return Response(
                    {'error': 'You can only update your own jobs.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            logger.info(f"Job updated by: {self.request.user.email}")
            serializer.save()      
    
    def perform_destroy(self, instance):
            # only the user who posted the job can delete it
            if instance.posted_by != self.request.user:
                return Response(
                    {'error': 'You can only delete your own jobs.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            logger.info(f"Job deleted by: {self.request.user.email}")
            instance.delete()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='my-jobs')
    def my_jobs(self, request):
            jobs       = Jobs.objects.filter(posted_by=request.user)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='search')
    def search(self, request):
            query    = request.query_params.get('q', '')
            location = request.query_params.get('location', '')
            jobs     = Jobs.objects.all()
    
            if query:
                jobs = jobs.filter(title__icontains=query)
            if location:
                jobs = jobs.filter(location__icontains=location)
    
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)




# Create your views here.

class JobListView(APIView):
    permission_classes = [IsAuthenticated,IsApplicant]
    serializer_class = JobSerializer
    def get(self, request):
        page      = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        data = get_latest_jobs_qs(
            user=request.user,
            page=page,
            page_size=page_size
        )
        return Response(data, status=status.HTTP_200_OK)
    

# jobs/views.py


class JobFilterView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class   = JobSerializer
    queryset           = Jobs.objects.filter()

    # backends
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # django-filter
    filterset_class    = JobFilter

    # search across multiple fields
    search_fields      = ['title', 'company', 'location', 'description']

    # allow sorting
    ordering_fields    = ['salary', 'created_at', 'title']
    ordering           = ['-created_at']                    # default ordering