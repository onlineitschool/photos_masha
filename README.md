# photos_masha

pip3 install awscli 
pip3 install awscli-plugin-endpoint

user1
пароль помнит браузер
https://u1.s3ui.itschool.cloud/browser/photos
https://u1.s3api.itschool.cloud/browser/photos

# Получить список объектов в бакете
for key in s3.list_objects(Bucket='bucket-name')['Contents']:
    print(key['Key'])