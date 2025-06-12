from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import requests
from bs4 import BeautifulSoup
# from urllib.parse import urljoin # Unused, removed
from PIL import Image  # For optional image processing

app = Flask(__name__)
CORS(app)  # Allow all origins for cross-origin requests

DATABASE_FILE = 'database.json'
IMAGES_DIR = 'images'  # Directory to store crawled images

# Ensure the images directory exists
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)


def load_users():
    """Load user data from database.json, adapting to 'users' list structure."""
    if not os.path.exists(DATABASE_FILE):
        # If file doesn't exist, create initial structure
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump({"users": [], "movies": []}, f, ensure_ascii=False, indent=4)
        return {}  # Return empty dictionary to indicate no users

    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            # Convert list structure to dictionary structure for easier lookup by username
            users_dict = {user['username']: user for user in data.get('users', [])}
            return users_dict
        except json.JSONDecodeError:
            # Handle empty or corrupted JSON file
            print(f"Warning: {DATABASE_FILE} is empty or corrupted. Initializing with empty data.")
            return {}


def save_users(users_dict):
    """Save user data to database.json, converting back to 'users' list structure."""
    # Convert dictionary structure back to list structure
    users_list = list(users_dict.values())

    # Read current movies data to preserve it when saving users
    current_data = {"users": [], "movies": []}
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            try:
                temp_data = json.load(f)
                current_data['movies'] = temp_data.get('movies', [])
            except json.JSONDecodeError:
                pass  # If file is empty or corrupted, use default empty values

    current_data['users'] = users_list

    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=4)


# Initialize and load user data at application start
# This 'users' variable will hold the dictionary-formatted user data
users = load_users()

# Example: Create a default user for testing if no users exist in the database
if not users:
    # Ensure the default user object has the 'username' key for proper saving
    users['111'] = {'username': '111', 'password': '111111', 'movies': []}
    save_users(users)
    print("Default user '111' with password '111111' created.")

# Global variable to store movie data (can be persisted to file if needed)
# Assuming for now that all users share the same crawled movie data
movies_data = []


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users_data = load_users()  # Load fresh data for each request
    if username in users_data and users_data[username]['password'] == password:
        return jsonify({"code": 200, "message": "登录成功", "username": username})
    return jsonify({"code": 401, "message": "用户名或密码错误"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"code": 400, "message": "用户名和密码不能为空"}), 400

    users_data = load_users()  # Load fresh data
    if username in users_data:
        return jsonify({"code": 409, "message": "用户已存在"}), 409

    users_data[username] = {'username': username, 'password': password, 'movies': []}  # Include username in user object
    save_users(users_data)
    return jsonify({"code": 200, "message": "注册成功"})


@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not all([username, old_password, new_password]):
        return jsonify({"code": 400, "message": "缺少必要的参数"}), 400

    users_data = load_users()  # Load fresh data
    if username not in users_data:
        return jsonify({"code": 404, "message": "用户不存在"}), 404

    # Validate old password
    if users_data[username]['password'] != old_password:
        return jsonify({"code": 401, "message": "旧密码不正确"}), 401

    # Update password
    users_data[username]['password'] = new_password
    save_users(users_data)
    return jsonify({"code": 200, "message": "密码修改成功"})


# Crawler section
@app.route('/start_crawler', methods=['POST'])
def start_crawler():
    global movies_data  # Declare usage of global variable
    movies_data = []  # Clear previous data before crawling
    try:
        url = 'https://movie.douban.com/top250'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors

        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='item')

        for i, item in enumerate(items):
            title = item.find('span', class_='title').get_text().strip()
            rating_text = item.find('span', class_='rating_num').get_text().strip()
            rating = float(rating_text)

            eval_people_text = item.find('div', class_='star').find_all('span')[-1].get_text().strip()
            # Extract only digits for evaluation people count
            eval_people = ''.join(filter(str.isdigit, eval_people_text))

            img_tag = item.find('img')
            img_url = img_tag['src'] if img_tag else ''

            image_path_local = ''
            if img_url:
                image_name = os.path.basename(img_url)
                image_path_local = os.path.join(IMAGES_DIR, image_name)
                # Check if image already exists to avoid re-downloading
                if not os.path.exists(image_path_local):
                    try:
                        img_data = requests.get(img_url, stream=True).content
                        with open(image_path_local, 'wb') as handler:
                            handler.write(img_data)
                        # Optional: Resize image if needed (Pillow library)
                        # with Image.open(image_path_local) as img:
                        #     img.thumbnail((200, 300)) # example resize
                        #     img.save(image_path_local)
                    except Exception as e:
                        print(f"Failed to download image {img_url}: {e}")
                        image_path_local = ''  # Set path to empty if download fails

            # Frontend will access via /images/image_name, so store relative path
            relative_image_path = f'/images/{os.path.basename(image_path_local)}' if image_path_local else ''

            movies_data.append({
                'title': title,
                'rating': rating,
                'eval_people': eval_people,
                'image_path': relative_image_path
            })
            if i >= 19:  # Limit to first 20 movies to keep data manageable
                break

        return jsonify({"code": 200, "message": "爬取成功", "movies": movies_data})

    except requests.exceptions.RequestException as e:
        print(f"Request to Douban Movies failed: {e}")
        return jsonify({"code": 500, "message": f"请求豆瓣电影失败: {e}"}), 500
    except Exception as e:
        print(f"Error during crawling: {e}")
        return jsonify({"code": 500, "message": f"爬取过程中发生错误: {e}"}), 500


# Serve static image files
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)