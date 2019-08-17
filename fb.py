import networkx as net
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from tqdm import tqdm
import json
from utils import scroll_down, fb_login

WEBDRIVER_PATH = r'PATH TO chromedriver.exe'
FB_EMAIL = 'YOUR EMAIL'
FB_PASSWORD = 'YOUR PASSWORD'

# Set up webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options)

# Log in to Facebook
fb_login(driver,FB_EMAIL,FB_PASSWORD)
profile_name = driver.find_element_by_id('userNav').text
profile_url = driver.find_element_by_css_selector('[title="Profile"]').get_attribute('href')
driver.get(profile_url + '/friends')

# Scraping friend list
scroll_down(driver)
frs = driver.find_elements_by_class_name('_698')
frs_mutual = {}
frs_url = {}
for i, fr in enumerate(frs):
    fr_name = fr.text.split('\n')[-2]
    fr_url = fr.find_element_by_css_selector('a[data-gt]').get_attribute('href')
    if 'profile.php' in fr_url:
        fr_url = fr_url.split('&')[0] + '&sk=friends_mutual'
    else:
        fr_url = fr_url.split('?')[0] + '/friends_mutual'
    frs_mutual[fr_name] = []
    frs_url[fr_name] = fr_url

# Scraping mutual friend list from each friend
for fr in tqdm(frs_url.keys()):
    driver.get(frs_url[fr])
    scroll_down(driver)
    mutuals = driver.find_elements_by_class_name('_698')
    for mutual in mutuals:
        mutual_name = mutual.text.split('\n')[-2]
        frs_mutual[fr].append(mutual_name)

driver.quit()

# Save dict
frs_mutual[profile_name] = list(frs_mutual.keys())
with open('frs_mutual.json', 'w') as fp:
    json.dump(frs_mutual, fp)
fp.close()

# Build and draw network
G = net.Graph(frs_mutual)
net.draw(G, with_labels=True, font_family='STKaiti', node_size=20, node_color="skyblue", alpha=0.6, linewidths=2)
