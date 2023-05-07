from datetime import date, timedelta
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from PIL import Image, ImageDraw

def main():
# u_20200525 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+105764&variable=slp&DB_vid=30&DB_tid=86248&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Apr&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Apr&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20200526 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+105768&variable=slp&DB_vid=30&DB_tid=86263&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Apr&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Apr&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20200603 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+105800&variable=slp&DB_vid=30&DB_tid=86357&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=May&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=May&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20200703 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+105920&variable=slp&DB_vid=30&DB_tid=87620&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Jun&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Jun&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20200803 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106044&variable=slp&DB_vid=30&DB_tid=88016&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Jul&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Jul&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20200904 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106172&variable=slp&DB_vid=30&DB_tid=88423&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Aug&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Aug&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20201005 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106296&variable=slp&DB_vid=30&DB_tid=88841&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Sep&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Sep&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20201105 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=192&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106420&variable=slp&DB_vid=30&DB_tid=89260&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Oct&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Oct&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20201205 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=195&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106540&variable=slp&DB_vid=30&DB_tid=89771&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Nov&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Nov&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
# u_20210103 = 'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=195&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106656&variable=slp&DB_vid=30&DB_tid=90214&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin=2020&mon_begin=Dec&day_begin=1&hour_begin=06+Z&year_end=2020&mon_end=Dec&day_end=1&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
    path = 'C:\meteo'
    sdate = date(2020, 12, 1)
    edate = date(2020, 12, 31)

    delta = edate - sdate
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        url = f'https://psl.noaa.gov/cgi-bin/GrADS.pl?dataset=NCEP+Reanalysis&DB_did=195&file=%2FDatasets%2Fncep.reanalysis%2Fsurface%2Fslp.1948.nc+slp.%25y4.nc+106656&variable=slp&DB_vid=30&DB_tid=90214&units=Pascals&longstat=Individual+Obs&DB_statistic=Individual+Obs&stat=&lat-begin=90.00S&lat-end=90.00N&lon-begin=0.00E&lon-end=357.50E&dim0=time&year_begin={day.year}&mon_begin={day.strftime("%b")}&day_begin={day.day}&hour_begin=06+Z&year_end={day.year}&mon_end={day.strftime("%b")}&day_end={day.day}&hour_end=06+Z&X=lon&Y=lat&output=plot&bckgrnd=white&typeplot=on&use_color=on&polar=on&fill=fill&cint=101500&range1=&range2=&scale=175&maskf=%2FDatasets%2Fncep.reanalysis%2Fsurface_gauss%2Fland.sfc.gauss.nc&maskv=Land-sea+mask&submit=Create+Plot+or+Subset+of+Data'
        print(day)
        download_map(url, path, day)


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        # remove URLs like '/hsts-pixel.gif?c=3.2.5'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls

def update_map(filename):
    img = Image.open(filename)
    img = img.convert("RGBA")

    pixdata = img.load()

    # Clean the background noise, if color != grey, then set to black.

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (125, 125, 125, 255):
                pixdata[x, y] = (0, 0, 0, 255)
    draw = ImageDraw.Draw(img)
    draw.line((136, 426, 712, 426), fill=0, width=2)
    draw.line((423, 139, 423, 715), fill=0, width=2)
    img.save(filename)
    del img

def download(url, pathname, day):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    curname = str(day).replace("-", "")
    filename = os.path.join(pathname, f"{curname}.gif")

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))
    update_map(filename)


def download_map(url, path, day):
    # get all images
    imgs = get_all_images(url)
    img = imgs[1]
    download(img, path, day)

main()