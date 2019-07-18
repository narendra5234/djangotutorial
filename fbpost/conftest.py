from fbpost.models import *
from datetime import datetime
from fbpost.model_methods import *
from django.db.models import *
from django.db import connection
import pytest

pytestmark = pytest.mark.django_db

USERS = [
    {"username": "user1", "pic_url": "https://dummy.url.com/pic.png"},
    {"username": "user2", "pic_url": "https://dummy.url.com/pic1.png"},
    {"username": "user3", "pic_url": "https://dummy.url.com/pic2.png"}
]
POSTS = [
    {"post_datetime": datetime.now(), "post_content": "post1", "user_id": 1},
    {"post_datetime": datetime.now(), "post_content": "post2", "user_id": 1},
    {"post_datetime": datetime.now(), "post_content": "post3", "user_id": 2}
]


@pytest.fixture
def user_setup():
    list_of_users = []
    for item in USERS:
        user = User.objects.create(username=item["username"], pic_url=item["pic_url"])
        list_of_users.append(user)
    return list_of_users


@pytest.fixture
def post_setup():
    list_of_posts = []
    for item in POSTS:
        post = Post.objects.create(post_datetime=item["post_datetime"], post_content=item["post_content"],
                                   user=User.objects.get(id=item["user_id"]))
        list_of_posts.append(post)
    return list_of_posts


