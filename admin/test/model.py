from rest_framework.test import APITestCase
from admin.models import Admin, GenericFileUpload, Message, MessageAttachment
from core.models import User


class TestModel(APITestCase):

    def test_Admin_model(self):
        user = User.objects.create_user(
            username='testuser', password='12345', phone='07051159763', email='kayodemutiu12@gmail.com'
        )
        testadmin = Admin.objects.create(
            user=user, name='Admin'
        )
        self.assertIsInstance(testadmin, Admin)
        self.assertEqual(testadmin.name, "Admin")

    def test_genericfileupload(self):
        user = User.objects.create_user(
            username='testuser', password='12345', phone='07051159763', email='kayodemutiu12@gmail.com'
        )

        testfile = GenericFileUpload.objects.create(
            file_upload='file'
        )
        self.assertIsInstance(testfile, GenericFileUpload)
        self.assertEqual(testfile.file_upload, "file")

    def test_message(self):
        user = User.objects.create_user(
            username='testuser', password='12345', phone='07051159763', email='kayodemutiu12@gmail.com'
        )
        message = Message.objects.create(
            sender=user, message='message', receiver=user
        )
        self.assertIsInstance(message, Message)
        self.assertEqual(message.message, 'message')

    def test_message_attachment(self):
        user = User.objects.create_user(
            username='testuser', password='12345', phone='07051159763', email='kayodemutiu12@gmail.com'
        )
        message = Message.objects.create(
            sender=user, message='message', receiver=user
        )
        testfile = GenericFileUpload.objects.create(
            file_upload='file'
        )

        fileattachment = MessageAttachment.objects.create(
            message=message, attachment=testfile, caption='attachment'
        )

        self.assertIsInstance(fileattachment, MessageAttachment)
        self.assertEqual(fileattachment.caption, 'attachment')
