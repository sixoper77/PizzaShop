from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("get-products/<slug:category_slug>/", views.get_products, name="get-products"),
    path("get-products/", views.get_products, name="get-products"),
    path("get_categories/", views.get_categories, name="get_categories"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("show-cart/", views.show_cart, name="show_cart"),
    path("clear-cart/", views.clear_cart, name="clear_cart"),
    path("save-telegram-id/", views.save_telegram_id, name="save_telegram_id"),
    path("save-telegram-order/", views.order, name="save_telegram_order"),
    path(
        "create-checkout-session-telegram",
        views.create_cheskout_session_telegram,
        name="create_cheskout_session_telegram",
    ),
]
