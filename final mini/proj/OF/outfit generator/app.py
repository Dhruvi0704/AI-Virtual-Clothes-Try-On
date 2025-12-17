from flask import Flask, request, render_template
import os

# Set TensorFlow environment variable to disable oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Model
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image, UnidentifiedImageError
from functools import lru_cache

app = Flask(__name__)

# Load pre-trained ResNet50 model with fine-tuning
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
model = Model(inputs=base_model.input, outputs=x)

def preprocess_images(image_paths):
    images = []
    for image_path in image_paths:
        try:
            img = load_img(image_path, target_size=(224, 224))
            img_array = img_to_array(img)
            images.append(img_array)
        except UnidentifiedImageError:
            print(f"Error: Cannot identify image file {image_path}")
            images.append(None)
    return np.array(images)

def extract_features(image_paths):
    images = preprocess_images(image_paths)
    valid_images = [img for img in images if img is not None]
    if not valid_images:
        return {}
    
    batch_array = np.array(valid_images)
    batch_array = preprocess_input(batch_array)
    
    try:
        features = model.predict(batch_array)
        return {path: features[i].flatten() for i, path in enumerate(image_paths) if images[i] is not None}
    except Exception as e:
        print(f"Error during feature extraction: {e}")
        return {}

@lru_cache(maxsize=128)
def get_cached_features(image_path):
    features = extract_features([image_path])
    if not features:
        print(f"No features found for {image_path}")
        return None
    return features.get(image_path, None)

def recommend_items(selected_item, items, num_recommendations=3):
    selected_features = get_cached_features(selected_item)
    if selected_features is None:
        print(f"No features found for selected item: {selected_item}")
        return []
    
    item_scores = []
    for item in items:
        item_features = get_cached_features(item)
        if item_features is None:
            print(f"No features found for item: {item}")
            continue
        similarity = cosine_similarity([selected_features], [item_features])[0][0]
        item_scores.append((similarity, item))
    
    item_scores.sort(reverse=True, key=lambda x: x[0])
    recommended_items = [item for _, item in item_scores[:num_recommendations]]
    return recommended_items

def recommend_combined(selected_item, shirts, bottoms, num_recommendations=3):
    recommended_shirts = recommend_items(selected_item, shirts, num_recommendations)
    recommended_bottoms = recommend_items(selected_item, bottoms, num_recommendations)
    return recommended_shirts, recommended_bottoms

# Load combined datasets for men and women (now with 10 items each)
men_shirts = [
    'static/men_shirt1.jpg', 'static/men_shirt2.jpg', 'static/men_shirt3.jpg', 'static/men_shirt4.jpg',
    'static/men_shirt5.jpg', 'static/men_shirt6.jpg', 'static/men_shirt7.jpg', 'static/men_shirt8.jpg',
    'static/men_shirt9.jpg', 'static/men_shirt10.jpg', 'static/men_shirt11.jpg', 'static/men_shirt12.jpg',
    'static/men_shirt13.jpg', 'static/men_shirt14.jpg', 'static/men_shirt15.jpg', 'static/men_shirt16.jpg',
    'static/men_shirt17.jpg', 'static/men_shirt18.jpg', 'static/men_shirt19.jpg', 'static/men_shirt20.jpg'
]
men_bottoms = [
    'static/men_bottom1.jpg', 'static/men_bottom2.jpg', 'static/men_bottom3.jpg', 'static/men_bottom4.jpg',
    'static/men_bottom5.jpg', 'static/men_bottom6.jpg', 'static/men_bottom7.jpg', 'static/men_bottom8.jpg',
    'static/men_bottom9.jpg', 'static/men_bottom10.jpg', 'static/men_bottom11.jpg', 'static/men_bottom12.jpg',
    'static/men_bottom13.jpg', 'static/men_bottom14.jpg', 'static/men_bottom15.jpg', 'static/men_bottom16.jpg',
    'static/men_bottom17.jpg', 'static/men_bottom18.jpg', 'static/men_bottom19.jpg', 'static/men_bottom20.jpg'
]
men_shoes = [
    'static/men_shoe1.jpg', 'static/men_shoe2.jpg', 'static/men_shoe3.jpg', 'static/men_shoe4.jpg',
    'static/men_shoe5.jpg', 'static/men_shoe6.jpg', 'static/men_shoe7.jpg', 'static/men_shoe8.jpg',
    'static/men_shoe9.jpg', 'static/men_shoe10.jpg', 'static/men_shoe11.jpg', 'static/men_shoe12.jpg',
    'static/men_shoe13.jpg', 'static/men_shoe14.jpg', 'static/men_shoe15.jpg', 'static/men_shoe16.jpg',
    'static/men_shoe17.jpg', 'static/men_shoe18.jpg', 'static/men_shoe19.jpg', 'static/men_shoe20.jpg'
]
women_tops = [
    'static/women_top1.jpg', 'static/women_top2.jpg', 'static/women_top3.jpg', 'static/women_top4.jpg',
    'static/women_top5.jpg', 'static/women_top6.jpg', 'static/women_top7.jpg', 'static/women_top8.jpg',
    'static/women_top9.jpg', 'static/women_top10.jpg', 'static/women_top11.jpg', 'static/women_top12.jpg',
    'static/women_top13.jpg', 'static/women_top14.jpg', 'static/women_top15.jpg', 'static/women_top16.jpg',
    'static/women_top17.jpg', 'static/women_top18.jpg', 'static/women_top19.jpg', 'static/women_top20.jpg'
]
women_bottoms = [
    'static/women_bottom1.jpg', 'static/women_bottom2.jpg', 'static/women_bottom3.jpg', 'static/women_bottom4.jpg',
    'static/women_bottom5.jpg', 'static/women_bottom6.jpg', 'static/women_bottom7.jpg', 'static/women_bottom8.jpg',
    'static/women_bottom9.jpg', 'static/women_bottom10.jpg', 'static/women_bottom11.jpg', 'static/women_bottom12.jpg',
    'static/women_bottom13.jpg', 'static/women_bottom14.jpg', 'static/women_bottom15.jpg', 'static/women_bottom16.jpg',
    'static/women_bottom17.jpg', 'static/women_bottom18.jpg', 'static/women_bottom19.jpg', 'static/women_bottom20.jpg'
]
women_shoes = [
    'static/women_shoe1.jpg', 'static/women_shoe2.jpg', 'static/women_shoe3.jpg', 'static/women_shoe4.jpg',
    'static/women_shoe5.jpg', 'static/women_shoe6.jpg', 'static/women_shoe7.jpg', 'static/women_shoe8.jpg',
    'static/women_shoe9.jpg', 'static/women_shoe10.jpg', 'static/women_shoe11.jpg', 'static/women_shoe12.jpg',
    'static/women_shoe13.jpg', 'static/women_shoe14.jpg', 'static/women_shoe15.jpg', 'static/women_shoe16.jpg',
    'static/women_shoe17.jpg', 'static/women_shoe18.jpg', 'static/women_shoe19.jpg', 'static/women_shoe20.jpg'
]

# New dataset for boys
boys_shirts = [
    'static/boys_shirt1.jpg', 'static/boys_shirt2.jpg', 'static/boys_shirt3.jpg', 'static/boys_shirt4.jpg',
    'static/boys_shirt5.jpg', 'static/boys_shirt6.jpg', 'static/boys_shirt7.jpg', 'static/boys_shirt8.jpg',
    'static/boys_shirt9.jpg', 'static/boys_shirt10.jpg' , 'static/boys_shirt11.jpg' , 'static/boys_shirt12.jpg'
    , 'static/boys_shirt13.jpg' , 'static/boys_shirt14.jpg' , 'static/boys_shirt15.jpg' , 'static/boys_shirt16.jpg' , 
    'static/boys_shirt17.jpg' , 'static/boys_shirt18.jpg' , 'static/boys_shirt19.jpg' , 'static/boys_shirt20.jpg'
]
boys_bottoms = [
    'static/boys_bottom1.jpg', 'static/boys_bottom2.jpg', 'static/boys_bottom3.jpg', 'static/boys_bottom4.jpg',
    'static/boys_bottom5.jpg', 'static/boys_bottom6.jpg', 'static/boys_bottom7.jpg', 'static/boys_bottom8.jpg',
    'static/boys_bottom9.jpg', 'static/boys_bottom10.jpg' , 'static/boys_bottom11.jpg' , 'static/boys_bottom12.jpg' , 
    'static/boys_bottom13.jpg', 'static/boys_bottom14.jpg', 'static/boys_bottom15.jpg' , 'static/boys_bottom16.jpg' , 
    'static/boys_bottom17.jpg' , 'static/boys_bottom18.jpg' , 'static/boys_bottom19.jpg' , 'static/boys_bottom20.jpg'
]

boys_shoes = [
    'static/boys_shoe1.jpg', 'static/boys_shoe2.jpg', 'static/boys_shoe3.jpg', 'static/boys_shoe4.jpg',
    'static/boys_shoe5.jpg', 'static/boys_shoe6.jpg', 'static/boys_shoe7.jpg', 'static/boys_shoe8.jpg',
    'static/boys_shoe9.jpg', 'static/boys_shoe10.jpg' , 'static/boys_shoe11.jpg' , 'static/boys_shoe12.jpg' , 
    'static/boys_shoe13.jpg' , 'static/boys_shoe14.jpg' , 'static/boys_shoe15.jpg' , 'static/boys_shoe16.jpg' , 
    'static/boys_shoe17.jpg' , 'static/boys_shoe18.jpg' , 'static/boys_shoe19.jpg' , 'static/boys_shoe20.jpg'
    ]

# New dataset for girls
girls_tops = [
    'static/girls_top1.jpg', 'static/girls_top2.jpg', 'static/girls_top3.jpg', 'static/girls_top4.jpg',
    'static/girls_top5.jpg', 'static/girls_top6.jpg', 'static/girls_top7.jpg', 'static/girls_top8.jpg',
    'static/girls_top9.jpg', 'static/girls_top10.jpg' , 'static/girls_top11.jpg' , 'static/girls_top12.jpg' , 
    'static/girls_top13.jpg' , 'static/girls_top14.jpg' , 'static/girls_top15.jpg' , 'static/girls_top16.jpg ', 
    'static/girls_top17.jpg', 'static/girls_top18.jpg','static/girls_top19.jpg', 'static/girls_top20.jpg'
]
girls_bottoms = [
    'static/girls_bottom1.jpg', 'static/girls_bottom2.jpg', 'static/girls_bottom3.jpg', 'static/girls_bottom4.jpg',
    'static/girls_bottom5.jpg', 'static/girls_bottom6.jpg', 'static/girls_bottom7.jpg', 'static/girls_bottom8.jpg',
    'static/girls_bottom9.jpg', 'static/girls_bottom10.jpg','static/girls_bottom11.jpg', 'static/girls_bottom12.jpg',
    'static/girls_bottom13.jpg','static/girls_bottom14.jpg','static/girls_bottom15.jpg','static/girls_bottom16.jpg',
    'static/girls_bottom17.jpg','static/girls_bottom18.jpg','static/girls_bottom19.jpg','static/girls_bottom20.jpg'
]
girls_shoes = [
    'static/girls_shoe1.jpg', 'static/girls_shoe2.jpg', 'static/girls_shoe3.jpg', 'static/girls_shoe4.jpg',
    'static/girls_shoe5.jpg', 'static/girls_shoe6.jpg', 'static/girls_shoe7.jpg', 'static/girls_shoe8.jpg',
    'static/girls_shoe9.jpg', 'static/girls_shoe10.jpg','static/girls_shoe11.jpg','static/girls_shoe12.jpg',
    'static/girls_shoe13.jpg','static/girls_shoe14.jpg','static/girls_shoe15.jpg','static/girls_shoe16.jpg',
    'static/girls_shoe17.jpg','static/girls_shoe18.jpg','static/girls_shoe19.jpg','static/girls_shoe20.jpg'
]

@app.route('/')
def gender_selection():
    return render_template('index.html')

@app.route('/men', methods=['GET', 'POST'])
def men_section():
    selected_item = None
    recommended_bottoms = []
    recommended_shirts = []
    recommended_shoes = []
    if request.method == 'POST':
        selected_shirt = request.form.get('shirt')
        selected_bottom = request.form.get('bottom')
        selected_shoe = request.form.get('shoe')
        if selected_shirt:
            selected_item = selected_shirt
            recommended_bottoms = recommend_items(selected_shirt, men_bottoms)
            recommended_shoes = recommend_items(selected_shirt, men_shoes)
        elif selected_bottom:
            selected_item = selected_bottom
            recommended_shirts = recommend_items(selected_bottom, men_shirts)
            recommended_shoes = recommend_items(selected_bottom, men_shoes)
        elif selected_shoe:
            selected_item = selected_shoe
            recommended_shirts, recommended_bottoms = recommend_combined(selected_shoe, men_shirts, men_bottoms)
            recommended_shoes = []  # Reset recommended shoes
    return render_template('men.html', men_shirts=men_shirts, men_bottoms=men_bottoms, men_shoes=men_shoes, selected_item=selected_item, recommended_bottoms=recommended_bottoms, recommended_shirts=recommended_shirts, recommended_shoes=recommended_shoes)

@app.route('/women', methods=['GET', 'POST'])
def women_section():
    selected_item = None
    recommended_bottoms = []
    recommended_shirts = []
    recommended_shoes = []
    if request.method == 'POST':
        selected_shirt = request.form.get('shirt')
        selected_bottom = request.form.get('bottom')
        selected_shoe = request.form.get('shoe')
        if selected_shirt:
            selected_item = selected_shirt
            recommended_bottoms = recommend_items(selected_shirt, women_bottoms)
            recommended_shoes = recommend_items(selected_shirt, women_shoes)
        elif selected_bottom:
            selected_item = selected_bottom
            recommended_shirts = recommend_items(selected_bottom, women_tops)
            recommended_shoes = recommend_items(selected_bottom, women_shoes)
        elif selected_shoe:
            selected_item = selected_shoe
            recommended_shirts, recommended_bottoms = recommend_combined(selected_shoe, women_tops, women_bottoms)
            recommended_shoes = []  # Reset recommended shoes
    return render_template('women.html', women_tops=women_tops, women_bottoms=women_bottoms, women_shoes=women_shoes, selected_item=selected_item, recommended_bottoms=recommended_bottoms, recommended_shirts=recommended_shirts, recommended_shoes=recommended_shoes)

@app.route('/kids', methods=['GET', 'POST'])
def kids_section():
    selected_item = None
    recommended_bottoms = []
    recommended_shirts = []
    recommended_shoes = []
    gender = request.form.get('gender', 'boys')  # Default to boys
    
    if request.method == 'POST':
        selected_shirt = request.form.get('shirt')
        selected_bottom = request.form.get('bottom')
        selected_shoe = request.form.get('shoe')
        
        if gender == 'boys':
            if selected_shirt:
                selected_item = selected_shirt
                recommended_bottoms = recommend_items(selected_shirt, boys_bottoms)
                recommended_shoes = recommend_items(selected_shirt, boys_shoes)
            elif selected_bottom:
                selected_item = selected_bottom
                recommended_shirts = recommend_items(selected_bottom, boys_shirts)
                recommended_shoes = recommend_items(selected_bottom, boys_shoes)
            elif selected_shoe:
                selected_item = selected_shoe
                recommended_shirts, recommended_bottoms = recommend_combined(selected_shoe, boys_shirts, boys_bottoms)
        else:  # girls
            if selected_shirt:
                selected_item = selected_shirt
                recommended_bottoms = recommend_items(selected_shirt, girls_bottoms)
                recommended_shoes = recommend_items(selected_shirt, girls_shoes)
            elif selected_bottom:
                selected_item = selected_bottom
                recommended_shirts = recommend_items(selected_bottom, girls_tops)
                recommended_shoes = recommend_items(selected_bottom, girls_shoes)
            elif selected_shoe:
                selected_item = selected_shoe
                recommended_shirts, recommended_bottoms = recommend_combined(selected_shoe, girls_tops, girls_bottoms)
    
    return render_template('kids.html', 
                         boys_shirts=boys_shirts, 
                         boys_bottoms=boys_bottoms, 
                         boys_shoes=boys_shoes,
                         girls_tops=girls_tops,
                         girls_bottoms=girls_bottoms,
                         girls_shoes=girls_shoes,
                         selected_item=selected_item,
                         recommended_bottoms=recommended_bottoms,
                         recommended_shirts=recommended_shirts,
                         recommended_shoes=recommended_shoes,
                         gender=gender)

if __name__ == '__main__':
    app.run(debug=True)