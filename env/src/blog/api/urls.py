from django.urls import path
from blog.api.views import(
	api_detail_blog_view,
	api_update_blog_view,
	api_delete_blog_view,
	api_create_blog_view,
	api_is_author_of_blogpost,
	like_blog_post_view,
	dislike_blog_post_view,
	inc_view_count_view,
	ApiBlogListView
)

app_name = 'blog_api'

urlpatterns = [
	path('<slug>/', api_detail_blog_view, name="detail"),
	path('<slug>/like', like_blog_post_view, name="like"),
	path('<slug>/dislike', dislike_blog_post_view, name="dislike"),
	path('<slug>/add_view_count',inc_view_count_view,name='add_view_count'),
	path('<slug>/update', api_update_blog_view, name="update"),
	path('<slug>/delete', api_delete_blog_view, name="delete"),
	path('create', api_create_blog_view, name="create"),
	path('list', ApiBlogListView.as_view(), name="list"),
	path('<slug>/is_author', api_is_author_of_blogpost, name="is_author"),
]