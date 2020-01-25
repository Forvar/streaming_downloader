import subprocess
import os
from multiprocessing.pool import ThreadPool
import threading
import sys
import hashlib

# Config
THREAD_N = 40


# Getting video file info and setting things up.
url = sys.argv[1]
outdir = str(hashlib.sha256(url))
subprocess.run(["mkdir", outdir])
subprocess.run(["wget", url, "-P", outdir])
base = os.path.dirname(url)
m3u8 = os.path.basename(url)


# Reading video pieces skipping things already downloaded
urls = []
files = []
with open(m3u8, "r") as f:
    for l in f:
        l = l.strip()
        if l == "" or l[0] == "#":
            continue
        files.append(l)
        if os.path.exists("out/" + l):
            print("already downloaded: ", l)
            continue
        urls.append(l)


# Downloading the video pieces in parallel
l = threading.Lock()
p = 0
def download(u):
    global p
    ret = subprocess.run(["wget", base + "/" + u, "-P", outdir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ret.returncode != 0:
        raise Exception("AAARGH non zero RC!")
    try:
        l.acquire()
        p += 1
        print("%s%%" % int(p/len(urls)*100))
    finally:
        l.release()
ThreadPool(THREAD_N).map(download, urls)

# Concatenating pieces
subprocess.run(["ffmpeg", "-i", outdir+"/"+m3u8, "-c", "copy", "-bsf:a", "aac_adtstoasc", outdir+"mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
