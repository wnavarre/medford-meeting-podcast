from internetarchive import upload

def new_md():
    return {
        'collection': 'city_of_medford_ma_meetings',
        'mediatype': 'audio',
        'coverage': 'US-MA'
    }

def md(meeting):
    out = new_md()
    out["date"] = meeting["DATE"]
    datetime.datetime.strptime(out["DATE"], "%Y-%m-%d") # Errors out if format is bad.

EXT_CHARS = string.ascii_lowercase + "0123456789"

def identifier(md, meeting):
    slug = meeting["SLUG"].replace(" ", "-").replace("_", "-")
    for e in slug:
        if e == "-" or e in EXT_CHARS:
            pass
        else:
            raise ValueError(e)
    return "medford_" + meeting["SLUG"] + "_" + md["date"]

def extension(st):
    last_dot = st.rfind(".")
    if last_dot == -1: raise ValueError(-1)
    ext = st[ last_dot + 1: ]
    ext = ext.lower()
    for c in ext:
        if c not in EXT_CHARS:
            raise ValueError(c)
    return ext

def process_meeting(meeting):
    src_url = meeting["SRC"]
    video_tmpfile = "videofile." + extension(src_url)
    audio_tmpfile = "audiofile.mp3"
    my_md = md(meeting)
    my_id = identifier(md, meeting)
    meeting["URL"] = "https://archive.org/download/{}/{}".format(my_id, audio_tmpfile)
    result = subprocess.run(["wget", src_url, "-O", audio_tmpfile))
    if result: raise AssertionError("wget")
    result = subprocess.run(["ffmpeg",
                             "-i", video_tmpfile,
                             "-vn",
                             "-acodec", "copy",
                             audio_tmpfile])
    if result: raise AssertionError("ffmpeg")
    upload(my_id, { audio_tmpfile : audio_tmpfile }, metadata=my_md)
