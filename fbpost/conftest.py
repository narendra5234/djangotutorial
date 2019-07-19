from fbpost.models import *
from datetime import datetime
from fbpost.model_methods import *
from django.db.models import *
from django.db import connection
import pytest

USERS = [
    {"username": "user1", "pic_url": "https://dummy.url.com/pic.png"},
    {"username": "user2", "pic_url": "https://dummy.url.com/pic1.png"},
    {"username": "user3", "pic_url": "https://dummy.url.com/pic2.png"}
]

POSTS = [
    {"post_datetime": datetime.now(), "post_content": "post1", "user_id": 1},
    {"post_datetime": datetime.now(), "post_content": "post2", "user_id": 1},
    {"post_datetime": datetime.now(), "post_content": "post3", "user_id": 2},
    {"post_datetime": datetime.now(), "post_content": "post4", "user_id": 2}
]

# for reaction_metrics
REACTIONS = [
    {"react_type": ReactionType.LIKE.value, "post_id": 1, "user_id": 2},
    {"react_type": ReactionType.HAHA.value, "post_id": 1, "user_id": 1},
    {"react_type": ReactionType.WOW.value, "post_id": 1, "user_id": 1},
    {"react_type": ReactionType.SAD.value, "post_id": 1, "user_id": 2},
    {"react_type": ReactionType.HAHA.value, "post_id": 1, "user_id": 3}
]

# for more positive metrics
NEWREACTIONS = [
    # more positives
    {"react_type": ReactionType.LIKE.value, "post_id": 1, "user_id": 1},
    {"react_type": ReactionType.HAHA.value, "post_id": 1, "user_id": 2},
    {"react_type": ReactionType.SAD.value, "post_id": 1, "user_id": 3},
    # equal_reactions
    {"react_type": ReactionType.SAD.value, "post_id": 2, "user_id": 2},
    {"react_type": ReactionType.HAHA.value, "post_id": 2, "user_id": 2},
    # more negatives
    {"react_type": ReactionType.SAD.value, "post_id": 3, "user_id": 2},
    {"react_type": ReactionType.HAHA.value, "post_id": 3, "user_id": 3},
    {"react_type": ReactionType.SAD.value, "post_id": 3, "user_id": 1},

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
    # first_post
    first_post = Post.objects.get(id=1)
    first_user = User.objects.get(id=1)
    first_post.reaction.create(react_type="HAHA", user=first_user)
    first_comment = first_post.comments.create(commented_by=first_user, comment_at=datetime.now(),
                                               comment_content="comment1")
    first_comment.reaction.create(react_type="WOW", user=first_user)
    first_reply = first_comment.reply.create(parent_comment=first_comment, commented_by=first_user,
                                             comment_at=datetime.now(), comment_content="reply1")
    first_reply.reaction.create(react_type="LIKE", user=first_user)

    # second post
    second_post = Post.objects.get(id=2)
    first_user = User.objects.get(id=1)
    second_post.reaction.create(react_type="HAHA", user=first_user)
    first_comment = second_post.comments.create(commented_by=first_user, comment_at=datetime.now(),
                                                comment_content="comment1")
    first_comment.reaction.create(react_type="WOW", user=first_user)
    first_reply = first_comment.reply.create(parent_comment=first_comment, commented_by=first_user,
                                             comment_at=datetime.now(), comment_content="reply1")
    first_reply.reaction.create(react_type="LIKE", user=first_user)
    return list_of_posts


@pytest.fixture
def post_and_comment_without_reaction_setup():
    list_of_posts = []
    for item in POSTS:
        post = Post.objects.create(post_datetime=item["post_datetime"], post_content=item["post_content"],
                                   user=User.objects.get(id=item["user_id"]))
        list_of_posts.append(post)
    first_post = Post.objects.get(id=1)
    first_user = User.objects.get(id=1)
    first_comment = first_post.comments.create(commented_by=first_user, comment_at=datetime.now(),
                                               comment_content="comment1")
    return list_of_posts


@pytest.fixture
def reaction_metrics_setup():
    list_of_posts = []
    for item in POSTS:
        post = Post.objects.create(post_datetime=item["post_datetime"], post_content=item["post_content"],
                                   user=User.objects.get(id=item["user_id"]))
        list_of_posts.append(post)
    list_of_reactions = []
    for item in REACTIONS:
        reactions = Reactions.objects.create(react_type=item["react_type"], post=Post.objects.get(id=item["post_id"]),
                                             user=User.objects.get(id=item["user_id"]))
        list_of_reactions.append(reactions)


@pytest.fixture
def more_positive_reaction_post_setup():
    list_of_posts = []
    for item in POSTS:
        post = Post.objects.create(post_datetime=item["post_datetime"], post_content=item["post_content"],
                                   user=User.objects.get(id=item["user_id"]))
        list_of_posts.append(post)
    list_of_reactions = []
    for item in NEWREACTIONS:
        reactions = Reactions.objects.create(react_type=item["react_type"], post=Post.objects.get(id=item["post_id"]),
                                             user=User.objects.get(id=item["user_id"]))
        list_of_reactions.append(reactions)
