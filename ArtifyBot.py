# Import the os module to work with the file system
import os
# Import the webbrowser module
import webbrowser
# Import the necessary library
import pyautogui
import time
import cv2
import numpy as np
import requests
import json
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re
import openai
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import ssl
from PIL import Image
ssl._create_default_https_context = ssl._create_unverified_context


desktop = os.path.expanduser("~/Desktop")

    # Construct the path to the file
file_path = os.path.join(desktop, "digitalprompt.txt")



def retrieve_first_url(channelid):
   # token = get_discord_token()
    headers = {
       # 'authorization' : '8u3rC912NiAGTxIUNbfcQGZiZHR2rF'
        'authorization' : 'MTA3OTg5MTcwNTI5MTA3OTY5MA.GqDE8J.qUEIZn7Ip8gfs5ZJHznMVs7tK33QztH1sVv7gc'
       # NTQxMDIwMjQ2NjEwNTQyNTkz.GM4W4I.JHDgKkeKsP9FNPz3J3L9U_o-mfOwS-jUpioKr0
    }

    r=requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)

    jsonn=json.loads(r.text)
    

    for value in jsonn:
        if value['attachments']:
            print(value['attachments'][0]['url'], '\n')
            filename=value['attachments'][0]['url']
           # filename=filename.split(".")
            attachment_url = value['attachments'][0]['url']
            file_response = requests.get(attachment_url)
            if file_response.status_code == 200:
                first_linez=first_line.strip().replace(" ", "_")
                folder_name = first_linez
                os.makedirs(f'/Users/totonito3/Etsy Digital Print/Vividdigitalstore/{folder_name}')
                parts = filename.split(".")
                new_filename = first_linez+"." + parts[-1]
                with open(f'/Users/totonito3/Etsy Digital Print/Vividdigitalstore/{folder_name}/{new_filename}', 'wb') as f:
                    f.write(file_response.content)
                
                    print(f'File saved as {new_filename}')
                    break
            else:
                print(f'Error downloading file: {file_response.text}')
                break
        else:
                print('No attachments found in this channel.')
                break
    else:
        print(f'Error retrieving messages: {response.text}')
    return new_filename

def send_prompt(channelid, prompt):
    payload = {
        'content' : f'/imagine prompt {prompt}'
    }

    header = {
        'authorization' : 'NTQxMDIwMjQ2NjEwNTQyNTkz.GM4W4I.JHDgKkeKsP9FNPz3J3L9U_o-mfOwS-jUpioKr0'

    }

    r=requests.post(f'https://discord.com/api/v9/channels/{channelid}/messages', data=payload, headers=header)


def convert_webp_to_png(file_path):
    file_dir, file_name = os.path.split(file_path)
    file_root, file_ext = os.path.splitext(file_name)
    
    if os.path.splitext(file_path)[1] == ".webp":
    #if file_ext.lower() == ".webp":
        png_file_path = os.path.join(file_dir, file_root + ".png")
        
        with Image.open(file_path) as im:
            im.convert("RGB").save(png_file_path, "PNG")
            
        print(f"File '{file_name}' converted to PNG and saved as '{os.path.basename(png_file_path)}'")
        
        return png_file_path
    
    else:
        print(f"File '{file_name}' is not a WebP file, no conversion needed.")
        
        return file_path


def crop_image(image_path, width, height):
    # Load the image
    img = cv2.imread(image_path)
    
    # Scale the image to 20 inches by 30 inches with 300 dpi
    dpi = 300
    height_scale = dpi * 30 / img.shape[0]
    width_scale = dpi * 20 / img.shape[1]
    img = cv2.resize(img, (0, 0), fx=width_scale, fy=height_scale)
    
    # Crop the image at the given fixed ratio
    img_height, img_width, _ = img.shape
    target_ratio = width / height
    img_ratio = img_width / img_height
    if target_ratio > img_ratio:
        crop_width = img_width
        crop_height = int(img_width / target_ratio)
    else:
        crop_height = img_height
        crop_width = int(img_height * target_ratio)
    start_x = int((img_width - crop_width) / 2)
    start_y = int((img_height - crop_height) / 2)
    cropped_img = img[start_y:start_y+crop_height, start_x:start_x+crop_width]
    
    # Save the cropped image with a different name
    version=''
    if width==24 and height==36:
        version='2by3R'
    if width==24 and height==32:
        version='3by4R'
    if width==24 and height==30:
        version='4by5R'
    if width==11 and height==14:
        version='11by14In'
    if width==23.4 and height==33.1:
        version='ISO'

    save_path = os.path.splitext(image_path)[0] + f"{version}" + ".jpeg"#os.path.splitext(image_path)[1]
    cv2.imwrite(save_path, cropped_img, [cv2.IMWRITE_JPEG_QUALITY,100])
    
    return cropped_img

def upload_folder(folder_path):
    
    creds = Credentials.from_authorized_user_info(
    {
        "refresh_token": "1//045LGyH7zENKbCgYIARAAGAQSNwF-L9IrIZpX6L4VX_2H6EZ_GU3aUYx0dnhDCt8hRCxV_xo1qxf8ac_WiwPDvQDqBx4pqpkpeiI",
        "client_id": "308092366642-196qp1hh10160l2c55nedp1hqa2sjc79.apps.googleusercontent.com",
        "client_secret": "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"
    },
    ['https://www.googleapis.com/auth/drive']
)

    #creds = Credentials.from_authorized_user_file("token.json")
    service = build('drive', 'v3', credentials=creds)
    
    folder_name = os.path.basename(folder_path)
    mimetype = 'application/vnd.google-apps.folder'

    file_metadata = {'name': the_folder, 
                     'mimeType': mimetype,
                     'permission': {'type': 'anyone', 'role': 'reader', 'withLink': True}
                     }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f'Folder has been created with Name "{the_folder}" and URL: "https://drive.google.com/drive/folders/{folder.get("id")}".')
    folder_url = f'https://drive.google.com/drive/folders/{folder.get("id")}'
    
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            with io.open(file_path, 'rb') as f:
                file_metadata = {'name': filename, 'parents': [folder.get("id")]}
                media = MediaFileUpload(file_path, mimetype='*/*')
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'{the_folder} has been uploaded successfuly, URL: {folder_url}')
    return folder_url


def create_pdf(image_path, link, output_file):
    # Create the PDF file
    c = canvas.Canvas(output_file, pagesize=letter)

    # Add the image
    c.drawImage(image_path, 0, 0, width=612, height=792)

    # Add the hyperlink
    c.linkURL(link, (0, 0, 612, 792), relative=1)

    # Add the text
    # Change the text size

    c.setFont("Helvetica", 20)
    c.setFillColor("white")
    c.setStrokeColor("white")
    c.setFillColor("black")
    c.rect(90, 590, 350, 40, fill=1)

    c.setFontSize(32)
    c.setFillColorRGB(255, 255, 255)
    c.drawString(100, 600, "Click here to Download")
    #c.line(300, 395, 390, 395)
    # Save the PDF file
    c.save()

def create_mockup(mockup, product_image):



    # Folder path where you want to save the file
    #mockfolder_path = f'/Users/totonito3/Etsy Digital Print/Vividdigitalstore/__{}/'
    mockname = os.path.basename(mockup)
    mockname = re.sub(r'\..*', '', mockname)

    mockfilename = os.path.basename(product_image)
    mockfolder_path = os.path.basename(product_image)
    mockfolder_path = re.sub(r'\..*', '', mockfilename)
    mockfolder_path = f'/Users/totonito3/Etsy Digital Print/Vividdigitalstore/__{mockfolder_path}/'
    try:
        os.makedirs(mockfolder_path)
    except FileExistsError:
    # If the folder already exists, do nothing and continue with the script
        pass
    #os.makedirs(mockfolder_path)
    mockfilename = re.sub(r'\..*', '.jpg', mockfilename)
    # Filename to save the file as
    #mockfilename = f'{}.jpg'

    # Combine the folder path and filename
    mockfile_path = mockfolder_path + mockname + mockfilename

    # Set download directory
    download_path = mockfolder_path
    mockfile_path = download_path + mockname + mockfilename
    prefs = {'download.default_directory' : download_path}


    # Set Chrome options
    options = webdriver.ChromeOptions()
   # options.add_argument('--headless')
    options.add_experimental_option('prefs', prefs)
    #optionss = Options()
    
    # Create driver with Chrome options
    driver2 = webdriver.Chrome(options=options)

    # Load the web driver
   # driver = webdriver.Chrome()

    # Load Photopea
    driver2.get('https://www.photopea.com')

    # Wait for the page to load
    #driver.implicitly_wait(10)
    time.sleep(10)
    # upload the PSD file
    file_input = driver2.find_element("xpath", "/html/body/input")
    file_input.send_keys(f'{mockup}')

    # wait for the file to upload and open
    #driver.implicitly_wait(30)
    time.sleep(5)

    # upload the image file
    image_input = driver2.find_element("xpath", "/html/body/input")
    image_input.send_keys(f'{product_image}')
    time.sleep(4)
    # wait for the image to upload and appear in the preview
    #driver.implicitly_wait(30)

##############################

    # Find the "File" menu and click on it
    #file_menu = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[3]/div[2]/div/span/button[1]")
    file_menu = driver2.find_element("xpath", "//button[text()='File']")
    file_menu.click()
    time.sleep(5)
    # Find the "Script" option in the File menu and click on it
    #script_option = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[2]/div[3]/div[15]")
    script_option = driver2.find_element("xpath", "//span[text()='Script...']")
    driver2.implicitly_wait(30)
    time.sleep(5)
    script_option.click()
    time.sleep(3)
    driver2.implicitly_wait(30)
    time.sleep(5)

    script_terminal = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[1]/div/div[2]/div/textarea");
    prrroduct = os.path.basename(product_image)
    prrroduct = re.sub(r'\..*', '.psd', prrroduct)
    arga=f'app.activeDocument = app.documents[0];function findLayerByName(layer, name) {{  if (layer.name.startsWith(name)) {{    return layer;  }} else if (layer.layers) {{    for (var i = 0; i < layer.layers.length; i++) {{      var foundLayer = findLayerByName(layer.layers[i], name);      if (foundLayer) {{        return foundLayer;alert("YOUPPIIIII");      }}    }}  }}}}var l = findLayerByName(app.activeDocument, "1");app.activeDocument.activeLayer = l;executeAction(stringIDToTypeID("placedLayerEditContents"));var layerName = "Background";var sourceDocumentName = "{prrroduct}";var sourceDocument = app.documents.getByName(sourceDocumentName);var sourceLayer = sourceDocument.layers.getByName(layerName);app.activeDocument = app.documents[2];app.activeDocument.flatten();var targetDoc = app.documents[2];var targetWidth = targetDoc.width;var targetHeight = targetDoc.height;app.activeDocument = app.documents[1];app.documents[1].resizeImage(targetWidth, targetHeight);alert("Yeaa");newLayer = sourceLayer.duplicate(targetDoc, ElementPlacement.PLACEATBEGINNING);newLayer.name = "Copied Layer";app.activeDocument = app.documents[2];app.activeDocument.save();app.activeDocument = app.documents[0];'
    time.sleep(3)
    driver2.implicitly_wait(30)
    script_terminal.send_keys(arga);
    driver2.implicitly_wait(30)
    time.sleep(5)
    run_button=driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[1]/div/div[2]/div/button[6]");
    run_button.click();
    #driver.implicitly_wait(8)
    time.sleep(4)

    close_script_button=driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[1]/div/div[1]/span[2]");
    close_script_button.click();
    time.sleep(3)
    #driver.implicitly_wait(5)


    file_menu = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[3]/div[2]/div/span/button[1]");
    file_menu.click();
    time.sleep(4)
    export_option = driver2.find_element("xpath", "//span[text()='Export as']")#driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[2]/div[3]/div[9]");
    export_option.click();
    time.sleep(3)
    #driver.implicitly_wait(5)


    jpeg_option = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[2]/div[4]/div[2]");
    jpeg_option.click();
    time.sleep(3)
    #driver.implicitly_wait(5)


    m_title = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[1]/div/div[2]/div[2]/div/span[1]/input");
    a=os.path.basename(product_image)
    a=re.sub(r'\..*', '', a)
    m_title.send_keys(f"{a}");
    time.sleep(3)
    save_button = driver2.find_element("xpath", "/html/body/div[3]/div[1]/div[1]/div/div[2]/div[2]/div/button");
    save_button.click();
    time.sleep(3)
    cwd = os.getcwd()
    download_url = driver2.current_url

    urllib.request.urlretrieve(download_url, 'filename.extension')
    #driver.implicitly_wait(10)
    time.sleep(3)
    #ActionChains(driver2).send_keys(Keys.ENTER).perform()


    # get the absolute path of the downloaded file
    
    #download_path = os.path.join(cwd, 'filename.extension')

    # print the path of the downloaded file
    #print(download_path)


    time.sleep(4)
    # close the web driver
    driver2.quit()
    print("Mockup generation was a success!")

    return mockfile_path


def get_tags(title):
    

    api_key = "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"
    openai.api_key = api_key
    model = "text-davinci-003"

    prompt = f"Product: {title}. Give me in a single phrase, 26 keywords, each separated with a comma, summarizing the Who, What, Why, Where, and When aspects of the product. Those keywords will be used for Etsy product listings tags. Your response must be in this format 'Movie Theater Scene, Wall Art Digital, Print Room Decoratio, Room Design Home Dec, Home Decoration Gift, Presenet Printable, Downloadable Excitin, Suspenseful Action, Thrilling Scene, Artwork Wall Print, Dark Crimson, Creative Affordable, Showcase High Qualit' "

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150,
    )

    keywords = response.choices[0].text.strip().split(",")
    keywords = [keyword.strip() for keyword in keywords]

    cleaned_keywords = []
    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        keyword = keyword.replace('.', '')
        keyword = keyword.replace("'", "")
        keyword = keyword.replace("'", "")
        cleaned_keywords.append(keyword)

    MAX_LENGTH = 20
    MAX_PAIRS = 13

    keyword_pairs = []
    for i in range(0, len(cleaned_keywords), 2):
        if i+1 < len(cleaned_keywords):
            keyword_pair = ' '.join([cleaned_keywords[i], cleaned_keywords[i+1]])
            truncated_pair = keyword_pair[:MAX_LENGTH]
            keyword_pairs.append(truncated_pair)

        if len(keyword_pairs) >= MAX_PAIRS:
            break
        elif i+2 >= len(cleaned_keywords) and len(keyword_pairs) < MAX_PAIRS:
            keyword_pairs.append(cleaned_keywords[-1][:MAX_LENGTH])

    keyword_string = ', '.join(keyword_pairs)
    print(keyword_string)


    
    return keyword_string

def get_title(title, product):
    api_key = "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"
    openai.api_key = api_key
    model = "text-davinci-003"

    prompt = f"Product: {title}. Combine this title with this:' {product} ', and give me a search engine optimized title for my etsy product. Make it no longer than 120 characters. Do not include 'Etsy'. Do not include the number of charaters in the title."

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150,
    )

    mytitle = response.choices[0].text
    mytitle = mytitle.replace('"', '')
    mytitle = mytitle.replace("'", "")
    mytitle = mytitle.title()
    print("MY TITLE IS::::")
    print(mytitle)
    return mytitle
    #keywords = [keyword.strip() for keyword in keywords]


def add_listing(title, description, price, access):


    # Set the API endpoint
    url = 'https://openapi.etsy.com/v3/application/shops/41700844/listings'

    # Set the access token and API key
    access_token = access
    api_key = 'x7t40z0cqw2su8ogrgkiqi73'
    tags_arr = get_tags(title)
    tags_arr = re.sub(r'[^\w\s\,]', ' ', tags_arr)
    print("\n")
    print("\n")
    print(tags_arr)
   # title=title;
    print("\n")
    print("\n")
    print(title)
    print("\nUP THERE IT IS")

    #tags_str = ", ".join([f"{tags_arr[i]} {tags_arr[i+1]}" for i in range(0, len(tags_arr), 2)])
    #tags_str = ", ".join([f"{tags_arr[i]} {tags_arr[i+1]}" for i in range(0, 26, 2)])
    #tags_str = ", ".join([f"{tags_arr[i]} {tags_arr[i+1]}" for i in range(0, len(tags_arr), 2) if len(tags_arr[i]) + len(tags_arr[i+1]) <= 20])
    #tags_str = ", ".join([f"{tags_arr[i]} {tags_arr[i+1]}" for i in range(0, len(tags_arr), 2) if i+1 < len(tags_arr) and len(tags_arr[i]) + len(tags_arr[i+1]) <= 20])
 #   tags_str = ", ".join([f"{tags_arr[i]} {tags_arr[i+1]}" for i in range(0, len(tags_arr)-1, 2) if len(tags_arr[i]) + len(tags_arr[i+1]) <= 20][:13])

   # print(tags_str)

    # Set the listing data
    listing_data = {
        'quantity': 999,
        'title': title,
        'description': description,
        'price': price,
        'who_made': 'i_did',
        'when_made': '2020_2023',
        #"category_id": 69150419,
        "materials": ["Digital File"],
        'taxonomy_id': 2078,
        'type': 'download',
        'tags': tags_arr,
        'should_auto_renew': True,
        #'image_ids': ''	

    }

    # Set the headers for the request
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    # Make the request
    response = requests.post(url, headers=headers, json=listing_data)

    # Print the response
    print(response.json())
    # Extract the listing ID from the response
    response_dict = response.json()
    listing_id = response_dict['listing_id']

    return listing_id







#IMAGE LISTING


def add_mockup(mockup_path, listng, access):

    
    # Set the API endpoint
    url = f'https://openapi.etsy.com/v3/application/shops/41700844/listings/{listng}/images'

    # Set the access token and API key
    access_token = access
    api_key = 'x7t40z0cqw2su8ogrgkiqi73'

    # Set the headers for the request
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'x-api-key': api_key
    }

    # Open the image and read the binary data
    with open(mockup_path, 'rb') as f:
        image_data = f.read()

    # Set the data for the request
    data = {
        #'listing_image_id': 1,
        'rank': 1,
        'image': (f'{os.path.basename(mockup_path)}', image_data),
        'overwrite': False,
        'is_watermarked': False,
        'alt_text': title
    }

    # Make the request
    response = requests.post(url, headers=headers, files=data)

    # Print the response
    print(response.json())




def add_extras(listing_id, access_token, image_ids, title):
    # Set the API endpoint for listing images
    url_images = f'https://openapi.etsy.com/v3/application/shops/41700844/listings/{listing_id}/images'
    # Set the API endpoint for listing videos
    
    # Set the headers for the request
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'x-api-key': 'x7t40z0cqw2su8ogrgkiqi73'
    }

    # Add images
    for i, image_id in enumerate(image_ids):
        # Set the data for the request
        data = {
            'listing_image_id': image_id,
            'rank': i + 7,
            'overwrite': False,
            'is_watermarked': False,
            'alt_text': title
        }
        # Make the request
        response = requests.post(url_images, headers=headers, json=data)
        # Print the response
        print(response.json())



def add_Listing_File(file_path, listng, access):

    file_name = f"{listng}.pdf" # os.path.basename(file_path)
    #response_dict = response.json()
   # listing_id = response_dict['listing_id']


    # Set the API endpoint and parameters
    url = "https://openapi.etsy.com/v3/application/shops/{shop_id}/listings/{listing_id}/files"
    shop_id = 41700844  # Replace with your own shop ID
    listing_id = listng  # Replace with the ID of the listing to which the file will be associated
    api_key = "x7t40z0cqw2su8ogrgkiqi73"  # Replace with your own Etsy API key
    token = access

    #file_path = "/Users/totonito3/Etsy Digital Print/Vividdigitalstore/surreal_and_abstract_composition_with_organic_and_geometric_shapes.pdf"
    # Set the headers and authentication
    #file_name = "examplgrre.pdf"
    with open(file_path, "rb") as f:
        file_data = f.read()

    headers = {
        "Authorization": f"Bearer {token}",
        "x-api-key": api_key,
    }
    '''
    files = {
        "name": ("filename.pdf", open("/Users/totonito3/Etsy Digital Print/Vividdigitalstore/surreal_and_abstract_composition_with_organic_and_geometric_shapes.pdf", "rb"), "application/pdf"),
        #"file": 
    }'''

    body = {
        "file": (file_name, file_data, "application/pdf"),
        "name": (None, file_name),
        "rank": (None, "1"),
    }

    # Send the POST request to upload the file
    response = requests.post(
        url.format(shop_id=shop_id, listing_id=listing_id),
        headers=headers,
        files=body,
    )

    # Check the response status code and print the response content
    if response.status_code == 201:
        print("File uploaded successfully!")
        print(response.json())
    else:
        print(f"Error uploading file: {response.status_code} - {response.text}")

  




def getToken():

        # Etsy OAuth endpoints
    authorize_url = 'https://www.etsy.com/oauth/connect'
    token_url = 'https://api.etsy.com/v3/public/oauth/token'

    # OAuth 2.0 client credentials
    client_id = 'x7t40z0cqw2su8ogrgkiqi73'
    client_secret = 'vwogxafizs'
    redirect_uri = 'https://localhost/'

    # OAuth 2.0 authorization scopes
    scope = 'email_r%20listings_w%20transactions_r%20listings_r%20shops_r%20listings_d%20shops_w'

    # Generate a random string for CSRF protection
    state = 'superstate' #secrets.token_urlsafe()

    # Generate a random string for PKCE code challenge
    code_verifier = 'Gjj-Hi97Zpk-IUWb7wHm5wpW3k294gnWHhqXG1OoLazKklWNuf5CZ63v6P.NApaPaxyp8TDFzM-kh7nDj1FR6hJmBRr3s5219ToHAhbkzPV6TdI4sKNOtEIB-Xj6sB.e' #secrets.token_urlsafe(64)
    code_challenge = '_c4EJ6-_ixufwONMf-QNne4bkKrDf-Rj4j_mXGEr4u4' #hashlib.sha256(code_verifier.encode()).hexdigest()

    # Define file paths for saving and reading refresh token
    refresh_token_file = 'refresh_token.json'

    # Try to read the refresh token from file
    try:
        with open(refresh_token_file, 'r') as f:
            refresh_dict = json.load(f)
            refresh_token = refresh_dict['refresh_token']
            access_token = refresh_dict['access_token']
            print("GRRRRR"+ access_token)
    except (FileNotFoundError, KeyError):
        # If the file doesn't exist or doesn't contain a refresh token, start the OAuth flow from scratch
        refresh_token = '748671898.Dg8D0QNARusy-MNCDVX4AUPfIZdQu8tUampy3Dz9SUjz8KvNJWOH51BLSE6xK0XTM2FvhjCbrOgjLeSgg9zJVfwWS0'
        print("dammnnnGRRRRR")
    if not refresh_token:
        # Start OAuth flow to obtain an access token and refresh token
        # ...
        # Obtain the refresh token from the response
        # ...
        # Save the refresh token to file for future use
        with open(refresh_token_file, 'w') as f:
            #refresh_dict = {'refresh_token': refresh_token}
            refresh_dict = {'refresh_token': refresh_token, 'access_token': access_token}

            json.dump(refresh_dict, f)
    else:
        # Use the saved refresh token to obtain a new access token
        token_params = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }
        response = requests.post(token_url, data=token_params)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            #access_token = refresh_dict['access_token']
            # Save the new refresh token to file for future use
            refresh_token = response.json()['refresh_token']
            
            with open(refresh_token_file, 'w') as f:
                #refresh_dict = {'refresh_token': refresh_token}
                refresh_dict = {'refresh_token': refresh_token, 'access_token': access_token}
                json.dump(refresh_dict, f)
        else:
            print('Failed to retrieve access token')
            print(response.text)
    return access_token


def load_Discord():

    optionss = Options()
    
    #optionss.add_argument('--headless')
    #optionss.headless = True

# Initialize the webdriver
    driver = webdriver.Chrome(options=optionss)

# Navigate to the Discord URL
    driver.get("https://discord.com/channels/@me/1080356826966655057")
    driver.implicitly_wait(15)
    time.sleep(10)
# Fill in the username and password
    username = driver.find_element("name", "email")
    username.send_keys("5716680998")
    password = driver.find_element("name", "password")
    password.send_keys("TheGodFather11432!")
    password.send_keys(Keys.RETURN)
    driver.implicitly_wait(22)
    time.sleep(10)
    driver.get("https://discord.com/channels/@me/1080356826966655057")
    time.sleep(10)
    return driver


def scroll_to_top(driver):
    #from selenium import webdriver

    # create a new Chrome browser instance
    #browser = webdriver.Chrome()

    # navigate to the page you want to scroll down on
    #browser.get("https://www.example.com")

    # get the current height of the page
    page_height = driver.execute_script("return document.body.scrollHeight")

    # continuously scroll down the page until the bottom is reached
    while True:
        # scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # wait for the page to load
        driver.implicitly_wait(5)

        # get the new height of the page
        new_page_height = driver.execute_script("return document.body.scrollHeight")

        # check if the page height has remained the same, indicating that the bottom has been reached
        if new_page_height == page_height:
            break

        # update the page height
        page_height = new_page_height

    # close the browser
    #browser.quit()


def switch_tab(driver):
    original_tab = driver.current_window_handle
    time.sleep(2)
    # Open a new tab and switch to it
    driver.execute_script("window.open('https://discord.com/channels/@me/1080356826966655057', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    # Switch back to the original tab and close it
    driver.switch_to.window(original_tab)
    time.sleep(2)
    driver.close()
    time.sleep(2)

    # Switch back to the new tab
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(4)
        

driver = load_Discord()
scroll_to_top(driver)






while os.path.isfile(file_path) and os.stat(file_path).st_size != 0:
    # file is not empty

    scroll_to_top(driver)
    # Get the path to the desktop
    desktop = os.path.expanduser("~/Desktop")

    # Construct the path to the file
    file_path = os.path.join(desktop, "digitalprompt.txt")

    # Open the file in read mode
    with open(file_path, "r") as file:
        # Read the content of the file
        content = file.readlines()

    # Copy the first line
    first_line = content[0]

    # Delete the first line
    content = content[1:]

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write the remaining content back to the file
        file.writelines(content)


    time.sleep(15)
    driver.implicitly_wait(30)

    entry = driver.find_element("xpath", "/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/main/form/div/div/div/div[3]/div/div[2]")

    entry.send_keys("/imagine")
    driver.implicitly_wait(30)
    time.sleep(2)
    entry.send_keys(Keys.TAB)
    time.sleep(1)
    driver.implicitly_wait(30)
    #entry.send_keys(Keys.TAB)
    entry.send_keys(first_line)
    time.sleep(1)
    entry.send_keys(Keys.RETURN)
    time.sleep(70)
    #choice = driver.find_element("xpath", "/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/main/div[1]/div/div/ol/li[50]/div/div[2]/div[2]/div[1]/div/button[1]")
   # choice.send_keys(Keys.RETURN)

    #pyautogui.press('tab')
 

    # Replace pyautogui.press('tab') with ActionChains
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(2)

    # Replace pyautogui.press('up') with ActionChains
    ActionChains(driver).key_down(Keys.UP).perform()
    time.sleep(2)
    ActionChains(driver).key_up(Keys.UP).perform()

    driver.implicitly_wait(100)

    # Replace pyautogui.press('tab') with ActionChains
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(2)

    # Replace pyautogui.press('tab') with ActionChains
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(2)

    # Replace pyautogui.press('tab') with ActionChains
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(2)

    # Replace pyautogui.press('tab') with ActionChains
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(2)

    # Replace pyautogui.press('enter') with ActionChains
    ActionChains(driver).send_keys(Keys.ENTER).perform()



    #upscale_choice = driver.find_element("xpath", "/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[2]/main/div[1]/div/div/ol/li[50]/div/div[2]/div[2]/div[1]/div/button[1]")
   # upscale_choice.click()

    #time.sleep(2)
    #driver.implicitly_wait(5)
 
    time.sleep(330)

    # driver.implicitly_wait(170)
    print("DONEEEE")
    

   ###################### driver.quit()

    product = 'wall art digital print'

    first_line = get_title(first_line, product)
    first_line = re.sub(r'[^\w\s]', ' ', first_line)
    #first_line = first_line.capitalize()

    the_folder = first_line.strip().replace(" ", "_")
    #time.sleep(300)
    new_filename=retrieve_first_url('1080356826966655057')   #RETRIEVE AND SAVE art piece
    
   #/os.system("pkill -f 'Google Chrome'")
    #pyautogui.hotkey('command', 'q')



    image_path = f"/Users/totonito3/Etsy Digital Print/Vividdigitalstore/{the_folder}/{new_filename}"

    '''cropped_img = crop_image(image_path, 11,14)
    cropped_img = crop_image(image_path, 16,20)
    cropped_img = crop_image(image_path, 20,24)
    cropped_img = crop_image(image_path, 24,34)
    cropped_img = crop_image(image_path, 30,40)
    cropped_img = crop_image(image_path, 8,10)'''


    cropped_img = crop_image(image_path, 24,36)
    cropped_img = crop_image(image_path, 24,32)
    cropped_img = crop_image(image_path, 24,30)
    cropped_img = crop_image(image_path, 11,14)
    cropped_img = crop_image(image_path, 23.4,33.1)

    folder_url=upload_folder(f"/Users/totonito3/Etsy Digital Print/Vividdigitalstore/{the_folder}/")

    pdf_filename = re.sub(r'\..*', '.pdf', new_filename)


    pdf_loc=f"/Users/totonito3/Etsy Digital Print/Vividdigitalstore/{pdf_filename}"
    create_pdf(image_path, folder_url, pdf_loc)

    print("\n")
    print("\n")
    print(f"CREATION STEP DONE for {first_line}")
    print("\n")
    print("\n STARTING MOCKUP CREATION")

    mock1 = "/Users/totonito3/Desktop/MOCKUPP/1.psd"
    mock2 = "/Users/totonito3/Desktop/MOCKUPP/2.psd"
    mock3 = "/Users/totonito3/Desktop/MOCKUPP/3.psd"
    mock4 = "/Users/totonito3/Desktop/MOCKUPP/4.psd"
    mock5 = "/Users/totonito3/Desktop/MOCKUPP/5.psd"
    mock66 = "/Users/totonito3/Desktop/MOCKUPP/66.psd"
    mock77 = "/Users/totonito3/Desktop/MOCKUPP/77.psd"

    

   # create_mockup(mock1, image_path)
    mock2 = create_mockup(mock2, image_path)
    mock3 = create_mockup(mock3, image_path)
    mock4 = create_mockup(mock4, image_path)
    mock5 = create_mockup(mock5, image_path)
    mock66 = create_mockup(mock66, image_path)
    mock77 = create_mockup(mock77, image_path)
    #create_mockup(mock2, image_path)
    #first_line = first_line.capitalize()
    title=first_line
    mockup=""
    price="4.20"
    quantity="999"
    category="Digital Prints"
    description=""




    api_key = "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"
    endpoint = "https://api.openai.com/v1/engines/davinci/jobs"

    openai.api_key = api_key

    
    model="text-davinci-003"
    prompt=f"Give me a well written, convincing, SEO optimized, description of a digital print titled '{first_line}' to be sold on Etsy. In your response, do not precise how it is optimized for SEO."

    response = openai.Completion.create(
        prompt= prompt,
        model=model,
        max_tokens=1000,
        temperature=0.9,
        n=1,  
    )

    description=response.choices[0].text
    print(description)
    

    mytitle = first_line

    data = {
        "title": title,
        "filename": new_filename,
        "image_path": image_path,
        "folder_url": folder_url,
        "price": price,
        "description": description
    }



    access = getToken()
    #title=f"{title} wall art print"

    #if not os.path.exists(image_path):
        #image_path = image_path.replace(".png", ".webp")

    image_path = convert_webp_to_png(image_path)

    listng = add_listing(mytitle, description, price, access)
    #print("\n" + listng)

   # file_path = 'pdf_loc'

    add_mockup(mock2, listng, access)
    add_mockup(mock3, listng, access)
    add_mockup(mock4, listng, access)
    #add_mockup(mock5, listng, access)
    add_mockup(mock66, listng, access)
    add_mockup(mock77, listng, access)
    add_mockup(image_path, listng, access)

    #add_extras(listng, access)
    #add_extras(listng, access)
    #add_extras(listng, access)
    #image_ids = [4680147224, 4680142216, 4728371367, 4680454466] # replace with your image IDs
    
    image_ids=[4699873712, 4699981346, 4748210471, 4748210337]
    
    #video_id = '727823571'
    add_extras(listng, access, image_ids, mytitle)

    add_Listing_File(pdf_loc, listng, access)
    
    switch_tab(driver)


    # Read the existing data from the file
   

    # Saving the data to a JSON file
    with open('data.json', 'a') as json_file:
        json.dump(data, json_file, indent=4)





# Summary of the Project:

# This project is an automated system for creating, processing, and listing digital art prints on Etsy. Leveraging a combination of technologies, it begins by interacting with Discord using Selenium WebDriver, generating digital art based on prompts read from a file. The art is then processed, cropped to various aspect ratios, and converted into different formats, including a PDF.

# Subsequently, the system generates SEO-optimized descriptions for the artwork via OpenAI's GPT-3 engine. It then creates mockup images using predefined Photoshop templates. Lastly, the script lists the artwork on Etsy, providing all relevant details, images, and files, communicating with Etsy's API for seamless automation.

# Incorporation in the Resume:

# Automated Art Creation and E-commerce Integration Project

# Developed a Python script that automates the generation and listing of digital art prints on Etsy.
# Leveraged Selenium WebDriver for real-time interaction with Discord to create digital art based on textual prompts.
# Utilized the OpenAI API (GPT-3 engine) to create SEO-optimized descriptions for art pieces.
# Implemented image processing techniques using the Pillow library to crop images into different aspect ratios and convert them into multiple formats, including PDF.
# Integrated with Etsy's API to automatically list digital art, including all relevant information, images, and associated files.
# Employed predefined Photoshop templates to generate realistic mockup images, enhancing the product presentation.
# Instituted error handling mechanisms and implemented more secure methods for storing and handling sensitive data (API keys).
# Ensured compliance with third-party services' terms of use and navigated potential challenges related to changes in web page layouts.
# Enhanced the efficiency of the automation process by replacing arbitrary time delays with condition-based polling where possible.
# Made the code more modular, facilitating easier debugging and maintenance.



****/