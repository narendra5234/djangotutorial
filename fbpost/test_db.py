from fbpost.models import *
from datetime import datetime
from fbpost.model_methods import *
from django.db.models import *
from django.db import connection
import pytest


class ReactionType(Enum):
    HAHA = "HAHA"
    WOW = "WOW"
    LIKE = "LIKE"
    LOVE = "LOVE"
    ANGRY = "ANGRY"
    SAD = "SAD"


# CREATE USER
@pytest.mark.django_db
def test_create_user():
    user = create_user("user1", "https://dummy.url.com/pic.png")
    assert user.username == "user1"
    assert user.pic_url == "https://dummy.url.com/pic.png"


# CREATE POST
@pytest.mark.django_db
def test_create_post(user_setup):
    post_id = create_post(1, "post1")
    post = Post.objects.get(id=post_id)
    assert post.post_content == "post1"
    assert post.user.id == 1


# DELETE POST
@pytest.mark.django_db
def test_create_post_no_user(user_setup):
    with pytest.raises(User.DoesNotExist):
        create_post(5, "post1")


@pytest.mark.django_db
def test_delete_post(post_setup):
    delete_post(2)
    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(id=2)


#
@pytest.mark.django_db
def test_delete_post_no_post(post_setup):
    with pytest.raises(Post.DoesNotExist):
        delete_post(5)


# ADD COMMENT
@pytest.mark.django_db
def test_add_comment(user_setup, post_setup):
    comment_id = add_comment(1, 1, "comment1")
    comment = Comment.objects.get(id=comment_id)
    assert comment.comment_content == "comment1"
    assert comment.commented_by.id == 1
    assert comment.post.id == 1


@pytest.mark.django_db
def test_add_comment_no_user(user_setup, post_setup):
    with pytest.raises(Post.DoesNotExist):
        add_comment(5, 1, "comment1")


@pytest.mark.django_db
def test_add_comment_no_post(user_setup, post_setup):
    with pytest.raises(User.DoesNotExist):
        add_comment(1, 5, "comment1")


# REACTIONS TO POST
@pytest.mark.django_db
def test_react_to_post(user_setup, post_setup):
    reaction = react_to_post(1, 1, "WOW")
    assert reaction.react_type == "WOW"
    assert reaction.user.id == 1
    assert reaction.post.id == 1


@pytest.mark.django_db
def test_react_to_post_no_user(user_setup, post_setup):
    with pytest.raises(User.DoesNotExist):
        react_to_post(5, 1, "WOW")


@pytest.mark.django_db
def test_react_to_post_no_post(user_setup, post_setup):
    with pytest.raises(Post.DoesNotExist):
        react_to_post(1, 5, "WOW")


@pytest.mark.django_db
def test_react_to_post_no_reaction(user_setup, post_setup):
    with pytest.raises(Exception, match=r"Reaction"):
        react_to_post(1, 1, "SUPER")


# REACTIONS TO COMMENT
@pytest.mark.django_db
def test_react_to_post(user_setup):
    reaction = react_to_comment(1, 1, "WOW")
    assert reaction.react_type == "WOW"
    assert reaction.user.id == 1
    assert reaction.post.id == 1


@pytest.mark.django_db
def test_react_to_post_no_user(user_setup):
    with pytest.raises(User.DoesNotExist):
        react_to_post(5, 1, "WOW")


@pytest.mark.django_db
def test_react_to_post_no_post(user_setup, post_setup):
    with pytest.raises(Comment.DoesNotExist):
        react_to_post(1, 5, "WOW")


@pytest.mark.django_db
def test_react_to_post_no_reaction(user_setup, post_setup):
    with pytest.raises(Exception, match=r"Reaction"):
        react_to_post(1, 1, "SUPER")
