from django.urls import path

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_lisiting",views.create_listing,name="create_listing"),
    path("<int:listing_id>/display_listing", views.display_listing, name="display_listing"),
    path("<int:listing_id>/add_watchlist",views.add_watchlist,name="add_watchlist"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/new_bid", views.new_bid, name="new_bid"),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("closed_lists",views.closed_list,name="closed_list"),
    path("select_list",views.select_list,name="select_list"),   
]
urlpatterns += staticfiles_urlpatterns()