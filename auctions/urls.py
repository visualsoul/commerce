from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:pk>", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.view_categories, name="categories"),
    path("category/<str:category_id>", views.view_category, name="category")
]
