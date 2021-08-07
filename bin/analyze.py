import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).parent.parent / "etc"))

from lib.io import read_json

client = MongoClient('mongodb://localhost:9999')
db = client.tinder
users = db.users


objects = read_json('data/objects.json')

data = pd.DataFrame \
    .from_dict(objects, orient='index', columns=['count']) \
    .sort_values(by='count', ascending=False)

# Remove common features
common_features = [
    'Forehead', 'Chin', 'Jaw', 'Sleeve', 'Hairstyle', 'Neck', 'Gesture', 'Eyebrow',
    'Nose', 'Cheek', 'Mouth',
    'Cool', 'Fun', # I don't understand this
    'Happy', # covered by Smile
    'Vision care', 'Glasses', # covered by Eyewear
    'Smile', 'Sky', # always top 2
    ]
data = data.drop(labels=common_features)

top_20 = data[:20]

ax = sns.barplot(data=top_20, y=top_20.index, x='count')
ax.set_title('Most common objects in 125 Tinder photos from 49 recommendations')
ax.set_ylabel('object')
plt.show()
