from dotenv import load_dotenv
import os


load_dotenv()

ALGORITHM = os.getenv('ALGORITHM') # "HS256"
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') #"12345dfdfsdfsccsss" #os.environ['JWT_SECRET_KEY']     # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY') #"12345dfdfsdfsccsss" #os.environ['JWT_REFRESH_SECRET_KEY']      # should be kept secret

AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME=os.getenv('AWS_REGION_NAME')
AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')
MONGODB_URL=os.getenv('MONGODB_URL')

DATA_ROOT=os.getenv("DATA_ROOT")

