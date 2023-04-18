
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Event(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=False)
    alert = models.IntegerField(blank=True, null=True)
    accesslevel = models.IntegerField(db_column='accessLevel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event'


class Followers(models.Model):
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userID', primary_key=True)  # Field name made lowercase.
    followingid = models.ForeignKey('User', models.DO_NOTHING, db_column='followingID', related_name='userID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Followers'
        unique_together = (('userid', 'followingid'),)


class Groups(models.Model):
    groupid = models.AutoField(db_column='GroupID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Groups'


class Logins(models.Model):
    studentid = models.OneToOneField('User', models.DO_NOTHING, db_column='studentID', primary_key=True)  # Field name made lowercase.
    userName = models.CharField(max_length=64, blank=False, null=False)
    pwd = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Logins'


class Messages(models.Model):
    msgid = models.AutoField(db_column='msgID', primary_key=True)  # Field name made lowercase.
    msgcontent = models.CharField(db_column='msgContent', max_length=280, blank=True, null=True)  # Field name made lowercase.
    touser = models.ForeignKey('User', models.DO_NOTHING, db_column='toUser', blank=True, null=True)  # Field name made lowercase.
    fromuser = models.ForeignKey('User', models.DO_NOTHING, db_column='fromUser', blank=True, null=True, related_name='toUser')  # Field name made lowercase.
    togroup = models.ForeignKey(Groups, models.DO_NOTHING, db_column='toGroup', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Messages'


class Notifications(models.Model):
    notificationid = models.IntegerField(db_column='notificationID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userID', blank=True, null=True)  # Field name made lowercase.
    notificationmsg = models.CharField(db_column='notificationMsg', max_length=280)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notifications'


class Posts(models.Model):
    postid = models.IntegerField(db_column='postID', primary_key=True)  # Field name made lowercase.
    threadid = models.IntegerField(db_column='threadID')  # Field name made lowercase.
    fromuser = models.ForeignKey('User', models.DO_NOTHING, db_column='fromUser')  # Field name made lowercase.
    threadtitle = models.CharField(db_column='threadTitle', max_length=140, blank=True, null=True)  # Field name made lowercase.
    threaddescription = models.CharField(db_column='threadDescription', max_length=280, blank=True, null=True)  # Field name made lowercase.
    postcontent = models.CharField(db_column='postContent', max_length=280, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Posts'


class Professor(models.Model):
    profid = models.AutoField(db_column='profID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor'


class Roles(models.Model):
    roleid = models.AutoField(db_column='RoleID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    cancreateevent = models.IntegerField(db_column='canCreateEvent', blank=True, null=True)  # Field name made lowercase.
    candeleteevent = models.IntegerField(db_column='canDeleteEvent', blank=True, null=True)  # Field name made lowercase.
    canviewevents = models.IntegerField(db_column='canViewEvents', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles'


class Studentevents(models.Model):
    studentid = models.OneToOneField('User', models.DO_NOTHING, db_column='studentID', primary_key=True)  # Field name made lowercase.
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventID')  # Field name made lowercase.
    groupid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='GroupID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StudentEvents'
        unique_together = (('studentid', 'eventid'),)


class Studentsingroup(models.Model):
    studentid = models.OneToOneField('User', models.DO_NOTHING, db_column='studentID', primary_key=True)  # Field name made lowercase.
    groupid = models.ForeignKey(Groups, models.DO_NOTHING, db_column='GroupID')  # Field name made lowercase.
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'StudentsInGroup'
        unique_together = (('studentid', 'groupid'),)


class User(models.Model):
    studentid = models.AutoField(db_column='studentID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    standing = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


