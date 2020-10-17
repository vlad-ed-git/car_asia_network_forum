from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F
from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer, BlogPostUpdateSerializer, BlogPostCreateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


# Url: https://<your-domain>/api/blog/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_blog_view(request, slug):

    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data)


# cause digital ocean adds keys and such stuff to path of image files stored
def get_blog_images(request, blog_post):
    data = {'featured_image' : None, 'extra_image_one' : None, 'extra_image_two' : None, 'extra_image_three' : None }

    # featured image
    if blog_post.featured_image:
        featured_image_url = str(request.build_absolute_uri(blog_post.featured_image.url))
        if "?" in featured_image_url:
            featured_image_url = featured_image_url[:featured_image_url.rfind("?")]
        data['featured_image'] = featured_image_url

    # extra image one
    if blog_post.extra_image_one:
        extra_image_one_url = str(request.build_absolute_uri(blog_post.extra_image_one.url))
        if "?" in extra_image_one_url:
            extra_image_one_url = extra_image_one_url[:extra_image_one_url.rfind("?")]
        data['extra_image_one'] = extra_image_one_url

    # extra image two
    if blog_post.extra_image_two:
        extra_image_two_url = str(request.build_absolute_uri(blog_post.extra_image_two.url))
        if "?" in extra_image_two_url:
            extra_image_two_url = extra_image_two_url[:extra_image_two_url.rfind("?")]
        data['extra_image_two'] = extra_image_two_url

    # extra image three
    if blog_post.extra_image_three:
        extra_image_three_url = str(request.build_absolute_uri(blog_post.extra_image_three.url))
        if "?" in extra_image_three_url:
            extra_image_three_url = extra_image_three_url[:extra_image_three_url.rfind("?")]
        data['extra_image_three'] = extra_image_three_url

    return data

# Url: https://<your-domain>/api/blog/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_blog_view(request, slug):

    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': "You don't have permission to edit that."})

    if request.method == 'PUT':
        serializer = BlogPostUpdateSerializer(
            blog_post, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = UPDATE_SUCCESS
            data['pk'] = blog_post.pk
            data['title'] = blog_post.title
            data['body'] = blog_post.body
            data['slug'] = blog_post.slug
            data['likes'] = blog_post.total_likes()
            data['dislikes'] = blog_post.total_dislikes()
            data['views'] = blog_post.views
            data['date_updated'] = blog_post.date_updated
            image_data = get_blog_images(request, blog_post)
            if image_data['featured_image']:
                data['featured_image'] = image_data['featured_image']
            if image_data['extra_image_one']:
                data['extra_image_one'] = image_data['extra_image_one']
            if image_data['extra_image_two']:
                data['extra_image_two'] = image_data['extra_image_two']
            if image_data['extra_image_three']:
                data['extra_image_three'] = image_data['extra_image_three']
            data['username'] = blog_post.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_is_author_of_blogpost(request, slug):
    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    user = request.user
    if blog_post.author != user:
        data['response'] = "False"
        return Response(data=data)
    data['response'] = "True"
    return Response(data=data)


# Url: https://<your-domain>/api/blog/<slug>/add_view_count
# Headers: Authorization: Token <token>
@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def inc_view_count_view(request, slug):
    data = {}
    try:
        BlogPost.objects.filter(slug = slug).update(views = F('views') + 1)
        data['response'] = SUCCESS
        return Response(data=data)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as err:
        data['response'] = ERROR
        data['error'] = str(err)
        return Response(data=data)

# Url: https://<your-domain>/api/blog/<slug>/like
# Headers: Authorization: Token <token>
@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def like_blog_post_view(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    data = {}
    try:
        user = request.user
        blog.likes.add(user)
        blog.dislikes.remove(user)
        data['response'] = SUCCESS
        return Response(data=data)
    except Exception as err:
        data['response'] = ERROR
        data['error'] = str(err)
        return Response(data=data)



# Url: https://<your-domain>/api/blog/<slug>/dislike
# Headers: Authorization: Token <token>
@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def dislike_blog_post_view(request, slug):
    try:
        blog = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    try:
        user = request.user
        blog.dislikes.add(user)
        blog.likes.remove(user)
        data['response'] = SUCCESS
        return Response(data=data)
    except Exception as err:
        data['response'] = ERROR
        data['error'] = str(err)
        return Response(data=data)

# Url: https://<your-domain>/api/blog/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def api_delete_blog_view(request, slug):

    try:
        blog_post = BlogPost.objects.get(slug=slug)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({'response': "You don't have permission to delete that."})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data['response'] = DELETE_SUCCESS
        return Response(data=data)


# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):

    if request.method == 'POST':

        data = request.data.copy()
        data['author'] = request.user.pk
        serializer = BlogPostCreateSerializer(data=data)

        data = {}
        if serializer.is_valid():
            blog_post = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = blog_post.pk
            data['title'] = blog_post.title
            data['body'] = blog_post.body
            data['slug'] = blog_post.slug
            data['date_updated'] = blog_post.date_updated
            data['likes'] = blog_post.total_likes()
            data['dislikes'] = blog_post.total_dislikes()
            data['views'] = blog_post.views
            image_data = get_blog_images(request, blog_post)
            if image_data['featured_image']:
                data['featured_image'] = image_data['featured_image']
            if image_data['extra_image_one']:
                data['extra_image_one'] = image_data['extra_image_one']
            if image_data['extra_image_two']:
                data['extra_image_two'] = image_data['extra_image_two']
            if image_data['extra_image_three']:
                data['extra_image_three'] = image_data['extra_image_three']
            data['username'] = blog_post.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Url:
#		1) list: https://<your-domain>/api/blog/list
#		2) pagination: http://<your-domain>/api/blog/list?page=2
#		3) search: http://<your-domain>/api/blog/list?search=search_query
#		4) ordering: http://<your-domain>/api/blog/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/blog/list?search=search_query&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiBlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'body', 'author__username')
