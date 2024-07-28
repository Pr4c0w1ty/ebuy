from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("filterCategory", views.filterCategory, name="filterCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.showWatchlist, name="watchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
]
