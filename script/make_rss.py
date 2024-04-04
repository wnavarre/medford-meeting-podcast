def rss(entries, out):
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write('<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:podcast="https://podcastindex.org/namespace/1.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">\n')

    out.write('<channel>\n')
    out.write('<atom:link href="https://wnavarre.github.io/medford-meetings-podcast/meetings.rss" rel="self" type="application/rss+xml" />\n')
    out.write('<title>Medford, MA Meetings</title>\n')
    out.write('<description>Audio meetings in Medford, MA</description>\n')
    out.write('<link>https//medfordma.org/</link>\n')
    out.write('<language>en-us</language>\n')
    out.write('<itunes:category text="News" />\n')
    out.write('<podcast:locked>no</podcast:locked>\n')
    out.write('<itunes:explicit>true</itunes:explicit>\n')
    out.write('</channel>\n')
    entries = list(entries)
    entries.sort(key=lambda x: x["DATE"])
    for entry in entries:
        if not entry.get("URL"): continue
        job = entry["JOB"]
        if job[0:4] != "DONE": continue
        out.write('<item>\n')
        out.write('<title>{} {}</title>\n'.format(entry["SLUG"], entry["DATE"]))
        out.write('<guid isPermaLink="false">{}</guid>\n'.format(entry["JOB"]))
        out.write('<enclosure type="audio/m4a" url="{}" length="{}" />\n'.format(
            entry["URL"],
            entry["BYTES"]
        ))
        out.write('</item>\n')
