import os
from google.cloud import translate_v2 as translate
 
# Set the environment variable programmatically
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\SIFT2.0\\credentials\\vertex-key.json"
client = translate.Client()
print(client.translate("दिल्ली में वायु प्रदूषण बहुत खतरनाक स्तर पर है", target_language="en"))
