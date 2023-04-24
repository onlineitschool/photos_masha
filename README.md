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

docker run -d --name minio-u1 --network net52 \
-p 172.10.0.1:1202:9000 \
-p 172.10.0.1:1203:9001 \
-e "MINIO_ROOT_USER=user1" -e "MINIO_ROOT_PASSWORD=user1dsfjklKJLJKL50ert" quay.io/minio/minio server /data --console-address ":9001"