from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create-listing"),
    path('item<int:item_id>', views.item, name="item"),
    path('watchlist<int:item_id>', views.watchlist, name='watchlist'),
    path('show_watchlist', views.show_watchlist, name="show-watchlist"),
    path('place_bid<int:item_id>', views.place_bid, name="place-bid"),
    path('add_comment<int:item_id>', views.add_comment, name="add-comment"),
    path('close_bid<int:item_id>', views.close_bid, name="close-bid"),
    path("closed_listing", views.closed_listing, name="closed-listing"),
    path("listing<int:category_id>", views.category_listing, name="category-listing"),
]
