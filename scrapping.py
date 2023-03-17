import requests
import numpy as np
from bs4 import BeautifulSoup

def return_product_mabe(website):
  try:
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    title = soup.find("meta", property="og:type")
    if title and title["content"] == "Product":
      box = soup.find('div', class_="name")
      producto = soup.find('h1').get_text().replace("\n","").replace("\t","")
      producto_corto = ""
      for word in producto.split():
        if(str.isnumeric(word[0]) or word[0] == "("):
          break
        producto_corto = producto_corto + " " + word
      producto_corto = producto_corto.lower()
      return producto_corto[1:]
    else:
      print("no es página de producto " + website)
      return None
  except:
    print("Error en la página " + website)
    return None

def return_product_macstore(website):
  try:
    result = requests.get(website)
  except:
    print("ERROR EN CARGAR LA PAGINA "  + website)
    return None
  content = result.text
  soup = BeautifulSoup(content, 'lxml')
  title = soup.find("meta", property="og:type")
  if title and title["content"]== "eCommerce": 
    #print(title["content"])
    box = soup.find('div',class_="name")
    try:
      producto = soup.find('h3').get_text().replace("\n","").replace("\t","")
      return producto.lower()
    except:
      print("ERROR GRAVE!!!!!!!! EN MACSTORE en la página" + website)
      return None
  else:
    print("no es pagina producto  " + website )
    return None

def return_product_acer(website):
  try:
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    title = soup.find("meta", property="og:type")
    if title and title["content"] == "product":
      title2 = soup.find("meta", property="og:description")
      producto = title2["content"]
      if producto is None:
        return None
      producto_corto = ""
      for word in producto.split():
        if(not (str.isalnum(word[0])) or word[0] == "(" or word[0] == "|"):  
            break
        producto_corto = producto_corto + " " + word
      producto_corto = producto_corto.lower()
      return producto_corto[1:]
    else:
      print("no es página de producto " + website)
      return None
  except:
    print("Error en la página " + website)
    return None

def return_product_asus(website):
    """https://"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        goal = soup.select_one("title").string
        producto_corto = ""
        for word in goal.split():
            if str.isnumeric(word[0]):
                producto_corto = producto_corto + " " + word
                break
            if word[0] == "|" or word[0] == "(":
                break
            if not str.isalpha(word[0]):
                break
            producto_corto = producto_corto + " " + word
        return producto_corto[1:]
    except:
        print("Hay un error en la página " + website)
        return None

def return_product_hp(website):
    """https://"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        goal = soup.select_one("title").string
        producto_corto = ""
        for word in goal.split():
            if str.isnumeric(word[0]):
                producto_corto = producto_corto + " " + word
                break
            if word[0] == "|" or word[0] == "(":
                break
            if not str.isalpha(word[0]):
                break
            producto_corto = producto_corto + " " + word
        return producto_corto[1:]
    except:
        print("Hay un error en la página " + website)
        return None
    
def return_product_huawei(website):
    """https://"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"name":"keywords"})
        idx = title["content"].find(",")
        producto_corto = title["content"][:idx]
        return producto_corto
    except:
        print("Hay un error en la página " + website)
        return None

def return_product_lenovo(website):
    """https://www."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"name":"productInfo.name" })
        dirty_prod = title["content"]
        producto_corto = ""
        for word in dirty_prod.split():
            if str.isnumeric(word[0]):
                producto_corto = producto_corto + " " + word
                break
            if word[0] == "(":
                break
            producto_corto = producto_corto + " " + word
        return producto_corto[1:]
    except:
        print("Hay un error en la página " + website)
        return None
    
def return_product_lg(website):
    """https://www."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"property":"og:title" })
        dirty_prod = title["content"]
        producto_corto = ""
        idx=0
        for word in dirty_prod.split():
            if str.isnumeric(word[0]) or idx > 4 or (not str.isalpha(word)):
                break
            producto_corto = producto_corto + " " + word
            idx += 1
        return producto_corto[1:]
    except:
        print("Hay un error en la página " + website)
        return None
    
def return_product_oppo(website):
    """https://."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"property":"og:title" })
        dirty_prod = title["content"]
        producto_corto = ""
        idx=0
        for word in dirty_prod.split():
            if str.isnumeric(word[0]) or word[0] == "|":
                producto_corto = producto_corto + " " + word
                break
            producto_corto = producto_corto + " " + word
            idx += 1
        return producto_corto[1:]
    except:
        print("Hay un error en la página " + website)
        return None
    
def return_product_samsung(website):
    """https://www."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"name":"keywords" })
        dirty_prod = title["content"]
        idx = dirty_prod.find(",")
        producto_corto = dirty_prod[:idx]
        return producto_corto
    except:
        print("Hay un error en la página " + website)
        return None
    
def return_product_telcel(website):
    """https://www."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"name":"title" })
        dirty_prod = title["content"]
        producto_corto =""
        for word in dirty_prod.split():
            if word[0].isnumeric():
                producto_corto = producto_corto + " " + word
                break
            if word[0] == "-" or word[0] == "|":
                 break
            producto_corto = producto_corto + " " + word
        return producto_corto[1:]
    except:
        print("Hay un error en la página " + website)
        return None
    
def return_product_xiaomi(website):
    """https://www."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        content=requests.get(website, headers=headers).text
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find("meta", {"itemprop":"keywords" })
        dirty_prod = title["content"] + " "
        idx=dirty_prod.find(",")
        producto_corto = dirty_prod[:idx]
        return producto_corto
    except:
        print("Hay un error en la página " + website)
        return None
    
def get_products(paginas, marcas):
    procesado_scrapp = np.zeros(len(paginas))
    productos = [None for _ in range(len(paginas))]
    productos_name = [None for _ in range(len(paginas))]
    idx = 0
    for i in range(len(paginas)):
        producto = None
        marca_found = False

        print("Procesando producto " + str(i) + " ...")

        if marcas[i] == "mabe":
            website = "https://" + paginas[i]
            producto = return_product_mabe(website)
            marca_found = True                
        if marcas[i] == "macstore":
            website = "https://www." + paginas[i]
            producto =  return_product_macstore(website)
            marca_found = True
        if marcas[i] == "acer":
            website = "https://www." + paginas[i]
            producto = return_product_acer(website)
            marca_found = True
        if marcas[i] == "asus":
            website = "https://www." + paginas[i]
            producto = return_product_asus(website)
            marca_found = True
        if marcas[i] == "hp":
            website = "https://www." + paginas[i]
            producto =  return_product_hp(website)
            marca_found = True
        if marcas[i] == "huawei":
            website = "https://" + paginas[i]
            producto =  return_product_huawei(website)
            marca_found = True
        if marcas[i] == "lenovo":
            website = "https://www." + paginas[i]
            producto =  return_product_lenovo(website)
            marca_found = True
        if marcas[i] == "lg":
            website = "https://www." + paginas[i]
            producto =  return_product_lg(website)
            marca_found = True
        if marcas[i] == "oppo":
            website = "https://www." + paginas[i]
            producto =  return_product_oppo(website)
            marca_found = True
        if marcas[i] == "samsung":
            website = "https://www." + paginas[i]
            producto =  return_product_samsung(website)
            marca_found = True
        if marcas[i] == "telcel":
            website = "https://www." + paginas[i]
            producto =  return_product_telcel(website)
            marca_found = True
        if marcas[i] == "xiaomi":
            website = "https://www." + paginas[i]
            producto =  return_product_xiaomi(website)
            marca_found = True
        if marca_found == False:
            print("\tPágina " + str(i) + " No encontrada")
            producto == None
        if producto == None:
            procesado_scrapp[i] = 0
            continue
        productos[i] = marcas[i] + " " + producto
        productos_name[i] = producto
    return productos, productos_name
