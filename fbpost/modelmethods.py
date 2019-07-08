from fbpost.models import *
from datetime import datetime

from enum import Enum


class ReactionType(Enum):
    HAHA = "HAHA"
    WOW = "WOW"
    LIKE = "LIKE"
    LOVE = "LOVE"
    ANGRY = "ANGRY"
    SAD = "SAD"


def covert_datetime_object_to_string(posted_time):
    return posted_time.strftime("%Y-%m-%d %H:%M:%S.%f")


def convert_user_to_dict(user):
    return {"name": user.username, "user_id": user.id, "profile_pic_url": user.pic_url}


def covert_reaction_to_dict(reaction):
    list_of_reactions = []
    reaction_dictionary = {}
    for reaction_object in reaction.all():
        list_of_reactions.append(reaction_object.react_type)
    reaction_dictionary['reactions'] = {"count": len(list_of_reactions), "type": list(set(list_of_reactions))}
    return reaction_dictionary


def covert_comment_to_dict(comment):
    list_of_reply_dictionary = []
    comment_dictionary = {
        "comment_id": comment.id,
        "commenter": convert_user_to_dict(comment.user),
        "commented_at": covert_datetime_object_to_string(comment.comment_at),
        "comment_content": comment.comment_content,
        'reactions': covert_reaction_to_dict(comment.reaction)
    }
    reply_query_set = comment.reply.all()
    for reply in reply_query_set:
        reply_dictionary = covert_comment_to_dict(reply.comment)
        list_of_reply_dictionary.append(reply_dictionary)
    comment_dictionary["replies_count"] = len(list_of_reply_dictionary)
    comment_dictionary["replies"] = list_of_reply_dictionary
    return comment_dictionary


def create_post(user_id, post_content):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("User Not Found")
        return
    post = Post.objects.create(post_datetime=covert_datetime_object_to_string(datetime.now()),
                               post_content=post_content, user=user)
    return post.id


def get_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except User.DoesNotExist:
        print("Post Not Found")
        return

    post_dictionary = {
        'post_id': post_id,
        'posted_by': convert_user_to_dict(post.user),
        'posted_at': covert_datetime_object_to_string(post.post_datetime),
        'post_content': post.post_content,
        'reactions': covert_reaction_to_dict(post.reaction)
    }

    comment_queryset = post.comments.all()
    list_of_comments_dictionary = []
    for comment in comment_queryset:
        comment_dictionary = covert_comment_to_dict(comment.comment)
        list_of_comments_dictionary.append(comment_dictionary)

    post_dictionary["comments"] = list_of_comments_dictionary
    post_dictionary["comments_count"] = len(list_of_comments_dictionary)
    return post_dictionary


def get_user_posts(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("User Not Found")
    list_of_user_posts = []
    for user_posts in user.posts.all():
        list_of_user_posts.append(get_post(user_posts.id))
    return list_of_user_posts


def delete_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Post Not Found")
        return
    post.delete()


def react_to_post(user_id, post_id, reaction_type):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Invalid User")
        return
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Invalid Post")
        return
    if reaction_type not in [ReactionType.HAHA.value, ReactionType.LIKE.value, ReactionType.SAD.value,
                             ReactionType.WOW.value, ReactionType.LOVE.value]:
        print("Reaction doesn't exist")
        return

    try:
        reaction = Reactions.objects.get(user_id=user_id, post_id=post_id)
    except Reactions.DoesNotExist:
        print("No Reaction Found")
        r = Reactions.objects.create(react_type=reaction_type, post=post,
                                     user=user)
        return
    if reaction_type == reaction.react_type:
        reaction.delete()
    else:
        reaction.react_type = reaction_type
        reaction.save()


def get_posts_reacted_by_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("User Not Found")
        return
    list_of_posts = []
    reaction = Reactions.objects.filter(user=user)
    for posts in reaction:
        post_id = posts.post
        list_of_posts.append(post_id.id)
    return list_of_posts


def get_reactions_to_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Post Not Found")
        return
    list_of_reactions = []
    reaction_query_set = Reactions.objects.filter(post=post)
    #     print(reaction)
    for reaction_object in reaction_query_set:
        user_dict = convert_user_to_dict(reaction_object)
        user_dict['reaction'] = reaction_object.react_type
        list_of_reactions.append(user_dict)
    return list_of_reactions


def get_reaction_metrics(post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Post Not Found")
        return
    count_dictionary = {}
    reaction = Reactions.objects.filter(post=post)
    for reaction_object in reaction:
        if reaction_object.react_type not in count_dictionary.keys():
            count_dictionary[reaction_object.react_type] = 1
        else:
            count_dictionary[reaction_object.react_type] += 1
    return count_dictionary


def get_posts_with_positive_reactions():
    list_of_positive_reactions = ['LIKE', 'LOVE', 'HAHA', 'WOW']
    list_of_negative_reactions = ['ANGRY', 'SAD']
    list_of_positive_posts = []
    post = Post.objects.all()
    for post_object in post:
        reaction = post_object.reaction.all()
        positives, negatives = 0, 0
        for reaction_object in reaction:
            if reaction_object.react_type in list_of_positive_reactions:
                positives += 1
            elif reaction_object.react_type in list_of_negative_reactions:
                negatives += 1
        if positives > negatives:
            list_of_positive_posts.append(post_object.id)
    return list_of_positive_posts


def add_comment(post_id, user_id, comment_text):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Invalid User")
        return
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        print("Invalid Post")
        return
    comment = Comment.objects.create(user=user, post=post, comment_at=covert_datetime_object_to_string(datetime.now()),
                                     comment_content=comment_text)
    return comment.id


def react_to_comment(user_id, comment_id, reaction_type):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Invalid User")
        return
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        print("Invalid Comment")
        return
    if reaction_type not in ["HAHA", "LIKE", "SAD", "WOW", "LOVE"]:
        print("Reaction doesn't exist")
        return

    try:
        reaction = Reactions.objects.get(user_id=user_id, comment_id=comment_id)
    except Reactions.DoesNotExist:
        print("No Reaction Found")
        r = Reactions.objects.create(react_type=reaction_type, user=user, comment=comment)
        return
    if reaction_type == reaction.react_type:
        reaction.delete()
    else:
        reaction.react_type = reaction_type
        reaction.save()


def reply_to_comment(comment_id, user_id, reply_text):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        print("Invalid User")
        return
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        print("Invalid Comment")
        return

    reply = Comment.objects.create(parent_comment=comment, user=user,
                                   comment_at=covert_datetime_object_to_string(datetime.now()),
                                   comment_content=reply_text)
    return reply.id


def get_replies_for_comment(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        print("Invalid Comment")
        return
    list_of_reply_dictionary = covert_comment_to_dict(comment.comment)
    list_of_reply_dictionary.pop('reactions', None)
    return list_of_reply_dictionary
