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
    path('show_watchlist<int:user_id>', views.show_watchlist, name="show-watchlist"),
    path('place_bid<int:item_id>', views.place_bid, name="place-bid"),
]
